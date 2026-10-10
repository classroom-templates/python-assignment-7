#!/usr/bin/env python3

"""
Assignment 7 — Supplied Tests

Run this test module from the project directory with:

    python test.py

or, on systems where Python 3 is named explicitly:

    python3 test.py

These tests are part of the Assignment 7 contract.

You are allowed and encouraged to read this file. The tests show you what
interfaces, behaviors, and selected structural requirements your program is
expected to satisfy.

DO NOT MODIFY THIS FILE.

This file is also intended to serve as an example of a properly structured test
module at your current level of understanding.

Notice several design ideas in this file:

- testing code is kept separate from the program being tested;
- the program modules are imported and tested independently;
- small helper functions support repeated testing work;
- individual test functions focus on specific behaviors;
- alternate data is used so hardcoded answers do not pass;
- structural requirements can be inspected with Python's `ast` module;
- output can be captured and examined without changing the program;
- tests are collected in one place and run by a simple test driver;
- failures are reported clearly so they can guide development.

You are not expected to reproduce all of these techniques from memory yet.
The purpose is to begin recognizing what a test module looks like and how
testing can be organized separately from application code.

The tests verify:

- required project files;
- required function names and parameter lists;
- dependency metadata;
- correct NumPy behavior;
- selected function-design requirements;
- required learning-exercise structures;
- module behavior with alternate data; and
- complete program output.

Passing all supplied tests is necessary, but it is not the same as earning a
perfect assignment grade. The tests do not evaluate every course requirement,
including the quality of your documentation, Git history, README, ESSAY,
overall design choices, or your understanding of the submitted work.

Use the tests throughout development:

    write or complete a small capability
    run test.py
    read the results
    reason about any failure
    correct your program
    test again

The goal is not merely to make every line say PASS.

The goal is to understand why it passes.
"""

import ast
import importlib
import io
import math
import re
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np


PROJECT_DIR = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "main.py",
    "analysis.py",
    "report.py",
    "benchmark.py",
    "requirements.txt",
    ".gitignore",
]

REQUIRED_FUNCTIONS = {
    "analysis": {
        "calculate_sensor_means": ["readings"],
        "calculate_overall_mean": ["readings"],
        "get_high_readings": ["readings", "threshold"],
        "apply_calibration": ["readings", "offset"],
        "find_highest_average_sensor": ["readings"],
    },
    "report": {
        "display_report": [
            "readings",
            "sensor_means",
            "overall_mean",
            "high_readings",
            "adjusted_readings",
            "highest_sensor",
            "threshold",
            "calibration_offset",
            "python_time",
            "numpy_time",
        ],
    },
    "benchmark": {
        "python_double": ["values"],
        "numpy_double": ["values"],
        "run_benchmark": ["size"],
    },
    "main": {
        "main": [],
    },
}


