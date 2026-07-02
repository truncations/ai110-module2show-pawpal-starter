"""PawPal system class skeletons.

Generated from diagrams/uml_draft.mmd. Method bodies are stubbed out
with `raise NotImplementedError` and are yours to fill in.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta


@dataclass
class Constraints:
    frequency: int
    cooldown: float
    duration: float
    prerequisites: list[str] = field(default_factory=list)
    start_time: time | None = None
    priority_level: int = 0

    # checks if the current time right now is in range of our task's required time.
    def is_satisfiable(self) -> bool:
        current_time = datetime.now()

        for count in range(self.frequency):
            temp_date = datetime(year=2000, month=1, day=1)
            time_in_datetime = datetime.combine(date=temp_date, time=time) + timedelta(hours=self.cooldown*count)
            end_time = time_in_datetime + timedelta(hours=self.duration)
            if not (current_time.hour >= self.start_time.hour and current_time.hour <= end_time.hour):
                return False

        return True
    
    # get the max number of times a person can do the given task based on the cooldown, duration, and start time of task.
    def get_max_frequency(self) -> int:
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

        max_freq = (available_hours + self.cooldown) / (self.duration + self.cooldown)
        return max(0, int(max_freq))

    # is the frequency number inputted (for user input) allowed?
    def frequency_is_allowed(self, new_freq: int) -> bool:
        return new_freq > 0 and new_freq <= self.get_max_frequency()



@dataclass
class Task:
    name: str
    description: str
    constraints: Constraints
    status: str = "Incomplete" # inputs either: Complete, In Progress, Incomplete

    def mark_complete(self):
        self.status = "Complete"

@dataclass
class Pet:
    species: str
    color: str
    birthdate: datetime
    height: float
    weight: float
    tasks: list[Task] = field(default_factory=list)
    allergies: list[str] = field(default_factory=list)

    def get_age(self) -> int:
        current_datetime = datetime.now()
        age_of_pet_data = current_datetime - self.birthdate
        return age_of_pet_data // 365
    
    def create_task(self, name: str, description: str, constraints: Constraints) -> "Task":
        task = Task(name=name, description=description, constraints=constraints)
        self.tasks.append(task)
        return task

@dataclass
class Owner:
    name: str
    age: int
    work_starttime: time
    work_endtime: time
    pets: dict[str, Pet] = field(default_factory=dict)

    def get_all_tasks(self) -> dict[str, list[Task]]:
        return {pet_name : pet.tasks for pet_name, pet in self.pets.items()}

    def create_plan(self) -> "Scheduler":
        """Build one plan for this owner, aggregating tasks across all pets."""
        return Scheduler(owner=self)

    # can the pet be created with the user's parameters even with barely any information?
    def can_create_pet(self, pet_name: str, species: str, color: str, year: int, month: int, day: int, height: float, weight: float):
        if month == 12:
            next_month = datetime(year=year + 1, month=1, day=1)
        elif month >= 1 and month < 12:
            next_month = datetime(year=year, month=month + 1, day=1)
        else:
            return False
        return pet_name != "" and (day >= 1 and day <= (next_month - datetime(year=year, month=month, day=1)).days)

    def create_pet(self, pet_name: str, species: str, color: str, year: int, month: int, day: int, height: float, weight: float) -> "Pet":
        # creates birthdate here because a user can't input a birthdate object.
        birthdate = datetime(year=year, month=month, day=day)
        new_pet = Pet(species=species, color=color, birthdate=birthdate, height=height, weight=weight)
        self.pets[pet_name] = new_pet
        return new_pet


@dataclass
class Scheduler:
    owner: Owner

    # organized by start time.
    def get_organized_tasks(self, task_list) -> list:
        tasks = task_list
        tasks.sort(key=lambda task: (task.constraints.start_time is None, task.constraints.start_time))
        return tasks

    def get_plan_str(self) -> str:
        tasks = self.owner.get_all_tasks()
        str_to_return = "No tasks scheduled."

        if len(tasks) <= 0:
            return str_to_return

        str_to_return = "Scheduled tasks for following pets:\n===============\n"
        for pet_name in tasks.keys():
            str_to_return += f"{pet_name}"
            organized_task_list_for_pet = self.get_organized_tasks(tasks[pet_name])
            # should be Task object for all tasks.
            for task in organized_task_list_for_pet:
                str_to_return += f"\t{task.constraints.start_time.strftime("%I:%M %p") if task.constraints.start_time else "<Unscheduled>"} | {task.status} | {task.name}"
                if len(task.constraints.prerequisites) > 0:
                    str_to_return += f"\n\t\t* Prerequisites: {", ".join(task.constraints.prerequisites)}"
    
        return str_to_return

