import streamlit as st
from ai_setting import get_openai_client, create_thread, create_message, get_message, get_history_message
from db_setting import check_user_name, sign_up, check_user, save_thread_id, check_user_thread


def user_info_form_callback(user_name, password):
    # 提交数据到数据库
    if st.session_state.user_sign_type == "sign_in":
        res = check_user(user_name, password)
        if res:
            st.info("登录成功")
            return True
        else:
            st.info("用户名或密码不正确，请修改之后再登录")
            return False

    else:
        # 检查用户名是否具有唯一性
        res = check_user_name(user_name)
        if not res:
            # 插入数据
            sign_up(user_name, password)
            return True
        else:
            st.info("用户名已被占用，请修改之后再注册")
            return False


def user_sign_section():
    # 登录页面
    with st.form(key="user_info_form"):
        user_name = st.text_input("用户名", max_chars=6, key="user_name")
        password = st.text_input("密码", max_chars=12, key="password")

        if st.session_state.user_sign_type == "sign_in":
            submitted = st.form_submit_button("登录")
        else:
            submitted = st.form_submit_button("注册")

        if submitted:
            if user_name and password:
                sign_res = user_info_form_callback(user_name, password)
                if sign_res:
                    st.session_state.name = user_name
                    st.rerun()
            else:
                st.info("用户名、密码不能为空,请修改之后重试")


def click_sign_in():
    st.session_state.user_sign_type = "sign_in"


def click_sign_up():
    st.session_state.user_sign_type = "sign_up"


def app():
    st.title("时间管理大师")
    announce = st.caption('''
    :blue[🏆核心亮点：] 融合备忘录、提醒事项、日历三项能力的贴心助理。
    
    :red[⚠️注意：] 对话历史记录与用户账号关联，首次使用请注册，已有账号请直接登录。:red[❗️❗️❗]
    ''')

    # 分界线
    divider = st.divider()

    if "name" not in st.session_state:
        st.session_state.name = ""

    if "user_sign_type" not in st.session_state:
        st.session_state.user_sign_type = ""

        col1, col2 = st.columns(2)
        with col1:
            st.button("登录", key="sign_in", on_click=click_sign_in)
        with col2:
            st.button("注册", key="sign_up", on_click=click_sign_up)

    elif st.session_state.user_sign_type and not st.session_state.name:
        user_sign_section()

    st.markdown("""
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                right: 10px;
                width: auto;
                background-color: transparent;
                text-align: right;
                padding-right: 10px;
                padding-bottom: 10px;
            }
        </style>
        <div class="footer">Made with 🧡 by hw of fc</div>
    """, unsafe_allow_html=True)

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = ''

    # 查询用户线程是否存在
    status, thread_id = check_user_thread(st.session_state.name)
    if status:
        st.session_state["thread_id"] = thread_id

    if st.session_state.user_sign_type and st.session_state.name:

        with st.sidebar:
            api_key = st.text_input('Your OpenAI API key:', 'sk-...')
            st.image("./static/cover.png")

            thread_btn = st.button("生成对话线程")

        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "OPENAI_API_KEY" not in st.session_state:
            st.session_state["OPENAI_API_KEY"] = ''
        if "init_info" not in st.session_state:
            st.session_state.init_info = ''
        if "OPENAI_API_KEY" not in st.session_state:
            st.session_state["OPENAI_API_KEY"] = ''
        if "openai_client" not in st.session_state:
            st.session_state["openai_client"] = ''
        if "history" not in st.session_state:
            st.session_state["history"] = 0

        if thread_btn:
            if api_key and api_key.startswith("sk-") and api_key != "sk-...":
                announce.empty()
                divider.empty()

                st.session_state["OPENAI_API_KEY"] = api_key
                client = get_openai_client(api_key=api_key)
                st.session_state["openai_client"] = client

                if not st.session_state["thread_id"]:
                    with st.spinner('Wait for it...'):
                        thread_id = create_thread(client)
                        save_thread_id(st.session_state.name, thread_id)
                    st.session_state["thread_id"] = thread_id

                st.info("对话线程已开启，现在请在下方的方框内输入你的计划吧")

            else:
                announce.empty()
                divider.empty()
                st.warning = st.write("请输入正确的API Key令牌")

        if st.session_state["thread_id"] and st.session_state["openai_client"] and not st.session_state["history"]:
            # st.rerun()
            announce.empty()
            divider.empty()

            # 展示历史记录
            result = get_history_message(st.session_state["openai_client"], st.session_state["thread_id"])
            st.session_state["history"] = 1

            for r in result:
                st.session_state.messages.append(r)
                with st.chat_message(r["role"]):
                    st.markdown(r["content"])

        user_plan = st.chat_input("Please enter your plan...")

        if user_plan:
            if api_key and api_key.startswith("sk-") and api_key != "sk-...":
                st.session_state["OPENAI_API_KEY"] = api_key

            announce.empty()
            divider.empty()

            if not st.session_state["OPENAI_API_KEY"]:
                st.warning = st.write("请输入正确的API Key令牌")
            elif not st.session_state["thread_id"]:
                st.warning = st.write("请先点击「生成生成对话线程」")

            else:
                # Display chat messages from history on app rerun
                st.session_state.messages.append({"role": "user", "content": user_plan})

                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    run_id = create_message(st.session_state["openai_client"], st.session_state["thread_id"], user_plan)
                    response = get_message(st.session_state["openai_client"], st.session_state["thread_id"], run_id)
                    message_placeholder.markdown(response)

                st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    app()
