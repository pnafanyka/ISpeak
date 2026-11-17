import streamlit as st
import os

x = os.detenv("a")

st.title("ELIZA")

# Инициализируем историю чата, если её ещё нет
if "messages" not in st.session_state:
    st.session_state.messages = []

# Показываем все старые сообщения при каждом запуске страницы
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Реагируем на ввод пользователя
if prompt := st.chat_input("What is up?"):
    # Показываем сообщение пользователя
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Сохраняем сообщение пользователя в историю
    st.session_state.messages.append({"role": "user", "content": prompt})

    if prompt == 'hi' or prompt == 'hello':
        response = prompt + '!'

    elif 'sad' in prompt:
        response = 'Oh, that’s awful. What happened?'

    elif 'always' in prompt:
        response = 'Can you give a specific example?'

    else: 
        response = 'I’m sorry, I can’t help you...'

    # Показываем ответ бота
    with st.chat_message("ai"):
        st.markdown(response)
    
    # Сохраняем ответ бота в историю
    st.session_state.messages.append({"role": "ai", "content": response})






from gigachat import GigaChat

# Укажите ключ авторизации, полученный в личном кабинете, в интерфейсе проекта GigaChat API
with GigaChat(credentials="ваш_ключ_авторизации") as client:
    response = client.chat.create("Какие факторы влияют на стоимость страховки на дом?")
    print(response.messages[0].content[0].text)
