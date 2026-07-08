from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
    task = Task(description="Morning walk", duration_minutes=20)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Feeding", duration_minutes=10))

    assert len(pet.tasks) == initial_count + 1
