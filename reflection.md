# PawPal+ Project Reflection

## 1. System Design

//Three core actions user should be able to perform
1. enter user and pet info
2. add and edit tasks (pet care tasks (e.g. walks, feeding, grooming)) that considered constraints (time available, priority, owner preferences)
3. generate a daily plan & able to view created tasks

**a. Initial design**

The initial UML design includes seven core classes:

1. **Owner**: Represents the pet owner with flexible time availability. Stores name, list of available time windows, and preferences. Responsible for querying whether a given task duration fits within any available window.

2. **Pet**: Represents the pet being cared for. Stores name, species, age, and special needs. Responsible for returning a list of essential care requirements.

3. **Task**: Represents a single pet care task (e.g., walk, feeding, grooming). Stores title, duration in minutes, priority level (high/medium/low), and whether it's essential. Responsible for calculating priority scores and determining if it can be skipped.

4. **TimeWindow**: Represents a contiguous block of available time (e.g., 8:00–12:00). Stores start and end times. Responsible for calculating duration and checking if tasks fit within bounds.

5. **ScheduledTask**: Binds a Task to a specific time slot. Stores a reference to the task, start time, and end time. Responsible for detecting time conflicts and checking if it fits within available windows (enforces sequential scheduling).

6. **DailyPlan**: Represents the complete daily schedule output. Stores date, list of scheduled items, list of skipped tasks, and total time used. Responsible for adding tasks without conflicts, validating feasibility, and generating human-readable explanations of scheduling decisions.

7. **Scheduler**: The core orchestration engine. References the owner, pet, and pool of available tasks. Responsible for the main algorithm: sorting tasks by priority, fitting them into available time windows sequentially, tracking what was scheduled vs. skipped, and generating the final plan with reasoning.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. During implementation, I refined the initial design to make the scheduling logic more realistic and easier to build.

One important change was adding more explicit time-management behavior to the model. Instead of only storing a general list of available time windows, I made the system more focused on how tasks are actually placed within those windows. This led to stronger responsibilities for `ScheduledTask` and `DailyPlan`, so they now handle conflict detection and time-slot placement more directly.

I also decided to make the scheduler’s reasoning more explicit. In the initial concept, the plan simply needed to "choose tasks"; during implementation, I realized it would be more useful for the system to track both scheduled tasks and skipped tasks and explain why a task was included or left out. That made the design more aligned with the app’s goal of helping an owner understand the plan.

Finally, I made the pet model more useful by planning for essential care requirements to be attached to the pet itself. This makes the system better suited for daily routines where some tasks should be prioritized automatically before optional ones.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

One tradeoff in the current scheduler is that it checks for conflicts using simple time-of-day matches rather than fully modeling overlapping durations across the whole day. In practice, this means the system can detect obvious overlaps like two tasks scheduled at the same start time, but it is still a lightweight approach rather than a full calendar-style planner.

- Why is that tradeoff reasonable for this scenario?

That tradeoff is reasonable for this project because the goal is to provide a clear, readable scheduling demo rather than a production-grade calendar engine. The simpler approach makes the code easier to understand and maintain while still giving useful warnings when tasks appear to clash.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project as a design partner, debugger, and quality-checker. It was especially useful for turning the initial UML ideas into Python classes, identifying places where the design could be simplified, and drafting tests for the scheduler behaviors. I also used it to help improve the Streamlit UI and to refine the README so the project read like a complete product rather than a coding exercise.

The most helpful prompts were specific and focused, such as asking for a class structure that matched my current implementation, asking for test cases around recurring tasks and conflict detection, and asking for a clearer explanation of a bug or design issue. The AI was most effective when I provided the existing code and asked for targeted improvements rather than broad rewrites.

**b. Judgment and verification**

One example of an AI suggestion I rejected was a proposal to place too much scheduling logic directly inside the UI layer. That would have made the app easier to write quickly, but it would have mixed presentation logic with scheduling rules and made the system harder to test and maintain. I modified that idea by keeping the UI thin and making the Scheduler responsible for the actual scheduling behavior.

I evaluated the AI’s suggestions by checking them against the existing class responsibilities and by verifying the results with tests. If a suggestion improved clarity without adding unnecessary complexity, I kept it. If it made the design less cohesive, I adjusted it.

A key part of using separate chat sessions was keeping each phase focused. I used one thread for architecture and UML, another for implementation and debugging, and another for polishing the UI, tests, and documentation. That helped me stay organized and prevented earlier design ideas from being mixed with later implementation details.

The biggest lesson was that being the lead architect means setting clear boundaries, defining the system structure first, and using AI as a force multiplier rather than letting it take over the design. The human still needs to decide what belongs in each class, what tradeoffs are acceptable, and what the final product should prioritize.

---

## 4. Testing and Verification

**a. What you tested**

I tested the core behaviors that matter most for a scheduler: task sorting, recurring-task creation, conflict detection, and basic pet/owner task management. These tests were important because they verify that the system behaves correctly in the situations a pet owner is most likely to care about, such as overlapping appointments or daily tasks that should repeat.

**b. Confidence**

I am reasonably confident in the current scheduler for this project scope. The test suite covers the main success paths and the most important edge cases, and the implementation is simple enough to reason about clearly. If I had more time, I would test additional edge cases such as multiple pets sharing the same time windows, longer overlapping durations, and more complex recurring schedules with weekly or monthly patterns.

---

## 5. Reflection

**a. What went well**

I am most satisfied with how the system ended up being organized. The classes have clear responsibilities, the scheduler behavior is easy to explain, and the app now demonstrates the algorithmic features in a way that is understandable to a beginner.

**b. What you would improve**

If I had another iteration, I would improve the scheduler to support more realistic calendar-style planning, such as checking full time ranges more carefully and allowing more detailed time-window handling. I would also add persistence so appointments and pets are saved between sessions.

**c. Key takeaway**

One important lesson from this project is that strong AI-assisted development still depends on a clear human design vision. The AI can generate code quickly, but the architect’s job is to decide what the system should do, how responsibilities should be divided, and how to keep the implementation clean and maintainable.
