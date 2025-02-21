class Languages:
    SUPPORTED_LANGUAGES = {
        'ru': 'Русский',
        'en': 'English'
    }

    @classmethod
    def get_supported_languages(cls):
        return cls.SUPPORTED_LANGUAGES
