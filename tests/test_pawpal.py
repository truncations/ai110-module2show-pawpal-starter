from datetime import datetime, time

from pawpal_system import Constraints, Pet


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
