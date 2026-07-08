from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner("Jordan")

    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")

    mochi.add_task(Task(description="Morning walk", duration_minutes=30, priority="high", is_essential=True, time_of_day="10:30"))
    mochi.add_task(Task(description="Feeding", duration_minutes=10, priority="high", time_of_day="08:00"))
    mochi.add_task(Task(description="Grooming", duration_minutes=20, priority="medium", time_of_day="09:15"))
    mochi.add_task(Task(description="Brush", duration_minutes=15, priority="medium", time_of_day="09:15"))
    luna.add_task(Task(description="Play time", duration_minutes=15, priority="low", time_of_day="17:00"))
    luna.add_task(Task(description="Brush", duration_minutes=10, priority="medium", time_of_day="11:00"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    completed_task = mochi.tasks[0]
    next_occurrence = mochi.complete_task(completed_task)

    scheduler = Scheduler(owner, pet=mochi)
    plan = scheduler.generate_daily_plan()

    print("Today's Schedule")
    print("=" * 20)
    for item in plan.scheduled_items:
        print(f"- {item.start_time.strftime('%H:%M')} - {item.end_time.strftime('%H:%M')} : {item.task.description} ({item.task.duration_minutes} min)")

    if plan.skipped_tasks:
        print("\nSkipped tasks:")
        for task in plan.skipped_tasks:
            print(f"- {task.description}")

    print("\nSorted tasks by time:")
    for task in scheduler.sort_by_time(mochi.get_pending_tasks()):
        print(f"- {task.time_of_day} : {task.description}")

    print("\nPending tasks for Mochi:")
    for task in scheduler.filter_tasks(owner.get_all_tasks(), completed=False, pet_name="Mochi"):
        print(f"- {task.description}")

    conflict_warning = scheduler.detect_conflicts(mochi.tasks)
    if conflict_warning:
        print(f"\n{conflict_warning}")

    if next_occurrence is not None:
        print(f"\nNext recurring task created: {next_occurrence.description} due {next_occurrence.due_date}")


if __name__ == "__main__":
    main()
