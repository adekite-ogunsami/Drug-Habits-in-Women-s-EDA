import streamlit as st
from pages import _home, _documentation
from data_viz import show_data_visualization
from predictive_model import show_predictive_page

st.set_page_config(
    page_title="Substance Abuse Amongst Women",
    layout="wide",
    initial_sidebar_state="collapsed"
)


if 'page' not in st.session_state:
    st.session_state.page = 'home'

PAGES = {
    "Home": _home.show_home_page,
    "Descriptive Analysis": show_data_visualization,
    "Predictive Analysis": show_predictive_page,
    "Documentation": _documentation.show_documentation_page
}


if st.session_state.page == 'home':
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.sidebar.empty()

    st.sidebar.title("Navigation")
    current_page_display_name = ""
    if st.session_state.page == 'statistical':
        current_page_display_name = "Descriptive Analysis"
    elif st.session_state.page == 'predictive':
        current_page_display_name = "Predictive Analysis"
    elif st.session_state.page == 'documentation':
        current_page_display_name = "Documentation"
    elif st.session_state.page == 'home':
        current_page_display_name = "Home"

    try:
        selected_page_index = list(PAGES.keys()).index(current_page_display_name)
    except ValueError:
        selected_page_index = 0
    selected_page = st.sidebar.radio(
        "Go to",
        list(PAGES.keys()),
        index=selected_page_index
    )

    if selected_page == "Home":
        st.session_state.page = 'home'
    elif selected_page == "Descriptive Analysis":
        st.session_state.page = 'statistical'
    elif selected_page == "Predictive Analysis":
        st.session_state.page = 'predictive'
    elif selected_page == "Documentation":
        st.session_state.page = 'documentation'


if st.session_state.page == 'home':
    _home.show_home_page()
elif st.session_state.page == 'statistical':
    show_data_visualization()
elif st.session_state.page == 'predictive':
    show_predictive_page()
elif st.session_state.page == 'documentation':
    _documentation.show_documentation_page()
