import pyttsx3

engine = pyttsx3.init(driverName="sapi5")
voices = engine.getProperty('voices')

# Find the voice with Cantonese language
for voice in voices:
    if voice.languages[0] == 'zh-HK':
        engine.setProperty('voice', voice.id)
        break

engine.say("你好，你好嗎？")
engine.runAndWait()