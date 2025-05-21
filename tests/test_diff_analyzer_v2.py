from ai_workflow import DiffAnalyzerV2


def test_diff_analyzer_v2_feat(tmp_path):
    analyzer = DiffAnalyzerV2()
    old = ""
    new = 'def foo():\n    """doc"""\n    return 1\n'
    analysis = analyzer.analyze_file_diff(old, new, "src/foo.py")
    test_old = ""
    test_new = "def test_foo():\n    assert foo() == 1\n"
    test_analysis = analyzer.analyze_file_diff(test_old, test_new, "tests/test_foo.py")
    result = analyzer.verify_marker_alignment([analysis, test_analysis], "feat")
    assert result["compliant"] is True


def test_diff_analyzer_v2_docs(tmp_path):
    analyzer = DiffAnalyzerV2()
    old = "Old"
    new = "New"
    analysis = analyzer.analyze_file_diff(old, new, "docs/readme.md")
    result = analyzer.verify_marker_alignment([analysis], "docs")
    assert result["compliant"] is True


def test_diff_analyzer_v2_fix_requires_test(tmp_path):
    analyzer = DiffAnalyzerV2()
    old = "def foo():\n    return 1\n"
    new = "def foo():\n    return 2\n"
    analysis = analyzer.analyze_file_diff(old, new, "src/foo.py")
    result = analyzer.verify_marker_alignment([analysis], "fix")
    assert result["compliant"] is False
    test_old = ""
    test_new = "def test_foo():\n    assert foo() == 2\n"
    test_analysis = analyzer.analyze_file_diff(test_old, test_new, "tests/test_foo.py")
    result = analyzer.verify_marker_alignment([analysis, test_analysis], "fix")
    assert result["compliant"] is True


def test_coding_standard_check(tmp_path):
    analyzer = DiffAnalyzerV2()
    old = ""
    new = "def bar():\n    return 1\n"
    analysis = analyzer.analyze_file_diff(old, new, "src/bar.py")
    result = analyzer.check_coding_standards([analysis])
    assert result["compliant"] is False
