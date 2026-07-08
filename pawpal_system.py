from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import List, Optional


@dataclass
class TimeWindow:
    """Represents a contiguous block of available time."""
    start_time: time
    end_time: time

    def get_duration(self) -> int:
        """Return the duration of this time window in minutes."""
        if self.end_time < self.start_time:
            raise ValueError("end_time must be after start_time")
        return int((datetime.combine(datetime.today(), self.end_time) - datetime.combine(datetime.today(), self.start_time)).total_seconds() // 60)


@dataclass
class Task:
    """Represents a single pet care task."""
    description: str
    duration_minutes: int
    frequency: str = "daily"
    priority: str = "medium"
    completed: bool = False
    is_essential: bool = False
    time_of_day: Optional[str] = None
    due_date: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate task settings when a task is created."""
        if self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be positive")
        self.priority = self.priority.lower()
        if self.time_of_day is not None:
            self.time_of_day = self._normalize_time(self.time_of_day)

    def _normalize_time(self, value: str) -> str:
        """Validate and normalize a time string in HH:MM format."""
        if not isinstance(value, str):
            raise ValueError("time_of_day must be a string")
        parts = value.split(":")
        if len(parts) != 2 or not all(part.isdigit() for part in parts):
            raise ValueError("time_of_day must be in HH:MM format")

        hour, minute = int(parts[0]), int(parts[1])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("time_of_day must be a valid time")
        return f"{hour:02d}:{minute:02d}"

    def get_priority_score(self) -> int:
        """Return a numeric score for sorting tasks by importance."""
        priority_scores = {"low": 1, "medium": 2, "high": 3}
        return priority_scores.get(self.priority, 2) + (5 if self.is_essential else 0)

    def can_skip(self) -> bool:
        """Return True if the task can be skipped when time is limited."""
        return not self.is_essential

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task as completed and create the next occurrence for daily or weekly tasks."""
        self.completed = True
        if self.frequency.lower() not in {"daily", "weekly"}:
            return None

        interval = timedelta(days=1 if self.frequency.lower() == "daily" else 7)
        next_due_date = (self.due_date or datetime.now()) + interval
        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            priority=self.priority,
            is_essential=self.is_essential,
            time_of_day=self.time_of_day,
            due_date=next_due_date,
        )


@dataclass
class Pet:
    """Represents a pet that needs care."""
    name: str
    species: str
    age: int = 0
    special_needs: str = ""
    tasks: List[Task] = field(default_factory=list)

    def get_care_requirements(self) -> List[Task]:
        """Return the essential care tasks for this pet."""
        return [task for task in self.tasks if task.is_essential]

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's list of care tasks."""
        if task.due_date is None:
            task.due_date = datetime.now()
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return the tasks that are still incomplete."""
        return [task for task in self.tasks if not task.completed]

    def add_recurring_task(self, task: Task) -> None:
        """Add a recurring task and initialize its due date."""
        if task.due_date is None:
            task.due_date = datetime.now()
        self.tasks.append(task)

    def complete_task(self, task: Task) -> Optional[Task]:
        """Complete a task for this pet and add its next recurring occurrence to the pet's task list."""
        next_task = task.mark_complete()
        if next_task is not None:
            self.tasks.append(next_task)
        return next_task


