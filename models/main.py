from ultralytics import YOLO
import easyocr
import cv2

def classify(img):
    model = YOLO(r"C:\workarea\infosys\flask\models\classification\weights\best.pt")
    results = model.predict(img)
    return results[0].names[results[0].probs.top1]

def text(img):
    model = YOLO(r"C:\workarea\infosys\flask\models\objde\weights\best.pt")
    reader = easyocr.Reader(['en']) 
    results = model(img)
    image = cv2.imread(img)
    extracted_data = {}  
    for result in results[0].boxes.data.tolist(): 
        x1, y1, x2, y2, confidence, class_id = map(int, result[:6])
        field_class = model.names[class_id] 
        cropped_roi = image[y1:y2, x1:x2]
        gray_roi = cv2.cvtColor(cropped_roi, cv2.COLOR_BGR2GRAY)
        text = reader.readtext(gray_roi, detail=0) 
        extracted_data[field_class] = ' '.join(text)
    return extracted_data