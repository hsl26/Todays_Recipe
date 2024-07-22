import streamlit as st
from recipe import recipe_page

def login_page():
    with st.form("lojin_form"):
        # 페이지 제목
        st.title("Today's Recipe")

        # 로그인 양식
        st.header('log-in')

        # 사용자 입력 필드
        id = st.text_input('id')
        password = st.text_input('password', type='password')

        # 로그인 버튼
        if st.form_submit_button('로그인'):
            # 예시로 간단한 사용자 검증 로직 (실제 프로젝트에서는 데이터베이스 검증 등을 사용)
            if id not in st.session_state.id_list:
                st.success("회원정보가 없습니다. 회원가입을 진행해주세요")
            else:
                correct_pw = st.session_state.pw_list[st.session_state.id_list.index(id)]
                if password == correct_pw:
                    st.success(f"환영합니다, {id}님!")
                    # 로그인 성공 후의 로직을 여기에 추가할 수 있습니다.
                    # 예를 들어, 사용자의 세션을 관리하는 코드 등.
                    st.session_state.page = 'recipe'
                    st.rerun()

                else:
                    st.error('잘못된 비밀번호입니다.')

        if st.form_submit_button('아직 회원이 아니신가요?'):
            st.session_state.page = 'signup'
            st.rerun()

def signup_page():
    def append_info(id, pw):
        st.session_state.id_list.append(id)
        st.session_state.pw_list.append(pw)

    if 'id_check' not in st.session_state:
        st.session_state.id_check = False

    def id_check():
        st.session_state.id_check = True

    # 페이지 제목
    st.title('회원가입 화면')

    # 회원가입 양식
    st.header('회원가입')

    # 사용자 입력 필드
    id = st.text_input('id')

    if st.button('아이디 중복 확인'):
        if id not in st.session_state.id_list:
            id_check()
            st.success("사용 가능한 아이디 입니다.")
        else:
            st.error("사용 불가능한 아이디 입니다. 다시 입력해주세요")

    password = st.text_input('pw', type='password')
    email = st.text_input('e-mail')
    fullname = st.text_input('name')

    # 제출 버튼
    if st.button('회원가입'):
        if id and password and email and fullname and st.session_state.id_check:
            # 여기서 실제 회원가입 로직을 추가할 수 있습니다.
            # 예를 들어, 데이터베이스에 사용자 정보를 저장하는 코드 등.
            append_info(id, password)
            st.session_state.page = 'complete'
            st.rerun()
        else:
            st.error('모든 필드를 입력과 아이디 중복확인을 마쳐주세요.')

    if st.button('로그인으로 돌아가기'):
        st.session_state.page = 'login'
        st.rerun()

def complete_signup_page(id):
    with st.form("complete_form"):
        st.subheader(f'🎉{id}님, 회원가입을 환영합니다🎉')
        st.subheader('서비스를 이용하시려면 로그인을 진행해 주세요.')
        
        if st.form_submit_button('로그인 하러 가기'):
            st.session_state.page = 'login'
            st.rerun()