# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

The initial design I decided to go for is to focus on the following three core actions:
    1. Create a "pet" categorization that holds all of the tasks FOR the given pet only.
    2. Create tasks for specified pet.
    3. Generate and display a daily plan given constraints and priorities.

These core actions will then be connected with the following classes which should fulfill all of the core actions necessary: Pet, Task, Constraint, Plan, and Owner.

In general, the classes should have these following relationships with each other:
    Pet has a Pet Owner and Tasks.
    Task has Constraints.
    Plan has Tasks.
There is NO inheritance to be made for this project.

- What classes did you include, and what responsibilities did you assign to each?

The classes I decided to include are the following with their responsibilities assigned to each:
    * Pet - To store specific information about tasks and constraints for a particular pet.
    * Task - An action that the pet owner must do to best care for their pet.
    * Constraint - Limits that the pet owner must consider for either the pet or for themselves.
    * Plan - Stores the plan for tasks, constraints and more.
    * Owner - Stores the pet owner's information.

**b. Design changes**

- Did your design change during implementation?
    Yes. My design changed during implementation.
- If yes, describe at least one change and why you made it.
    I moved the method create_plan() to another class. Instead of the class Pet, I moved up to the Owner because it logically justifies the realism of the scenario; an Owner creates a plan, not the pet itself. This also means that an owner can create multiple pets. Additionally, I replaced the data types of "datetime" to be "datetime.time" for some variables like work start time and work end time because it is unrealistic to hold datetime for a work start time and work end time since we don't need to know a particular day. I also did this with the start_time for task.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    My constraints that my scheduler considers are the following properties: Priority, Time, Prerequisites, Frequency of task, and Duration.
- How did you decide which constraints mattered most?
    I decided on which constraints mattered most by determining the impact of the person's lifestyle if I included the constraint in a realistic manner. I also wanted to create constraints to make sure that the person couldn't commit to an action that was either excessive or impossible to do. Once I understood these questions, I came up with a few simple constraints to help answer both of these questions which was Priority; to tell the person which tasks are most important, Time; what time to start the task, Prerequisites; Any actions that must be done BEFORE handling the task, Frequency of Task; how often the task should be done, and Duration; how long the task is being done for.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    One tradeoff that my scheduler makes mainly is for memory complexity; I prioritize readability for code over the efficiency of the program which can end up doing unnecessary steps. For the most important example, this can be well shown in _group_scheduled_tasks(), find_scheduling_conflicts() and check_task_for_conflicts(). Although this method _group_scheduled_tasks() was reformatted to help follow D.R.Y (don't repeat yourself), it added extra steps to the program than I initially thought with AI's assistance on analysis when analyzing check_task_for_conflicts() where through each requested scheduled task, the program would build a group of dictionaries only to pick up one single set from the dictionary every single query.
- Why is that tradeoff reasonable for this scenario?
    Because the amount of tasks that would be created for a single pet would be pretty small, and realistically, the number of tasks for a pet at max would be around 10-15, and the number of pets would be at max 3. If we do the mathematics, that's a list/dictionary of size 45 which is nowhere near enough of a huge dataset that the performance makes a difference. But this also means that we can use _group_scheduled_tasks() as a method for future methods if we choose to implement other sorting/filtering methods (thanks to its flexibility, as shown with its use in check_task_for_conflicts() and find_scheduling_conflicts()).
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
