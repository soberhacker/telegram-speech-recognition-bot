import re
import logging
from whisper.model import Whisper
from whisper import load_model
import config.botSettings as config

def transcribe_whisper(model, file_path, language='ru'):    
    whisper_model: Whisper = model
    logging.info('Audio recognition started (whisper)')    
    result = whisper_model.transcribe(file_path, verbose=False, language = language)
    rawtext = ' '.join([segment['text'].strip() for segment in result['segments']]) # type: ignore
    rawtext = re.sub(" +", " ", rawtext)
    alltext = re.sub(r"([\.\!\?]) ", r"\1\n", rawtext)
    logging.info(f'Recognized: {alltext}')
    return alltext

def load_whisper_model(lang_code) -> Whisper:
    whisper_model = config.whisper_model + ('.' + lang_code if lang_code == 'en' else '' )
    return load_model(whisper_model)        

""" # TODO: Add async transcribe_whisper and transcribe_vosk
async def stt(audio_file_path) -> str:
    logging.info('Audio recognition started')
    loop = asyncio.get_event_loop()    
    try:
        return await loop.run_in_executor(None, transcribe_whisper, audio_file_path)
    except:
        await asyncio.sleep(30)
        try:
            return await loop.run_in_executor(None, transcribe_whisper, audio_file_path)
        except:
            await asyncio.sleep(30)
            return await loop.run_in_executor(None, transcribe_whisper, audio_file_path) """