# Assignment 7 — Sensor Data Analyzer

## Description

**Read this entire assignment before you begin, and pay special attention to testing using test.py.**

In this assignment, you will build your first **multifile Python program** that uses a **third-party library**.

You will create a small sensor-data analysis application organized across several modules. The program will use NumPy for numerical array operations, a separate reporting module for output, and a separate benchmark module to compare an ordinary Python loop with a vectorized NumPy operation.

This assignment introduces several important project-level concepts at the same time:

- multifile program architecture;
- driver files and supporting modules;
- module imports and namespaces;
- virtual environments;
- third-party packages;
- dependency declaration with `requirements.txt`;
- NumPy `ndarray` objects;
- vectorized numerical operations;
- Boolean filtering;
- multidimensional arrays;
- theoretical algorithmic efficiency using Big O;
- empirical performance measurement using benchmarking; and
- testing modules independently.

Because this is your **first multifile Python project**, the starter repository is intentionally more complete than recent assignments.

The architecture, files, required function interfaces, and supplied tests are already provided.

Your job is to complete the implementation correctly and understand why the project is organized this way.

Future assignments will expect you to create more of this structure independently.

---

## Learning Objectives

By completing this assignment, you should be able to:

- explain the difference between a module, package, and library;
- explain the purpose of a Python virtual environment;
- create and activate a `.venv`;
- install a third-party package into the active environment;
- explain the purpose of `requirements.txt`;
- use imports to connect multiple program modules;
- explain the role of `main.py` as the driver file;
- use NumPy arrays for numerical data;
- calculate along an array axis;
- use NumPy Boolean filtering;
- use vectorized array arithmetic;
- preserve input data rather than mutate it unintentionally;
- use explicit loops when the assignment requires them as a learning exercise;
- distinguish theoretical algorithmic efficiency from empirical performance;
- explain why two O(n) implementations can have different measured runtimes;
- benchmark equivalent operations fairly;
- use supplied tests to verify separate modules and the complete program;
- maintain meaningful incremental Git history; and
- use generative AI while retaining responsibility for understanding, design, and verification.

---

## Background

Before beginning this assignment, complete and review:

