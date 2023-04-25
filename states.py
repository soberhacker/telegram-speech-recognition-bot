from aiogram.dispatcher.filters.state import State, StatesGroup

class VoiceRecognitionStates(StatesGroup):
    language = State()

class ErrorStates(StatesGroup):    
    emptyOrUnsupportedLanguage = State()

class FinishStates(StatesGroup):
    success = State()
    cancel = State()
