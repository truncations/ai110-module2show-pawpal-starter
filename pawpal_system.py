"""PawPal system class skeletons.

Generated from diagrams/uml_draft.mmd. Method bodies are stubbed out
with `raise NotImplementedError` and are yours to fill in.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Constraint:
    frequency: int
    cooldown: float
    duration: float
    prerequisites: list[str] = field(default_factory=list)
    time: datetime | None = None
    priority_level: int = 0

    # getters/setters (dataclass fields are public by default; add explicit
    # property accessors here if you need validation or computed access)


@dataclass
class Task:
    task_name: str
    task_description: str
    constraint: Constraint

    def get_due_date(self, start_date: datetime) -> datetime:
        raise NotImplementedError

    def get_days_left(self) -> float:
        raise NotImplementedError

    # getters/setters


@dataclass
class Pet:
    species: str
    color: str
    birthdate: datetime
    height: float
    weight: float
    tasks: list[Task] = field(default_factory=list)
    allergies: list[str] = field(default_factory=list)

    def get_age(self) -> float:
        raise NotImplementedError

    def create_plan(self) -> "Plan":
        raise NotImplementedError

    # getters/setters


@dataclass
class Owner:
    name: str
    age: int
    work_starttime: datetime
    work_endtime: datetime
    pets: list[Pet] = field(default_factory=list)

    # getters/setters


@dataclass
class Plan:
    owner: Owner
    tasks: list[Task] = field(default_factory=list)

    def print_plan_cli(self) -> None:
        raise NotImplementedError

    # getters/setters
