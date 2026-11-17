import os
import streamlit as st
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from utils.auth import authenticator

load_dotenv()
SYSTEM_PROMPT1 = os.getenv("SYSTEM_PROMPT1", "").strip()
SYSTEM_PROMPT2 = os.getenv("SYSTEM_PROMPT2", "").strip()

# Инициализируем историю чата
if "messages" not in st.session_state:
    st.session_state.messages = []


def clear_chat_history() -> None:
    """Полностью очищает историю переписки в session_state."""
    st.session_state.messages = []


# Верхняя панель: название, переключатель режимов и кнопка очистки на одном уровне
col_title, col_mode, col_clear = st.columns(
    [2.2, 2.5, 1.3], vertical_alignment="center"
)

with col_title:
    st.title("ISpeak")

with col_mode:
    selected_mode = st.radio(
        "Режим общения",
        options=["Normal", "Mode Cockney"],
        horizontal=True,
        label_visibility="collapsed",
        key="mode_selector",
        on_change=clear_chat_history,
    )

with col_clear:
    st.button(
        "Очистить чат",
        use_container_width=True,
        on_click=clear_chat_history,
    )

# Определяем системный промпт для активного режима
active_system_prompt = (
    SYSTEM_PROMPT1 if selected_mode == "Normal" else SYSTEM_PROMPT2
)

# Отрисовываем историю сообщений
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def get_gigachat_response(history: list[dict], system_prompt: str) -> str:
    if authenticator.is_expired():
        authenticator.update()

    giga_messages = []

    # Всегда передаём актуальный системный промпт выбранного режима первым сообщением
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


# Обработка нового сообщения пользователя
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
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )
            except Exception as e:
                st.error(f"Ошибка при обращении к GigaChat API: {e}")