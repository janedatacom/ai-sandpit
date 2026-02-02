"""Generate a synthetic university/adult-ed text classification dataset.

Outputs:
- Chapter06/Labs/assets/at_risk_student_profiles.csv
- Chapter06/Labs/assets/at_risk_student_messages_500.csv

The join key is `student_id`.

This script is deterministic by default (seeded) so labs are repeatable.
"""

from __future__ import annotations

import csv
import random
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


ASSETS_DIR = Path(__file__).resolve().parent / "assets"


@dataclass(frozen=True)
class StudentProfile:
    student_id: str
    age_band: str
    study_mode: str
    program: str
    employment: str
    cohort: str


def _weighted_choice(rng: random.Random, items: list[str], weights: list[float]) -> str:
    return rng.choices(items, weights=weights, k=1)[0]


def _make_student_id(index: int) -> str:
    return f"S{index:06d}"


def generate_student_profiles(rng: random.Random, *, count: int) -> list[StudentProfile]:
    age_bands = ["18-24", "25-34", "35-44", "45-54", "55+"]
    age_weights = [0.35, 0.35, 0.18, 0.09, 0.03]

    study_modes = ["online", "on-campus", "blended"]
    study_mode_weights = [0.55, 0.20, 0.25]

    programs = [
        "Graduate Certificate (Data)",
        "Adult Education (Short Course)",
        "Bachelor (Business)",
        "Bachelor (IT)",
        "Diploma (Community Services)",
        "Micro-credential (Cybersecurity)",
    ]
    program_weights = [0.18, 0.20, 0.18, 0.18, 0.13, 0.13]

    employment = ["full-time", "part-time", "casual", "unemployed", "career-break"]
    employment_weights = [0.35, 0.25, 0.20, 0.12, 0.08]

    cohorts = ["2025-T1", "2025-T2", "2025-T3", "2026-T1"]
    cohort_weights = [0.25, 0.25, 0.20, 0.30]

    profiles: list[StudentProfile] = []
    for i in range(1, count + 1):
        profiles.append(
            StudentProfile(
                student_id=_make_student_id(i),
                age_band=_weighted_choice(rng, age_bands, age_weights),
                study_mode=_weighted_choice(rng, study_modes, study_mode_weights),
                program=_weighted_choice(rng, programs, program_weights),
                employment=_weighted_choice(rng, employment, employment_weights),
                cohort=_weighted_choice(rng, cohorts, cohort_weights),
            )
        )

    return profiles


def _pick_unit_code(rng: random.Random) -> str:
    prefixes = ["EDU", "BUS", "IT", "DAT", "CYS", "COM"]
    return f"{rng.choice(prefixes)}{rng.randint(100, 699)}"


def _pick_assessment(rng: random.Random) -> str:
    return rng.choice(
        [
            "quiz 1",
            "quiz 2",
            "assignment 1",
            "assignment 2",
            "group project",
            "final assessment",
            "weekly reflection",
            "capstone submission",
        ]
    )


def _at_risk_templates() -> list[str]:
    return [
        "I’m really behind in week {week} and I don’t think I can catch up. Can someone help me make a plan?",
        "I’ve missed two deadlines and I’m worried I’m going to fail. What are my options from here?",
        "I’m considering withdrawing because I can’t keep up with work and study at the moment.",
        "I failed {assessment} and I don’t understand what I’m doing wrong. I need guidance. Any chance to talk to someone?",
        "I haven’t been able to access the LMS for days and I’ve fallen behind. I’m getting stressed about it.",
        "I’m overwhelmed by the workload and I’m not sure I should continue this unit.",
        "I submitted {assessment} late again. I’m worried about penalties and failing the unit.",
        "I keep getting low marks and I don’t know how to improve. I’m thinking of deferring.",
        "I’m struggling to understand the lectures and I’m too far behind to participate in tutorials.",
        "I’ve missed several weeks due to personal commitments and I’m not sure I can recover this term.",
    ]


def _not_at_risk_templates() -> list[str]:
    return [
        "Can you confirm the due date for {assessment} in week {week}?",
        "Where do we submit {assessment}? I can’t find the link.",
        "Is there a recording for this week’s lecture?",
        "Can someone explain question 3 on the practice quiz?",
        "I’m getting an error when uploading my file—any tips?",
        "Do we need APA 7th for {assessment}?",
        "What’s the format for the weekly reflection?",
        "I missed the live session but I’m up to date—where can I find the slides?",
        "I failed to attach my file last time; can I resubmit the correct document?",
        "How do I join a group for the group project?",
        "Is there an extension process for {assessment}?",
        "I’m enjoying the unit so far—thanks for the clear explanations.",
    ]


def _render_message(rng: random.Random, *, label: int, week: int) -> str:
    assessment = _pick_assessment(rng)
    template = rng.choice(_at_risk_templates() if label == 1 else _not_at_risk_templates())
    return template.format(week=week, assessment=assessment)


def generate_messages(
    rng: random.Random,
    *,
    profiles: list[StudentProfile],
    count: int,
    at_risk_rate: float,
) -> list[dict[str, str]]:
    channels = ["lms_forum", "email", "chat", "support_ticket"]
    channel_weights = [0.45, 0.25, 0.15, 0.15]

    start = datetime(2026, 2, 1, 9, 0, tzinfo=timezone.utc)

    rows: list[dict[str, str]] = []
    for i in range(count):
        student = rng.choice(profiles)
        label = 1 if rng.random() < at_risk_rate else 0
        week = rng.randint(1, 12)

        created_at = start + timedelta(hours=i * 3) + timedelta(minutes=rng.randint(0, 55))
        unit_code = _pick_unit_code(rng)
        channel = _weighted_choice(rng, channels, channel_weights)
        text = _render_message(rng, label=label, week=week)

        rows.append(
            {
                "message_id": str(uuid.uuid4()),
                "student_id": student.student_id,
                "created_at": created_at.isoformat(),
                "channel": channel,
                "program": student.program,
                "unit_code": unit_code,
                "week": str(week),
                "text": text,
                "label": str(label),
            }
        )

    return rows


def write_student_profiles_csv(path: Path, profiles: list[StudentProfile]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["student_id", "age_band", "study_mode", "program", "employment", "cohort"],
        )
        writer.writeheader()
        for p in profiles:
            writer.writerow(
                {
                    "student_id": p.student_id,
                    "age_band": p.age_band,
                    "study_mode": p.study_mode,
                    "program": p.program,
                    "employment": p.employment,
                    "cohort": p.cohort,
                }
            )


def write_messages_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "message_id",
                "student_id",
                "created_at",
                "channel",
                "program",
                "unit_code",
                "week",
                "text",
                "label",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    seed = 20260202
    rng = random.Random(seed)

    profiles = generate_student_profiles(rng, count=200)
    messages = generate_messages(rng, profiles=profiles, count=500, at_risk_rate=0.30)

    write_student_profiles_csv(ASSETS_DIR / "at_risk_student_profiles.csv", profiles)
    write_messages_csv(ASSETS_DIR / "at_risk_student_messages_500.csv", messages)

    print("Wrote:")
    print(f"- {ASSETS_DIR / 'at_risk_student_profiles.csv'}")
    print(f"- {ASSETS_DIR / 'at_risk_student_messages_500.csv'}")
    print("Join key: student_id")


if __name__ == "__main__":
    main()
