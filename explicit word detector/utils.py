import string 

def pre_processing_data(input_text):
    input_text="".join([i if i not in string.punctuation else " " for i in input_text])
    return input_text

def postprocess(predictions):
    # Convert numeric predictions to a user-friendly format
    if predictions==0:
        return {'status': True,'error': None}
    else: 
        return {'status':False,'error': None}
