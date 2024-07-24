import streamlit as st
import streamlit.components.v1 as components
from streamlit_cookies_controller import CookieController

import user_db as db

def navigation_button():
    cols = st.columns([1]) 
    with cols[0]:
        if st.button("목록으로 돌아가기"):
            st.session_state.page = 'myrecipe_list'
            st.rerun()

def display_my_recipe_view():
    recipe_info = """
                ### 계란말이 레시피

                #### 재료
                - 계란 4개
                - 당근 1/4개
                - 양파 1/4개
                - 대파 1/2대
                - 소금 약간
                - 식용유 약간

                #### 요리 순서
                1. 당근, 양파, 대파를 잘게 다져줍니다.
                2. 계란을 그릇에 깨서 넣고 잘 풀어줍니다.
                3. 풀어놓은 계란에 다진 당근, 양파, 대파를 넣고 소금을 약간 뿌려 잘 섞어줍니다.
                4. 중불로 예열한 프라이팬에 식용유를 약간 두르고 계란물을 팬에 얇게 부어줍니다.
                5. 계란물이 반쯤 익으면 한쪽 끝에서부터 계란을 말아줍니다.
                6. 계란을 말아가면서 프라이팬의 남은 공간에 다시 계란물을 조금씩 부어가며 계속 말아줍니다.
                7. 계란말이가 완성되면 도마에 올려 한 김 식힌 후 먹기 좋은 크기로 썰어줍니다.

                즐겁게 요리하세요!
                """
    
    st.markdown(f"{recipe_info}")

    navigation_button()



