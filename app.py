import streamlit as st
from datetime import datetime

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
This simple planner helps you organize pet care tasks with clear sorting, filtering, and conflict checks.
"""
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

if "pet" not in st.session_state:
    st.session_state.pet = Pet(name="Mochi", species="dog")

if not any(pet.name == st.session_state.pet.name and pet.species == st.session_state.pet.species for pet in st.session_state.owner.pets):
    st.session_state.owner.add_pet(st.session_state.pet)

st.subheader("Owner and pet")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
pet_name = st.text_input("Pet name", value=st.session_state.pet.name)
species = st.selectbox("Species", ["dog", "cat", "other"], index=["dog", "cat", "other"].index(st.session_state.pet.species))

if owner_name != st.session_state.owner.name:
    st.session_state.owner.name = owner_name

if pet_name != st.session_state.pet.name or species != st.session_state.pet.species:
    st.session_state.pet.name = pet_name
    st.session_state.pet.species = species

if st.button("Add pet to owner"):
    new_pet = Pet(name=pet_name, species=species)
    if not any(existing.name.lower() == new_pet.name.lower() for existing in st.session_state.owner.pets):
        st.session_state.owner.add_pet(new_pet)
    st.session_state.pet = new_pet
    st.success(f"Added {pet_name} to {st.session_state.owner.name}'s pets.")

st.divider()

st.subheader("Add an appointment")
with st.form("task_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Appointment", value="Vet Visit")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    task_time = st.time_input("Time", value=datetime.now().time())
    submitted = st.form_submit_button("Add appointment")

    if submitted:
        task = Task(
            description=task_title,
            duration_minutes=int(duration),
            priority=priority,
            time_of_day=task_time.strftime("%H:%M"),
            due_date=datetime.combine(datetime.now().date(), task_time),
        )
        st.session_state.pet.add_task(task)

        scheduler = Scheduler(st.session_state.owner, pet=st.session_state.pet)
        conflict_warning = scheduler.detect_conflicts(st.session_state.pet.tasks)
        if conflict_warning:
            st.warning(
                f"⚠️ {st.session_state.pet.name} already has a task at this time. "
                f"{conflict_warning} Please choose another time or review the schedule before confirming."
            )
        else:
            st.success(f"Added '{task_title}' for {st.session_state.pet.name} without conflicts.")

st.divider()

st.subheader("Scheduler overview")
scheduler = Scheduler(st.session_state.owner, pet=st.session_state.pet)

pet_filter = st.selectbox(
    "View appointments for",
    ["All pets"] + [pet.name for pet in st.session_state.owner.pets],
)

if pet_filter == "All pets":
    visible_tasks = scheduler.filter_tasks(st.session_state.owner.get_all_tasks(), completed=False)
else:
    visible_tasks = scheduler.filter_tasks(st.session_state.owner.get_all_tasks(), completed=False, pet_name=pet_filter)

sorted_tasks = scheduler.sort_by_time(visible_tasks)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Total appointments", len(sorted_tasks))
with col_b:
    st.metric("Number of pets", len(st.session_state.owner.pets))
with col_c:
    conflict_warning = scheduler.detect_conflicts(sorted_tasks)
    st.metric("Number of conflicts", 1 if conflict_warning else 0)

chart_data = {pet.name: len(pet.get_pending_tasks()) for pet in st.session_state.owner.pets}
if chart_data:
    st.caption("Appointments by pet")
    st.bar_chart(chart_data)

if sorted_tasks:
    schedule_rows = []
    for task in sorted_tasks:
        matching_pet = next((pet for pet in st.session_state.owner.pets if task in pet.tasks), st.session_state.pet)
        schedule_rows.append(
            {
                "Pet": matching_pet.name,
                "Appointment": task.description,
                "Time": task.time_of_day or "Not set",
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority.title(),
            }
        )

    st.caption("Upcoming appointments in sorted order")
    st.dataframe(schedule_rows, use_container_width=True)
else:
    st.info("No upcoming appointments yet. Add one above to build the schedule.")

if pet_filter == "All pets":
    conflict_warning = scheduler.detect_conflicts(st.session_state.owner.get_all_tasks())
else:
    conflict_warning = scheduler.detect_conflicts(
        scheduler.filter_tasks(st.session_state.owner.get_all_tasks(), completed=False, pet_name=pet_filter)
    )

if conflict_warning:
    st.warning(conflict_warning)
else:
    st.success("No scheduling conflicts found for the selected view.")
