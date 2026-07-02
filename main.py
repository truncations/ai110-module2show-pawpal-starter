from pawpal_system import Pet, Task, Owner, Scheduler, Constraints
from datetime import datetime, time

def main():
    new_owner = Owner("Aaron", 18, 7, 16)
    pet_one = Pet("jack", "golden retriever", "white", datetime(2000, 1, 1), 4.2, 98.5)
    pet_two = Pet("box", "doberman", "black-orange", datetime(2018, 4, 17), 5.1, 101.32)

    pet_one.create_task("Walk", "Morning walk around the block", Constraints(frequency=1, cooldown=0, duration=0.5, start_time=time(7, 0)))
    pet_one.create_task("Feed", "Midday feeding", Constraints(frequency=1, cooldown=0, duration=0.25, start_time=time(12, 30)))
    pet_one.create_task("Grooming", "Brush coat and check for ticks", Constraints(frequency=1, cooldown=0, duration=0.5, start_time=time(18, 0)))

    pet_two.create_task("Feed", "Morning feeding", Constraints(frequency=1, cooldown=0, duration=0.25, start_time=time(8, 0)))
    pet_two.create_task("Walk", "Afternoon walk in the park", Constraints(frequency=1, cooldown=0, duration=0.75, start_time=time(14, 15)))
    pet_two.create_task("Vet Checkup", "Routine wellness checkup", Constraints(frequency=1, cooldown=0, duration=1.0, start_time=time(20, 45)))

    new_owner.add_pet(pet_one)
    new_owner.add_pet(pet_two)

    scheduler = new_owner.create_plan()
    print(scheduler.get_plan_str())

if __name__ == "__main__":
    main()