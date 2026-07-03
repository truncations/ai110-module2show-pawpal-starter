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
    I used AI tools in this project as a companion to help me figure out how I wanted to design most of my program by asking it questions on how I could implement features, as well as asking for suggestions if I ended up having any difficulties throughout my development process. When I design brainstormed, I created a separate markdown file (Notes) to help me determine what would be best to develop this application's system. Additionally, when I debugged, I asked AI questions on why the functionality behaved the way it did.
- What kinds of prompts or questions were most helpful?
    The kind of prompt that does help the most is when I ask AI to co-op an implementation that I would seek for, by breaking down the problem into smaller steps (like problem solving) and working small steps at a time. Each step, I asked AI for feedback but also provided my insight and thoughts (basically as much context as I could) to help the AI guide me towards a correct direction and explain me what I could do to improve and whatnot.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    One AI suggestion that I did not accept during my development process was when I needed to implement the feature of determining schedule conflicts. I had created a function similar to _group_scheduled_tasks() where I needed to group tasks by a start time key (before refactoring it with the assistance of AI), and needed to determine whether a created task or any already created task had scheduling conflict. I noticed a suggestion where when I prompted to implement both of these features, it would not use the function _group_scheduled_tasks() to actually determine the scheduling conflicts properly which completely ruined the idea of using modularized code. It tried to create its own function on its own which I ended up completely scraping.
- How did you evaluate or verify what the AI suggested?
    I evaluated or verified what the AI suggested by testing the application itself with the streamlit package, to make sure that the application runs as expected throughout each step I used AI to help me write code. I intricately tested and tried to think of being the consumer in the application, to see what a consumer would do when using my application. For the system, I created test cases as shown in test_pawpal.py, and manually tested with main.py to help make sure that the backend of the program was properly functional and that it wouldn't have any issues going forward.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    The behaviors I tested were of the following:
        - Ensured I could get all tasks from every pet.
        - Filtering the tasks by completion status was functional
        - Sorting the tasks for a particular pet by start time was functional
        - Whether the scheduling conflict would kick in, to stop the user from scheduling a task that would conflict with another.
        - Whether I could create a pet in the first place
        - Whether the constraints I gave would actually limit the user when the constraint was necessary.
        - Whether marking a task complete or incomplete was functional. 
- Why were these tests important?
    These tests are important because they verify the core functionality of the program, as well as ensure that the common user flow is functional so that an everyday consumer can use the program without hassle. They also make sure to handle cases where a user could make a mistake in inputting information that could cause an application to break, or be unrealistic in general (for this case, a pet task scheduler).
**b. Confidence**

- How confident are you that your scheduler works correctly?
    I am confident that my scheduler works correctly, I gave it around a 4 stars out of 5 for the functionality of the scheduler.
- What edge cases would you test next if you had more time?
    The edge cases that I would test if I had more time would be mostly the extreme scenarios; basically hacking the program, or doing excessive inputs. That way I can see if the program can hold up even under the most unbearable difficulty, since I only tested for common user interactions. I should've tested how the program behaves when I for example, auto clicked on buttons, or inputted weird values in other places. I additionally should've tested for some of the very well known edge cases (as we studied in class) like empty lists or None type.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    The part of this project I felt most satisfied with was the frequency system I created where you had a limit on how frequent you could make the task daily. If you had a task that repeated too much (under the duration and cooldown) to the point it'd bleed over to the next day, then creating the task would be invalid. Even though it's a small feature, it was something that I felt proud of since it covers up a scenario where a user could try to schedule a task that would repeat too many times in a single day.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    If I had another iteration, I would likely improve the task system that I had created as I completely disregarded the entire idea of recurring schedules and should've added some form of calendar that the user could see where they could see weekly, monthly tasks that were scheduled for a given period. That way the user could realistically have more information to plan for their lifestyle.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    One important thing I learned about designing systems is that planning a system using UML to show 'has-a' or 'is-a' relationships makes Object Oriented Programming way more convenient by providing a boilerplate that I can follow and adapt towards without having to freestyle a system entirely from scratch. Using UML, I can also visualize the separation between classes which will eventually be helpful when I get into systems like backend-frontend, or model-view-controller.