class Owner:
    """Represents the pet owner with availability constraints."""

    def __init__(self, name: str, time_availability: Optional[List[TimeWindow]] = None, preferences: str = ""):
        """Initialize an owner with a name, availability, and preferences."""
        self.name = name
        self.time_availability = time_availability or [TimeWindow(time(8, 0), time(18, 0))]
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""
        self.pets.append(pet)

    def get_available_windows(self) -> List[TimeWindow]:
        """Return the owner's available time windows for the day."""
        return self.time_availability

    def has_time_for_task(self, duration: int) -> bool:
        """Return True if any time window can fit a task of the given length."""
        return any(window.get_duration() >= duration for window in self.time_availability)

    def get_all_tasks(self) -> List[Task]:
        """Collect all pending tasks from the owner's pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_pending_tasks())
        return tasks
class ScheduledTask:
    """Binds a Task to a specific time slot."""

    def __init__(self, task: Task, start_time: time, end_time: time):
        """Store a task and its assigned time range."""
        self.task = task
        self.start_time = start_time
        self.end_time = end_time

    def overlaps_with(self, other: 'ScheduledTask') -> bool:
        """Return True if this scheduled task overlaps with another."""
        return not (self.end_time <= other.start_time or other.end_time <= self.start_time)

    def fits_in_window(self, window: TimeWindow) -> bool:
        """Return True if the task fits entirely within the given time window."""
        return window.start_time <= self.start_time and window.end_time >= self.end_time
class DailyPlan:
    """Represents a complete daily schedule for a pet."""

    def __init__(self, date: datetime, owner: Owner, pet: Pet):
        """Create a daily plan for a specific pet and date."""
        self.date = date
        self.owner = owner
        self.pet = pet
        self.scheduled_items: List[ScheduledTask] = []
        self.skipped_tasks: List[Task] = []
        self.total_time_used = 0

    def add_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
        """Add a scheduled task to the plan if it does not conflict."""
        if any(scheduled_task.overlaps_with(existing) for existing in self.scheduled_items):
            raise ValueError("Task overlaps with an existing scheduled task")
        self.scheduled_items.append(scheduled_task)
        self.total_time_used += int((datetime.combine(self.date, scheduled_task.end_time) - datetime.combine(self.date, scheduled_task.start_time)).total_seconds() // 60)

    def is_feasible(self) -> bool:
        """Return True if the plan has no conflicting time slots."""
        return all(not self._has_conflict(item) for item in self.scheduled_items)

    def _has_conflict(self, item: ScheduledTask) -> bool:
        """Return True if a scheduled item conflicts with the plan."""
        return any(item.overlaps_with(other) for other in self.scheduled_items if other is not item)

    def get_explanation(self) -> str:
        """Return a human-readable explanation of the scheduled and skipped tasks."""
        lines = [f"Plan for {self.pet.name} on {self.date.date()}:"]
        for item in self.scheduled_items:
            lines.append(f"- Scheduled {item.task.description} from {item.start_time} to {item.end_time}")
        if self.skipped_tasks:
            lines.append("Skipped:")
            for task in self.skipped_tasks:
                lines.append(f"- {task.description}")
        return "\n".join(lines)
class Scheduler:
    """The core scheduling engine that generates daily plans."""

    def __init__(self, owner: Owner, pet: Optional[Pet] = None):
        """Initialize the scheduler with an owner and optional primary pet."""
        self.owner = owner
        self.pet = pet

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all pending tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def organize_tasks(self) -> List[Task]:
        """Return pending tasks sorted by importance, duration, and time of day."""
        return sorted(
            self.get_all_tasks(),
            key=lambda task: (
                -task.get_priority_score(),
                task.duration_minutes,
                task.time_of_day or "23:59",
            ),
        )

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by their planned time of day, using HH:MM values for sorting."""
        return sorted(tasks, key=lambda task: task.time_of_day or "23:59")

    def filter_tasks(
        self,
        tasks: List[Task],
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Return tasks filtered by completion status and/or the pet they belong to."""
        filtered_tasks: List[Task] = []
        for task in tasks:
            if completed is not None and task.completed != completed:
                continue
            if pet_name is not None:
                matching_pet = next((pet for pet in self.owner.pets if task in pet.tasks), None)
                if matching_pet is None or matching_pet.name.lower() != pet_name.lower():
                    continue
            filtered_tasks.append(task)
        return filtered_tasks

    def generate_daily_plan(self) -> DailyPlan:
        """Create a simple daily plan for the selected pet."""
        if self.pet is None:
            raise ValueError("A pet must be selected before generating a daily plan")

        plan = DailyPlan(datetime.now(), self.owner, self.pet)
        current_time = datetime.combine(plan.date.date(), time(8, 0))

        for task in self.organize_tasks():
            if task.is_essential or self.owner.has_time_for_task(task.duration_minutes):
                start_time = current_time.time()
                end_time = (current_time + timedelta(minutes=task.duration_minutes)).time()
                try:
                    plan.add_scheduled_task(ScheduledTask(task, start_time, end_time))
                    current_time += timedelta(minutes=task.duration_minutes)
                except ValueError:
                    plan.skipped_tasks.append(task)
            else:
                plan.skipped_tasks.append(task)
        return plan

    def rank_tasks_by_priority(self) -> List[Task]:
        """Sort tasks by priority and duration."""
        return self.organize_tasks()

    def find_time_slot_for_task(self, task: Task) -> Optional[TimeWindow]:
        """Find a time window large enough for the task."""
        for window in self.owner.get_available_windows():
            if window.get_duration() >= task.duration_minutes:
                return window
        return None

    def detect_conflicts(self, tasks: List[Task]) -> Optional[str]:
        """Return a warning message when two tasks overlap in time; otherwise return None."""
        seen: List[tuple[str, str]] = []
        for task in tasks:
            if task.time_of_day is None:
                continue
            start = task.time_of_day
            end_hour, end_minute = map(int, start.split(":"))
            end_time = (datetime(2000, 1, 1, end_hour, end_minute) + timedelta(minutes=task.duration_minutes)).strftime("%H:%M")
            for existing_start, existing_end in seen:
                if not (end_time <= existing_start or start >= existing_end):
                    pet_name = next((pet.name for pet in self.owner.pets if task in pet.tasks), "unknown")
                    return f"Warning: conflict detected for {pet_name} between {task.description} and another task at the same time."
            seen.append((start, end_time))
        return None
