from datetime import datetime

from pawpal_system import Constraints, Owner, Pet, Task, Scheduler
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

WORK_HOUR_OPTIONS = [
    f"{((hour % 12) or 12)}:00 {'AM' if hour < 12 else 'PM'}" for hour in range(24)
]

TASK_START_TIME_OPTIONS = [
    f"{((minutes // 60) % 12) or 12}:{minutes % 60:02d} {'AM' if (minutes // 60) < 12 else 'PM'}"
    for minutes in range(0, 24 * 60, 30)
]

PRIORITY_LEVELS = {"low": 1, "medium": 2, "high": 3}

with st.sidebar:
    st.header("Owner Information")
    owner_name = st.text_input("Owner name", value="Aaron")
    work_start_label = st.selectbox("Work start time", WORK_HOUR_OPTIONS, index=9)
    work_end_label = st.selectbox("Work end time", WORK_HOUR_OPTIONS, index=17)

work_starttime_hr = WORK_HOUR_OPTIONS.index(work_start_label)
work_endtime_hr = WORK_HOUR_OPTIONS.index(work_end_label)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name,
        work_starttime_hr=work_starttime_hr,
        work_endtime_hr=work_endtime_hr,
    )
else:
    st.session_state.owner.name = owner_name
    st.session_state.owner.work_starttime_hr = work_starttime_hr
    st.session_state.owner.work_endtime_hr = work_endtime_hr

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** — a scheduling assistant that helps pet owners plan daily care
routines (walks, feedings, meds, playtime, and more) around their own work hours.

**What you can do here:**
- 🐶 **Pet Information** — register one or more pets with basic details like species, color, and birthdate.
- 📝 **Tasks** — create recurring care tasks for each pet, with duration, cooldown time between
  repeats, frequency per day, priority, start time, and optional prerequisites. Tasks can also be
  filtered, sorted, and marked complete.
- 📅 **Build Schedule** — generate a conflict-aware daily schedule across all pets and tasks,
  respecting the owner's work hours and each task's constraints.
