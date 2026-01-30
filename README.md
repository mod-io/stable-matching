# Algorithm Abstraction Programming Assignment 1

## STABLE MATCHING (GALE–SHAPLEY ALGORITHM)

This project implements the hospital–student stable matching problem using the hospital-proposing Gale–Shapley algorithm. It also includes a verifier to check whether a proposed matching is valid and stable, and a scalability experiment to measure runtime performance.

---

## AUTHORS

Stephen Davis — UFID: 63144483
Sebastian Robalino — UFID: 84159795

---

## REPOSITORY STRUCTURE

```
stable-matching/
│
├── src/
│   ├── Gale-Shapely.py          (matching engine + scalability benchmark)
│   ├── verifier.py             (validity and stability checker)
│
├── data/
│   ├── example.in              (example input instance)
│   ├── example.out             (one valid matching output)
│   ├── matcher_runtime.png     (runtime graph for matching algorithm)
│   ├── verifier_runtime.png    (runtime graph for verifier)
│
└── README.md
```

---

## REQUIREMENTS

Python 3.x
matplotlib

To install matplotlib:

```
python -m pip install matplotlib
```

---

## INPUT FORMAT

The input describes a one-to-one matching market with complete strict rankings.

First line:

```
n
```

Next n lines:
Hospital preference lists

Next n lines:
Student preference lists

Each preference line is a permutation of the integers 1 through n.

---

## OUTPUT FORMAT (MATCHER)

The matcher outputs n lines of the form:

```
i j
```

meaning hospital i is matched to student j.

---

## RUNNING THE MATCHING ALGORITHM (TASK A)

From the src directory:

```
python Gale-Shapely.py ../data/example.in ../data/output.out
```

This runs the hospital-proposing Gale–Shapley algorithm and writes the resulting matching to output.out.

---

## RUNNING THE VERIFIER (TASK B)

```
python verifier.py ../data/example.in ../data/example.out
```

The verifier checks:

* Validity (each hospital and student appears exactly once)
* Stability (no blocking pair exists)

The output will be either:

```
VALID STABLE
```

or a message describing why the matching is invalid or unstable.

---

## SCALABILITY EXPERIMENT (TASK C)

To measure runtime performance for increasing problem sizes:

```
python Gale-Shapely.py --bench 512
```

This command:

* Generates random preference instances for n = 1, 2, 4, 8, ..., 512
* Measures the runtime of the matching algorithm
* Measures the runtime of the verifier

Produces two line graphs:

* matcher_runtime.png
* verifier_runtime.png

---

## OBSERVED TREND (TASK C)

As n increases, the runtime of both the Gale–Shapley matching algorithm and the verifier increases approximately quadratically.

This behavior is expected:

* The hospital-proposing Gale–Shapley algorithm performs at most n² proposals.
* The verifier checks for blocking pairs using ranking tables, resulting in roughly O(n²) comparisons.

The generated graphs reflect this trend, with runtime increasing significantly as n doubles.

---

## ASSUMPTIONS

Input files follow the specified format.
Preference lists are complete and contain no duplicates.
Hospitals and students are labeled from 1 to n.

---

## HOW TO REPRODUCE RESULTS

Clone the repository
Install Python dependencies
Run the matcher, verifier, or benchmark commands listed above
Verify the output files and generated graphs
