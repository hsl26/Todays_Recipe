import streamlit as st
import user_db as db
from streamlit_cookies_controller import CookieController
import time


def navigation_button():
    cols = st.columns([1]) 
    with cols[0]:
        if st.button('이전으로 돌아가기'):
            st.session_state.page = 'mypage'
            st.rerun()

tmp_save_list = ['딸기 케이크', '메론 케이크']
    
def display_my_recipe_list():
    st.markdown("## 내 레시피")
    navigation_button()
    st.divider()
    for idx, rec_food in enumerate(tmp_save_list, start=1):
        cols = st.columns([2, 1]) 
        with cols[0]:
            st.markdown(f"**{idx}. {rec_food}**")
        with cols[1]:
            if st.button("저장된 레시피 보러가기", key=idx):
                st.session_state.page = 'myrecipe_view'
                st.rerun() 
        st.divider()
        