# generate_test_report.py
import pytest
import sys
import os

# Get the target path from CLI or use default
target = sys.argv[1] if len(sys.argv) > 1 else "tests\\unit\\test_profanity_filter.py"
normalized = target.replace("\\", "/")

# Determine base name for report (func > file > dir)
if "::" in normalized:
    report_name = normalized.split("::")[-1]
else:
    base = os.path.basename(normalized)
    name, ext = os.path.splitext(base)
    report_name = name if ext == ".py" else base

pytest.main([
    target,  # can be a directory (like "tests"), a specific test file ("tests\\unit\\test_profanity_filter.py") or single test ("tests\\unit\\test_profanity_filter.py::test_func")
    "--capture=tee-sys",  # capture stdout for the reporter
    "--tb=long",          # full tracebacks, short – minimal traceback or no – no traceback at all
    "--maxfail=1000",     # stop after N test failures.
    "-p", "report_generator.markdown_reporter", # loads a custom plugin (our Markdown reporter). "report_generator.markdown_reporter" must point to a valid Python module that implements pytest hooks.
    f"--report-name={report_name}"
])
