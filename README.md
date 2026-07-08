# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

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

Verified by running the demo script in the terminal:

```text
Today's Schedule
====================
- 08:00 - 08:30 : Morning walk (30 min)
- 08:30 - 08:40 : Feeding (10 min)
- 08:40 - 09:00 : Grooming (20 min)
- 09:00 - 09:15 : Play time (15 min)
```

## 🧪 Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

These tests check the core scheduling behavior of PawPal+, including:

- task sorting and ordering
- recurring task behavior for daily and weekly care items
- conflict detection for overlapping task times
- basic pet and owner task management

Example test run:

```text
============================= test session starts ==============================
platform darwin -- Python 3.13.0, pytest-7.4.1, pluggy-1.0
rootdir: /Users/qiuzifeng/Desktop/CodePath 2026/ai110-module2show-pawpal-starter
collected 12 items

tests/test_pawpal.py::test_mark_complete_changes_task_status PASSED
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED
tests/test_pawpal_system.py::test_task_can_be_marked_complete PASSED
tests/test_pawpal_system.py::test_pet_tracks_and_filters_tasks PASSED
tests/test_pawpal_system.py::test_owner_collects_tasks_from_all_pets PASSED
tests/test_pawpal_system.py::test_scheduler_organizes_pending_tasks_across_pets PASSED
tests/test_pawpal_system.py::test_scheduler_can_sort_tasks_by_time_of_day PASSED
tests/test_pawpal_system.py::test_scheduler_can_filter_tasks_by_completion_and_pet_name PASSED
tests/test_pawpal_system.py::test_mark_complete_creates_next_occurrence_for_daily_task PASSED
tests/test_pawpal_system.py::test_pet_tracks_next_occurrence_when_recurring_task_is_completed PASSED
tests/test_pawpal_system.py::test_scheduler_reports_conflict_warning_for_overlapping_tasks PASSED
tests/test_pawpal_system.py::test_sort_by_time_returns_tasks_in_chronological_order PASSED
tests/test_pawpal_system.py::test_mark_complete_creates_a_new_task_for_the_following_day PASSED
tests/test_pawpal_system.py::test_scheduler_flags_duplicate_times_as_conflicts PASSED

============================== 12 passed in 0.02s ==============================
```

Confidence Level: ★★★★★

The scheduler logic is currently well covered for its core behaviors, and the passing test run gives strong confidence in the reliability of the planning and recurrence features.

## 📐 Smarter Scheduling

The scheduler now includes a few lightweight but useful planning features that make the demo feel more realistic.

| Feature | Method | What it does |
|---------|--------|--------------|
| Sorting behavior | `Scheduler.sort_by_time()` | Orders tasks by their planned time of day so the output is easier to read and follow. |
| Filtering behavior | `Scheduler.filter_tasks()` | Filters tasks by completion status and by pet name, which helps the app focus on pending or pet-specific care items. |
| Conflict detection | `Scheduler.detect_conflicts()` | Checks for overlapping task times and returns a warning message instead of crashing the program. |
| Recurring tasks | `Task.mark_complete()` and `Pet.complete_task()` | When a daily or weekly task is completed, a new task for the next occurrence is created automatically. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
