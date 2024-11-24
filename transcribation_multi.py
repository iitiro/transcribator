import assemblyai as aai
import os

# Шлях до файлу з API ключем
api_key_file = '/Users/ikudinov/Documents/Code/keys/api_assembly.txt'
# Папка з файлами для транскрипції
audio_folder = '/Users/ikudinov/Documents/Code/!transcribation/audio'
# Папка для збереження текстових файлів
text_folder = '/Users/ikudinov/Documents/Code/!transcribation/text'

# Перевірка наявності файлу з API ключем
if not os.path.exists(api_key_file):
    print(f"Файл {api_key_file} не знайдено.")
    exit(1)

# Читання ключа з файлу
with open(api_key_file, 'r') as file:
    api_key = file.read().strip()

# Встановлення API ключа
aai.settings.api_key = api_key
transcriber = aai.Transcriber()

# Перевірка наявності папки для текстових файлів, якщо її немає - створюємо
if not os.path.exists(text_folder):
    os.makedirs(text_folder)

# Пошук файлів у папці для транскрипції
files = [f for f in os.listdir(audio_folder) if f.endswith(('.mp3', '.mp4', '.wav', '.m4a'))]

# Перевірка, чи є файли для транскрипції
if not files:
    print(f"У папці {audio_folder} не знайдено файлів для транскрипції.")
    exit(1)

# Відображення списку доступних файлів
print("Доступні файли для транскрипції:")
for i, file in enumerate(files):
    print(f"{i + 1}: {file}")

# Вибір файлу для транскрипції
file_index = int(input("Введіть номер файлу для транскрипції: ").strip()) - 1
if file_index < 0 or file_index >= len(files):
    print("Неправильний вибір файлу.")
    exit(1)

# Вибраний файл
selected_file = os.path.join(audio_folder, files[file_index])

# Вибір мови запису
language_choice = input("Введіть мову запису: 'en' для англійської, 'ua' або 'ru' для інших мов: ").strip().lower()

if language_choice == 'en':
    # Конфігурація для англомовних записів з розпізнаванням спікерів
    config = aai.TranscriptionConfig(speaker_labels=True)
    
    # Виконання транскрипції
    transcript = transcriber.transcribe(
        selected_file,
        config=config
    )

    # Формування імені текстового файлу на основі назви аудіофайлу
    output_filename = os.path.splitext(files[file_index])[0] + ".txt"
    output_filepath = os.path.join(text_folder, output_filename)

    # Запис транскрипції у текстовий файл
    with open(output_filepath, 'w', encoding='utf-8') as f:
        for utterance in transcript.utterances:
            f.write(f"Speaker {utterance.speaker}: {utterance.text}\n")

    print(f"Транскрипт збережено: {output_filepath}")

elif language_choice in ['ua', 'ru']:
    # Конфігурація для інших мов (без розпізнавання спікерів)
    config = aai.TranscriptionConfig(
        speech_model=aai.SpeechModel.best,
        language_detection=True
    )     

    # Виконання транскрипції
    transcript = transcriber.transcribe(selected_file, config)

    # Перевірка на помилки транскрипції
    if transcript.status == aai.TranscriptStatus.error:
        print(f"Транскрипція не вдалася для {files[file_index]}: {transcript.error}")
    else:
        # Формування імені текстового файлу на основі назви аудіофайлу
        output_filename = os.path.splitext(files[file_index])[0] + ".txt"
        output_filepath = os.path.join(text_folder, output_filename)

        # Запис транскрипції у текстовий файл
        with open(output_filepath, 'w', encoding='utf-8') as f:
            for sentence in transcript.get_sentences():
                f.write(sentence.text + "\n")

        print(f"Транскрипт збережено: {output_filepath}")

else:
    print("Неправильний вибір мови. Спробуйте ще раз.")

print("Обробка завершена.")