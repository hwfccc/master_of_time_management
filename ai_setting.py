import time
import streamlit as st
from openai import OpenAI

assistant_id = st.secrets["assistant_id"]


def get_openai_client(api_key):
    """
    获取openai client
    :param api_key:
    :return:
    """

    return OpenAI(api_key=api_key)


def create_thread(openai_client):
    """
    Create a thread.
    :param openai_client:
    :return:
    """

    thread = openai_client.beta.threads.create()
    return thread.id


def create_message(openai_client, thread_id, content):
    """
    Create a thread.
    :param openai_client:
    :param thread_id:
    :param content:
    :return:
    """

    message = openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

    run = openai_client.beta.threads.runs.create(
      thread_id=thread_id,
      assistant_id=assistant_id
    )

    return run.id


def get_history_message(openai_client, thread_id):

    message_res = openai_client.beta.threads.messages.list(thread_id)

    history_message = list()

    for info in message_res:
        history_message.append((info.role, info.content[0].text.value, info.created_at))

    return [{"role": i[0], "content": i[1]} for i in sorted(history_message, key=lambda x: x[2])]


def get_message(openai_client, thread_id, run_id):

    while True:
        run = openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

        print(run.status)

        if run.status == "completed":
            messages = openai_client.beta.threads.messages.list(
                thread_id=thread_id
            )

            return messages.data[0].content[0].text.value

        else:
            time.sleep(2)
