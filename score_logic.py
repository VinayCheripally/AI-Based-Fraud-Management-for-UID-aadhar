from difflib import SequenceMatcher
def normalize_text(text):
    """Normalize text by removing non-alphanumeric characters and extra spaces."""
    import re
    return re.sub(r'[^a-zA-Z0-9 ]', '', text).strip().lower()
def name_match(input_name, extracted_name):

    input_parts = sorted(input_name.split())
    extracted_parts = sorted(extracted_name.split())

    if input_name == extracted_name or set(input_parts) == set(extracted_parts):
        return True

    if len(input_parts) == len(extracted_parts):
        for inp, ext in zip(input_parts, extracted_parts):
            if len(ext) == 1 and inp.startswith(inp):
                continue
            if inp != ext:
                return False
        return True

    if len(input_parts) != len(extracted_parts):
        input_set, extracted_set = set(input_parts), set(extracted_parts)
        if input_set.issubset(extracted_set) or extracted_set.issubset(input_set):
            return True

    for inp, ext in zip(input_parts, extracted_parts):
        if len(inp) == 1 and ext.startswith(inp):
            continue
        if inp != ext:
            return False
    return True

def address_match(input_address, extracted_address, cutoff=70):
    input_address = normalize_text(input_address)
    extracted_address = normalize_text(extracted_address)

    input_address = input_address.replace("marg", "").replace("lane", "").replace("township", "")
    extracted_address = extracted_address.replace("marg", "").replace("lane", "").replace("township", "")

    input_fields = input_address.split()
    extracted_fields = extracted_address.split()
    
    match_scores = []
    for input_field in input_fields:
        field_scores = [SequenceMatcher(None, input_field, ext_field).ratio() for ext_field in extracted_fields]
        match_scores.append(max(field_scores) if field_scores else 0)

    final_score = sum(match_scores) / len(match_scores) * 100 if match_scores else 0
    return final_score >= cutoff

def overall_match(input_name, extracted_name, input_address, extracted_address,input_uid,extracted_uid):
    """Evaluate the overall match for name and address."""
    name_matched = name_match(input_name, extracted_name)
    address_matched = address_match(input_address, extracted_address)
    return name_matched and address_matched and input_uid==extracted_uid

# Example Usage
# input_name = "Phani Vishwanath"
# extracted_name = "P Vishwanath"
# input_address = "123 Marg Lane, Some Town"
# extracted_address = "123 Lane, Some Town"
# input_pincode = "560001"
# extracted_pincode = "560 001"
# input_uid =  1
# extracted_uid = 1
# print(overall_match(input_name, extracted_name, input_address, extracted_address, input_pincode, extracted_pincode,input_uid ,extracted_uid))

# ignore_terms = [
#         "PO-",
#         "PO",
#         "Marg",
#         "Peeth",
#         "Veedhi",
#         "Rd",
#         "Lane",
#         "NR",
#         "Beside",
#         "Opposite",
#         "OPP",
#         "Behind",
#         "near",
#         "Enclave",
#         "Township",
#         "Society",
#         "Soc",
#         "Towers",
#         "Block",
#         "S/o",
#         "C/o",
#         "D/o",
#         "W/o",
#  ]
# stop_words = [
#         "dr",
#         "mr",
#         "mrs",
#         "smt",
#         "ms",
#         "col",
#         "professor",
#         "jt1",
#         "jt",
#         "prof",
#         "huf",
#         "minor",
#         "bhai",
# ]