"""
)

st.divider()

pet_tab, tasks_tab, schedule_tab = st.tabs(["🐶 Pet Information", "📝 Tasks", "📅 Build Schedule"])

with pet_tab:
    st.subheader("Pet Information")
    pet_name = st.text_input("Pet name", value="Mochi")

    pet_col1, pet_col2 = st.columns(2)
    with pet_col1:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with pet_col2:
        color = st.selectbox(
            "Color", ["black", "white", "brown", "tan", "gray", "orange", "blue", "red", "cream"]
        )

    birthdate = st.date_input(
        "Birthdate",
        min_value=datetime(1900, 1, 1),
        max_value=datetime.now(),
    )

    size_col1, size_col2 = st.columns(2)
    with size_col1:
        height = st.text_input("Height (in feet)", value="1.0")
    with size_col2:
        weight = st.text_input("Weight (in pounds)", value="1.0")

    if st.button("Add pet"):
        try:
            height_val = float(height)
            weight_val = float(weight)
        except ValueError:
            st.error("Height, and weight must be numbers.")
        else:
            owner = st.session_state.owner
            if owner.can_create_pet(
                pet_name, species, color, birthdate.year, birthdate.month, birthdate.day, height_val, weight_val
            ):
                owner.create_pet(
                    pet_name, species, color, birthdate.year, birthdate.month, birthdate.day, height_val, weight_val
                )
            else:
                st.error("Invalid pet details. Check the pet name and birth date.")

    if st.session_state.owner.pets:
        st.write("Available pets:")
        st.table(
            [
                {
                    "name": pet.name,
                    "species": pet.species,
                    "color": pet.color,
                    "birthdate": pet.birthdate.strftime("%Y-%m-%d"),
                    "height": pet.height,
                    "weight": pet.weight,
                }
                for pet in st.session_state.owner.pets.values()
            ]
        )
    else:
        st.info("No pets yet. Add one above.")

with tasks_tab:
    st.subheader("Scheduling Tasks")
    st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

    if not st.session_state.owner.pets:
        st.warning("Add a pet in the Pet Information tab before creating tasks.")
        selected_pet = None
    else:
        pet_names = list(st.session_state.owner.pets.keys())
        selected_pet_name = st.selectbox("Selected Pet to schedule Task", pet_names)
        selected_pet = st.session_state.owner.pets[selected_pet_name]

    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_description = st.text_input("Task description", value="Walk around the block")

    col3, col4, col5 = st.columns(3)
    with col3:
        duration = st.slider("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        cooldown = st.slider("Cooldown (minutes)", min_value=0, max_value=240, value=1)
    with col5:
        frequency = st.slider("Frequency (times per day)", min_value=1, max_value=24, value=1)

    col6, col7 = st.columns(2)
    with col6:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col7:
        start_time_label = st.selectbox("Start time", TASK_START_TIME_OPTIONS)

    prerequisites_input = st.text_input("Prerequisites (comma-separated, optional)", value="")

    if st.button("Add task"):
        if selected_pet is None:
            st.error("Select a pet before adding a task.")

        else:
            prerequisites = [item.strip() for item in prerequisites_input.split(",") if item.strip()]
            constraints = Constraints(
                frequency=int(frequency),
                cooldown=float(cooldown),
                duration=duration,
                prerequisites=prerequisites,
                start_time=datetime.strptime(start_time_label, "%I:%M %p").time(),
                priority_level=PRIORITY_LEVELS[priority],
            )

            if not constraints.frequency_is_allowed(int(frequency)):
                max_frequency = constraints.get_max_frequency()
                st.error(
                    f"That's too frequent — at a {duration}-minute duration and {cooldown}-minute "
                    f"cooldown starting at {start_time_label}, this task can only repeat {max_frequency}x "
                    "per day before it runs past midnight into the next day. Lower the frequency or "
                    "reduce the duration/cooldown."
                )
            else:
                scheduler = st.session_state.owner.create_plan()
                candidate_task = Task(name=task_title, description=task_description, constraints=constraints)
                conflict_message = scheduler.check_task_for_conflicts(candidate_task)

                if conflict_message:
                    st.error(conflict_message)
                else:
                    selected_pet.create_task(task_title, task_description, constraints)

    if selected_pet is not None and selected_pet.tasks:
        st.write(f"Current tasks for {selected_pet.name}:")

        control_col1, control_col2 = st.columns(2)
        with control_col1:
            status_filter = st.radio(
                "Filter by status", ["All", "Complete", "Incomplete"], horizontal=True
            )
        with control_col2:
            sort_by_time = st.toggle("Sort by start time")

        scheduler = st.session_state.owner.create_plan()

        if status_filter == "All":
            tasks_to_show = selected_pet.tasks
        else:
            status_matches = scheduler.filter_tasks(status=status_filter)
            tasks_to_show = [task for task in selected_pet.tasks if task in status_matches]

        if sort_by_time:
            tasks_to_show = scheduler.sort_tasks_by_time(tasks_to_show)

        priority_labels = {1: "🟢 Low", 2: "🟡 Medium", 3: "🔴 High"}
        for task_index, task in enumerate(tasks_to_show):
            with st.container(border=True):
                title_col, status_col = st.columns([3, 1])
                with title_col:
                    st.markdown(f"#### {task.name}")
                with status_col:
                    is_complete = st.checkbox(
                        f"Complete ({task.status})",
                        value=task.status == "Complete",
                        key=f"{selected_pet.name}-{task.name}-{task_index}-complete",
                    )
                    if is_complete and task.status != "Complete":
                        selected_pet.mark_task_complete(task)
                        st.rerun()
                    elif not is_complete and task.status == "Complete":
                        task.mark_incomplete()
                        st.rerun()
                    
                if task.description:
                    st.caption(task.description)

                detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
                detail_col1.metric("Start", task.constraints.start_time.strftime("%I:%M %p"))
                detail_col2.metric("Duration", f"{task.constraints.duration} min")
                detail_col3.metric("Frequency", f"{task.constraints.frequency}x/day")
                detail_col4.metric(
                    "Priority",
                    priority_labels.get(task.constraints.priority_level, task.constraints.priority_level),
                )

                st.caption(f"Cooldown: {task.constraints.cooldown} min")
                if task.constraints.prerequisites:
                    st.markdown(f"**Prerequisites:** {', '.join(task.constraints.prerequisites)}")
    else:
        st.info("No tasks yet. Add one above.")

with schedule_tab:
    st.subheader("Build Schedule")
    st.caption("Generates a daily schedule across all pets, grouped by pet and sorted by start time.")

    if st.button("Generate schedule"):
        st.session_state.schedule_built = True

    if not st.session_state.owner.pets:
        st.warning("Add a pet and some tasks before generating a schedule.")
    elif not st.session_state.get("schedule_built"):
        st.info("Click **Generate schedule** to build the daily plan.")
    else:
        scheduler = st.session_state.owner.create_plan()
        all_tasks = st.session_state.owner.get_all_tasks()
        total_tasks = sum(len(tasks) for tasks in all_tasks.values())

        if total_tasks == 0:
            st.info("No tasks scheduled yet. Add tasks in the Tasks tab.")
        else:
            conflicts = scheduler.find_scheduling_conflicts()
            completed = len(scheduler.filter_tasks(status="Complete"))

            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            metric_col1.metric("Total tasks", total_tasks)
            metric_col2.metric("Completed", completed)
            metric_col3.metric("Pending", total_tasks - completed)
            metric_col4.metric("Conflicts", len(conflicts))

            if conflicts:
                for group in conflicts:
                    time_str = group[0].constraints.start_time.strftime("%I:%M %p")
                    names = ", ".join(task.name for task in group)
                    st.error(f"⚠️ Conflict at {time_str}: {names}")
            else:
                st.success("No scheduling conflicts. 🎉")

            st.divider()

            status_labels = {
                "Complete": "✅ Complete",
                "In Progress": "🔄 In Progress",
                "Incomplete": "⏳ Incomplete",
            }
            priority_labels = {1: "🟢 Low", 2: "🟡 Medium", 3: "🔴 High"}

            for pet_name, tasks in all_tasks.items():
                if not tasks:
                    continue

                st.markdown(f"#### 🐾 {pet_name}")
                sorted_tasks = scheduler.sort_tasks_by_time(tasks)

                rows = [
                    {
                        "Time": task.constraints.start_time.strftime("%I:%M %p")
                        if task.constraints.start_time
                        else "Unscheduled",
                        "Task": task.name,
                        "Status": status_labels.get(task.status, task.status),
                        "Duration": f"{task.constraints.duration} min",
                        "Priority": priority_labels.get(task.constraints.priority_level, "—"),
                        "During work hours": "🏢 Yes" if scheduler.is_task_in_work_hours(task) else "🏠 No",
                        "Prerequisites": ", ".join(task.constraints.prerequisites)
                        if task.constraints.prerequisites
                        else "—",
                    }
                    for task in sorted_tasks
                ]

                st.dataframe(rows, width="stretch", hide_index=True)
