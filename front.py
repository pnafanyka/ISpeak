# import streamlit as st
# import os


# st.title("ELIZA")

# # Инициализируем историю чата, если её ещё нет
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Показываем все старые сообщения при каждом запуске страницы
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Реагируем на ввод пользователя
# if prompt := st.chat_input("What is up?"):
#     # Показываем сообщение пользователя
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     # Сохраняем сообщение пользователя в историю
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     if prompt == 'hi' or prompt == 'hello':
#         response = prompt + '!'

#     elif 'sad' in prompt:
#         response = 'Oh, that’s awful. What happened?'

#     elif 'always' in prompt:
#         response = 'Can you give a specific example?'

#     else: 
#         response = 'I’m sorry, I can’t help you...'

#     # Показываем ответ бота
#     with st.chat_message("ai"):
#         st.markdown(response)
    
#     # Сохраняем ответ бота в историю
#     st.session_state.messages.append({"role": "ai", "content": response})






# from gigachat import GigaChat

# # Укажите ключ авторизации, полученный в личном кабинете, в интерфейсе проекта GigaChat API
# with GigaChat(credentials="ваш_ключ_авторизации") as client:
#     response = client.chat.create("Какие факторы влияют на стоимость страховки на дом?")
#     print(response.messages[0].content[0].text)


import streamlit as st
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from utils.auth import authenticator

st.title("ISpeak")

# 1. Инициализируем историю чата в session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Отрисовываем все сообщения из истории при каждом перезапуске страницы
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def get_gigachat_response(history: list[dict]) -> str:
    # Проверяем и при необходимости обновляем токен перед каждым запросом
    if authenticator.is_expired():
        authenticator.update()

    # Преобразуем словари из session_state в типизированные объекты Messages
    giga_messages = [
        Messages(
            role=MessagesRole.USER if msg["role"] == "user" else MessagesRole.ASSISTANT,
            content=msg["content"],
        )
        for msg in history
    ]

    with GigaChat(
        access_token=authenticator.api_token,
        verify_ssl_certs=False,
        model="GigaChat-3-Ultra",
    ) as giga:
        response = giga.chat(Chat(messages=giga_messages))
        return response.choices[0].message.content


# 3. Обрабатываем новый ввод пользователя
if prompt := st.chat_input("Введите сообщение..."):
    # Показываем и сохраняем сообщение пользователя
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Получаем и отображаем ответ модели
    with st.chat_message("assistant"):
        with st.spinner("Генерация ответа..."):
            try:
                reply = get_gigachat_response(st.session_state.messages)
                st.markdown(reply)
                # Сохраняем ответ в историю только после успешного получения
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Ошибка при обращении к GigaChat API: {e}")