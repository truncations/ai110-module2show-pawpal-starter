# This file will temporarily exist for the time being as of 6/23/2026 due to being on vacation. 
## Once vacation is complete, these notes will be stored on my local working PC and will be removed upon the next commit.

The three core actions that a user should be able to perform:
- Create a "pet" categorization that holds all of the tasks FOR the given pet only.
- Create tasks for specified pet.
- Generate and display a daily plan given constraints and priorities.
*DOCUMENT THIS IN reflection.md under "What classes did you include, and what responsibilities did you assign to each?"*

Main objects needed for system:
- Pet | To store specific information about tasks and constraints for a particular pet.
    Attributes:
        * Tasks <list: class Task>
        * Owner <class Pet Owner>
        * Species <str>
        * Color <str>
        * Birthdate <datetime (?)>
        * Height <float>
        * Weight <float>
        * Allergies <list: str>
    Methods:
        * get_age() -> float | gets age in years.
        * Getters and Setters
        * create_plan() -> Plan class | Creates a plan based on the constraints and priorities
- Task | An action that the pet owner must do to best care for their pet.
    Attributes:
        * Task Name <str>
        * Task Description <str>
        * Constraint <class Constraint>
    Methods:
        * get_due_date(start_date) -> datetime | Gets due date based on the start_date (adding duration).
        * get_days_left() -> float | Gets number of days left before due date arrives (i assume that date & time being inputted is "now").
        * Getters and Setters
- Constraint | Limits that the pet owner must consider for either the pet or for themselves.
    Attributes:
        * Frequency (amt per day) <int>
        * Cooldown (amt in hours) <float>
        * Duration (amt in hours) <float>
        * Preqrequisites <list: str>
        * Time <datetime (?)>
        * Priority Level <int>
    Methods:
        * Getters and Setters
- Plan | Stores the plan for tasks, constraints and more.
    Attributes:
        * Owner <class Pet Owner>
        * Tasks <list: class Task>
    Methods:
        * print_plan_cli() -> None | Prints plan in the command line interface as a readable form.
        * Getters and Setters
- Pet Owner | Stores the pet owner's information.
    Attributes:
        * Name <str>
        * Age <int>
        * Work starttime <datetime (?)>
        * Work endtime <datetime (?)>
    Methods:
        * Getters and Setters