def normalize_output(text):
    """Normalize line endings and trailing whitespace."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    result = "\n".join(
        line.rstrip() for line in text.strip().splitlines()
    )

    return result


def close_enough(actual, expected):
    """Compare numeric values safely."""
    result = False

    try:
        result = math.isclose(
            float(actual),
            float(expected),
            rel_tol=1e-9,
            abs_tol=1e-9,
        )
    except (TypeError, ValueError):
        result = False

    return result


def load_tree(filename):
    """Read and parse one Python source file."""
    path = PROJECT_DIR / filename

    if not path.exists():
        raise AssertionError(f"{filename} was not found.")

    source = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise AssertionError(
            f"{filename} has a syntax error on line "
            f"{exc.lineno}: {exc.msg}"
        ) from exc

    result = (source, tree)

    return result


def get_function_nodes(tree):
    """Return top-level function definitions keyed by name."""
    functions = {}

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = node

    return functions


def import_module_safely(module_name):
    """Import a project module while capturing unexpected import output."""
    if str(PROJECT_DIR) not in sys.path:
        sys.path.insert(0, str(PROJECT_DIR))

    if module_name in sys.modules:
        del sys.modules[module_name]

    captured = io.StringIO()

    try:
        with redirect_stdout(captured):
            module = importlib.import_module(module_name)
    except Exception as exc:
        raise AssertionError(
            f"{module_name}.py could not be imported: "
            f"{type(exc).__name__}: {exc}"
        ) from exc

    result = (module, captured.getvalue())

    return result


def count_returns(function_node):
    """Count return statements in a required top-level function."""
    count = 0

    for node in ast.walk(function_node):
        if isinstance(node, ast.Return):
            count += 1

    return count


def called_simple_names(function_node):
    """Collect simple function calls made inside a function."""
    calls = set()

    for node in ast.walk(function_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)

    return calls


def called_attribute_names(function_node):
    """Collect attribute-style calls such as np.mean() or np.argmax()."""
    calls = set()

    for node in ast.walk(function_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)

    return calls


def contains_loop(function_node):
    """Determine whether a function contains an explicit for/while loop."""
    result = False

    for node in ast.walk(function_node):
        if isinstance(node, (ast.For, ast.While)):
            result = True

    return result


def max_loop_depth(function_node):
    """Return the maximum explicit loop nesting depth inside a function."""
    maximum = 0

    def visit_statements(statements, depth):
        nonlocal maximum

        for statement in statements:
            if isinstance(statement, (ast.For, ast.While)):
                current = depth + 1

                if current > maximum:
                    maximum = current

                visit_statements(statement.body, current)
                visit_statements(statement.orelse, current)
            else:
                nested_groups = []

                if isinstance(statement, ast.If):
                    nested_groups = [
                        statement.body,
                        statement.orelse,
                    ]
                elif isinstance(statement, ast.Try):
                    nested_groups = [
                        statement.body,
                        statement.orelse,
                        statement.finalbody,
                    ]

                    for handler in statement.handlers:
                        nested_groups.append(handler.body)

                for group in nested_groups:
                    visit_statements(group, depth)

    visit_statements(function_node.body, 0)

    return maximum


def has_standard_run_guard(tree):
    """Check for the standard course run guard."""
    result = False

    for node in tree.body:
        if isinstance(node, ast.If):
            test = node.test

            correct_test = (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and len(test.ops) == 1
                and isinstance(test.ops[0], ast.Eq)
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            )

            if correct_test and len(node.body) == 1:
                statement = node.body[0]

                correct_call = (
                    isinstance(statement, ast.Expr)
                    and isinstance(statement.value, ast.Call)
                    and isinstance(statement.value.func, ast.Name)
                    and statement.value.func.id == "main"
                    and not statement.value.args
                    and not statement.value.keywords
                )

                if correct_call:
                    result = True

    return result


def test_01_required_project_files():
    """Required project files exist and dependency metadata is correct."""
    for filename in REQUIRED_FILES:
        assert (PROJECT_DIR / filename).exists(), (
            f"Missing required file: {filename}"
        )

    requirements = (
        PROJECT_DIR / "requirements.txt"
    ).read_text(encoding="utf-8")

    requirement_lines = []

    for line in requirements.splitlines():
        cleaned = line.strip()

        if cleaned and not cleaned.startswith("#"):
            requirement_lines.append(cleaned.lower())

    has_numpy = False

    for line in requirement_lines:
        if re.match(r"^numpy(?:\s*[<>=!~].*)?$", line):
            has_numpy = True

    assert has_numpy, (
        "requirements.txt must declare NumPy."
    )

    gitignore = (
        PROJECT_DIR / ".gitignore"
    ).read_text(encoding="utf-8")

    normalized = [
        line.strip().rstrip("/")
        for line in gitignore.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    assert ".venv" in normalized, (
        ".gitignore must ignore the .venv/ directory."
    )


def test_02_required_functions_and_signatures():
    """Required functions exist with the exact parameter lists."""
    for module_name, functions in REQUIRED_FUNCTIONS.items():
        _, tree = load_tree(f"{module_name}.py")
        nodes = get_function_nodes(tree)

        for name, expected_parameters in functions.items():
            assert name in nodes, (
                f"Missing required function: "
                f"{module_name}.{name}()"
            )

            actual_parameters = [
                argument.arg
                for argument in nodes[name].args.args
            ]

            assert actual_parameters == expected_parameters, (
                f"{module_name}.{name}() must use parameters "
                f"({', '.join(expected_parameters)})."
            )

            assert nodes[name].args.vararg is None, (
                f"{module_name}.{name}() must not use *args."
            )

            assert nodes[name].args.kwarg is None, (
                f"{module_name}.{name}() must not use **kwargs."
            )


def test_03_main_run_guard_and_safe_imports():
    """Modules import without output and main.py uses the standard run guard."""
    _, main_tree = load_tree("main.py")

    assert has_standard_run_guard(main_tree), (
        'Expected the standard run guard in main.py:\n'
        'if __name__ == "__main__":\n'
        '    main()'
    )

    for module_name in [
        "analysis",
        "benchmark",
        "report",
        "main",
    ]:
        _, import_output = import_module_safely(module_name)

        assert normalize_output(import_output) == "", (
            f"Importing {module_name}.py produced output. "
            "Supporting modules should not run the application "
            "when imported."
        )


def test_04_sensor_means_and_overall_mean():
    """Mean functions work with alternate NumPy data."""
    analysis, _ = import_module_safely("analysis")

    readings = np.array([
        [10.0, 20.0, 30.0],
        [40.0, 50.0, 60.0],
    ])

    sensor_means = analysis.calculate_sensor_means(readings)
    overall_mean = analysis.calculate_overall_mean(readings)

    assert isinstance(sensor_means, np.ndarray), (
        "calculate_sensor_means() must return a NumPy ndarray."
    )

    assert np.allclose(
        sensor_means,
        np.array([20.0, 50.0]),
    ), (
        "calculate_sensor_means() returned incorrect values."
    )

    assert close_enough(overall_mean, 35.0), (
        f"Expected overall mean 35.0, "
        f"received {overall_mean!r}."
    )


def test_05_mean_functions_use_numpy_mean():
    """The required mean calculations use NumPy's mean operation."""
    _, tree = load_tree("analysis.py")
    nodes = get_function_nodes(tree)

    for name in [
        "calculate_sensor_means",
        "calculate_overall_mean",
    ]:
        calls = called_attribute_names(nodes[name])

        assert "mean" in calls, (
            f"{name}() must use NumPy's mean operation."
        )


