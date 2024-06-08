from plyer import camera, filechooser
from vosk import Model, KaldiRecognizer
from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import wave  # создание и чтение аудиофайлов формата wav
import json  # работа с json-файлами и json-строками
import os 
import pyaudio

class Photo:
    # def __init__(self):

    def take_photo(callback):
        # Используем Plyer для доступа к камере и получения фотографии
        try:
            camera.take_picture(on_complete=callback, filename='photo.jpg')
        except NotImplementedError:
            print("Функция камеры не реализована для этой платформы")

    def load_photo(callback):
        # Используем Plyer для открытия файлового диалога
        try:
            filechooser.open_file(on_selection=callback)
        except NotImplementedError:
            print("Функция выбора файла не реализована для этой платформы")

class Audio:
    def __init__(self):
        model_path = r"C:\Users\Alexander\Downloads\vosk-model-small-ru-0.22\vosk-model-small-ru-0.22"
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Путь к модели {model_path} не существует.")
        
        try:
            self.model = Model(model_path)
            print("Модель успешно загружена.")
        except Exception as e:
            print(f"Не удалось создать модель: {e}")
            raise
        
        self.vosk_recognizer = KaldiRecognizer(self.model, 16000)
        print("Распознаватель успешно инициализирован.")
        
        self.recognized_text = ""
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()
        print("Инициализация завершена.")
        self.record_and_recognize_audio()

    def record_and_recognize_audio(self):
        with self.microphone:
            self.recognizer.adjust_for_ambient_noise(self.microphone, duration=2)

            try:
                print("Идёт запись...")
                audio = self.recognizer.listen(self.microphone, 5, 10)

                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())
            except speech_recognition.WaitTimeoutError:
                print("Проверьте ваш микрофон..")
                return

            try:
                print("Распознаю..")
                self.recognized_text = self.use_offline_recognition()
                if not self.recognized_text:
                    return "Аудио не содержит голосового сообщения, проверьте ваш микрофон"
                else:
                    return str(self.recognized_text)
            except Exception as e:
                print("Ошибка при распознавании:", e)
        
    def use_offline_recognition(self):
        recognized_data = ""

        wave_audio_file = wave.open("microphone-results.wav", "rb")
        offline_recognizer = KaldiRecognizer(self.model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                try:
                    print('обрабатываю')
                    recognized_data = offline_recognizer.Result()

                    recognized_data = json.loads(recognized_data)
                    res_recognize = recognized_data.get("text", "")
                    return str(res_recognize)
                except:
                    print("не распознанно")
                    return recognized_data
        return recognized_data

    #  def record_and_recognize_audio(self):
    #     p = pyaudio.PyAudio()
    #     stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    #     stream.start_stream()

    #     print("Listening...")
    #     recognized_data = ""
    #     while True:
    #         data = stream.read(4000)
    #         if len(data) == 0:
    #             break
    #         if self.recognizer.AcceptWaveform(data):
    #             result = self.recognizer.Result()
    #             recognized_data = json.loads(result)["text"]
    #             break

    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()

    #     print("Recognized:", recognized_data)
    #     return recognized_data
    