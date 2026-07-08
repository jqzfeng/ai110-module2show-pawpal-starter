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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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
