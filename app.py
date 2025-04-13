import streamlit as st
import requests

# API endpoint
API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:bfNgfeoN/application"

# Page settings
st.set_page_config(page_title="Applications", layout="centered")
st.title("💼 Track Applications")

# Fixed color palette
domain_colors = [
    "#2e6f9a", "#6a1b9a", "#d84315", "#00897b", "#5e35b1", "#ef6c00",
    "#3949ab", "#00acc1", "#8e24aa", "#7cb342", "#c62828"
]

# Map to hold consistent domain-color pairs
domain_color_map = {}

# Function to fetch data from API
@st.cache_data(ttl=5)  # Cache the data for 5 minutes
def fetch_jobs():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

# Get jobs data
jobs = fetch_jobs()

if not jobs:
    st.warning("No job listings available or error fetching data.")
else:
    # Loop through each job and display details
    for i, job in enumerate(jobs):
        with st.container():
            # Create two columns for job details and recruiters
            job_col, recruiter_col = st.columns([8, 3])  # Adjust column width if needed
            with job_col:
                # Display job details on the left
                job_title = job.get('job_title', 'No Title')
                company = job.get('company', 'No Company')
                domain = job.get('domain', 'N/A')
                linkedin_url = job.get('linkedin_url','#')
                min_salary = job.get('min_salary')
                max_salary = job.get('max_salary')

                if min_salary > 0 and max_salary > 0:
                    salary_display = f"|💰 **Salary:**: \\${min_salary:,} - \\${max_salary:,}"
                elif min_salary > 0 or max_salary > 0:
                    salary_display = f"|💰 **Salary:**: ${max(min_salary, max_salary):,}"
                else:
                    salary_display = ""
                if domain not in domain_color_map:
                    domain_color_map[domain] = domain_colors[len(domain_color_map) % len(domain_colors)]
                domain_color = domain_color_map[domain]

                st.markdown(
                    f"""
                    <div style="margin-bottom: 5px;">
                        <div style="font-size: 22px; font-weight: 700;">
                            <a href="{linkedin_url}" target="_blank" style="color: white; text-decoration: none;">{job_title}</a>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 16px; color: gray;">{company}</span>
                            <span style="
                                background-color: {domain_color};
                                color: white;
                                font-size: 11px;
                                padding: 4px 10px;
                                border-radius: 20px;
                                font-weight: 500;
                            ">
                                {domain}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(f"📍 **Location:** {job.get('location', 'N/A')} {salary_display}")
                st.markdown(f"📝 **Description:** {job.get('description', 'No description available.')}")

            with recruiter_col:
                # Display recruiters on the right with reduced margin
                # st.markdown("#### 👥 Recruiters", unsafe_allow_html=True)
                
                recruiters = job.get("_contacts", [])
                if not recruiters:
                    st.write("No recruiters available.")
                else:
                    # Display smaller recruiter cards with less padding and smaller font
                    for idx, recruiter in enumerate(recruiters[0:3]):
                        name = recruiter.get('name') if job.get('name') and len(recruiter.get('name')) <= 15 else recruiter.get('short_name')
                        initials = ''.join([part[0] for part in recruiter.get('name', 'NA').split()[:2]]).upper()
                        top_margin = "40px" if idx == 0 else "0px"
                        st.markdown(
                            f"""
                            <a href="{recruiter.get('linkedin_url', '#')}" target="_blank" style="text-decoration: none;">
                                <div style="
                                    display: flex;
                                    align-items: center;
                                    background-color: #3a3a3a;
                                    border-radius: 30px;
                                    padding: 6px 10px;
                                    margin-bottom: 6px;
                                    margin-top: {top_margin};
                                    min-width: 170px;
                                    width: fit-content;
                                    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
                                ">
                                    <div style="
                                        background-color: #00aaff;
                                        border-radius: 50%;
                                        width: 30px;
                                        height: 30px;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                        font-weight: 700;
                                        color: white;
                                        margin-right: 10px;
                                        font-size: 13px;
                                    ">{initials}</div>
                                    <div>
                                        <div style="color: white; font-weight: 600; font-size: 14px; margin-bottom: 1px;">{name}</div>
                                        <div style="color: #cccccc; font-size: 11px; font-style: italic; margin-top: -5px; line-height: 12px">
                                        {recruiter.get('title', 'No Title')}
                                    </div>
                                    </div>
                                </div>
                            </a>
                            """,
                            unsafe_allow_html=True
                        )

        
        # Add a separator between job listings except for the last one
        if i < len(jobs) - 1:
            st.markdown("---")