def test_06_high_readings_boolean_filtering():
    """High readings are selected correctly with NumPy-style vectorized work."""
    analysis, _ = import_module_safely("analysis")
    _, tree = load_tree("analysis.py")
    node = get_function_nodes(tree)["get_high_readings"]

    readings = np.array([
        [70.0, 75.0, 75.1],
        [80.0, 60.0, 90.0],
    ])

    original = readings.copy()
    result = analysis.get_high_readings(readings, 75.0)

    expected = np.array([75.1, 80.0, 90.0])

    assert isinstance(result, np.ndarray), (
        "get_high_readings() must return a NumPy ndarray."
    )

    assert np.allclose(result, expected), (
        f"Expected {expected}, received {result}."
    )

    assert np.array_equal(readings, original), (
        "get_high_readings() must not modify the original array."
    )

    assert not contains_loop(node), (
        "get_high_readings() must use NumPy Boolean filtering, "
        "not an explicit Python loop."
    )


def test_07_calibration_vectorized_and_nonmutating():
    """Calibration uses vectorized array arithmetic and preserves the input."""
    analysis, _ = import_module_safely("analysis")
    _, tree = load_tree("analysis.py")
    node = get_function_nodes(tree)["apply_calibration"]

    readings = np.array([
        [10.0, 20.0],
        [30.0, 40.0],
    ])

    original = readings.copy()
    result = analysis.apply_calibration(readings, -0.5)

    expected = np.array([
        [9.5, 19.5],
        [29.5, 39.5],
    ])

    assert isinstance(result, np.ndarray), (
        "apply_calibration() must return a NumPy ndarray."
    )

    assert np.allclose(result, expected), (
        "apply_calibration() returned incorrect values."
    )

    assert np.array_equal(readings, original), (
        "apply_calibration() must not modify the original array."
    )

    assert not np.shares_memory(readings, result), (
        "apply_calibration() should return a new array."
    )

    assert not contains_loop(node), (
        "apply_calibration() must use vectorized NumPy arithmetic, "
        "not an explicit Python loop."
    )


def test_08_highest_sensor_uses_required_loop():
    """Highest-average sensor is correct and uses the required learning loop."""
    analysis, _ = import_module_safely("analysis")
    _, tree = load_tree("analysis.py")
    node = get_function_nodes(tree)[
        "find_highest_average_sensor"
    ]

    first_highest = np.array([
        [100.0, 100.0],
        [20.0, 20.0],
        [30.0, 30.0],
    ])

    last_highest = np.array([
        [10.0, 10.0],
        [20.0, 20.0],
        [90.0, 100.0],
    ])

    first_result = analysis.find_highest_average_sensor(
        first_highest
    )
    last_result = analysis.find_highest_average_sensor(
        last_highest
    )

    assert first_result[0] == 1
    assert close_enough(first_result[1], 100.0)

    assert last_result[0] == 3
    assert close_enough(last_result[1], 95.0)

    calls = called_simple_names(node)

    assert "calculate_sensor_means" in calls, (
        "find_highest_average_sensor() must call "
        "calculate_sensor_means()."
    )

    assert contains_loop(node), (
        "find_highest_average_sensor() must use an explicit loop "
        "for this learning exercise."
    )

    attribute_calls = called_attribute_names(node)

    assert "argmax" not in attribute_calls, (
        "Do not use NumPy argmax() in "
        "find_highest_average_sensor()."
    )


