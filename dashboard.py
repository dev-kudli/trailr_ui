import streamlit as st

def show_dashboard():
    # Set the title
    st.markdown("## 📊 Dashboard")

    # Create two columns for the dashboard layout
    col1, col2 = st.columns(2)

    # Cold Emails Sent Card
    with col1:
        st.metric(label="Cold Emails Sent", value=50, delta=None, delta_color="normal")
    
    # Applications Applied Card
    with col2:
        st.metric(label="Applications Applied", value=100, delta=None, delta_color="normal")
