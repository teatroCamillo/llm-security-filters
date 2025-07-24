# report_generator/markdown_reporter.py
import pytest
import datetime
import os

def pytest_addoption(parser):
    parser.addoption("--report-name", action="store", default="tests", help="Base name for test report file")

class MarkdownReporter:
    def __init__(self):
        self.results = []
        self.start_time = datetime.datetime.now()
        self.counts = {
            "passed": 0,
            "failed": 0,
            "skipped": 0
        }
        self.failed_tests = []
        self.test_target_name = "tests"

    def pytest_configure(self, config):
        self.test_target_name = config.getoption("report_name")

    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            self.results.append(report)
            if report.passed:
                self.counts["passed"] += 1
            elif report.failed:
                self.counts["failed"] += 1
                self.failed_tests.append(report.nodeid)
            elif report.skipped:
                self.counts["skipped"] += 1

    def pytest_sessionfinish(self, session, exitstatus):
        filename = f"test_report_{self.test_target_name}_{self.start_time:%Y%m%d_%H%M%S}.md"
        output_path = os.path.join("test_reports", filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# 🧪 Test Report for `{self.test_target_name}` ({self.start_time})\n\n")
            f.write(f"Total tests: {len(self.results)}\n\n")

            for report in self.results:
                outcome = (
                    "✅ PASSED" if report.passed else
                    "❌ FAILED" if report.failed else
                    "⚠️ SKIPPED"
                )
                f.write(f"- `{report.nodeid}` — {outcome}\n")
                if report.capstdout:
                    f.write(f"**Stdout**:\n```\n{report.capstdout}\n```\n")
                if report.failed:
                    f.write(f"**Traceback**:\n```\n{report.longrepr}\n```\n")
                f.write("\n---\n\n")

            f.write("\n---\n\n")
            f.write("## ✅ Summary\n\n")
            f.write(f"- Total: {len(self.results)}\n")
            f.write(f"- ✅ Passed: {self.counts['passed']}\n")
            f.write(f"- ❌ Failed: {self.counts['failed']}\n")
            f.write(f"- ⚠️ Skipped: {self.counts['skipped']}\n")

            if self.failed_tests:
                f.write("\n## ❌ Failed Tests\n\n")
                for nodeid in self.failed_tests:
                    f.write(f"- `{nodeid}`\n")

def pytest_configure(config):
    reporter = MarkdownReporter()
    reporter.pytest_configure(config)
    config.pluginmanager.register(reporter, "markdown-reporter")
