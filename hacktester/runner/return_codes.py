OK = 0
COMPILATION_ERROR = 4
TIME_LIMIT_ERROR = 2
MEMORY_LIMIT_ERROR = -9
WRONG_ANSWER = 1
LINT_ERROR = 5
RUN_EXCEPTION = 6
UNKNOWN_EXCEPTION = 7
CALLED_PROCESS_ERROR = 8
UNSUPPORTED_TEST_TYPE = 9
REQUIREMENTS_FAILED = 10


RETURN_CODE_OUTPUT = {
    OK: "OK",
    COMPILATION_ERROR: "compilation_error",
    TIME_LIMIT_ERROR: "time_limit_reached",
    MEMORY_LIMIT_ERROR: "memory_limit_reached",
    WRONG_ANSWER: "incorrect_answer",
    LINT_ERROR: "lint_error",
    RUN_EXCEPTION: "runtime_error",
    UNKNOWN_EXCEPTION: "test_run_error",
    CALLED_PROCESS_ERROR: "test_failed_to_run",
    UNSUPPORTED_TEST_TYPE: "test_type_unsupported",
    REQUIREMENTS_FAILED: "requirements_failed_to_install"
}
