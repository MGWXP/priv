from ai_workflow.regression_suite import RegressionSuiteRunner


def test_regression_suite_runner(tmp_path):
    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    test_file = test_dir / "test_sample.py"
    test_file.write_text("def test_ok():\n    assert True\n")

    runner = RegressionSuiteRunner(str(test_dir))
    result = runner.run()

    assert result["returncode"] == 0
    assert "1 passed" in result["summary"]
