import streamlit as st
from streamlit_cookies_controller import CookieController
from login_signup import login_page
from login_signup import signup_page
from login_signup import complete_signup_page
from recipe import recipe_page
from user_db import get_user_name
# ex_id_list = ["ksj020919", "abcd1234", "efgh5678", "1234"]
# ex_pw_list = ["kys101014!", "ABCD1234!", "EFGH5678!", "1234"]

cookies = CookieController()
if cookies.get('logged_in') == 'True':
    logged_in=st.session_state.logged_in = True
else:
    logged_in=st.session_state.logged_in = False
st.session_state.user_name = get_user_name(cookies.get('user_id'))

if cookies.get("logged_in") == 'True':
    st.session_state.page = 'recipe'
elif 'page' not in st.session_state:
    st.session_state.page = 'login'

# if 'id_list' not in st.session_state:
#     st.session_state.id_list = ex_id_list
# if 'pw_list' not in st.session_state:    
#     st.session_state.pw_list = ex_pw_list
if st.session_state.page == 'login':
    st.session_state.user_name = None
# 현재 페이지 상태에 따라 화면 표시
if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'signup':
    signup_page()
elif st.session_state.page == 'recipe':
    recipe_page()
elif st.session_state.page == 'complete':
    complete_signup_page()