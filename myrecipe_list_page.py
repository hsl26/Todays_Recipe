import streamlit as st
import user_db as db
from streamlit_cookies_controller import CookieController
import time

from user_db import *

def navigation_button():
    st.markdown("""
    <style>
        div[data-testid="column"] {
            display: flex;
            align-items: center;
        }
        div[data-testid="column"]:nth-child(2) {
            justify-content: flex-end;
        }
    </style>
    """, unsafe_allow_html=True)
    cols = st.columns([1,1]) 
    with cols[0]:
        st.markdown("## 내 레시피")
    with cols[1]:
        if st.button('이전으로 돌아가기'):
            st.session_state.page = 'mypage'
            st.rerun()

def display_my_recipe_list():
    st.markdown("""
    <style>
        div[data-testid="column"] {
            display: flex;
            align-items: center;
        }
        div[data-testid="column"]:nth-child(2) {
            justify-content: flex-end;
        }
    </style>
    """, unsafe_allow_html=True)
    cookies = CookieController()
    user_id = cookies.get('user_id')

    food_list = get_users_all_food(user_id)
    
    
    navigation_button()
    st.divider()
    for idx, rec_food in enumerate(food_list, start=1):
        food = food_list[idx-1]
        cols = st.columns([5, 3, 1]) 
        with cols[0]:
            st.markdown(f"### {idx}. {rec_food}")
        with cols[1]:
            if st.button("저장된 레시피 보러가기", key=idx):
                st.session_state.page = 'myrecipe_view'
                st.session_state.my_food_name = rec_food
                st.rerun() 
        with cols[2]:
            if st.button("삭제", key=(user_id,food)):
                db.remove_recipe(user_id, food) 
                st.rerun()
        st.divider()
        