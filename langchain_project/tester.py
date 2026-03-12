import os

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
TEST_PROMPT = f"""
Analyse actions and tests in {GITHUB_REPOSITORY} and generate issues to improve test coverage and CI configuration.
Tests must include edge cases and boundary conditions and contain assertions to verify expected behavior,
so issues must be created both to implement tests to cover untested code and improve existing test suites with additional tests.
Issues must be created with a title and a description. 
The title should be a short summary of the issue, while the description should provide a list of changes to improve test coverage and CI configuration.
CI code must be such that it runs all unit tests and exits with a failure status code when a test fails or the coverage doesn't reach a given threshold.
Black box testing is also a requirement for the automated test suite, so issues must be created to implement it when it's not present.
Black box tests must assert expected behavior based on the specification of the code, without relying on its implementation details.
Other tools such as static analysis, check style, linters and vulnerability scanners must be used in every CI run to identify potential issues in the codebase.
Such tools might be suggested in the issues when they're not present in the CI configuration.
"""