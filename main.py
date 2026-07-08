from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner("Jordan")

    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")

    mochi.add_task(Task(description="Morning walk", duration_minutes=30, priority="high", is_essential=True))
    mochi.add_task(Task(description="Feeding", duration_minutes=10, priority="high"))
    luna.add_task(Task(description="Grooming", duration_minutes=20, priority="medium"))
    luna.add_task(Task(description="Play time", duration_minutes=15, priority="low"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

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


if __name__ == "__main__":
    main()
