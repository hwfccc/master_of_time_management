import streamlit as st
from ai_setting import get_openai_client, create_thread, create_message, get_message


def app():
    st.title("时间管理大师 v0.1.0")
    announce = st.caption('''
    :blue[🏆核心亮点：] 融合备忘录、提醒事项、日历三项能力的贴心助理。
    ''')

    # 分界线
    divider = st.divider()
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

    with st.sidebar:
        api_key = st.text_input('Your OpenAI API key:', 'sk-...')
        st.image("./cover.png")

        btn = st.button("生成对话线程")

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
    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = ''

    if btn:
        if api_key and api_key.startswith("sk-") and api_key != "sk-...":
            announce.empty()
            divider.empty()
            # st.warning.empty()

            st.session_state["OPENAI_API_KEY"] = api_key

            client = get_openai_client(api_key=api_key)
            thread_id = create_thread(client)
            st.session_state["thread_id"] = thread_id
            st.session_state["openai_client"] = client

            st.write('对话线程已开启，现在请在下方的方框内输入你的计划吧')

        else:
            announce.empty()
            divider.empty()
            st.warning = st.write("请输入正确的API Key令牌")

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
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"][0])

            # Display new user question.
            with st.chat_message("user"):
                st.markdown(user_plan)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                run_id = create_message(st.session_state["openai_client"], st.session_state["thread_id"], user_plan)

                response = get_message(st.session_state["openai_client"], st.session_state["thread_id"], run_id)
                full_response += response
                message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": [full_response, 1]})


if __name__ == "__main__":
    app()