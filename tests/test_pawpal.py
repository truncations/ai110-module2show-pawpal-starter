from datetime import datetime, time

from pawpal_system import Constraints, Owner, Pet


def test_mark_complete_changes_status():
    constraints = Constraints(frequency=1, cooldown=0, duration=0.5, start_time=time(7, 0))
    pet = Pet("jack", "golden retriever", "white", datetime(2000, 1, 1), 4.2, 98.5)
    task = pet.create_task("Walk", "Morning walk around the block", constraints)

    assert task.status == "Incomplete"
    task.mark_complete()
    assert task.status == "Complete"


def test_create_task_increases_pet_task_count():
    constraints = Constraints(frequency=1, cooldown=0, duration=0.25, start_time=time(12, 30))
    pet = Pet("box", "doberman", "black-orange", datetime(2018, 4, 17), 5.1, 101.32)

    assert len(pet.tasks) == 0
    pet.create_task("Feed", "Midday feeding", constraints)
    assert len(pet.tasks) == 1


def test_sort_tasks_by_time_orders_scheduled_before_unscheduled():
    pet = Pet("Jack", "golden retriever", "white", datetime(2000, 1, 1), 4.2, 98.5)
    owner = Owner("Aaron", work_starttime_hr=9, work_endtime_hr=17)
    owner.add_pet(pet)
    scheduler = owner.create_plan()

    pet.create_task("Afternoon walk", "", Constraints(frequency=1, cooldown=0, duration=20, start_time=time(15, 0)))
    pet.create_task("Groom", "", Constraints(frequency=1, cooldown=0, duration=20))  # no start_time
    pet.create_task("Morning walk", "", Constraints(frequency=1, cooldown=0, duration=20, start_time=time(7, 0)))

    ordered = scheduler.sort_tasks_by_time(pet.tasks)

    assert [task.name for task in ordered] == ["Morning walk", "Afternoon walk", "Groom"]


def test_mark_task_complete_daily_recurrence_schedules_next_occurrence():
    pet = Pet("Jack", "golden retriever", "white", datetime(2000, 1, 1), 4.2, 98.5)
    constraints = Constraints(frequency=1, cooldown=0, duration=20, start_time=time(7, 0))
    task = pet.create_task("Walk", "Morning walk", constraints)
    task.due_date = datetime(2026, 7, 1, 7, 0)
    task.recurrence = "Daily"

    pet.mark_task_complete(task)

    assert task.status == "Complete"
    assert len(pet.tasks) == 2

    next_task = pet.tasks[-1]
    assert next_task is not task
    assert next_task.status == "Incomplete"
    assert next_task.recurrence == "Daily"
    assert next_task.due_date == datetime(2026, 7, 2, 7, 0)
    assert next_task.constraints.start_time == time(7, 0)


def test_mark_task_complete_weekly_recurrence_schedules_next_occurrence():
    pet = Pet("Jack", "golden retriever", "white", datetime(2000, 1, 1), 4.2, 98.5)
    constraints = Constraints(frequency=1, cooldown=0, duration=20, start_time=time(7, 0))
    task = pet.create_task("Bath", "Weekly bath", constraints)
    task.due_date = datetime(2026, 7, 1, 7, 0)
    task.recurrence = "Weekly"

    pet.mark_task_complete(task)

    next_task = pet.tasks[-1]
    assert next_task.due_date == datetime(2026, 7, 8, 7, 0)
    assert next_task.recurrence == "Weekly"


def test_mark_task_complete_without_recurrence_does_not_schedule_next_occurrence():
    pet = Pet("Jack", "golden retriever", "white", datetime(2000, 1, 1), 4.2, 98.5)
    constraints = Constraints(frequency=1, cooldown=0, duration=20, start_time=time(7, 0))
    task = pet.create_task("One-off vet visit", "", constraints)

    pet.mark_task_complete(task)

    assert task.status == "Complete"
    assert len(pet.tasks) == 1


def test_find_scheduling_conflicts_detects_overlap_across_pets():
    owner = Owner("Aaron", work_starttime_hr=9, work_endtime_hr=17)
    dog = Pet("Jack", "dog", "white", datetime(2000, 1, 1), 4.2, 98.5)
    cat = Pet("Whiskers", "cat", "black", datetime(2019, 1, 1), 1.0, 9.0)
    owner.add_pet(dog)
    owner.add_pet(cat)

    shared_time = time(8, 0)
    due = datetime(2026, 7, 2)

    task_a = dog.create_task("Walk", "", Constraints(frequency=1, cooldown=0, duration=20, start_time=shared_time))
    task_a.due_date = due
    task_b = cat.create_task("Feed", "", Constraints(frequency=1, cooldown=0, duration=10, start_time=shared_time))
    task_b.due_date = due
    task_c = dog.create_task("Groom", "", Constraints(frequency=1, cooldown=0, duration=15, start_time=time(9, 0)))
    task_c.due_date = due

    scheduler = owner.create_plan()

    assert scheduler.has_scheduling_conflicts() is True

    conflicts = scheduler.find_scheduling_conflicts()
    assert len(conflicts) == 1
    assert {task.name for task in conflicts[0]} == {"Walk", "Feed"}

    warning = scheduler.check_task_for_conflicts(task_a)
    assert warning is not None
    assert "Feed" in warning

    assert scheduler.check_task_for_conflicts(task_c) is None


def test_has_scheduling_conflicts_false_when_all_start_times_unique():
    owner = Owner("Aaron", work_starttime_hr=9, work_endtime_hr=17)
    pet = Pet("Jack", "dog", "white", datetime(2000, 1, 1), 4.2, 98.5)
    owner.add_pet(pet)

    due = datetime(2026, 7, 2)
    task_a = pet.create_task("Walk", "", Constraints(frequency=1, cooldown=0, duration=20, start_time=time(7, 0)))
    task_a.due_date = due
    task_b = pet.create_task("Feed", "", Constraints(frequency=1, cooldown=0, duration=10, start_time=time(8, 0)))
    task_b.due_date = due

    scheduler = owner.create_plan()

    assert scheduler.has_scheduling_conflicts() is False
    assert scheduler.find_scheduling_conflicts() == []
