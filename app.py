from datetime import datetime

from pawpal_system import Constraints, Owner, Pet, Task
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
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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
                selected_pet.create_task(task_title, task_description, constraints)

    if selected_pet is not None and selected_pet.tasks:
        st.write(f"Current tasks for {selected_pet.name}:")
        priority_labels = {1: "🟢 Low", 2: "🟡 Medium", 3: "🔴 High"}
        for task in selected_pet.tasks:
            with st.container(border=True):
                title_col, status_col = st.columns([3, 1])
                with title_col:
                    st.markdown(f"#### {task.name}")
                with status_col:
                    st.markdown(f"**Status:** {task.status}")
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
    st.caption("This button should call your scheduling logic once you implement it.")

    if st.button("Generate schedule"):
        st.warning(
            "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
        )
        st.markdown(
            """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
        )
