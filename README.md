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

Main UI Features:
1. Sidebar for inputting Owner Information
2. Multiple pages, one for inputting your pets, one for inputting tasks for each pet, and one to build a schedule.
3. Pet Information page allows you to input information about a pet to then be added to the database.
4. Tasks page allows you to add tasks to a specific pet, and you can provide requirements for the task.
5. You can build a CLI-readable schedule that should be friendly to read for the user.

Describe your app in numbered steps so a reader can follow along without watching a video:

1. User enters owner information on side bar; name, work start time, and work end time.
2. User scrolls down to Pet Information Section
3. User inputs pet information. For example, a pet named "Dakota", a black dog species, with it being born on March 19th, 2018. It's height is 3.5 feet, and it's 99.3 pounds.
4. User presses Add Pet to add the pet.
5. User navigates to Tasks page by the Tasks tab.
6. User selects the "Dakota" pet to schedule tasks for the pet. No task can have the same start time.
7. User creates a select number of tasks for the "Dakota" Pet.
8. User presses Add task for each task.
9. User can read the list of tasks created for the "Dakota" pet.
10. User can choose to filter the tasks by "All", "Complete', or "Incomplete" status. This shows tasks within the given filters.
11. User can also then choose to sort the tasks for a particular pet by a start time to have a schedule for a pet.
12. User navigates to the Build Schedule tab.
13. User presses Generate Schedule to create a daily schedule for all tasks for each pet.


A fenced code block of sample CLI output from running main.py:
```python
[Task(name='Walk', description='Morning walk around the block', constraints=Constraints(frequency=1, cooldown=0, duration=0.5, prerequisites=[], start_time=datetime.time(7, 0), priority_level=0), status='Complete', due_date=None, recurrence=None), Task(name='Grooming', description='Brush coat and check for ticks', constraints=Constraints(frequency=1, cooldown=0, duration=0.5, prerequisites=[], start_time=datetime.time(18, 0), priority_level=0), status='Complete', due_date=None, recurrence=None), Task(name='Walk', description='Afternoon walk in the park', constraints=Constraints(frequency=1, cooldown=0, duration=0.75, prerequisites=[], start_time=datetime.time(14, 15), priority_level=0), status='Complete', due_date=None, recurrence=None)]
[Task(name='Feed', description='Midday feeding', constraints=Constraints(frequency=1, cooldown=0, duration=0.25, prerequisites=[], start_time=datetime.time(12, 30), priority_level=0), status='Incomplete', due_date=None, recurrence=None), Task(name='Feed', description='Morning feeding', constraints=Constraints(frequency=1, cooldown=0, duration=0.25, prerequisites=[], start_time=datetime.time(8, 0), priority_level=0), status='Incomplete', due_date=None, recurrence=None), Task(name='Vet Checkup', description='Routine wellness checkup', constraints=Constraints(frequency=1, cooldown=0, duration=1.0, prerequisites=[], start_time=datetime.time(20, 45), priority_level=0), status='Incomplete', due_date=None, recurrence=None)]
[[Task(name='Feed', description='Midday feeding', constraints=Constraints(frequency=1, cooldown=0, duration=0.25, prerequisites=[], start_time=datetime.time(9, 0), priority_level=0), status='Incomplete', due_date=datetime.datetime(2026, 7, 3, 0, 0), recurrence=None), Task(name='Feed', description='Morning feeding', constraints=Constraints(frequency=1, cooldown=0, duration=0.25, prerequisites=[], start_time=datetime.time(9, 0), priority_level=0), status='Incomplete', due_date=datetime.datetime(2026, 7, 3, 0, 0), recurrence=None)]]
Invalid: 'Vet Follow-up' at 09:00 AM conflicts with existing task(s): Feed, Feed
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
