from deep_translator import GoogleTranslator
from fastapi import FastAPI, Request
from langdetect import detect
from Main_function import main_function
app = FastAPI()
def detect_language(text):
    try:
        return detect(text)
    except:
        return "Unknown"
def translate_ar_to_en(arabic_text):
    translated = GoogleTranslator(source='ar', target='en').translate(arabic_text)
    return translated

def translate_en_to_ar(english_text):
    translated = GoogleTranslator(source='en', target='ar').translate(english_text)
    return translated
@app.post("/post_message/", response_model=dict)
async def receive_message(request: Request):
    body_text = await request.body()
    body_str = body_text.decode("utf-8")


    try:
        data = eval(body_str)
    except Exception as e:
        return {"error": "Invalid JSON body"}

    user_id = data.get('user_id')
    message = data.get('message')
    if detect_language(message) == "ar":
        message = translate_ar_to_en(message)
        processed_message = main_function(message, user_id)
        print(message)
        processed_message = translate_en_to_ar(processed_message)
    else:
        processed_message = main_function(message, user_id)
    if not message:
        return {"error": "No message found in the request body"}


    print(processed_message)
    response = {
        "status": 200,
        "message": processed_message
    }

    return response