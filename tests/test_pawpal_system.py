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
