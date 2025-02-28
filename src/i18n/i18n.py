import json
from os import listdir
from os.path import join, isdir

from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message

from src.i18n.languages import Languages


class I18n:
    def __init__(self, default_language='ru'):
        self.default_language = default_language
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        languages_dir = 'i18n'
        for lang in Languages.SUPPORTED_LANGUAGES:
            lang_path = join(languages_dir, lang)
            if isdir(lang_path):
                with open(join(lang_path, 'strings.json'), 'r', encoding='utf-8') as file:
                    if lang not in self.translations:
                        self.translations[lang] = {}
                    self.translations[lang].update(json.load(file))


    def translate(self, user_data: Message | CallbackData | None, key: str):
        language = user_data.from_user.language_code
        if language in self.translations or language is None:
            return self.translations.get(language if language else self.default_language, {}).get(key, key)
        else:
            raise ValueError(f"Language '{language}' is not supported.")


i18n = I18n()
