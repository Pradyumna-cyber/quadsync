import streamlit as st
from PIL import Image
import base64
import os


def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.warning(f"Logo file not found at {image_path}. Using text-only header.")
        return None

logo_path = "/Users/pradyumnadeepakaher/Downloads/quadsync.png"


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1E90FF 0%, #00BFFF 100%);
        padding-top: 0;
    }
    
    .sidebar .sidebar-content img {
        margin: 20px;
        height: 80px;
        border-radius: 10px;
    }

    .stButton button {
        width: 100%;
        text-align: left;
        padding: 0.75rem 1rem;
        background-color: #007ACC;
        color: white;
        border: none;
        border-radius: 0.25rem;
        margin-bottom: 0.5rem;
        transition: background-color 0.3s;
        font-size: 1rem;
    }
    .header-container h1 {
    color: white;
            }

    .stButton button:hover {
        background-color: #005A92;
    }

    .project-card {
    color: white;
    background-color: #e6f7ff;  
    border-radius: 10px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    color: #333;
}

    
    .progress-bar {
        background-color: #f0f0f0;
        border-radius: 5px;
        height: 15px;
        position: relative;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .progress-bar-fill {
        background-color: #1E90FF;
        height: 100%;
        border-radius: 5px;
        transition: width 0.5s ease-in-out;
    }

    .project-card h3 {
        color: #1E90FF;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .project-card p {
        margin: 5px 0;
        color: #666;
    }

    h1, h2, h3, h4 {
        color: #007ACC;
        font-weight: 600;
    }

    .header-container {
    padding: 20px;
    background-color: #1E90FF;  
    color: white;                
    text-align: center;
    border-radius: 10px;
    margin-bottom: 20px;
}

    
    .revenue-section {
        color: #2C3E50;
        font-size: 1.2rem;
        margin: 20px 0;
    }

    .sidebar .sidebar-content h1 {
        color: white;
        font-size: 1.5rem;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

logo_base64 = get_image_base64(logo_path)
if logo_base64:
    st.sidebar.markdown(f"<img src='data:image/png;base64,{logo_base64}' alt='QuaddyNC Logo'>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<h1>QuaddyNC</h1>", unsafe_allow_html=True)

# Initialize session state variables
if "projects" not in st.session_state:
    st.session_state.projects = []
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "team_members" not in st.session_state:
    st.session_state.team_members = [
        {"name": "Harsh", "percentage": 25.0},
        {"name": "Pradyumna", "percentage": 25.0},
        {"name": "Prabhat", "percentage": 25.0},
        {"name": "Kartik P", "percentage": 25.0}
    ]

def add_project():
    with st.form("project_form", clear_on_submit=True):
        title = st.text_input("Project Title")
        desc = st.text_area("Project Description")
        # progress = st.slider("Progress", 0, 100, 0)
        team_members = st.multiselect("Team Members", [member["name"] for member in st.session_state.team_members])
        uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            project_data = {
                "title": title,
                "desc": desc,
                "progress": progress,
                "team_members": team_members,
                "files": uploaded_files
            }
            st.session_state.projects.append(project_data)
            st.success(f"Project '{title}' added successfully!")

def add_job():
    with st.form("job_form", clear_on_submit=True):
        job_title = st.text_input("Job Title")
        job_desc = st.text_area("Job Description")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.jobs.append({"title": job_title, "desc": job_desc})
            st.success(f"Job '{job_title}' added successfully!")

def display_project_card(project):
    """Display project details in a card format."""
    with st.container():
        col1, col2 = st.columns([3, 1])  # Two columns for layout
        with col1:
            st.markdown(f"<div class='project-card'><h3>{project['title']}</h3>", unsafe_allow_html=True)
            st.write(f"**Description:** {project['desc']}")
            st.write(f"**Team Members:** {', '.join(project['team_members'])}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.progress(project['progress'])

def display_project_details(project):
    st.markdown("<div class='header-container'><h1>Project Details</h1></div>", unsafe_allow_html=True)
    st.write(f"**Title:** {project['title']}")
    st.write(f"**Description:** {project['desc']}")
    st.write(f"**Team Members:** {', '.join(project['team_members'])}")

    # Progress Bar
    st.subheader("Progress Bar")
    sections = ["Project Details (Title, Files, Tech Stack)", "Project Images and Code Files",
                "Complete Project Code and Images", "Final Question about Project"]
    for i, section in enumerate(sections):
        st.write(f"**{section}**")
        st.progress((i + 1) * 25)  # Update progress for each section completed

    st.subheader("Upload Additional Files")
    if project['files']:
        st.write("**Uploaded Files:**")
        for uploaded_file in project['files']:
            st.write(f"- {uploaded_file.name}")
    
    st.subheader("Download Project Files")
    if st.button("Zip and Download"):
        # Logic to zip and download files goes here
        st.success("Files are being prepared for download!")
    
    st.button("Mark as Done", on_click=lambda: mark_project_done(project))

def mark_project_done(project):
    project['progress'] = 100  # Mark project as completed
    st.success(f"Project '{project['title']}' marked as done!")
    st.experimental_rerun()  # Rerun the app to update the display

with st.sidebar:
    st.title("Menu")
    if st.button("Dashboard"):
        st.session_state.current_page = "Dashboard"
    if st.button("Projects"):
        st.session_state.current_page = "Projects"
    if st.button("Revenue Distribution"):
        st.session_state.current_page = "Revenue Distribution"
    if st.button("Hiring"):
        st.session_state.current_page = "Hiring"

with st.container():
    if st.session_state.current_page == "Dashboard":
        st.markdown("<div class='header-container'><h1>Dashboard</h1></div>", unsafe_allow_html=True)
        st.write("Welcome to the quadsync Project Management and Business Dashboard.")
        
        if st.session_state.projects:
            st.subheader("Current Projects")
            for project in st.session_state.projects:
                display_project_card(project)  # Display each project as a card
                if st.button(f"Open Project: {project['title']}"):
                    display_project_details(project)
        else:
            st.info("No projects added yet.")

    elif st.session_state.current_page == "Projects":
        st.markdown("<div class='header-container'><h1>Project Management</h1></div>", unsafe_allow_html=True)
        add_project()
        
        if st.session_state.projects:
            for project in st.session_state.projects:
                with st.expander(f"Project: {project['title']}"):
                    st.write(f"**Description:** {project['desc']}")
                    st.write(f"**Team Members:** {', '.join(project['team_members'])}")
                    st.write(f"**Progress:** {project['progress']}%")

    elif st.session_state.current_page == "Revenue Distribution":
        st.title("Revenue Distribution")
        
        # Input for total revenue and deduction amount
        total_revenue = st.number_input("Enter Total Revenue (₹)", min_value=0.0, step=0.01)
        deduction_amount = st.number_input("Enter Deduction Amount (₹)", min_value=0.0, step=0.01)

        st.subheader("Team Members")
        
        total_percentage = 0
        for i, member in enumerate(st.session_state.team_members):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input(f"Name {i+1}", value=member['name'], key=f"name_{i}")
            with col2:
                percentage = st.number_input(
                    f"Percentage {i+1}",
                    min_value=0.0,
                    max_value=100.0,
                    value=member['percentage'],
                    step=0.1,
                    key=f"percentage_{i}"
                )
            st.session_state.team_members[i] = {"name": name, "percentage": percentage}
            total_percentage += percentage

        if st.button("Add Team Member"):
            st.session_state.team_members.append({"name": "", "percentage": 0.0})

        if st.button("Distribute"):
            if total_revenue <= 0:
                st.warning("Total revenue must be greater than zero.")
            elif deduction_amount >= total_revenue:
                st.warning("Deduction amount must be less than total revenue.")
            elif abs(total_percentage - 100) > 0.01:
                st.warning(f"Total percentage must equal 100%. Current total: {total_percentage:.2f}%")
            else:
                remaining_revenue = total_revenue - deduction_amount
                
                # Display the financial details
                st.markdown(f"<h3 style='color: #28a745;'>Total Revenue: ₹{total_revenue:.2f}</h3>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='color: #dc3545;'>Deduction Amount: ₹{deduction_amount:.2f}</h4>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='color: #007bff;'>Remaining Revenue: ₹{remaining_revenue:.2f}</h4>", unsafe_allow_html=True)
                st.write("### Distribution Breakdown:")

                for member in st.session_state.team_members:
                    # Skip empty names or percentages
                    if member["name"] and member["percentage"] > 0:
                        amount = remaining_revenue * (member["percentage"] / 100)
                        st.markdown(f"<div style='padding: 10px; background-color: #f8f9fa; border-radius: 5px;'>"
                                    f"- <span style='color: #333; font-weight: bold;'>{member['name']}</span>: "
                                    f"<span style='color: #17a2b8; font-weight: bold;'>₹{amount:.2f}</span> "
                                    f"({member['percentage']:.1f}%)</div>", unsafe_allow_html=True)

    elif st.session_state.current_page == "Hiring":
        st.markdown("<div class='header-container'><h1>Hiring</h1></div>", unsafe_allow_html=True)
        add_job()
        
        if st.session_state.jobs:
            for job in st.session_state.jobs:
                st.write(f"**Job Title:** {job['title']}")
                st.write(f"**Description:** {job['desc']}")
