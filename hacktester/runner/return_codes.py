OK = 0
COMPILATION_ERROR = 1
TIME_LIMIT_ERROR = 2
MEMORY_LIMIT_ERROR = 3
WRONG_ANSWER = 4
LINT_ERROR = 5
RUN_EXCEPTION = 6
UNKNOWN_EXCEPTION = 7
CALLED_PROCESS_ERROR = 8
UNSUPPORTED_TEST_TYPE = 9


RETURN_CODE_OUTPUT = {
    OK: "OK",
    COMPILATION_ERROR: "compilation error",
    TIME_LIMIT_ERROR: "time limit reached",
    MEMORY_LIMIT_ERROR: "memory limit reached",
    WRONG_ANSWER: "incorrect answer",
    LINT_ERROR: "lint error",
    RUN_EXCEPTION: "runtime error",
    UNKNOWN_EXCEPTION: "test failed to run",
    CALLED_PROCESS_ERROR: "test failed to run",
    UNSUPPORTED_TEST_TYPE: "test type unsupported"
}
