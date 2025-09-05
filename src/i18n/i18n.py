import json
from os.path import join, isdir

from src.i18n.languages import Languages


class I18n:
    def __init__(self, default_language='ru'):
        self.default_language = default_language
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        languages_dir = 'src/i18n'
        for lang in Languages.SUPPORTED_LANGUAGES:
            lang_path = join(languages_dir, lang)
            if isdir(lang_path):
                with open(join(lang_path, 'strings.json'), 'r', encoding='utf-8') as file:
                    if lang not in self.translations:
                        self.translations[lang] = {}
                    self.translations[lang].update(json.load(file))


    def translate(self, language_code: str | None, key: str):
        if language_code in self.translations or language_code is None:
            return self.translations.get(
                language_code if language_code else self.default_language, {}
            ).get(key, key)
        raise ValueError(f"Language '{language_code}' is not supported.")


i18n = I18n()
