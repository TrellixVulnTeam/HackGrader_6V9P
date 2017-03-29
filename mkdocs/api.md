## API

### Format of the data sent to /grade

#### for unittest:

    {
    "test_type": "unittest",
    "language": language,   # currently supported `java, python, ruby, javascript/nodejs`
    "solution": file, # base_64 format
    "test": file, # base_64 format
    "extra_options": { 
        'qualified_class_name': "com.hackbulgaria.grader.Tests", # for java binary solutions only
    }}

##### Format of the solution and test content for `JavaScript`

* Functions in solution file must be exported (e.g., `module.exports = function() { };`)
* Test file must require the solution file (e.g., `var testedFunc = require('solution')`)
* Use `describe` or `it`


#### for output_checking:

    {
    "test_type": "output_checking",
    "language": language,   # currently supported `java, python, ruby`
    "solution": file, # base_64 format
    "test": file, # archive with `.in` and `.out` files
    "extra_options": {
        "class_name": `solution class name` # for java binary solutions only
        "archive_test_type": True #
    }}

##### Optional fields in extra_options:
        
-   `time_limit`: integer # set time limit for the test suite in seconds
-   `lint`: True # In case we want to run rubocop(ruby) or flake8(python).
-   `archive_test_type`: True # if the test file is archive
-   `archive_solution_type`: True # if the solution file is archive


### Format of the data returned by /check_result

#### for unittest:

    {
    "run_status": run.status,  # the status of the test run
    "result_status": result.status, # the status of the test result
    "run_id": run.id,
    "output": {"test_status": test_status,  # the status of the result ("ok", "compilation_error" etc..)
               "test_output": result.output} # the output of the result
    }


#### for output_checking:

    {
    "run_status": run.status,  # the status of the test run
    "result_status": result.status, # the status of the test result
    "run_id": run.id,
    "output": [{"test_status": test_status,
                "test_output": result.output},] # the list contains results for for each .in .out pair of tests
    }