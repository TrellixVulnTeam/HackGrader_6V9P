import json

from .base import UnittestPreparator, OutputCheckingPreparator


class PythonPreparator:
    dependencies = "requirements.txt"

    def prepare(self):
        run_data = super().prepare()

        flake8_configuration = "[flake8]\nignore = W292\nmax-line-length = 120\ndisable-noqa = True"

        self.test_environment.create_new_file('.flake8', flake8_configuration)

        return run_data

    def merge_requirements_data(self):
        solution_requirements = self.get_solution_requirements_data()
        test_requirements = self.get_test_requirements_data()

        merged_requirements = {}
        requirements = ""

        if solution_requirements:
            for line in solution_requirements:
                requirement, version = tuple(line.strip("\n").split("=="))
                merged_requirements[requirement] = version

        if test_requirements:
            for line in test_requirements:
                requirement, version = tuple(line.strip("\n").split("=="))
                merged_requirements[requirement] = version

        for requirement, version in merged_requirements.items():
            requirements += "{}=={}\n".format(requirement, version)

        return requirements


class JavaScriptPreparator:
    dependencies = "package.json"
    """
    TODO: Predefine merge_requirements_data() when you are ready to handle
    dependecies file.
    """

    def prepare(self):
        run_data = super().prepare()

        project_json_data = {
            "scripts": {
                "test": "mocha --reporter tap test.js"
            }
        }

        self.test_environment.create_new_file(self.dependencies, json.dumps(project_json_data))

        return run_data


class RubyPreparator:
    """
    # dependencies = "Gemfile"
    TODO: Predefine merge_requirements_data() when you are ready to handle
    dependecies file.
    """

    def prepare(self):
        run_data = super().prepare()

        rubocop_configuration = '''
            AllCops:
              Exclude:
                - '**/test.rb'
            Documentation:
              Enabled: false
            Style/TrailingBlankLines:
              Enabled: false
        '''

        self.test_environment.create_new_file('.rubocop.yml', rubocop_configuration)

        return run_data


class JavaPreparator:
    def get_solution(self):
        return "{}{}".format(self.test_data['extra_options'].get("class_name"), self.extension)


class PythonUnittestPreparator(PythonPreparator, UnittestPreparator):
    pass


class RubyUnittestPreparator(RubyPreparator, UnittestPreparator):
    pass


class JavaUnittestPreparator(JavaPreparator, UnittestPreparator):
    pass


class JavaScriptUnittestPreparator(JavaScriptPreparator, UnittestPreparator):
    pass


class PythonOutputCheckingPreparator(PythonPreparator, OutputCheckingPreparator):
    pass


class RubyOutputCheckingPreparator(RubyPreparator, OutputCheckingPreparator):
    pass


class JavaOutputCheckingPreparator(JavaPreparator, OutputCheckingPreparator):
    pass
