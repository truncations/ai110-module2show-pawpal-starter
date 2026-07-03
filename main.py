from pawpal_system import Pet, Task, Owner, Scheduler, Constraints
from datetime import datetime, time

def main():
    new_owner = Owner("Aaron", 18, 7)
    pet_one = Pet("jack", "golden retriever", "white", datetime(2000, 1, 1), 4.2, 98.5)
    pet_two = Pet("box", "doberman", "black-orange", datetime(2018, 4, 17), 5.1, 101.32)

    pet_one_walk = pet_one.create_task("Walk", "Morning walk around the block", Constraints(frequency=1, cooldown=0, duration=0.5, start_time=time(7, 0)))
    pet_one.create_task("Feed", "Midday feeding", Constraints(frequency=1, cooldown=0, duration=0.25, start_time=time(12, 30)))
    pet_one_grooming = pet_one.create_task("Grooming", "Brush coat and check for ticks", Constraints(frequency=1, cooldown=0, duration=0.5, start_time=time(18, 0)))

    pet_two_feed = pet_two.create_task("Feed", "Morning feeding", Constraints(frequency=1, cooldown=0, duration=0.25, start_time=time(8, 0)))
    pet_two_walk = pet_two.create_task("Walk", "Afternoon walk in the park", Constraints(frequency=1, cooldown=0, duration=0.75, start_time=time(14, 15)))
    pet_two.create_task("Vet Checkup", "Routine wellness checkup", Constraints(frequency=1, cooldown=0, duration=1.0, start_time=time(20, 45)))

    new_owner.add_pet(pet_one)
    new_owner.add_pet(pet_two)

    # Mark tasks complete out of order (skip "Feed" in pet_one, skip the first task in pet_two).
    pet_one_grooming.mark_complete()
    pet_one_walk.mark_complete()
    pet_two_walk.mark_complete()

    scheduler = new_owner.create_plan()
    print(scheduler.filter_tasks(status="Complete"))
    print(scheduler.filter_tasks(status="Incomplete"))

    # Put pet_one's "Feed" and pet_two's "Feed" on the same due date and start time to trigger a conflict.
    shared_due_date = datetime(2026, 7, 3)
    shared_start_time = time(9, 0)
    pet_one_feed = pet_one.tasks[1]
    pet_one_feed.due_date = shared_due_date
    pet_one_feed.constraints.start_time = shared_start_time
    pet_two_feed.due_date = shared_due_date
    pet_two_feed.constraints.start_time = shared_start_time

    print(scheduler.find_scheduling_conflicts())

    candidate_task = Task(
        name="Vet Follow-up",
        description="Check-in call with the vet",
        constraints=Constraints(frequency=1, cooldown=0, duration=0.25, start_time=shared_start_time),
        due_date=shared_due_date,
    )
    print(scheduler.check_task_for_conflicts(candidate_task))

if __name__ == "__main__":
    main()