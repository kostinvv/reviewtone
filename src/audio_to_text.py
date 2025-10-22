# pip install pydub SpeechRecognition.
# https://www.ffmpeg.org/download.html
# https://www.gyan.dev/ffmpeg/builds/ -- для Windows.

import speech_recognition

from pydub import AudioSegment

def ogg_to_wav(filename):
    try:
        new_filename = filename.replace('.ogg', '.wav')
        audio = AudioSegment.from_file(filename)
        audio.export(new_filename, format='wav')
        return new_filename
    except Exception as e:
        print(f"Error converting OGG to WAV: {e}")
        return None
    
def recognize_speech(wav_filename: str) -> str | None:
    recognizer = speech_recognition.Recognizer()
    try:
        with speech_recognition.WavFile(wav_filename) as source:
            wav_audio = recognizer.record(source)
        text = recognizer.recognize_google(wav_audio, language='ru-RU')
        return text
    except speech_recognition.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "Не удалось распознать речь."
    except speech_recognition.RequestError as e:
        print(f"Could not request results from Google service; {e}")
        return "Произошла ошибка при обращении к сервису распознавания."
    
