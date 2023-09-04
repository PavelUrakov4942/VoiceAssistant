import os
import sys
import webbrowser
import pyttsx3
import speech_recognition
import wikipedia


sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

# Слово, активирующее ассистента
trigger = 'ассистент'

# Словарь ассистента
commands_dict = {
    'commands': {
        'greeting': ['привет', 'добрый день', 'добрый вечер', 'доброе утро'],
        'create_task': ['сделай заметку', 'добавь заметку'],
        'exit': ['пока', 'до свидания', 'всего доброго'],
        'web_search': ['найди в интернете'],
        'wiki': ['найди в википедии'],
        'app': ['открой программу', 'запусти программу']
    }
}


# Функция активации работы ассистента
def activation():
    while True:
        query = listen_command()
        if query.count(trigger) != 0:
            talk('Слушаю вас')
            main()


# Функция распознавания команд пользователя
def main():
    while True:
        query = listen_command()
        for key, variant in commands_dict['commands'].items():
            if query in variant:
                globals()[key]()


# Функция озвучивания текста ассистентом
def talk(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Функция распознавания речи с помощью встроенной языковой модели
def listen_command():
    query = ''
    with speech_recognition.Microphone() as mic:
        sr.adjust_for_ambient_noise(source=mic, duration=0.5)
        audio = sr.listen(source=mic)
        try:
            query = sr.recognize_vosk(audio_data=audio, language='ru-RU').lower()
            query = query[14:-3]
            print(query)
        except speech_recognition.UnknownValueError:
            talk('Извините, я не распознал речь. Можете повторить?')
        return query


# Функция ответа ассистента на приветствие
def greeting():
    return talk('Привет')


# Функция создания текстовой заметки ассистентом
def create_task():
    talk('Что записать в заметки?')
    query = listen_command()
    with open('notes.txt', 'a') as file:
        file.write(f'{query}\n')
    return talk(f'Пункт {query} добавлен в заметки!')


# Функция осуществления ассистентом запроса в браузер
def web_search():
    talk('Что найти?')
    query = listen_command()
    webbrowser.open(f'https://www.google.com/search?q={query}&oq={query}&aqs=edge.0.69i59j0i131i433i512j0i512l6.2107j0j1&sourceid=chrome&ie=UTF-8')


# Функция осуществления ассистентом запроса в википедию
def wiki():
    talk('Что найти?')
    query = listen_command()
    wikipedia.set_lang('ru')
    try:
        result = wikipedia.summary(query, sentences=3)
        talk(result)
    except:
        talk('Не могу выполнить ваш запрос. Повторите попытку.')


# Функция запуска ассистентом указанного приложения в системе
def app():
    talk('Запускаю')
    os.system("здесь должен быть путь к приложению в файловой системе")


# Функция завершения работы программы
def exit():
    talk('До свидания')
    sys.exit()


if __name__ == '__main__':
    activation()