- **Modularity and Multifile Programs Part I** lecture and notes;
- **Modularity and Multifile Programs Part II** lecture and notes;
- **Libraries, Packages, and NumPy** lecture and notes;
- **Algorithmic Efficiency and Performance Analysis** lecture and notes;
- the course handout **`requirements.txt` — Declaring Python Dependencies**;
- the [Best Practices for Procedural Programming](https://katrompas.accprofessors.com/best-practice-procedural-programming);
- the course [Commenting Guidelines](https://katrompas.accprofessors.com/commenting);
- the [.gitignore guidelines](https://katrompas.accprofessors.com/gitignore-guidelines);
- the [README Guidelines](https://katrompas.accprofessors.com/readme-guidelines); and
- the course [commit guidelines](https://katrompas.accprofessors.com/committing).

This assignment assumes that you understand:

- functions and function contracts;
- `main()` as a driver;
- imports and module namespaces;
- cohesion and separation of responsibilities;
- explicit data flow through parameters and return values;
- lists and multidimensional traversal;
- NumPy arrays and vectorized operations;
- Big O at the introductory level; and
- benchmarking as empirical performance measurement.

---

## Starter Repository

Your starter repository contains:

```text
ASSIGNMENT.md
ESSAY.md
README.md
.gitignore
requirements.txt
main.py
analysis.py
report.py
benchmark.py
test.py
```

Do not rename these files.

Do not modify `test.py`.

The starter source files already contain:

- the required module structure;
- imports;
- required function names and parameter lists;
- function stubs;
- comments identifying important learning requirements; and
- incomplete docstrings that you must finish according to course standards.

This assignment is heavily scaffolded intentionally.

---

# Part I — Prepare the Python Environment

## 1. Complete `requirements.txt`

The starter `requirements.txt` contains an instructional comment.

Replace the instructional content with the third-party dependency required by this project:

```text
numpy
```

Do not use `pip freeze`.

For this assignment, manually declare the dependency you actually need.

## 2. Create the virtual environment

From the repository root:

### Windows using Git Bash

```bash
python -m venv .venv
```

### macOS

```bash
python3 -m venv .venv
```

## 3. Activate the environment

### Windows using Git Bash

```bash
source .venv/Scripts/activate
```

### macOS

```bash
source .venv/bin/activate
```

After activation, your terminal prompt will normally indicate that `.venv` is active.

## 4. Install project dependencies

With the virtual environment **active**:

```bash
python -m pip install -r requirements.txt
```

## 5. Verify NumPy

Run:

```bash
python -c "import numpy as np; print(np.__version__)"
```

A NumPy version number should be displayed.

## 6. Verify `.gitignore`

The supplied `.gitignore` already ignores:

```text
.venv/
```

Do not remove this entry.

Your virtual environment must **not** be committed to Git.

Remember:

> Source code belongs in Git. Dependencies are declared in `requirements.txt`. Installed packages live in `.venv/`.

---

# Part II — Project Architecture

The project is intentionally separated by responsibility:

```text
main.py
    program driver and orchestration

analysis.py
    NumPy numerical analysis

report.py
    formatted program output

benchmark.py
    performance comparison

test.py
    supplied testing module
```

This organization demonstrates **cohesion**.

Functions with related responsibilities are kept together, while unrelated responsibilities are separated into different modules.

The intended dependency structure is approximately:

```text
main.py
   |
   +----> analysis.py
   |
   +----> benchmark.py
   |
   +----> report.py

test.py
   |
   +----> analysis.py
   +----> benchmark.py
   +----> report.py
   +----> main.py
```

`main.py` is the application driver.

The supporting modules should not start the application when imported.

---

# Part III — Required Sensor Data

The supplied `main.py` already contains the required NumPy array:

```python
readings = np.array([
    [72.4, 73.1, 71.8, 74.2, 75.0],
    [68.9, 69.5, 70.1, 69.8, 71.2],
    [80.2, 79.8, 81.1, 82.0, 80.7],
    [65.5, 66.0, 64.8, 67.1, 66.4],
])
```

Each row represents one sensor.

Each column represents one observation.

Therefore the array has:

```text
4 sensors
5 observations per sensor
20 total readings
```

The supplied driver also defines:

```python
threshold = 75.0
calibration_offset = -0.5
```

Do not change the required data, threshold, or calibration offset in the final submitted program.

---

# Part IV — `analysis.py`

The analysis module contains five required functions.

The module must use NumPy for the required numerical work.

Computational functions must return their results and must not print.

The original `readings` array must not be modified.

---

## `calculate_sensor_means(readings)`

This function must:

- receive a two-dimensional NumPy array;
- calculate the mean of each sensor row;
- use NumPy's `mean` operation;
- use the correct axis;
- return a one-dimensional NumPy array containing one mean per sensor;
- contain no more than one `return` statement; and
- not print anything.

For the required data, the result is approximately:

```text
[73.30, 69.90, 80.76, 65.96]
```

Do not hardcode these values.

---

## `calculate_overall_mean(readings)`

This function must:

- receive the complete NumPy array;
- use NumPy's `mean` operation;
- calculate the mean of all readings;
- return the resulting value;
- contain no more than one `return` statement; and
- not print anything.

For the required data:

```text
72.48
```

when formatted to two decimal places.

---

## `get_high_readings(readings, threshold)`

This function must:

- receive the complete readings array and a threshold;
- use a NumPy Boolean expression to create the selection condition;
- use Boolean filtering to select values **strictly greater than** the threshold;
- return a NumPy array containing the selected readings;
- preserve NumPy's normal traversal order;
- contain no explicit `for` or `while` loop;
- contain no more than one `return` statement;
- not modify `readings`; and
- not print anything.

For the required data and threshold `75.0`, the selected readings are:

```text
80.20
79.80
81.10
82.00
80.70
```

Notice that `75.0` itself is **not** included because the requirement is strictly greater than the threshold.

---

## `apply_calibration(readings, offset)`

This function must:

- receive the readings array and numeric calibration offset;
- apply the offset to the entire array using vectorized NumPy arithmetic;
- return a **new NumPy array**;
- contain no explicit `for` or `while` loop;
- not modify the original `readings` array;
- contain no more than one `return` statement; and
- not print anything.

For this assignment:

```text
offset = -0.5
```

so every reading is reduced by `0.5`.

---

## `find_highest_average_sensor(readings)`

This function must:

- call `calculate_sensor_means(readings)`;
- determine which sensor has the highest mean;
- return a tuple:

  ```text
  (one-based sensor number, sensor average)
  ```

- use an explicit loop;
- initialize the running highest position from actual data;
- contain no more than one `return` statement;
- not modify the supplied array; and
- not print anything.

For the required data:

```text
Sensor 3
80.76
```

### Required Learning Exercise: Do Not Use `argmax()`

NumPy provides `argmax()`, which could identify the position of the largest average more directly.

**Do not use `argmax()` in this function.**

The explicit loop is required as a learning exercise.

The purpose is to connect earlier repetition and running-state algorithms with values produced by NumPy.

This is not a claim that the explicit loop is always the most idiomatic professional NumPy solution.

---

# Part V — `benchmark.py`

This module compares two implementations of the same operation:

> multiply every value by `2`

One implementation uses an ordinary Python list and explicit loop.

The other uses a NumPy array and vectorized arithmetic.

Both process every element.

Therefore both are:

```text
O(n)
```

The benchmark investigates their **measured performance**, not their Big O classification.

---

## `python_double(values)`

This function must:

- receive a Python list;
- create a new Python list;
- use an explicit loop;
- append each doubled value to the result list;
- return the new list;
- contain no more than one `return` statement; and
- not print anything.

---

## `numpy_double(values)`

This function must:

- receive a NumPy array;
- use vectorized NumPy multiplication;
- return a new NumPy array containing doubled values;
- contain no explicit loop;
- contain no more than one `return` statement; and
- not print anything.

---

## `run_benchmark(size)`

This function must compare the two doubling implementations fairly.

It must return:

```text
(python_time, numpy_time)
```

Both values must be elapsed times in seconds.

### Benchmark Pseudocode

Use the following algorithm:

```text
create Python list containing size values
create NumPy array containing equivalent size values

start timer
call python_double() using the Python list
stop timer
calculate Python elapsed time

start timer
call numpy_double() using the NumPy array
stop timer
calculate NumPy elapsed time

verify both result collections have the same length

return Python elapsed time and NumPy elapsed time
```

### Important Benchmark Rule

Create **both input collections before timing begins**.

Do not include NumPy array construction inside the NumPy timing while excluding list construction from the Python timing.

The benchmark must compare the same conceptual operation on already-created data.

Use:

```python
from time import perf_counter
```

for timing.

The supplied `main.py` will call:

```python
benchmark.run_benchmark(500_000)
```

The actual timing numbers will vary by machine and from one run to another.

You are **not** required to prove that NumPy is always faster.

---

# Part VI — `report.py`

The report module contains:

```python
display_report(
    readings,
    sensor_means,
    overall_mean,
    high_readings,
    adjusted_readings,
    highest_sensor,
    threshold,
    calibration_offset,
    python_time,
    numpy_time,
)
```

This function intentionally has a long parameter list.

Do **not** redesign the required interface for this assignment.

The function receives its dependencies explicitly rather than depending on global program state or recalculating analysis owned by another module.

Long parameter lists also create design tradeoffs.

You will analyze this interface in `ESSAY.md`.

---

## Required Report Behavior

`display_report()` must display:

- the program title;
- the array shape;
- each sensor's mean;
- the overall mean;
- each reading strictly above the threshold;
- the sensor with the highest average;
- the complete calibrated two-dimensional array;
- the Python benchmark time;
- the NumPy benchmark time; and
- the statement that both doubling operations are O(n).

The function should use the results supplied through parameters.

Do not repeat the analysis calculations inside `report.py`.

---

## Required Learning Exercise: Explicit Traversal

More compact Python and NumPy formatting techniques exist.

For this assignment, `display_report()` must use explicit traversal.

In particular:

- use a loop when displaying sensor means;
- use a loop when displaying high readings; and
- use a **nested loop** when displaying the calibrated two-dimensional array.

The nested loop is required as a learning exercise to reinforce multidimensional traversal.

This is not a claim that manual nested-loop formatting is always the cleanest professional Python solution.

---

# Part VII — `main.py`

`main.py` is the driver file.

The required imports and data are already supplied.

Complete `main()` so that it:

1. calls the required analysis functions;
2. retains their returned results;
3. calls `benchmark.run_benchmark(500_000)`;
4. retains both timing results; and
5. calls `report.display_report()` using all required values.

`main()` should coordinate the application.

Do not move analysis, reporting, or benchmarking implementation into the driver.

Use module namespaces clearly:

```python
analysis.function_name(...)
benchmark.function_name(...)
report.function_name(...)
```

The standard run guard is already supplied:

```python
if __name__ == "__main__":
    main()
```

Do not remove it.

---

# Part VIII — Required Output

Timing values will vary.

All other output must follow this form exactly:

```text
Sensor Data Analyzer
Data shape: 4 sensors x 5 observations
Sensor Means
Sensor 1: 73.30
Sensor 2: 69.90
Sensor 3: 80.76
Sensor 4: 65.96
Overall Mean: 72.48
Readings Above 75.00
80.20
79.80
81.10
82.00
80.70
Highest Average Sensor: Sensor 3 - 80.76
Calibrated Readings (-0.50)
Sensor 1: 71.90 72.60 71.30 73.70 74.50
Sensor 2: 68.40 69.00 69.60 69.30 70.70
Sensor 3: 79.70 79.30 80.60 81.50 80.20
Sensor 4: 65.00 65.50 64.30 66.60 65.90
Benchmark
Python loop time: <measured value> seconds
NumPy time: <measured value> seconds
Both doubling operations are O(n).
```

Numeric sensor values must display with the formatting shown.

Benchmark values must display with exactly six digits after the decimal point.

Do not hardcode measured timing values.

---

# Part IX — Supplied Tests

The repository includes:

```text
test.py
```

Do not modify it.

Run:

```bash
python test.py
```

or:

```bash
python3 test.py
```

depending on your system.

The supplied test module is also a teaching example.

Read its module docstring and inspect the tests.

The tests demonstrate how a separate test module can:

- import application modules;
- test functions independently;
- use alternate data;
- capture output;
- inspect selected structural requirements;
- verify module interfaces; and
- test a complete application.

The supplied tests verify:

- required project files;
- dependency metadata;
- required function signatures;
- run guard and import-safe module behavior;
- sensor and overall means;
- use of NumPy mean;
- Boolean filtering;
- vectorized calibration;
- preservation of the original array;
- the required explicit loop for highest-sensor analysis;
- prohibition of `argmax()` in that learning exercise;
- the single-return rule;
- equivalent Python and NumPy doubling behavior;
- required loop/vectorization contrast;
- benchmark return values;
- required report traversal;
- report behavior with alternate supplied values; and
- complete application output.

The final program should report:

```text
15/15 tests passed
```

Passing the tests is necessary, but it does not represent the complete assignment grade.

There is **no Classroom 50 autograding** for this assignment.

### **Run the supplied tests locally throughout development.**

---

# Part X — Programming Standards and Constraints

The normal course standards apply.

In particular:

- each source file must contain the required file header docstring;
- every function must contain a course-standard function docstring;
- each function may contain no more than one `return` statement;
- computational functions return rather than print;
- supporting modules must not unexpectedly execute application behavior when imported;
- dependencies should be explicit;
- avoid global program state;
- do not modify supplied arrays unless the specification explicitly requires mutation;
- `main.py` remains the driver;
- use the module architecture supplied by the assignment.

Do not use:

- `while True`;
- `break`;
- `continue`;
- recursion;
- classes;
- lambda expressions;
- comprehensions where the assignment requires explicit traversal;
- `np.argmax()` in `find_highest_average_sensor()`;
- explicit loops where vectorized NumPy operations are required;
- file input/output; or
- additional third-party libraries.

Do not create additional user-defined functions unless specifically approved.

---

# Part XI — Documentation Requirements

The supplied function docstrings contain a short description and this instruction:

```text
(complete this docstring to course standards and erase this comment)
```

You must replace that instruction with the complete course-standard documentation.

For example, an appropriate final docstring includes fields such as:

```python
"""
:purpose: ...
:param readings: ...
:param threshold: ...
:return: ...
:assumptions/preconditions: ...
:side-effects: ...
"""
```

Use descriptions appropriate to the actual function.

Do not merely copy generic wording.

The documentation should explain the interface and contract of the function you implemented.

---

# Part XII — Git and Development Process

Develop incrementally.

Do not complete the entire project and then create one final code commit.

This assignment contains several distinct modules and capabilities. Your Git history should show those capabilities being developed and integrated over time.

Your repository must contain **at least twelve meaningful program-development commits**.

**Twelve** is the minimum, not the target.

Meaningful milestones may include:

- preparing the project environment;
- completing dependency metadata;
- implementing a numerical analysis capability;
- implementing Boolean filtering;
- implementing calibration;
- implementing highest-sensor analysis;
- implementing one benchmark approach;
- completing the benchmark;
- implementing reporting;
- integrating modules through the driver;
- fixing a real test failure; or
- making another coherent program improvement.

Do not manufacture meaningless commits merely to reach the minimum.

Changes only to:

```text
README.md
ESSAY.md
```

do not count toward the required program-development commits.

Test before committing.

Push regularly.

---

# Part XIII — Generative AI

Use of generative AI is required.

You may use AI as a:

- tutor;
- programming partner;
- design critic;
- debugging assistant;
- NumPy explanation tool;
- testing assistant; or
- performance-analysis assistant.

You may show AI the complete assignment and supplied tests.

You remain responsible for:

- understanding every line of code;
- rejecting techniques outside the assignment scope;
- verifying NumPy behavior;
- interpreting test failures;
- preserving required learning exercises;
- evaluating benchmark design;
- making final implementation decisions; and
- explaining the completed project in `ESSAY.md`.

AI may suggest `np.argmax()`, comprehensions, alternative formatting techniques, additional modules, classes, or other valid approaches that violate this assignment's required learning design.

Follow the assignment contract.

---

# Part XIV — `README.md`

Complete the supplied README according to the course [README Guidelines](https://katrompas.accprofessors.com/readme-guidelines).

In addition to normal project documentation, include an **Environment / Dependencies** section that explains:

- Python 3 is required;
- NumPy is required;
- the project uses a virtual environment;
- dependencies are declared in `requirements.txt`; and
- dependencies can be installed with:

  ```bash
  python -m pip install -r requirements.txt
  ```

Do not include `.venv/` in the repository.

---

# Part XV — `ESSAY.md`

Complete all five supplied questions.

The questions focus on:

- multifile architecture and module responsibilities;
- virtual environments and `requirements.txt`;
- NumPy versus explicit Python iteration;
- Big O versus measured performance; and
- the intentionally long `display_report()` interface.

Each question is worth **2 points**, for a total of **10 points**.

Your answers must refer to your actual project and demonstrate substantive reasoning.

---

# Final Review and Submission

Before submitting:

### 1. Activate the virtual environment

Make sure `.venv` is active.

### 2. Verify the dependency

Run:

```bash
python -c "import numpy as np; print(np.__version__)"
```

### 3. Run the complete program

```bash
python main.py
```

Verify the report manually.

### 4. Run the supplied tests

```bash
python test.py
```

Verify:

```text
15/15 tests passed
```

### 5. Check Git status

```bash
git status
```

Your working tree should be clean.

### 6. Review development history

```bash
git log --oneline
```

Verify that your history shows meaningful incremental development and contains at least **twelve** qualifying program-development commits.

### 7. Review the repository

Confirm that the repository contains:

```text
ASSIGNMENT.md
ESSAY.md
README.md
.gitignore
requirements.txt
main.py
analysis.py
report.py
benchmark.py
test.py
```

Confirm that `.venv/` is **not** present on GitHub.

### 8. Review documentation

Verify that:

- all instructional docstring comments have been removed;
- every function has a complete course-standard docstring;
- the README is complete;
- the ESSAY is complete; and
- temporary debugging code has been removed.

### 9. Submit through Blackboard

Submit the normal HTTPS URL of the completed GitHub repository in Blackboard.
