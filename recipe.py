import streamlit as st
from streamlit_cookies_controller import CookieController
import streamlit.components.v1 as components
import time
from user_db import get_user_name

def recipe_page():
    cookies = CookieController()
    st.write(f'안녕하세요 {get_user_name(cookies.get("user_id"))}님')

    if st.button('로그아웃'):
        
        cookies.set('logged_in', 'False')
        cookies.set('user_id', '')
        st.success('로그아웃 되었습니다.')
        st.session_state.page = 'login'
        time.sleep(1)
        st.rerun()

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
                                    <p><a href="{link}" target="_blank" style="color: white; font-style: italic;">{ingred} 구매 링크 바로가기</a></p>
                             </ul>
                            </div>
                        </div>
                    </div>  
                    """, unsafe_allow_html=True)
        
        
    need_ingredient = set(['계란', '소금', '밥', '대파', '당근', '올리브 오일'])
    have_ingredient = set(['계란', '소금', '올리브 오일', '밥', '양배추', '딸기'])
    add_ingredient = need_ingredient - have_ingredient

    st.title('메뉴 이름')

    st.header('재료')
    st.header('레시피')
    st.header('추가구매 추천 재료')
    if add_ingredient:
        for ingred in list(add_ingredient):
            purchase_link = f"https://www.kurly.com/search?sword={ingred}"
            img_url = "https://res.kurly.com/images/marketkurly/logo/logo_sns_marketkurly.jpg"  # 예시 이미지 URL을 적절히 변경
            description = "마켓 컬리에서 찾은 관련 상품입니다."
            additional_ingredients(ingred, purchase_link, img_url, description)