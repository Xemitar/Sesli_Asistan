import requests
from PIL import Image
from io import BytesIO
import google.generativeai as genai
from gtts import gTTS
from playsound import playsound
import random
import os
import speech_recognition as sr
from openai import OpenAI
import sys



genai.configure(api_key="YOUR_API_KEY")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[])

recognizer = sr.Recognizer()
client = OpenAI()

def speech_to_text():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

        recognizer.adjust_for_ambient_noise(source, duration=0.02)

    try:
        text = recognizer.recognize_google(audio, language="tr-TR")
        print(f"Söylediğiniz şey: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Ne söylediğinizi anlayamadım.")
        return None
    except sr.RequestError as e:
        print(f"Hizmetine ulaşılamadı; hata: {e}")
        return None

def speak_response(response):
    tts = gTTS(response, lang="tr")
    rand = random.randint(1, 100000)
    file_name = str(rand) + ".mp3"
    tts.save(file_name)
    playsound(file_name)
    os.remove(file_name)

def siralama(liste):
    print(f"Söylenen şeyler , \n {liste}")

liste = []

def gorsel(komut):
    response = client.images.generate(
        model="dall-e-3",
        prompt=komut,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    res = requests.get(image_url)
    if res.status_code == 200:
        img = Image.open(BytesIO(res.content))
        img.show()
    else:
        print("Görüntü alınamadı. Hata kodu:", res.status_code)
print("Fatih Çolak ")
print("Herhangi birinden birine geçmek istiyorsanız 'Asistan' veya 'Resim' demeniz yeterlidir. ")
print("Programı bitirmek için 'bitir' demeniz yeterlidir.")

while True:
    print("Asistan mı yoksa resim mi?")
    speak_response("Asistan mı yoksa resim mi?")
    sendMessage = speech_to_text()

    if "asistan" in sendMessage:
        current_mode = "asistan"

        while True:
            print("Dinliyorum... ")
            sendMessage = speech_to_text()

            if "resim" in sendMessage:
                current_mode = "resim"
                break

            if "asistan" in sendMessage:  
                current_mode = "asistan"
                break

            if "bitir" in sendMessage:
                speak_response("Programdan çıkılıyor.")
                sys.exit()

            else:
                convo.send_message(sendMessage)
                response = convo.last.text
                print(response)
                speak_response(response)

    elif "resim" in sendMessage:
        current_mode = "resim"

        while True:
            speak_response("Aramak istediğiniz resmi sesle belirtin.")
            adana = speech_to_text()
            if "asistan" in adana:
                current_mode = "asistan"
                break
            if "bitir" in adana:
                speak_response("Programdan çıkılıyor.")
                sys.exit()
            gorsel(adana)


            speak_response("Başka bir resim aramak ister misiniz? ")
            cevap = speech_to_text()
            if "evet" in cevap:
                continue
            elif "hayır" in cevap:
                sys.exit()
            elif "bitir" in cevap:
                sys.exit()

    else:
        speak_response("Lütfen 'asistan' veya 'resim' şeklinde cevap verin.")
