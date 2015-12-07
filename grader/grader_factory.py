from language_graders.python import PythonGrader


class LanguageNotSupported(Exception):
    pass


class GraderFactory:
    GRADERS = {
        "python": PythonGrader
    }

    @classmethod
    def get_grader(cls, language):
        language = language.lower()
        if language not in cls.GRADERS:
            raise LanguageNotSupported(language)

        return cls.GRADERS[language]
