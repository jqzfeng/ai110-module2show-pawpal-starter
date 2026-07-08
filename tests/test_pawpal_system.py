from datetime import datetime, timedelta

from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_can_be_marked_complete():
    task = Task(description="Morning walk", duration_minutes=20, frequency="daily")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_pet_tracks_and_filters_tasks():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task("Morning walk", 20, "daily", priority="high"))
    pet.add_task(Task("Feeding", 10, "daily", priority="medium"))

    pending = pet.get_pending_tasks()

    assert len(pending) == 2
    assert pending[0].description == "Morning walk"


def test_owner_collects_tasks_from_all_pets():
    owner = Owner("Jordan")
    pet_one = Pet("Mochi", "dog")
    pet_two = Pet("Luna", "cat")

    pet_one.add_task(Task("Walk", 20, "daily", priority="high"))
    pet_two.add_task(Task("Brush", 15, "weekly", priority="low"))

    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    all_tasks = owner.get_all_tasks()

    assert len(all_tasks) == 2
    assert {task.description for task in all_tasks} == {"Walk", "Brush"}


def test_scheduler_organizes_pending_tasks_across_pets():
    owner = Owner("Jordan")
    pet_one = Pet("Mochi", "dog")
    pet_two = Pet("Luna", "cat")

    pet_one.add_task(Task("Walk", 20, "daily", priority="high"))
    pet_one.add_task(Task("Feed", 10, "daily", priority="medium"))
    pet_two.add_task(Task("Brush", 15, "weekly", priority="low"))

    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    scheduler = Scheduler(owner)
    organized = scheduler.organize_tasks()

    assert [task.description for task in organized] == ["Walk", "Feed", "Brush"]


def test_scheduler_can_sort_tasks_by_time_of_day():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Morning walk", 20, "daily", priority="high", time_of_day="10:30"))
    pet.add_task(Task("Feeding", 10, "daily", priority="medium", time_of_day="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner, pet=pet)
    sorted_tasks = scheduler.sort_by_time(pet.tasks)

    assert [task.description for task in sorted_tasks] == ["Feeding", "Morning walk"]


def test_scheduler_can_filter_tasks_by_completion_and_pet_name():
    owner = Owner("Jordan")
    pet_one = Pet("Mochi", "dog")
    pet_two = Pet("Luna", "cat")

    task_one = Task("Walk", 20, "daily", priority="high", time_of_day="09:00")
    task_two = Task("Brush", 15, "weekly", priority="low", time_of_day="11:00")
    task_two.mark_complete()

    pet_one.add_task(task_one)
    pet_two.add_task(task_two)

    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    scheduler = Scheduler(owner)
    pending_tasks = scheduler.filter_tasks(owner.get_all_tasks(), completed=False)
    pet_tasks = scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Mochi")

    assert [task.description for task in pending_tasks] == ["Walk"]
    assert [task.description for task in pet_tasks] == ["Walk"]


def test_mark_complete_creates_next_occurrence_for_daily_task():
    task = Task("Feed", 10, "daily", priority="high", time_of_day="08:00")

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.frequency == "daily"
    assert next_task.description == "Feed"
    assert next_task.due_date is not None
    assert next_task.due_date >= datetime.now() + timedelta(hours=23)
    assert next_task.due_date <= datetime.now() + timedelta(days=1, minutes=5)


def test_pet_tracks_next_occurrence_when_recurring_task_is_completed():
    pet = Pet("Mochi", "dog")
    task = Task("Feed", 10, "daily", priority="high", time_of_day="08:00")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task in pet.tasks
    assert len(pet.get_pending_tasks()) == 1


def test_scheduler_reports_conflict_warning_for_overlapping_tasks():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Feed", 10, "daily", priority="high", time_of_day="08:00"))
    pet.add_task(Task("Walk", 20, "daily", priority="high", time_of_day="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner, pet=pet)
    warning = scheduler.detect_conflicts(pet.tasks)

    assert warning is not None
    assert "conflict" in warning.lower()


def test_sort_by_time_returns_tasks_in_chronological_order():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Lunch walk", 20, "daily", priority="high", time_of_day="11:30"))
    pet.add_task(Task("Morning feeding", 10, "daily", priority="medium", time_of_day="08:00"))
    pet.add_task(Task("Afternoon check", 15, "daily", priority="low", time_of_day="09:15"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner, pet=pet)
    sorted_tasks = scheduler.sort_by_time(pet.tasks)

    assert [task.description for task in sorted_tasks] == [
        "Morning feeding",
        "Afternoon check",
        "Lunch walk",
    ]


def test_mark_complete_creates_a_new_task_for_the_following_day():
    task = Task(
        description="Feed",
        duration_minutes=10,
        frequency="daily",
        priority="high",
        time_of_day="08:00",
        due_date=datetime(2026, 1, 1, 8, 0),
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == datetime(2026, 1, 2, 8, 0)


def test_scheduler_flags_duplicate_times_as_conflicts():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Feed", 10, "daily", priority="high", time_of_day="08:00"))
    pet.add_task(Task("Walk", 20, "daily", priority="high", time_of_day="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner, pet=pet)
    warning = scheduler.detect_conflicts(pet.tasks)

    assert warning is not None
    assert "Feed" in warning or "Walk" in warning
