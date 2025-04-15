import streamlit as st
import requests

def fetch_jobs():
    try:
        response = requests.get("https://x8ki-letl-twmt.n7.xano.io/api:bfNgfeoN/application")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

@st.fragment
def show_applications():
    st.markdown("""
        <style>
        /* Reduce top margin and padding on the main block container */
        .block-container {
            padding-top: 2rem !important;
        }
        /* Optional: reduce side paddings as well if needed */
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Testing sticky header
    # st.markdown("""
    # <style>
    #     div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
    #         position: sticky;
    #         top: 2rem;
    #         z-index: 100; /* Make sure it stays above other elements */
    #     }
    #     .header-container {
    #         background-color: #f0f2f6; /* Change this to your desired background color */
    #         padding: 10px; /* Add some padding */
    #         border-radius: 5px; /* Add rounded corners */
    #     }
    # </style>
    # """, unsafe_allow_html=True)

    # with st.container():
    #     st.markdown("<div class='fixed-header'>", unsafe_allow_html=True) # Marker for sticky

    #     st.markdown("<div class='header-container'>", unsafe_allow_html=True)  # Container for the title and refresh button
    #     title_col, refresh_col = st.columns([4, 1])
    #     with title_col:
    #         st.markdown("<h2 style='margin-bottom: 0;'>💼 Track Applications</h2>", unsafe_allow_html=True)
    #     with refresh_col:
    #         st.markdown("<div style='margin-top: 22px;'></div>", unsafe_allow_html=True)
    #         refresh = st.button("Refresh", key="refresh_jobs", help="Refresh applications")
    #     st.markdown("</div>", unsafe_allow_html=True)  # Close the header container

    #     st.markdown("</div>", unsafe_allow_html=True)

    title_col, refresh_col = st.columns([4, 1])
    with title_col:
        # Title (align properly with button if needed)
        st.markdown("<h2 style='margin-bottom: 0;'>💼 Track Applications</h2>", unsafe_allow_html=True)
    with refresh_col:
        st.markdown("<div style='margin-top: 22px;'></div>", unsafe_allow_html=True)
        refresh = st.button("Refresh", key="refresh_jobs", help="Refresh applications")

    # Fetch data on first load or if refresh button is clicked
    if "job_data" not in st.session_state or refresh:
        st.session_state.job_data = fetch_jobs()

    jobs = st.session_state.job_data

    if not jobs:
        st.warning("No job listings available or error fetching data.")
        return

    domain_colors = [
        "#2e6f9a", "#6a1b9a", "#d84315", "#00897b", "#5e35b1", "#ef6c00",
        "#3949ab", "#00acc1", "#8e24aa", "#7cb342", "#c62828"
    ]
    domain_color_map = {}

    for i, job in enumerate(jobs):
        with st.container():
            job_col, recruiter_col = st.columns([8, 3])
            with job_col:
                job_title = job.get('job_title', 'No Title')
                company = job.get('company', 'No Company')
                domain = job.get('domain') or ""
                linkedin_url = job.get('linkedin_url', '#')
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
                                "{domain}"
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(f"📍 **Location:** {job.get('location', 'N/A')} {salary_display}")
                st.markdown(f"📝 **Description:** {job.get('description', 'No description available.')}")

            with recruiter_col:
                recruiters = job.get("_contacts", [])
                initials_color_map = {}
                if not recruiters:
                    st.write("No recruiters available.")
                else:
                    for idx, recruiter in enumerate(recruiters[:3]):
                        name = recruiter.get('name') if recruiter.get('name') and len(recruiter.get('name')) <= 15 else recruiter.get('short_name')
                        initials = ''.join([part[0] for part in recruiter.get('name', 'NA').split()[:2]]).upper()
                        title = recruiter.get('title') or "title unknown"
                        top_margin = "40px" if idx == 0 else "0px"
                        if initials not in initials_color_map:
                            initials_color_map[initials] = domain_colors[len(initials_color_map) % len(domain_colors)]

                        initials_color = initials_color_map[initials]
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
                                        background-color: {initials_color};
                                        border-radius: 50%;
                                        min-width: 30px;
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
                                            {title}
                                        </div>
                                    </div>
                                </div>
                            </a>
                            """,
                            unsafe_allow_html=True
                        )
        if i < len(jobs) - 1:
            st.markdown("---")
