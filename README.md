# llm-security-filters
## How to run
- run ollama
- python main.py
- (optional) if necessary, adjust the configuration

## Tests

### unit & integrated
pytest tests
pytest -s .\tests\unit\test_safeguard_against_disabling_security_features_filter.py::test_blocked_complex_input_high_entropy

### with .md report file
python generate_test_report.py
or (remember to point the test target in the generate_test_report.py)
python generate_test_report.py .\tests\unit\test_bypass_detection_filter.py ( or + '::test' )


### system
python -m tests.system.test_00      : -m used to run a module as a script. Relative imports work as expected.

### with .md report file
in test file in the end call generate_report()
Example:
ts.generate_report(test_cases, ts.compute_overall_metrics, "test_reports/test_L_00.md")

## Cache
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
