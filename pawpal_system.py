from dataclasses import dataclass
from datetime import datetime, time
from typing import List, Optional


@dataclass
class TimeWindow:
    """Represents a contiguous block of available time."""
    start_time: time
    end_time: time

    def get_duration(self) -> int:
        """
        Returns duration of this time window in minutes.
        """
        pass


@dataclass
class Pet:
    """Represents a pet that needs care."""
    name: str
    species: str
    age: int
    special_needs: str = ""

    def get_care_requirements(self) -> List['Task']:
        """
        Returns list of essential care tasks for this pet.
        """
        pass


@dataclass
class Task:
    """Represents a single pet care task."""
    title: str
    duration_minutes: int
    priority: str  # "high", "medium", "low"
    is_essential: bool = False

    def get_priority_score(self) -> int:
        """
        Returns numeric score for sorting (higher = more important).
        """
        pass

    def can_skip(self) -> bool:
        """
        Returns True if this task can be skipped if time runs out.
        """
        pass


class Owner:
    """Represents the pet owner with availability constraints."""

    def __init__(self, name: str, time_availability: List[TimeWindow], preferences: str = ""):
        """
        Initialize owner with name, available time windows, and preferences.

        Args:
            name: Owner's name
            time_availability: List of TimeWindow objects representing available slots
            preferences: Optional preferences (e.g., "morning person", "evening preferred")
        """
        self.name = name
        self.time_availability = time_availability
        self.preferences = preferences

    def get_available_windows(self) -> List[TimeWindow]:
        """
        Returns list of available time windows for the day.
        """
        pass

    def has_time_for_task(self, duration: int) -> bool:
        """
        Checks if any available window can fit a task of given duration.

        Args:
            duration: Task duration in minutes

        Returns:
            True if task can fit in any available window
        """
        pass


class ScheduledTask:
    """Binds a Task to a specific time slot."""

    def __init__(self, task: Task, start_time: time, end_time: time):
        """
        Initialize a scheduled task with task and time bounds.

        Args:
            task: The Task object to schedule
            start_time: Start time (e.g., 8:00 AM)
            end_time: End time (e.g., 8:30 AM)
        """
        self.task = task
        self.start_time = start_time
        self.end_time = end_time

    def overlaps_with(self, other: 'ScheduledTask') -> bool:
        """
        Checks if this scheduled task overlaps with another (for conflict detection).

        Args:
            other: Another ScheduledTask to check against

        Returns:
            True if time windows overlap
        """
        pass

    def fits_in_window(self, window: TimeWindow) -> bool:
        """
        Checks if this scheduled task fits entirely within a TimeWindow.

        Args:
            window: A TimeWindow to check against

        Returns:
            True if task fits within window bounds
        """
        pass


class DailyPlan:
    """Represents a complete daily schedule for a pet."""

    def __init__(self, date: datetime, owner: Owner, pet: Pet):
        """
        Initialize a daily plan for a specific date.

        Args:
            date: Date for this plan
            owner: Owner object (for reference)
            pet: Pet object (for reference)
        """
        self.date = date
        self.owner = owner
        self.pet = pet
        self.scheduled_items: List[ScheduledTask] = []
        self.skipped_tasks: List[Task] = []
        self.total_time_used = 0

    def add_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
        """
        Adds a ScheduledTask to the plan (if no conflicts).

        Args:
            scheduled_task: ScheduledTask to add
        """
        pass

    def is_feasible(self) -> bool:
        """
        Checks if the plan is valid (no conflicts, within time constraints).

        Returns:
            True if plan is feasible
        """
        pass

    def get_explanation(self) -> str:
        """
        Returns a human-readable explanation of why each task was chosen/skipped.

        Returns:
            Formatted explanation string
        """
        pass


class Scheduler:
    """The core scheduling engine that generates daily plans."""

    def __init__(self, owner: Owner, pet: Pet, available_tasks: List[Task]):
        """
        Initialize scheduler with owner, pet, and pool of tasks.

        Args:
            owner: Owner object
            pet: Pet object
            available_tasks: List of all possible tasks to consider
        """
        self.owner = owner
        self.pet = pet
        self.available_tasks = available_tasks

    def generate_daily_plan(self) -> DailyPlan:
        """
        Main scheduling algorithm: generates a daily plan based on constraints and priorities.

        Algorithm:
        1. Sort tasks by: is_essential DESC, priority DESC, duration ASC
        2. Initialize empty DailyPlan
        3. For each task:
           a. Find next available time slot that fits
           b. If found → add ScheduledTask to plan
           c. If NOT found → add to skipped_tasks
        4. Generate explanation
        5. Return plan

        Returns:
            A DailyPlan object with scheduled and skipped tasks
        """
        pass

    def rank_tasks_by_priority(self) -> List[Task]:
        """
        Sorts available tasks by priority (essential first, then by priority level).

        Returns:
            Sorted list of tasks
        """
        pass

    def find_time_slot_for_task(self, task: Task) -> Optional[TimeWindow]:
        """
        Finds the next available time slot that can fit a task.

        Args:
            task: Task to find a slot for

        Returns:
            A TimeWindow that fits the task, or None if no slot available
        """
        pass
