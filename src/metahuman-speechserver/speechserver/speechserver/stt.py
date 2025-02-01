import json
import speech_recognition as sr

def wav_to_text(path):
    try:
        r = sr.Recognizer()
        audio = sr.AudioFile(path)
        with audio as source:
            r.adjust_for_ambient_noise(source, duration=.2)
            audio_data = r.record(source)
            result = r.recognize_google(audio_data)
        return result
    except sr.UnknownValueError:
        return json.dumps({'error': 'Unable to recognize speech'})
    except Exception as ex:
        return json.dumps({'error': 'An error occurred during speech recognition'})
