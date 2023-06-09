# To download big files you should create new Telegram Client.
# Follow instructions at https://core.telegram.org/api/obtaining_api_id 
# and fullfil API_ID and API_HASH in botToken.py
download_big_files = True

# Whisper speech recognition software's model options and their relative speed and size of DB:
# tiny (x32, 78MB), base(x16, 145MB), small(x6, 484MB), medium(x2, 1.5GB), large(x1, 3.1GB).
# These are general models. English-only models also exist. Check https://github.com/openai/whisper .
whisper_model = 'small'

# Selecting the Speech Recognition Library: 'whisper' or 'vosk'
speech_recognition_lib = 'whisper'

# Path to the Language Models Folder for vosk
vosk_models_path = 'vosk_models'