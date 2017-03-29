from hacktester.runner.settings import (
    RUBY,
    JAVA,
    PYTHON,
    UNITTEST,
    JAVASCRIPT,
    OUTPUT_CHECKING,
)

from .test_preparators import (
    RubyUnittestPreparator,
    JavaUnittestPreparator,
    PythonUnittestPreparator,
    JavaScriptUnittestPreparator,

    RubyOutputCheckingPreparator,
    JavaOutputCheckingPreparator,
    PythonOutputCheckingPreparator
)


PREPARATOR_PICKER = {
    UNITTEST: {
        RUBY: RubyUnittestPreparator,
        PYTHON: PythonUnittestPreparator,
        JAVASCRIPT: JavaScriptUnittestPreparator,
        JAVA: JavaUnittestPreparator
    },
    OUTPUT_CHECKING: {
        RUBY: RubyOutputCheckingPreparator,
        JAVA: JavaOutputCheckingPreparator,
        PYTHON: PythonOutputCheckingPreparator
    }
}


class PreparatorFactory:
    @staticmethod
    def get(pending_task):
        test_type = pending_task.test_type.value
        language = pending_task.language.name.lower()

        preparator_cls = PREPARATOR_PICKER[test_type][language]

        return preparator_cls(pending_task)
