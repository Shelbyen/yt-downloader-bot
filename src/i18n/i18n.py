import json
from os import listdir
from os.path import join, isdir


class I18n:
    def __init__(self, default_language='tu'):
        self.default_language = default_language
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        languages_dir = 'i18n'
        for lang in listdir(languages_dir):
            lang_path = join(languages_dir, lang)
            if isdir(lang_path):
                for file_name in listdir(lang_path):
                    if file_name.endswith('.json'):
                        with open(join(lang_path, file_name), 'r', encoding='utf-8') as file:
                            if lang not in self.translations:
                                self.translations[lang] = {}
                            self.translations[lang].update(json.load(file))
