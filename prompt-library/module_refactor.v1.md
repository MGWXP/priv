---
name: "Module_Refactor"
version: "1.0"
description: "Refactors existing code to improve quality without changing functionality."
inputs: ["src/", "tests/"]
outputs: ["src/"]
dependencies: []
author: "AI"
last_updated: "2025-05-20"
marker: refactor
status: "active"
---

# Code Refactoring Module

## Purpose

This module guides the AI in refactoring existing code to improve quality, readability, performance, or maintainability without altering the core functionality.

## Prompt

You are an AI software engineer tasked with refactoring code in the project. Your goal is to improve the code quality while preserving the existing behavior. Follow these steps:

1. **Analyze Current Code**:
   - Review the code to be refactored
   - Identify code smells, inefficiencies, or readability issues
   - Check test coverage of the code you'll refactor
   - Note any potential risks in refactoring

2. **Plan Refactoring Strategy**:
   - List specific issues to address
   - Determine what patterns or techniques to apply
   - Create a step-by-step plan
   - Consider if any additional tests are needed before refactoring

3. **Implement Refactoring**:
   - Make changes incrementally, running tests after each change
   - Follow the project's style guidelines (see AGENTS.md)
   - Use meaningful variable/function names
   - Add or improve comments and docstrings
   - Apply appropriate design patterns if relevant
   - Reduce complexity and improve readability

4. **Focus Areas** (consider these common refactoring tasks):
   - Eliminate code duplication
   - Break down complex functions
   - Improve variable/function naming
   - Optimize inefficient algorithms
   - Replace magic numbers with named constants
   - Add type hints/annotations
   - Improve error handling
   - Enhance modularity and separation of concerns

5. **Verify Behavior**:
   - Run the test suite to ensure nothing broke: `pytest`
   - If tests are insufficient, suggest additional tests
   - Verify any performance claims with benchmarks if applicable

6. **Document Changes**:
   - Summarize what was refactored and why
   - Explain any architectural changes
   - Note any improvements in metrics (complexity, performance)

## Example Output

```
## Refactoring: Data Processing Module

I've refactored the data processing module to improve maintainability and performance:

### Issues Addressed:
1. Reduced function complexity in process_data()
2. Eliminated duplicate code in validation functions
3. Added type hints throughout the module
4. Improved variable naming for clarity
5. Extracted utility functions to separate file
6. Converted nested if statements to early returns
7. Improved error messages

### Performance Improvements:
- Replaced O(n²) algorithm with O(n log n) approach in sort_records()
- Reduced memory usage by streaming large records instead of loading entirely
- Added caching for repeated calculations

### Files Changed:
- src/data/processor.py
- src/data/validators.py (new file, extracted from processor.py)
- src/utils/data_helpers.py (new file)

All tests are passing, and the processing time for the benchmark dataset improved from 3.2s to 0.8s.

Test confirmation:
$ pytest tests/data/test_processor.py -v
15 passed in 1.32s
```

<* End of prompt instructions *>
