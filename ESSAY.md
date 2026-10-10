# Assignment 7 — Reflection

Answer each question clearly, specifically, and in your own words.

Your responses must demonstrate **depth of thought and actual engagement with your project**. Short, vague, or generic answers will not receive full credit.

Do not answer with statements such as:

> NumPy is faster.

or:

> We used different files because modularity is good.

Explain what the design means, why it was used, and what you observed or learned.

Whenever possible, refer to specific files, functions, test results, or benchmark behavior from your own project.

Each question is worth **2 points**, for a total of **10 points**.

---

## 1. Module Architecture

Explain why this project separates responsibilities among:

```text
main.py
analysis.py
report.py
benchmark.py
```

For each file, describe its primary responsibility.

Then explain how this design demonstrates **cohesion** and why placing all of the functions back into `main.py` would make the program less modular.

---

## 2. Virtual Environment and `requirements.txt`

Explain the difference between:

```text
.venv/
requirements.txt
```

Your answer must explain:

- what each one contains or represents;
- why `.venv/` should not be committed to Git;
- why `requirements.txt` should be committed; and
- how another developer could use `requirements.txt` to recreate the required third-party dependencies.

---

## 3. NumPy and Required Learning Exercises

Choose **one** of these NumPy-focused functions:

```text
get_high_readings()
apply_calibration()
```

Explain how the function uses NumPy differently from the explicit Python loops you used earlier in the course.

Then explain why `find_highest_average_sensor()` intentionally requires an explicit loop even though NumPy provides `argmax()`.

What is the assignment trying to reinforce by requiring the less compact solution in that function?

---

## 4. Algorithm Analysis vs. Performance Analysis

Both:

```text
python_double()
numpy_double()
```

process every element in their input, so both are O(n).

Explain why they can still have substantially different measured runtimes.

Your answer must distinguish:

- what Big O tells us;
- what benchmarking tells us; and
- why software engineers may need both theoretical algorithm analysis and empirical performance analysis.

Refer to the benchmark results you observed on your own machine.

---

## 5. The Long `display_report()` Interface

`display_report()` intentionally has a long parameter list.

Is that necessarily a design problem?

Explain why or why not.

Describe **at least two possible ways** the interface could be redesigned and discuss an advantage and disadvantage of each approach.

Examples of possibilities you may consider include:

- dividing reporting into additional functions;
- grouping related results into another data structure;
- using an object later in a more advanced design; or
- leaving the explicit parameter list as it is.

You are **not** being asked to redesign the submitted program.

The purpose of this question is to analyze the tradeoff.
