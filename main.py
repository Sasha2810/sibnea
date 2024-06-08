from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty 
from kivy.lang import Builder
from kivy.uix.image import Image
from func import Photo, Audio
# from jnius import autoclass
import os
import shutil
from datetime import date
from android.permissions import request_permissions, Permission
from android.storage import primary_external_storage_path # type: ignore
# Environment = autoclass('android.os.Environment')
# File = autoclass('java.io.File')
# FileOutputStream = autoclass('java.io.FileOutputStream')
# FileInputStream = autoclass('java.io.FileInputStream')

Builder.load_string("""
<MenuScreen>:
    orientation: "vertical"
    Label:
        font_size: "25sp"
        text: root.label1
        size_hint_y: None  # Фиксируем высоту Label
        height: 1400  # Задаем высоту Label
        padding: 20, 20  # Добавляем отступы вокруг текста       
    Button:
        text: "Сделать фотографию"
        size_hint: (0.4, 0.1)        
        size: 50, 20
        padding: 20
        pos_hint: {"center_y": .7, "center_x": .5}
        on_press: root.take_photo_app() 
    Button:
        text: "Загрузить фотографию"
        size_hint: (0.4, 0.1)         
        size: 50, 20
        padding: 20
        pos_hint: {"center_y": .6, "center_x": .5}
        on_press: root.load_photo_app()            
    Button:
        text: "Записать голос"
        size_hint: (0.4, 0.1)       
        size: 50, 20
        padding: 20
        pos_hint: {"center_y": .5, "center_x": .5}
        on_press: root.listen_audio()   
    Button:
        text: "Сохранить данные"
        size_hint: (0.4, 0.1)       
        size: 50, 20
        padding: 20
        pos_hint: {"center_y": .3, "center_x": .5}      
        on_press: root.download_data()     
    Label:
        font_size: "20sp"
        text: root.label2
        size_hint_y: None  # Фиксируем высоту Label
        height: 300  # Задаем высоту Label
        padding: 20, 20  # Добавляем отступы вокруг текста       
    Label:
        font_size: "20sp"
        text: root.label3
        size_hint_y: None  # Фиксируем высоту Label
        height: 200  # Задаем высоту Label
        padding: 20, 20  # Добавляем отступы вокруг текста      
""")

class MenuScreen(Screen):
    label1 = StringProperty("Добро пожаловать!")  # Устанавливаем label1 как StringProperty
    label2 = StringProperty("")
    label3 = StringProperty("")

    def save_file_to_android(self):
        if self.label2 and self.filename:
            # Получение директории загрузки на устройстве Android
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            # Путь к внешнему хранилищу
            storage_path = primary_external_storage_path()
            # Путь к папке, где будут сохраняться файлы
            destination_folder = os.path.join(storage_path, f"Data{date.today()}")
            # Создание папки, если она не существует
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            # Пути для сохранения файлов
            f1 = os.path.join(destination_folder, "data_txt.txt")
            f2 = os.path.join(destination_folder, self.filename)

            # Запись данных в файл
            with open(f1, 'w', encoding="utf-8") as f: 
                    f.write(self.label2)

            with open(f2, 'a', encoding="utf-8") as f:
                    f.write(self.label2)
                    f.write(f2)

            self.label3 = "Данные успешно сохранены на ваш телефон"
        else:
            self.label3 = "Не получилось сохранить данные, так как поступили не все данные"


    # функция обратного вызова, после того, как
    def take_photo_app(self):
        Photo.take_photo(self.photo_callback)

    def load_photo_app(self):
        Photo.load_photo(self.photo_callback)

    def photo_callback(self, full_path):
        # функция обратного вызова получает список выбранных файлов.
        if isinstance(full_path, list):
            self.full_path = full_path[0]
            print(self.full_path)
            # Используйте первый элемент списка для получения базового имени файла
            self.filename = os.path.basename(self.full_path)
            print(self.filename)
        # save_path = os.path.join(os.path.expanduser('~'), 'Downloads', file_name)

        #     try:
        #         shutil.copy(file_path, save_path)
        #         self.root.ids.file_path_label.text = f"Файл сохранен: {save_path}"
        #     except Exception as e:
        #         self.root.ids.file_path_label.text = f"Ошибка сохранения файла: {e}"

    def listen_audio(self):
        result_audio = Audio().recognized_text
        self.label2 = result_audio
        print(f"Распознание завершено: {self.label2}")
        return result_audio

    # def download_data(self):
    #     if self.label2 and self.filename:
    #         # Создание папки, если она не существует
    #         destination_folder = r'C:\Users\Alexander\Desktop\sibnea\kivy\folder'
    #         if not os.path.exists(destination_folder):
    #             os.makedirs(destination_folder)
            
    #         # Пути для сохранения файлов
    #         f1 = os.path.join(destination_folder, "data_txt.txt")
    #         f2 = os.path.join(destination_folder, self.filename)
    #         print(f2)
    #         # Запись данных в файл
    #         with open(f1, 'w', encoding="utf-8") as f: 
    #             f.write(self.label2)
    #         with open(f2, 'a', encoding="utf-8") as f:
    #             f.write(self.label2)
    #             f.write(f2)
            
    #         self.label3 = "Данные успешно сохранены на ваш телефон"
    #     else:
    #         self.label3 = "Не получилось сохранить данные, так как поступили не все данные"

            

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))  # Добавляем экран в ScreenManager
        return sm

if __name__ == '__main__':
    MyApp().run()
