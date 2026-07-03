# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

## objs: tasks, pet, daily plan
## three core actions: add a pet, schedule tasks, view daily plan

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

Today's Schedule for following Pets:
NOTE: [&] notation means the task scheduled is during your work hours.
===============
jack
        [&] 07:00 AM | Incomplete | Walk
        [&] 12:30 PM | Incomplete | Feed
        [*] 06:00 PM | Incomplete | Grooming
box
        [&] 08:00 AM | Incomplete | Feed
        [&] 02:15 PM | Incomplete | Walk
        [*] 08:45 PM | Incomplete | Vet Checkup
===============

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov

# Run with Python in Windows:
python -m pytest
```

These tests cover the core functionality of the pet application system. They ensure that the scheduler itself is mainly functional and that creating tasks doesn't cause any issues. They test for mainly whether the scheduler can detect recurrences, detect conflict in task scheduling, and ensure that sorting and filtering the scheduled items is valid.

Sample test output:

```
# Paste your pytest output here
=============================================================================================== test session starts ===============================================================================================
platform win32 -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0
rootdir: A:\programming\Python\CodePath - AI 110\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 8 items                                                                                                                                                                                                  

tests\test_pawpal.py ........                                                                                                                                                                                [100%]

================================================================================================ 8 passed in 0.04s ================================================================================================
```

Based on these tests, I feel that my confidence level is at a 4 star for this system's reliability.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | sort_tasks_by_time() | e.g., by priority, duration |
| Filtering | filter_tasks(), (Pet objects contain tasks so filtering by pet automatically incorporated) | e.g., skip tasks if time runs out |
| Conflict handling | check_task_for_conflicts(), has_scheduling_conflicts(), find_scheduling_conflicts() | e.g., overlapping time slots |
| Recurring tasks | mark_task_complete() | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
