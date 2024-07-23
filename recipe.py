import streamlit as st
import streamlit.components.v1 as components
from streamlit_cookies_controller import CookieController
import time
import re

import user_db as db
from llm import llm_recipe



def navigation_button():
    cols = st.columns([3, 1, 1]) 
    with cols[0]:
        if st.button("홈으로 돌아가기"):
            st.session_state.page = 'main'
            st.rerun()
    with cols[1]:
        if st.button("마이페이지"):
            st.session_state.page = 'mypage'
            st.rerun()
    with cols[2]:
        if st.button('로그아웃'):
            cookies = CookieController()
            cookies.set('logged_in', 'False')
            cookies.set('user_id', '')
            st.success('로그아웃 되었습니다.')
            st.session_state.page = 'login'
            time.sleep(1)
            st.rerun()


def recipe_page(index):
    cookies = CookieController()
    user_id = cookies.get("user_id")

    # HTML 스타일을 사용한 추가 재료 박스
    def additional_ingredients(ingred, link, img_url, description):
        st.markdown(f"""
                    <div style="padding: 10px; margin-top: 10px; border-bottom: 1px solid #ddd;">
                        <div style="display: flex; align-items: center;">
                            <img src="{img_url}" alt="preview" style="width: 100px; height: 100px; object-fit: cover; margin-right: 10px;">
                            <div>
                                <ul>
                                    <p style="font-weight: 700; font-size: 20px;">{ingred}</p>
                                    <p>{description}</p>
                                    <p><a href="{link}" target="_blank" style="color: gray; font-style: italic;">{ingred} 구매 링크 바로가기</a></p>
                             </ul>
                            </div>
                        </div>
                    </div>  
                    """, unsafe_allow_html=True)
    
    navigation_button()


    food_name = st.session_state.get("food_name", "정보가 없습니다.")
    
    # llm에 해당 음식 이름 전달 및 결과 반환
    response = llm_recipe.GetInformation(food_name)
    recipe_info = re.sub(r'\[.*\]', '', response)
    st.markdown(f"{recipe_info}")
    
    match = re.search(r'\[.*?\]', response)
    if match:
        ingredient_list = match.group()
        ingredient_list = ingredient_list.strip('[]').replace('"', '').split(', ')
    
    st.header('추가구매 추천 재료')
    
    if ingredient_list:
        need_ingredient = set(ingredient_list)
    else:
        need_ingredient = set([])
        
    have_ingredient = set(db.get_ingredient(user_id))
    add_ingredient = need_ingredient - have_ingredient
    
    if add_ingredient:
        for ingred in list(add_ingredient):
            purchase_link = f"https://www.kurly.com/search?sword={ingred}"
            img_url = "https://res.kurly.com/images/marketkurly/logo/logo_sns_marketkurly.jpg"  # 예시 이미지 URL을 적절히 변경
            description = "마켓 컬리에서 찾은 관련 상품입니다."
            additional_ingredients(ingred, purchase_link, img_url, description)