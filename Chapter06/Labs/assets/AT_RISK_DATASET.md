# Chapter 06 Lab 1 — Synthetic “At-risk language” dataset

This folder contains a **synthetic** (safe) dataset you can use for Chapter 6 Lab 1.

## Files

- `at_risk_student_messages_500.csv` — 500 student messages (text + label)
- `at_risk_student_profiles.csv` — student metadata for joins

## Join key

Join on:

- `student_id`

Example join intent:

- Train a model using message text (`text`) to predict `label`
- Join `student_profiles` to demonstrate data shaping (grouping/slicing by `study_mode`, `program`, etc.)

## Label definition

`label` is a binary flag:

- `1 tell staff to follow up` — language that suggests elevated risk of disengagement/non-completion/failing and warrants outreach
- `0 no follow up` — routine queries, neutral feedback, or non-urgent questions

## Columns

`at_risk_student_messages_500.csv`

- `message_id` — unique id
- `student_id` — join key into the student profile table
- `created_at` — ISO-8601 timestamp
- `channel` — `lms_forum` | `email` | `chat` | `support_ticket`
- `program` — program name (also present in profiles for convenience)
- `unit_code` — synthetic unit code
- `week` — teaching week number (1–12)
- `text` — the message body
- `label` — 0/1 target

`at_risk_student_profiles.csv`

- `student_id`
- `age_band`
- `study_mode`
- `program`
- `employment`
- `cohort`

## Re-generate

Re-create both CSVs deterministically by running:

- `python Chapter06/Labs/generate_at_risk_dataset.py`

This uses a fixed seed so you get the same output each run.
