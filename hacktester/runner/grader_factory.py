import inspect
import language_graders.languages


class LanguageNotSupported(Exception):
    pass


class GraderFactory:
    GRADERS = {}
    klasses = [m[0] for m in inspect.getmembers(language_graders.languages, inspect.isclass)
               if m[1].__module__ == 'language_graders.languages']

    for name in klasses:
        klass = getattr(language_graders.languages, name)
        GRADERS[klass.LANGUAGE_NAME] = klass

    @classmethod
    def get_grader(cls, language):
        language = language.lower()
        if language not in cls.GRADERS:
            raise LanguageNotSupported(language)

        return cls.GRADERS[language]
