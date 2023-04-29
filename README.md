# Telegram Speech Recognition Bot

This Telegram bot is designed to convert voice messages into text using speech recognition. Users can choose from multiple languages for the voice recognition, making it a versatile tool for multi-language chats or personal use.

## Features

- Supports English, Russian, Ukrainian, and Portuguese languages for speech recognition.
- Allows users to choose the language of the voice message for accurate transcription.
- Built on the Aiogram and Openai-Whisper libraries for efficient and easy-to-maintain code.

## Installation

1. Install [Python 3.10.10](https://www.python.org/downloads/release/python-31010/)

2. Open console and clone the repository:

```
git clone https://github.com/yourusername/telegram-speech-recognition-bot.git
```

3. Change to the bot's directory:

```
cd telegram-speech-recognition-bot
```

4. Install the required Python packages using pip:

```
pip install
```

5. Set up your API token:

- Create a new bot on Telegram by talking to the  [@botFather](https://t.me/botfather).
- Based on `config/_example/botToken.py` create `config/prod/botToken.py` (for production) and/or `config/dev/botToken.py` (for development). 
- Copy your API token and replace the placeholder `API_TOKEN` in `botToken.py`

6. Run the bot:

```
python -m TelegramSpeechRecognitionBot
```

## Usage

1. Start a chat with the bot.
2. Send a voice message to the bot.
3. Choose the language of the voice message from the provided options.
4. The bot will process the voice message and send you the transcribed text as a document.


## Support

If you have any issues or feature requests, please open an issue on the [GitHub](https://github.com/soberhacker/telegram-speech-recognition-bot).

If you like this plugin and are considering donating to support continued development, use the buttons below!

[![Buy me a banana](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20banana&emoji=🍌&slug=soberhacker&button_colour=5F5F5F&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00)](https://www.buymeacoffee.com/soberhacker)

[![Ko-fi Donation](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/soberhacker)

[![PayPal Donation](https://www.paypalobjects.com/webstatic/en_US/i/buttons/PP_logo_h_100x26.png)](https://www.paypal.com/donate/?hosted_button_id=VYSCUZX8MYGCU)
