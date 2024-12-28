from flask import Flask, request, jsonify, render_template
import os
from models.main import text,classify
import pandas as pd
import zipfile
import math
from score_logic import overall_match

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    zip_file = request.files['zipfile']
    excel_file = request.files['excelfile']
    zip_file.save(os.path.join(app.config['UPLOAD_FOLDER'], zip_file.filename))
    excel_file.save(os.path.join(app.config['UPLOAD_FOLDER'], excel_file.filename))
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'],zip_file.filename)  
    extract_dir = os.path.join(app.config['UPLOAD_FOLDER'],"extract/")
    with zipfile.ZipFile(zip_path,'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_file.filename)
    df = pd.read_excel(excel_path)
    for file_name in os.listdir(extract_dir):
        photo_id = os.path.splitext(file_name)[0]
        photo_path = os.path.join(extract_dir, file_name)
        srno = photo_id.replace("_","")[:3]
        verify = classify(photo_path)
        if verify == "aadhar":
            extracted_data = text(photo_path)
            if 'address' in extracted_data and 'name' in extracted_data and 'uid' in extracted_data:
                input_name = df.loc[df['SrNo']==srno,'Name'].values[0]
                input_address = (
                    str(df.loc[df['SrNo'] == srno, 'House Flat Number'].values[0]) +" "+
                    str(df.loc[df['SrNo'] == srno, 'Town'].values[0]) +" "+
                    str(df.loc[df['SrNo'] == srno, 'Street Road Name'].values[0]) + " "+
                    str(df.loc[df['SrNo'] == srno, 'City'].values[0]) + " " + 
                    str(df.loc[df['SrNo'] == srno, ' Floor Number'].values[0]) + " " + 
                    str(df.loc[df['SrNo'] == srno, 'Premise Building Name'].values[0]) + " "+ 
                    str(df.loc[df['SrNo'] == srno, 'PINCODE'].values[0])
                        )
                input_uid = int(df.loc[df['SrNo']==srno,'UID'].values[0])
                df.loc[df['SrNo']==srno,'Overall Match'] = overall_match(input_name,extracted_data['name'],input_address,extracted_data['address'],input_uid,int(extracted_data['uid'].replace(" ","")))
            else:
                df.loc[df['SrNo']==srno,"Final Remarks"] = "Given photo is does not have all the details"
        else:
            df.loc[df['SrNo']==srno,"Final Remarks"] = "Given photo is not a Aadhar"
    data =  df[['SrNo', 'Overall Match' , 'Final Remarks']].to_dict(orient='records')
    for row in data:
        if isinstance(row['Overall Match'], float) and math.isnan(row['Overall Match']):
            row['Overall Match'] = row['Final Remarks']
        elif row['Overall Match'] is False:
            row['Overall Match'] = "The aadhar does not match the one in the database"
        else:
            row['Overall Match']  ="The aadhar matches the one in the database"
    return render_template('process.html',data=data)
    




# @app.route('/process',methods=['POST'])
# def process():

#     return render_template('process.html')

if __name__ == '__main__':
    app.run()


# name there are rules
# pincode uid should be same
# address - 