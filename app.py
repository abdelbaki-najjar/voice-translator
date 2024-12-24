from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from gtts import gTTS
from deep_translator import GoogleTranslator
import os
import requests

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads' 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


languages = {
    "Arabe": "ar",
  "Anglais": "en",
  "Français": "fr",
  "Espagnol": "es",
  "Allemand": "de",
  "Chinois": "zh-CN",
  "Japonais": "ja"
}


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
        except Exception as e:
            print("Error:", e)
            return None

    try:
        text = recognizer.recognize_google(audio, language='auto')
        print("تم التعرف على الكلام:", text)
        return text
    except sr.RequestError:
        print("حدث خطأ أثناء التعرف على الكلام.")
        return None
    except sr.UnknownValueError:
        print("لم يتم فهم ما قلته.")
        return None

def translate_text(text, target_language):
    translated_text = GoogleTranslator(source='auto', target=target_language).translate(text) 
     
    
    return translated_text
# def translate_text(text, target_language):
#     try:
#         # Define the Lingua Robot endpoint
#         endpoint = "https://api.linguarobot.io/language-translation/text"

#         # Construct the request parameters
#         params = {
#             "source": "auto",  # Automatically detect the source language
#             "target": target_language,
#             "key": "",  # Leave empty as Lingua Robot doesn't require an API key
#             "text": text
#         }

#         # Send the translation request
#         response = requests.get(endpoint, params=params)
#         response.raise_for_status()

#         # Parse the response
#         translated_text = response.json()["translatedText"]
#         return translated_text
#     except Exception as e:
#         print("Error translating text:", e)
#         return None
def text_to_speech(text, language):
    tts = gTTS(text, lang=language)
    temp_file_path = 'static/temp.mp3'
    tts.save(temp_file_path)
    return temp_file_path
    
    #tts.save("output.mp3")

@app.route('/')
def home():
    return render_template('index.html', languages=languages)


@app.route('/upload', methods=['POST'])
def upload():
    target_language = request.form['target_language']
    print(target_language)
    text = recognize_speech()
    print(text)
    if text:
        translated_text = translate_text(text, target_language)
        print(translated_text)
        audio_file = text_to_speech(translated_text, target_language)
        return render_template('download.html', audio_file=audio_file, translated_text=translated_text)
    else:
        return "Error occurred while processing speech."

      




if __name__ == '__main__':
    app.run(debug=True)
