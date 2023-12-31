import streamlit as st
from sqlalchemy import text
# Initialize connection.
conn = st.connection('mysql', type='sql')


def check_user_name(user_name):
    """
    检查用户名是否唯一
    :return:
    """

    result = conn.query('SELECT id from gpts_001_tm_user where user_name=:user_name;',
                        params={"user_name": user_name},
                        ttl=0)

    if result.empty:
        return False

    return True


def sign_up(user_name, password):
    """
    用户注册
    :return:
    """

    with conn.session as session:
        session.execute(
            text('insert into gpts_001_tm_user(user_name, password) values(:user_name, :password);'
                 ).params(user_name=user_name, password=password))
        session.commit()


def check_user(user_name, password):
    """
    检查用户名与密码
    :param user_name:
    :param password:
    :return:
    """

    result = conn.query('SELECT id from gpts_001_tm_user where user_name=:user_name and password=:password;',
                        params={"user_name": user_name, "password": password}, ttl=0)

    if result.empty:
        return False

    return True


def save_thread_id(user_name, thread_id):
    """
    保存用户的线程id
    :param user_name:
    :param thread_id:
    :return:
    """

    with conn.session as session:
        session.execute(
            text('insert into gpts_001_tm_user_thread(user_name, thread_id) values(:user_name, :thread_id);'
                 ).params(user_name=user_name, thread_id=thread_id))
        session.commit()


def check_user_thread(user_name):
    """
    检查用户名thread
    :param user_name:
    :return:
    """

    result = conn.query('SELECT thread_id from gpts_001_tm_user_thread where user_name=:user_name;',
                        params={"user_name": user_name}, ttl=0)

    if result.empty:
        return False, ""

    return True, result["thread_id"][0]

