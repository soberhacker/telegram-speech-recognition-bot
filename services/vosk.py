import config.botSettings as config 
import os
from vosk import KaldiRecognizer, Model
import json
import logging
def load_vosk_model(lang_code):
    model_path = os.path.join(config.vosk_models_path, lang_code)
    return Model(model_path)

def transcribe_vosk(file_path, model):    
    logging.info('Audio recognition started (vosk)')

    with open(file_path, 'rb') as file:
        audio_data = file.read()

    recognizer = KaldiRecognizer(model, 16000)
    recognizer.AcceptWaveform(audio_data)
    result_json = recognizer.FinalResult()
    result = json.loads(result_json)
    text = result['text']
    logging.info(f'Recognized: {text}')
    return text
