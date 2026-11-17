# import streamlit as st
# from gigachat import GigaChat
# from gigachat.models import Chat, Messages, MessagesRole
# from utils.auth import authenticator
# import os


# SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "").strip()

# st.title("ISpeak")

# # 1. Инициализируем историю чата в session_state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # 2. Отрисовываем все сообщения из истории при каждом перезапуске страницы
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# def get_gigachat_response(history: list[dict]) -> str:
#     # Проверяем и при необходимости обновляем токен перед каждым запросом
#     if authenticator.is_expired():
#         authenticator.update()

#     # Преобразуем словари из session_state в типизированные объекты Messages
#     giga_messages = [
#         Messages(
#             role=MessagesRole.USER if msg["role"] == "user" else MessagesRole.ASSISTANT,
#             content=msg["content"],
#         )
#         for msg in history
#     ]

#     with GigaChat(
#         access_token=authenticator.api_token,
#         verify_ssl_certs=False,
#         model="GigaChat-3-Ultra",
#     ) as giga:
#         response = giga.chat(Chat(messages=giga_messages))
#         return response.choices[0].message.content


# # 3. Обрабатываем новый ввод пользователя
# if prompt := st.chat_input("Введите сообщение..."):
#     # Показываем и сохраняем сообщение пользователя
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Получаем и отображаем ответ модели
#     with st.chat_message("assistant"):
#         with st.spinner("Генерация ответа..."):
#             try:
#                 reply = get_gigachat_response(st.session_state.messages)
#                 st.markdown(reply)
#                 # Сохраняем ответ в историю только после успешного получения
#                 st.session_state.messages.append({"role": "assistant", "content": reply})
#             except Exception as e:
#                 st.error(f"Ошибка при обращении к GigaChat API: {e}")

# import os
# import streamlit as st
# from dotenv import load_dotenv
# from gigachat import GigaChat
# from gigachat.models import Chat, Messages, MessagesRole
# from utils.auth import authenticator

# # Явно загружаем переменные из .env (безопасно вызывать повторно, даже если это уже делает utils.auth)
# load_dotenv()
# SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "").strip()

# st.title("ISpeak")

# # 1. Инициализируем историю чата в session_state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # 2. Отрисовываем только сообщения пользователя и ассистента
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# def get_gigachat_response(history: list[dict]) -> str:
#     if authenticator.is_expired():
#         authenticator.update()

#     giga_messages = []

#     # Добавляем системный промпт в начало диалога, если он задан в .env
#     if SYSTEM_PROMPT:
#         giga_messages.append(
#             Messages(role=MessagesRole.SYSTEM, content=SYSTEM_PROMPT)
#         )

#     # Добавляем историю переписки
#     giga_messages.extend(
#         Messages(
#             role=MessagesRole.USER if msg["role"] == "user" else MessagesRole.ASSISTANT,
#             content=msg["content"],
#         )
#         for msg in history
#     )

#     with GigaChat(
#         access_token=authenticator.api_token,
#         verify_ssl_certs=False,
#         model="GigaChat-3-Ultra",
#     ) as giga:
#         response = giga.chat(Chat(messages=giga_messages))
#         return response.choices[0].message.content


# # 3. Обрабатываем новый ввод пользователя
# if prompt := st.chat_input("Введите сообщение..."):
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("assistant"):
#         with st.spinner("Генерация ответа..."):
#             try:
#                 reply = get_gigachat_response(st.session_state.messages)
#                 st.markdown(reply)
#                 st.session_state.messages.append({"role": "assistant", "content": reply})
#             except Exception as e:
#                 st.error(f"Ошибка при обращении к GigaChat API: {e}")

import os
import streamlit as st
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from utils.auth import authenticator

load_dotenv()
SYSTEM_PROMPT1 = os.getenv("SYSTEM_PROMPT1", "").strip()
SYSTEM_PROMPT2 = os.getenv("SYSTEM_PROMPT2", "").strip()

# Шапка приложения: название слева, переключатель режимов справа на одном уровне
col_title, col_mode = st.columns([3, 2], vertical_alignment="center")
with col_title:
    st.title("ISpeak")
with col_mode:
    selected_mode = st.radio(
        "Режим общения",
        options=["Normal", "Mode Cockney"],
        horizontal=True,
        label_visibility="collapsed",
    )

# Выбираем активный системный промпт в зависимости от переключателя
active_system_prompt = (
    SYSTEM_PROMPT1 if selected_mode == "Normal" else SYSTEM_PROMPT2
)

# 1. Инициализируем историю чата в session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Отрисовываем историю сообщений
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def get_gigachat_response(history: list[dict], system_prompt: str) -> str:
    if authenticator.is_expired():
        authenticator.update()

    giga_messages = []

    if system_prompt:
        giga_messages.append(
            Messages(role=MessagesRole.SYSTEM, content=system_prompt)
        )

    giga_messages.extend(
        Messages(
            role=MessagesRole.USER if msg["role"] == "user" else MessagesRole.ASSISTANT,
            content=msg["content"],
        )
        for msg in history
    )

    with GigaChat(
        access_token=authenticator.api_token,
        verify_ssl_certs=False,
        model="GigaChat-3-Ultra",
    ) as giga:
        response = giga.chat(Chat(messages=giga_messages))
        return response.choices[0].message.content


# 3. Обрабатываем ввод пользователя
if prompt := st.chat_input("Введите сообщение..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Генерация ответа..."):
            try:
                reply = get_gigachat_response(
                    st.session_state.messages,
                    active_system_prompt,
                )
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Ошибка при обращении к GigaChat API: {e}")