def test_09_single_return_rule():
    """Required functions contain no more than one return statement."""
    for module_name, functions in REQUIRED_FUNCTIONS.items():
        _, tree = load_tree(f"{module_name}.py")
        nodes = get_function_nodes(tree)

        for name in functions:
            count = count_returns(nodes[name])

            assert count <= 1, (
                f"{module_name}.{name}() contains "
                f"{count} return statements."
            )


def test_10_python_and_numpy_double_equivalent():
    """Python and NumPy doubling implementations produce equivalent results."""
    benchmark, _ = import_module_safely("benchmark")

    python_values = [1, 2, 3, 4, 5]
    numpy_values = np.array(
        [1, 2, 3, 4, 5]
    )

    python_result = benchmark.python_double(
        python_values
    )
    numpy_result = benchmark.numpy_double(
        numpy_values
    )

    assert isinstance(python_result, list), (
        "python_double() must return a Python list."
    )

    assert isinstance(numpy_result, np.ndarray), (
        "numpy_double() must return a NumPy ndarray."
    )

    assert python_result == [2, 4, 6, 8, 10]
    assert np.array_equal(
        numpy_result,
        np.array([2, 4, 6, 8, 10]),
    )


def test_11_benchmark_uses_loop_and_vectorization():
    """Benchmark implementations use the required contrasting approaches."""
    _, tree = load_tree("benchmark.py")
    nodes = get_function_nodes(tree)

    python_node = nodes["python_double"]
    numpy_node = nodes["numpy_double"]

    assert contains_loop(python_node), (
        "python_double() must use an explicit Python loop."
    )

    assert not contains_loop(numpy_node), (
        "numpy_double() must use a vectorized NumPy operation, "
        "not an explicit loop."
    )


def test_12_run_benchmark_returns_valid_times():
    """run_benchmark() returns two numeric, nonnegative timing values."""
    benchmark, _ = import_module_safely("benchmark")

    result = benchmark.run_benchmark(10_000)

    assert isinstance(result, tuple), (
        "run_benchmark() must return a tuple."
    )

    assert len(result) == 2, (
        "run_benchmark() must return "
        "(python_time, numpy_time)."
    )

    python_time = result[0]
    numpy_time = result[1]

    assert isinstance(
        python_time,
        (int, float),
    ), "Python timing must be numeric."

    assert isinstance(
        numpy_time,
        (int, float),
    ), "NumPy timing must be numeric."

    assert python_time >= 0, (
        "Python timing must not be negative."
    )

    assert numpy_time >= 0, (
        "NumPy timing must not be negative."
    )


def test_13_report_uses_required_explicit_traversal():
    """Report contains explicit loops, including nested 2-D traversal."""
    _, tree = load_tree("report.py")
    node = get_function_nodes(tree)["display_report"]

    assert contains_loop(node), (
        "display_report() must use explicit traversal."
    )

    assert max_loop_depth(node) >= 2, (
        "display_report() must include a nested loop when "
        "displaying the calibrated 2-D array."
    )


def test_14_report_with_supplied_alternate_results():
    """Report uses caller-supplied analysis and timing values."""
    report, _ = import_module_safely("report")

    readings = np.array([
        [10.0, 20.0],
        [30.0, 40.0],
    ])

    sensor_means = np.array([15.0, 35.0])
    overall_mean = 25.0
    high_readings = np.array([30.0, 40.0])
    adjusted = np.array([
        [9.5, 19.5],
        [29.5, 39.5],
    ])
    highest_sensor = (2, 35.0)

    captured = io.StringIO()

    with redirect_stdout(captured):
        result = report.display_report(
            readings,
            sensor_means,
            overall_mean,
            high_readings,
            adjusted,
            highest_sensor,
            25.0,
            -0.5,
            0.123456,
            0.012345,
        )

    expected = """Sensor Data Analyzer
Data shape: 2 sensors x 2 observations
Sensor Means
Sensor 1: 15.00
Sensor 2: 35.00
Overall Mean: 25.00
Readings Above 25.00
30.00
40.00
Highest Average Sensor: Sensor 2 - 35.00
Calibrated Readings (-0.50)
Sensor 1: 9.50 19.50
Sensor 2: 29.50 39.50
Benchmark
Python loop time: 0.123456 seconds
NumPy time: 0.012345 seconds
Both doubling operations are O(n)."""

    actual = normalize_output(captured.getvalue())

    assert actual == normalize_output(expected), (
        "display_report() did not produce the required output "
        "when supplied alternate results."
    )

    assert result is None, (
        "display_report() should display output rather than "
        "return a calculated result."
    )


