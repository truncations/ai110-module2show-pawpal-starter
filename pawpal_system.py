"""PawPal system class skeletons.

Generated from diagrams/uml_draft.mmd. Method bodies are stubbed out
with `raise NotImplementedError` and are yours to fill in.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, time, timedelta

@dataclass
class Constraints:
    frequency: int
    cooldown: int
    duration: int
    prerequisites: list[str] = field(default_factory=list)
    start_time: time | None = None
    priority_level: int = 0
    
    def get_max_frequency(self) -> int:
        """Get the max number of times a person can do the given task based on the cooldown, duration, and start time of task."""
        if self.duration <= 0:
            return 0

        available_hours = 24.0
        if self.start_time is not None:
            available_hours -= (
                self.start_time.hour
                + self.start_time.minute / 60
                + self.start_time.second / 3600
            )

        if available_hours <= 0:
            return 0

        if (self.duration/60 + self.cooldown/60) > 0:
            max_freq = (available_hours + self.cooldown/60) / (self.duration/60 + self.cooldown/60)
        else:
            max_freq = 0
        return max(0, int(max_freq))

    def frequency_is_allowed(self, new_freq: int) -> bool:
        """Is the frequency number inputted (for user input) allowed?"""
        return new_freq > 0 and new_freq <= self.get_max_frequency()

@dataclass
class Task:
    name: str
    description: str
    constraints: Constraints
    status: str = "Incomplete"
    due_date: datetime | None = None
    recurrence: str | None = None # Daily, Weekly, None
    
    def mark_complete(self):
        """Marks this task's status as complete."""
        self.status = "Complete"

    def mark_in_progress(self):
        """Marks this task's status as in progress."""
        self.status = "In Progress"

    def mark_incomplete(self):
        """Marks this task's status as incomplete."""
        self.status = "Incomplete"

@dataclass
class Pet:
    name: str
    species: str
    color: str
    birthdate: datetime
    height: float
    weight: float
    tasks: list[Task] = field(default_factory=list)
    allergies: list[str] = field(default_factory=list)

    def get_age(self) -> int:
        """Calculates the pet's age in years from its birthdate."""
        current_datetime = datetime.now()
        age_of_pet_data = current_datetime - self.birthdate
        return age_of_pet_data.days // 365
    
    def create_task(self, name: str, description: str, constraints: Constraints) -> "Task":
        """Creates a new task for this pet and adds it to its task list."""
        task = Task(name=name, description=description, constraints=constraints)
        self.tasks.append(task)
        return task
    
    def mark_task_complete(self, task: Task) -> None:
        """Marks the given task complete and, if it recurs, schedules its next occurrence."""
        task.mark_complete()

        if task.recurrence == "Daily":
            interval = timedelta(days=1)
        elif task.recurrence == "Weekly":
            interval = timedelta(days=7)
        else:
            return

        base_date = task.due_date if task.due_date is not None else datetime.now()
        next_task = Task(
            name=task.name,
            description=task.description,
            constraints=replace(task.constraints),
            due_date=base_date + interval,
            recurrence=task.recurrence,
        )
        self.tasks.append(next_task)
    

@dataclass
class Owner:
    name: str
    work_starttime_hr: int
    work_endtime_hr: int
    pets: dict[str, Pet] = field(default_factory=dict)

    def get_all_tasks(self) -> dict[str, list[Task]]:
        """Returns a mapping of pet name to that pet's list of tasks."""
        return {pet_name : pet.tasks for pet_name, pet in self.pets.items()}

    def create_plan(self) -> "Scheduler":
        """Build one plan for this owner, aggregating tasks across all pets."""
        return Scheduler(owner=self)

    def can_create_pet(self, pet_name: str, species: str, color: str, year: int, month: int, day: int, height: float, weight: float):
        """Can the pet be created with the user's parameters even with barely any information?"""
        if month == 12:
            next_month = datetime(year=year + 1, month=1, day=1)
        elif month >= 1 and month < 12:
            next_month = datetime(year=year, month=month + 1, day=1)
        else:
            return False
        return pet_name != "" and (day >= 1 and day <= (next_month - datetime(year=year, month=month, day=1)).days)

    def create_pet(self, pet_name: str, species: str, color: str, year: int, month: int, day: int, height: float, weight: float) -> "Pet":
        """Creates a new pet from the given parameters and adds it to this owner."""
        # creates birthdate here because a user can't input a birthdate object.
        birthdate = datetime(year=year, month=month, day=day)
        new_pet = Pet(name=pet_name, species=species, color=color, birthdate=birthdate, height=height, weight=weight)
        self.add_pet(new_pet)
        return new_pet
    
    def add_pet(self, pet: Pet) -> None:
        """Adds the given pet to this owner's collection of pets."""
        self.pets[pet.name] = pet


