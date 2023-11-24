import time
from openai import OpenAI

assistant_id = "asst_VwefqfzpjDmlQ7tMVbvxi8mY"


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

            print(messages)
            print(messages.data)
            return messages.data[0].content[0].text.value

        else:
            time.sleep(2)




# from openai import OpenAI
#
#
# client = OpenAI(api_key="")
#
# assistant = client.beta.assistants.create(
#     name="master of time management",
#     instructions="""
# # Role：时间管理大师
# ## Background：辅助事务繁杂的创业者，对众多信息进行整理，并辅助进行日程编排和回忆事项
# - 基于用户需求和所提供的大语言模型名称来进行优化以及中英文翻译，以实现更加符合特定语言模型特性的prompt来帮助用户提升语言模型的性能和实现特定的目标。
# - 根据用户选项来决定将要进行的任务
# ## Profile：
# - Author: 亮亮
# - Version: 1.0
# - Language: 中文
# - Description: 融合备忘录、提醒事项、日历三项能力的贴心助理
# ## Skills:
# - 时间管理大师
# - 能快速理解一个科技创业者的工作和生活日常事项
# - 能整理繁杂的事项，输出为清晰的表格
# ## Goals:
# - 理解{TaskType}中的每一项，并能够将用户输入的文本解析为其中的某个项，并记录
# - 通过用户输入的文本理解用户的目标
# ## Constrains:
# - 必须严格按照给定的格式输出。
# - 无论在任何情况下，不能跳出角色。
# - 任何情况下都只能对用户输入的文本进行整理，不需要针对用户输入的文本进行展开和回答
# - 不讲无意义的话或编造事实。
# ## TaskType
# - 灵感
# - 学习笔记
# - 待办
# - 日程
# - 提醒事项
# ## QuestionExample
# - 我今天有什么任务？
# - 我这周有哪些日程？
# - 我这个月有什么重要事项？
# - 帮我回顾近期的学习笔记
# ## Workflow:
# 1.理解用户输入的文本，并判断该内容为{TaskType}的哪一类，如果是符合其中任意一类，则只记录，并回复"已收录"
# 2.存储用户发送的文本在上下文中，并补充记录时间
# 3.如果用户输入的问题类似{QuestionExample}中的任何一项，则不是记录信息，而是对历史上下文中的文本进行分析并回答用户的问题。
# ## OutputFormat:
# markdown 的 TODO 和 表格
#     """,
#     tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
#     model="gpt-4-1106-preview"
# )

# import time
# from openai import OpenAI
#
#
# client = OpenAI(api_key="")


# assistant = client.beta.assistants.create(
#     name="Math Tutor",
#     instructions="You are a personal math tutor. Write and run code to answer math questions.",
#     tools=[{"type": "code_interpreter"}],
#     model="gpt-3.5-turbo-1106"
# )

# thread = client.beta.threads.create()
#
#
# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
# )


# run = client.beta.threads.runs.create(
#   thread_id=thread.id,
#   assistant_id=assistant.id
# )

# run = client.beta.threads.runs.create(
#   thread_id='thread_sdJZua7wXfo15Uwy4Kue561P',
#   assistant_id='asst_p8UKm6dXZjH7K5OOzOq07bHD'
# )

# run = client.beta.threads.runs.retrieve(
#   thread_id=thread.id,
#   run_id=run.id
# )


# run = client.beta.threads.runs.retrieve(
#   thread_id='thread_sdJZua7wXfo15Uwy4Kue561P',
#   run_id='run_bdp4qG2NsuXIy4joqpvlX0yS'
# )
#
# # messages = client.beta.threads.messages.list(
# #   thread_id=thread.id
# # )
#
# # print(assistant.id, thread.id, run.id)
#
#
# while run.status != "completed":
#     print(run.status)
#     time.sleep(2)
#
#     run = client.beta.threads.runs.retrieve(
#        thread_id=thread.id,
#        run_id=run.id
#     )
#
# messages = client.beta.threads.messages.list(
#  thread_id=thread.id
# )
#
# print(messages.data)
# print(messages.data[0].content[0].text.value)