def test_15_complete_program_output():
    """Complete program produces the required report structure."""
    completed = subprocess.run(
        [sys.executable, "main.py"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert completed.returncode == 0, (
        "main.py did not complete normally.\n"
        f"{completed.stderr}"
    )

    lines = normalize_output(
        completed.stdout
    ).splitlines()

    expected_static = [
        "Sensor Data Analyzer",
        "Data shape: 4 sensors x 5 observations",
        "Sensor Means",
        "Sensor 1: 73.30",
        "Sensor 2: 69.90",
        "Sensor 3: 80.76",
        "Sensor 4: 65.96",
        "Overall Mean: 72.48",
        "Readings Above 75.00",
        "80.20",
        "79.80",
        "81.10",
        "82.00",
        "80.70",
        "Highest Average Sensor: Sensor 3 - 80.76",
        "Calibrated Readings (-0.50)",
        "Sensor 1: 71.90 72.60 71.30 73.70 74.50",
        "Sensor 2: 68.40 69.00 69.60 69.30 70.70",
        "Sensor 3: 79.70 79.30 80.60 81.50 80.20",
        "Sensor 4: 65.00 65.50 64.30 66.60 65.90",
        "Benchmark",
    ]

    assert len(lines) == 24, (
        f"Expected 24 output lines, received {len(lines)}."
    )

    for index in range(len(expected_static)):
        assert lines[index] == expected_static[index], (
            f"Output line {index + 1} is incorrect.\n"
            f"Expected: {expected_static[index]}\n"
            f"Received: {lines[index]}"
        )

    python_match = re.fullmatch(
        r"Python loop time: ([0-9]+(?:\.[0-9]+)?) seconds",
        lines[21],
    )

    numpy_match = re.fullmatch(
        r"NumPy time: ([0-9]+(?:\.[0-9]+)?) seconds",
        lines[22],
    )

    assert python_match is not None, (
        "Python benchmark output line is incorrectly formatted."
    )

    assert numpy_match is not None, (
        "NumPy benchmark output line is incorrectly formatted."
    )

    assert float(python_match.group(1)) >= 0
    assert float(numpy_match.group(1)) >= 0

    assert lines[23] == (
        "Both doubling operations are O(n)."
    )


TESTS = [
    ("Required project files and dependency metadata",
     test_01_required_project_files),
    ("Required functions and signatures",
     test_02_required_functions_and_signatures),
    ("Run guard and import-safe modules",
     test_03_main_run_guard_and_safe_imports),
    ("Sensor means and overall mean",
     test_04_sensor_means_and_overall_mean),
    ("Mean functions use NumPy mean",
     test_05_mean_functions_use_numpy_mean),
    ("High readings use Boolean filtering",
     test_06_high_readings_boolean_filtering),
    ("Calibration is vectorized and nonmutating",
     test_07_calibration_vectorized_and_nonmutating),
    ("Highest sensor uses required loop",
     test_08_highest_sensor_uses_required_loop),
    ("Single-return rule",
     test_09_single_return_rule),
    ("Python and NumPy doubling are equivalent",
     test_10_python_and_numpy_double_equivalent),
    ("Benchmark loop vs. vectorization",
     test_11_benchmark_uses_loop_and_vectorization),
    ("run_benchmark() returns valid timings",
     test_12_run_benchmark_returns_valid_times),
    ("Report uses required explicit traversal",
     test_13_report_uses_required_explicit_traversal),
    ("Report works with alternate supplied results",
     test_14_report_with_supplied_alternate_results),
    ("Complete program output",
     test_15_complete_program_output),
]


def main():
    """Run all supplied Assignment 7 tests."""
    print("Assignment 7 Tests")
    print()

    passed = 0

    for number, (name, test_function) in enumerate(
        TESTS,
        start=1,
    ):
        try:
            test_function()
            status = "PASS"
            passed += 1
            detail = ""
        except AssertionError as exc:
            status = "FAIL"
            detail = str(exc)
        except Exception as exc:
            status = "FAIL"
            detail = (
                f"{type(exc).__name__}: {exc}"
            )

        print(
            f"{number:02d}. "
            f"{name:<48} "
            f"{status}"
        )

        if detail:
            for line in detail.splitlines():
                print(f"    {line}")

    print()
    print(f"{passed}/{len(TESTS)} tests passed")

    if passed == len(TESTS):
        print("All supplied tests passed.")
    else:
        print(
            "Review the failed tests and continue developing."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
