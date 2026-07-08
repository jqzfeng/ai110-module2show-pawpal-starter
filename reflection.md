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