@dataclass
class Scheduler:
    owner: Owner

    def sort_tasks_by_time(self, task_list) -> list:
        """Organized by start time."""
        tasks = task_list[:]
        tasks.sort(key=lambda task: (task.constraints.start_time is None, task.constraints.start_time))
        return tasks
    
    def is_task_in_work_hours(self, task: Task) -> bool:
        """Checks whether the task's start time falls within the owner's work hours."""
        if task.constraints.start_time is None:
            return False
        work_start = time(hour=self.owner.work_starttime_hr)
        work_end = time(hour=self.owner.work_endtime_hr)
        return work_start <= task.constraints.start_time <= work_end

    def filter_tasks(self, status: str | None = None) -> list[Task]:
        """Filters tasks across all of the owner's pets by completion status."""
        all_tasks = self.owner.get_all_tasks()

        filtered = []
        for tasks in all_tasks.values():
            for task in tasks:
                if status is not None and task.status != status:
                    continue
                filtered.append(task)
        return filtered

    def get_tasks_by_pet_name(self, pet_name: str) -> list[Task]:
        """Returns the list of tasks belonging to the pet with the given name."""
        all_tasks = self.owner.get_all_tasks()
        return all_tasks.get(pet_name, [])

    def _group_scheduled_tasks(self, include_completed: bool = False) -> dict[tuple, list[Task]]:
        """Groups tasks, across all pets, by (due date, start time), skipping unscheduled tasks."""
        groups: dict[tuple, list[Task]] = {}
        for task in self.filter_tasks():
            if task.constraints.start_time is None:
                continue
            if not include_completed and task.status == "Complete":
                continue
            key = (task.due_date.date() if task.due_date is not None else None, task.constraints.start_time)
            groups.setdefault(key, []).append(task)
        return groups

    def find_scheduling_conflicts(self, include_completed: bool = False) -> list[list[Task]]:
        """Finds groups of tasks, across all pets, that share the same due date and start time."""
        groups = self._group_scheduled_tasks(include_completed=include_completed)
        return [group for group in groups.values() if len(group) > 1]

    def has_scheduling_conflicts(self, include_completed: bool = False) -> bool:
        """Whether any two tasks, across all pets, are scheduled at the same time."""
        return len(self.find_scheduling_conflicts(include_completed=include_completed)) > 0

    def check_task_for_conflicts(self, task: Task, include_completed: bool = False) -> str | None:
        """Lightweight check for whether a task about to be scheduled collides with an existing one.

        Never raises: returns a warning message describing the conflict(s), or None if there
        aren't any (including if the check itself couldn't be completed for some reason).
        """
        try:
            if task.constraints.start_time is None:
                return None

            key = (task.due_date.date() if task.due_date is not None else None, task.constraints.start_time)
            groups = self._group_scheduled_tasks(include_completed=include_completed)
            conflicting = [existing for existing in groups.get(key, []) if existing is not task]

            if not conflicting:
                return None

            time_str = task.constraints.start_time.strftime("%I:%M %p")
            names = ", ".join(existing.name for existing in conflicting)
            return f"Warning: '{task.name}' at {time_str} conflicts with existing task(s): {names}"
        except Exception:
            return f"Warning: could not verify scheduling conflicts for '{getattr(task, 'name', 'this task')}'."

    def get_plan_str(self) -> str:
        """Builds a formatted string of the owner's full schedule across all pets."""
        tasks = self.owner.get_all_tasks()
        str_to_return = "No tasks scheduled."

        if len(tasks) <= 0:
            return str_to_return

        str_to_return = "\nToday's Schedule for following Pets:\nNOTE: [&] notation means the task scheduled is during your work hours.\n===============\n"
        for pet_name in tasks.keys():
            str_to_return += f"{pet_name}\n"
            organized_task_list_for_pet = self.sort_tasks_by_time(tasks[pet_name])
            # should be Task object for all tasks.
            for task in organized_task_list_for_pet:
                if self.is_task_in_work_hours(task):
                    str_to_return += "\t[&] "
                else:
                    str_to_return += "\t[*] "
                str_to_return += f"{task.constraints.start_time.strftime("%I:%M %p") if task.constraints.start_time else "<Unscheduled>"} | {task.status} | {task.name}"
                if len(task.constraints.prerequisites) > 0:
                    str_to_return += f"\n\t\t* Prerequisites: {", ".join(task.constraints.prerequisites)}"
                str_to_return += "\n"
        str_to_return += "===============\n"
        return str_to_return

