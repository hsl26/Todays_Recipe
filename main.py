import streamlit as st
from login_signup import login_page
from login_signup import signup_page
from login_signup import complete_signup_page
from recipe import recipe_page

ex_id_list = ["ksj020919", "abcd1234", "efgh5678", "1234"]
ex_pw_list = ["kys101014!", "ABCD1234!", "EFGH5678!", "1234"]

if 'page' not in st.session_state:
    st.session_state.page = 'login'

if 'id_list' not in st.session_state:
    st.session_state.id_list = ex_id_list
if 'pw_list' not in st.session_state:    
    st.session_state.pw_list = ex_pw_list

# 현재 페이지 상태에 따라 화면 표시
if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'signup':
    signup_page()
elif st.session_state.page == 'recipe':
    recipe_page()
elif st.session_state.page == 'complete':
    complete_signup_page(st.session_state.id_list[-1])