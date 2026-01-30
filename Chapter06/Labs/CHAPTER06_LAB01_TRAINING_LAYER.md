# Chapter 06 — Lab 1: Training Layer (Train + Evaluate a Baseline Model)

[Back to all lab instructions](../../LAB_INSTRUCTIONS.md)

**Duration**: ~30 minutes (hands-on)

## Goal

Run through a minimal, end-to-end **Training Layer** workflow in the Sandpit: open a workbench, access data, perform a small amount of shaping, train a baseline model, evaluate it, and save the resulting artifacts so the work is repeatable.

> Replace the placeholders in this lab once you paste/provide the official “Lab overview” steps (slide or text).

## Learning outcomes

By the end of this lab you can:

- Use a project workbench for interactive data science work
- Load a dataset and apply basic preparation steps
- Train a baseline model and capture evaluation metrics
- Save model artifacts + metadata so the work can be repeated and reviewed
- Explain where this lab sits in the lifecycle (Define/EDA/Shape/Train/Test)

## Prerequisites

| Item | Notes |
|---|---|
| Sandpit access | Cluster/console URL + credentials |
| A project/namespace | You can create or have one assigned |
| Workbench tooling | Jupyter/VS Code workbench available in your environment |
| Dataset | Use a safe dataset (public, synthetic, or facilitator-provided) |

---

## Lab steps

### Lab overview (timebox)

> Placeholder: insert screenshot/steps from the Chapter 6 Lab 1 overview slide.

| Step | What you’ll do | Time |
|---:|---|---:|
| 1 | Open a project workbench and confirm environment | ~5 mins |
| 2 | Load a dataset and run quick EDA | ~7 mins |
| 3 | Shape data + train a baseline model | ~10 mins |
| 4 | Evaluate (score/test) and capture results | ~5 mins |
| 5 | Save artifacts (model + metrics) to storage | ~3 mins |

---

### 1) Open a workbench and confirm environment

- [ ] Log in to the Sandpit / OpenShift console.
- [ ] Switch to your project/namespace.
- [ ] Launch a **Project Workbench** (Jupyter or VS Code-based).
- [ ] Confirm the runtime has Python available.

Suggested quick check (inside a notebook/terminal):

```bash
python --version
```

Capture:
- [ ] Workbench image/runtime name (if visible)
- [ ] Python version

---

### 2) Load a dataset and run quick EDA

Use one of these options:

- Option A: facilitator-provided dataset location (recommended)
- Option B: a small public dataset copied into the workbench
- Option C: synthetic dataset generated in-code

Tasks:
- [ ] Load dataset into a dataframe
- [ ] Inspect shape, column types, missing values
- [ ] Identify the target/label column (if supervised)

Capture:
- [ ] Dataset source/location
- [ ] Target/label definition
- [ ] Any quality issues found

---

### 3) Shape data + train a baseline model

Tasks (keep it simple):
- [ ] Split into train/test (and validation if needed)
- [ ] Basic preparation: encoding, scaling, missing value handling
- [ ] Train a baseline model (e.g., logistic regression / random forest)

Capture:
- [ ] What baseline model you chose and why
- [ ] Key preprocessing choices

---

### 4) Evaluate (score/test) and capture results

Tasks:
- [ ] Evaluate on held-out test data
- [ ] Record at least one primary metric and one diagnostic view

Examples:
- Classification: accuracy, precision/recall, confusion matrix
- Regression: MAE/RMSE, residuals plot

Capture:
- [ ] Metrics
- [ ] 2–3 example errors/failures (what does the model struggle with?)

---

### 5) Save artifacts (model + metrics)

Goal: make the outcome shareable and repeatable.

Tasks:
- [ ] Save the trained model artifact (e.g., pickle/onnx)
- [ ] Save a small `metrics.json` (and optionally `params.json`)
- [ ] Save the dataset version reference used for training

Where to store (pick what your environment supports):
- Object storage bucket/path
- Project storage (PVC)
- Git repo folder (small artifacts only)

Capture:
- [ ] Artifact location(s)
- [ ] What someone would need to reproduce the run (data version + code)

---

## Reflection (optional, 2 minutes)

- [ ] Which lifecycle stages did you complete in this lab?
- [ ] What would you automate next (pipeline candidate)?
- [ ] What would you require before deploying this model?

**Lab completed**
