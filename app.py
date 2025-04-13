import streamlit as st
import requests
from dashboard import show_dashboard
from applications import show_applications

st.set_page_config(page_title="Applications", layout="centered")

pg = st.navigation([st.Page(show_dashboard, title="📊 Home"), st.Page(show_applications, title="💼 Applications")])
pg.run()