import streamlit as st

from streamlit_cookies_controller import CookieController

from login_signup import login_page
from login_signup import signup_page
from login_signup import complete_signup_page
from recipe import recipe_page

from main_page import display_main_page
from mypage import display_mypage

from user_db import get_user_name

# ex_id_list = ["ksj020919", "abcd1234", "efgh5678", "1234", "1"]
# ex_pw_list = ["kys101014!", "ABCD1234!", "EFGH5678!", "1234", "1"]

st.title("레시피 추천 서비스")

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

if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_pw' not in st.session_state:
    st.session_state.user_pw = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

if st.session_state.page == 'login':
    st.session_state.user_name = None

# 현재 페이지 상태에 따라 화면 표시
if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'signup':
    signup_page()
elif st.session_state.page == 'recipe' and st.session_state.selected_index is not None:
    recipe_page(st.session_state.selected_index)
elif st.session_state.page == 'complete':
    complete_signup_page(st.session_state.id_list[-1])
elif st.session_state.page == 'main':
    display_main_page()
elif st.session_state.page == 'mypage':
    display_mypage()
    
