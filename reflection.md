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
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
