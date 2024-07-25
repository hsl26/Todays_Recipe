import streamlit as st
import streamlit.components.v1 as components
from streamlit_cookies_controller import CookieController
import time
import re
from streamlit_modal import Modal
import user_db as db
from llm import llm_recipe


def navigation_button():
    st.session_state.add_db = False
    st.session_state.modal_col_0 = False
    st.session_state.modal_col_1 = False
    
    cols = st.columns([3.05, 0.9, 1.15]) 
    
    modal = Modal(
        "내 레시피에 추가", 
        key="My recipes",
        
        # Optional
        padding=20,    # default value
        max_width=550  # default value
    )
    
    with cols[0]:
        if st.button("홈으로 돌아가기"):
            st.session_state.page = 'main'
            st.session_state['response'] = None
            st.rerun()
    with cols[1]:
        if st.button("마이페이지"):
            st.session_state.page = 'mypage'
            st.session_state['response'] = None
            st.rerun()
    with cols[2]:
        open_modal = st.button("내 레시피에 추가")
        if open_modal:
            if db.check_exists(st.session_state.user_id, st.session_state.get("food_name", "정보가 없습니다.")):
                modal.open()
            else:
                st.session_state.add_db = True
                db.insert_recipe(st.session_state.user_id, st.session_state.get("food_name", "정보가 없습니다."), st.session_state['response'])
        if modal.is_open():
            with modal.container():
                st.markdown("**이미 존재하는 레시피 이름입니다.**")
                
                new_food_name = st.text_input("저장을 원하신다면 새 레시피 이름을 적어주세요.", st.session_state.get("food_name", "정보가 없습니다."))
                modal_col_0, modal_col_1  = st.columns([4.3,1]) 
                with modal_col_0:
                    if st.button("이름 변경해서 추가"):
                        # 이름 변경해서 추가 로직
                        db.insert_recipe(st.session_state.user_id, new_food_name, st.session_state['response'])
                        st.session_state.modal_col_0 = True
                        st.session_state.modal_col_1 = False
                        # st.success("이름 변경해서 추가되었습니다.")
                with modal_col_1:
                    if st.button("덮어쓰기"):   
                        # 덮어쓰기 로직
                        db.replace_recipe(st.session_state.user_id, st.session_state.get("food_name", "정보가 없습니다."), new_food_name, st.session_state['response'])
                        # st.success("덮어쓰기가 완료되었습니다.")
                        st.session_state.modal_col_0 = False
                        st.session_state.modal_col_1 = True
                if st.session_state.modal_col_0:
                    st.success("이름 변경해서 추가되었습니다.")
                if st.session_state.modal_col_1:
                    st.success("덮어쓰기가 완료되었습니다.")
    if st.session_state.add_db:
        st.success('내 레시피에 추가되었습니다.')
        st.session_state.add_db = False
                    

def recipe_page(index):
    
    cookies = CookieController()
    user_id = cookies.get("user_id")

    # HTML 스타일을 사용한 추가 재료 박스
    def additional_ingredients(ingred, link):
        st.markdown(f"""
                <div style="padding: 5px; margin-top: 5px">
                    <ul style="list-style-type: disc; margin: 0; padding-left: 20px; align-items: center;">
                        <li>
                            <a href="{link}" 
                                    style="color: black; 
                                    text-decoration: none;
                                    font-size: 20px; 
                                    font-weight: bold;">
                                {ingred}
                            </a>
                        </li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    
    navigation_button()
    
    food_name = st.session_state.get("food_name", "정보가 없습니다.")
    
    if 'response' not in st.session_state:
        st.session_state['response'] = None
        
    if st.session_state['response'] is None:
        response = llm_recipe.GetInformation(food_name)
        st.session_state['response'] = response
    else:
        response = st.session_state['response']
    
    recipe_info = re.sub(r'\[.*\]', '', response)
    st.markdown(f"{recipe_info}")
    
    match = re.search(r'\[.*?\]', response)
    ingredient_list = []
    if match:
        ingredient_list = match.group()
        ingredient_list = ingredient_list.strip('[]').replace('"', '').split(', ')
    
    st.header('추가구매 추천 재료')
    
    # if ingredient_list:
    need_ingredient = set(ingredient_list)
    # else:
    #     need_ingredient = set([])
        
    have_ingredient = set(db.get_ingredient(user_id))
    add_ingredient = need_ingredient - have_ingredient
    
    if add_ingredient:
        #마켓컬리 로고사진과 문구 출력
        img_url = "https://res.kurly.com/images/marketkurly/logo/logo_sns_marketkurly.jpg"
        st.markdown(f"""
            <div style="padding: 10px; margin-top: 10px; border-bottom: 1px solid #ddd;">
                <div style="display: flex; flex-direction: column;">
                    <img src="{img_url}" alt="preview" style="width: 100px; height: 100px; object-fit: cover; margin-bottom: 10px;">
                </div>
                <div style="text-align: left; font-size: 18px; padding: 1px;">
                    <span>{"상품명을 누르시면 마켓컬리 구매 링크로 연결됩니다."}</span>
                </div>
            </div>  
            """, unsafe_allow_html=True)
        
        for ingred in list(add_ingredient):
            #추가 재료 품목을 링크로 출력
            purchase_link = f"https://www.kurly.com/search?sword={ingred}"
            additional_ingredients(ingred, purchase_link)
