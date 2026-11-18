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

# import os
# import streamlit as st
# from dotenv import load_dotenv
# from gigachat import GigaChat
# from gigachat.models import Chat, Messages, MessagesRole
# from utils.auth import authenticator

# load_dotenv()
# SYSTEM_PROMPT1 = os.getenv("SYSTEM_PROMPT1", "").strip()
# SYSTEM_PROMPT2 = os.getenv("SYSTEM_PROMPT2", "").strip()

# # Шапка приложения: название слева, переключатель режимов справа на одном уровне
# col_title, col_mode = st.columns([3, 2], vertical_alignment="center")
# with col_title:
#     st.title("ISpeak")
# with col_mode:
#     selected_mode = st.radio(
#         "Режим общения",
#         options=["Normal", "Mode Cockney"],
#         horizontal=True,
#         label_visibility="collapsed",
#     )

# # Выбираем активный системный промпт в зависимости от переключателя
# active_system_prompt = (
#     SYSTEM_PROMPT1 if selected_mode == "Normal" else SYSTEM_PROMPT2
# )

# # 1. Инициализируем историю чата в session_state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # 2. Отрисовываем историю сообщений
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# def get_gigachat_response(history: list[dict], system_prompt: str) -> str:
#     if authenticator.is_expired():
#         authenticator.update()

#     giga_messages = []

#     if system_prompt:
#         giga_messages.append(
#             Messages(role=MessagesRole.SYSTEM, content=system_prompt)
#         )

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


# # 3. Обрабатываем ввод пользователя
# if prompt := st.chat_input("Введите сообщение..."):
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("assistant"):
#         with st.spinner("Генерация ответа..."):
#             try:
#                 reply = get_gigachat_response(
#                     st.session_state.messages,
#                     active_system_prompt,
#                 )
#                 st.markdown(reply)
#                 st.session_state.messages.append({"role": "assistant", "content": reply})
#             except Exception as e:
#                 st.error(f"Ошибка при обращении к GigaChat API: {e}")


# import os
# import streamlit as st
# from dotenv import load_dotenv
# from gigachat import GigaChat
# from gigachat.models import Chat, Messages, MessagesRole
# from utils.auth import authenticator

# load_dotenv()
# SYSTEM_PROMPT1 = os.getenv("SYSTEM_PROMPT1", "").strip()
# SYSTEM_PROMPT2 = os.getenv("SYSTEM_PROMPT2", "").strip()

# # Инициализируем состояние сессии
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "current_mode" not in st.session_state:
#     st.session_state.current_mode = "Normal"


# def on_mode_change() -> None:
#     """Добавляет в историю скрытую инструкцию при переключении режима."""
#     new_mode = st.session_state.mode_selector
#     if new_mode == st.session_state.current_mode:
#         return

#     st.session_state.current_mode = new_mode

#     # Если история пуста, модель сразу получит новый SYSTEM_PROMPT без переходного сообщения
#     if not st.session_state.messages:
#         return

#     switch_note = (
#         "[SYSTEM NOTE: The user has switched your mode to NORMAL. "
#         "Stop using Cockney and strictly follow the Normal system prompt from this point on.]"
#         if new_mode == "Normal"
#         else "[SYSTEM NOTE: The user has switched your mode to MODE COCKNEY. "
#         "Switch immediately and strictly follow the Mode Cockney system prompt from this point on.]"
#     )

#     # Если пользователь переключил режим несколько раз подряд до отправки сообщения, перезаписываем последнюю скрытую метку
#     if st.session_state.messages[-1].get("hidden"):
#         st.session_state.messages[-1]["content"] = switch_note
#     else:
#         st.session_state.messages.append(
#             {
#                 "role": "user",
#                 "content": switch_note,
#                 "hidden": True,
#             }
#         )


# # Верхняя панель: заголовок, переключатель режимов и кнопка очистки на одном уровне
# col_title, col_mode, col_clear = st.columns(
#     [2.2, 2.5, 1.3], vertical_alignment="center"
# )

# with col_title:
#     st.title("ISpeak")  #[cite: 2]

# with col_mode:
#     selected_mode = st.radio(
#         "Режим общения",
#         options=["Normal", "Mode Cockney"],
#         horizontal=True,
#         label_visibility="collapsed",
#         key="mode_selector",
#         on_change=on_mode_change,
#     )

# with col_clear:
#     if st.button("Очистить чат", use_container_width=True):
#         st.session_state.messages = []
#         st.rerun()

# active_system_prompt = (
#     SYSTEM_PROMPT1 if selected_mode == "Normal" else SYSTEM_PROMPT2
# )

# # Отрисовываем только видимые для пользователя сообщения
# for message in st.session_state.messages:
#     if message.get("hidden"):
#         continue
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# def get_gigachat_response(history: list[dict], system_prompt: str) -> str:
#     if authenticator.is_expired():  #[cite: 2]
#         authenticator.update()  #[cite: 2]

#     giga_messages = []

#     if system_prompt:
#         giga_messages.append(
#             Messages(role=MessagesRole.SYSTEM, content=system_prompt)
#         )

#     for msg in history:
#         role = (
#             MessagesRole.USER
#             if msg["role"] == "user"
#             else MessagesRole.ASSISTANT
#         )
#         # Склеиваем подряд идущие сообщения роли user (скрытую метку смены режима + новый запрос),
#         # чтобы не нарушать строгое чередование ролей user/assistant в GigaChat API
#         if giga_messages and giga_messages[-1].role == role:
#             giga_messages[-1].content += f"\n\n{msg['content']}"
#         else:
#             giga_messages.append(Messages(role=role, content=msg["content"]))

#     with GigaChat(
#         access_token=authenticator.api_token,  #[cite: 2]
#         verify_ssl_certs=False,  #[cite: 2]
#         model="GigaChat-3-Ultra",  #[cite: 2]
#     ) as giga:
#         response = giga.chat(Chat(messages=giga_messages))  #[cite: 2]
#         return response.choices[0].message.content  #[cite: 2]


# # Обработка ввода пользователя
# if prompt := st.chat_input("Введите сообщение..."):  #[cite: 2]
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("assistant"):
#         with st.spinner("Генерация ответа..."):  #[cite: 2]
#             try:
#                 reply = get_gigachat_response(
#                     st.session_state.messages,
#                     active_system_prompt,
#                 )
#                 st.markdown(reply)
#                 st.session_state.messages.append(
#                     {"role": "assistant", "content": reply}
#                 )
#             except Exception as e:
#                 st.error(f"Ошибка при обращении к GigaChat API: {e}")  #[cite: 2]


# import os
# import streamlit as st
# from dotenv import load_dotenv
# from gigachat import GigaChat
# from gigachat.models import Chat, Messages, MessagesRole
# from utils.auth import authenticator

# load_dotenv()
# SYSTEM_PROMPT1 = os.getenv("SYSTEM_PROMPT1", "").strip()
# SYSTEM_PROMPT2 = os.getenv("SYSTEM_PROMPT2", "").strip()

# # Инициализируем историю чата
# if "messages" not in st.session_state:
#     st.session_state.messages = []


# def clear_chat_history() -> None:
#     """Полностью очищает историю переписки в session_state."""
#     st.session_state.messages = []


# # Верхняя панель: название, переключатель режимов и кнопка очистки на одном уровне
# col_title, col_mode, col_clear = st.columns(
#     [2.2, 2.5, 1.3], vertical_alignment="center"
# )

# with col_title:
#     st.title("ISpeak")

# with col_mode:
#     selected_mode = st.radio(
#         "Режим общения",
#         options=["Normal", "Mode Cockney"],
#         horizontal=True,
#         label_visibility="collapsed",
#         key="mode_selector",
#         on_change=clear_chat_history,
#     )

# with col_clear:
#     st.button(
#         "Очистить чат",
#         use_container_width=True,
#         on_click=clear_chat_history,
#     )

# # Определяем системный промпт для активного режима
# active_system_prompt = (
#     SYSTEM_PROMPT1 if selected_mode == "Normal" else SYSTEM_PROMPT2
# )

# # Отрисовываем историю сообщений
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# def get_gigachat_response(history: list[dict], system_prompt: str) -> str:
#     if authenticator.is_expired():
#         authenticator.update()

#     giga_messages = []

#     # Всегда передаём актуальный системный промпт выбранного режима первым сообщением
#     if system_prompt:
#         giga_messages.append(
#             Messages(role=MessagesRole.SYSTEM, content=system_prompt)
#         )

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


# # Обработка нового сообщения пользователя
# if prompt := st.chat_input("Введите сообщение..."):
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("assistant"):
#         with st.spinner("Генерация ответа..."):
#             try:
#                 reply = get_gigachat_response(
#                     st.session_state.messages,
#                     active_system_prompt,
#                 )
#                 st.markdown(reply)
#                 st.session_state.messages.append(
#                     {"role": "assistant", "content": reply}
#                 )
#             except Exception as e:
#                 st.error(f"Ошибка при обращении к GigaChat API: {e}")


import os
import streamlit as st
import streamlit.components.v1 as components
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


def render_fullscreen_button() -> None:
    """Рендерит кнопку переключения полноэкранного режима браузера."""
    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                background: transparent;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 40px;
                overflow: hidden;
            }
            #fs-btn {
                width: 100%;
                height: 38.4px;
                padding: 0.25rem 0.75rem;
                border-radius: var(--btn-radius, 0.5rem);
                border: var(--btn-border, 1px solid rgba(250, 250, 250, 0.2));
                background-color: var(--btn-bg, rgb(19, 23, 32));
                color: var(--btn-color, rgb(250, 250, 250));
                font-family: var(--btn-font, "Source Sans Pro", sans-serif);
                font-size: var(--btn-font-size, 1rem);
                font-weight: 400;
                line-height: 1.6;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
                white-space: nowrap;
                transition: border-color 0.15s, color 0.15s, background-color 0.15s;
            }
            #fs-btn:hover {
                border-color: rgb(255, 75, 75);
                color: rgb(255, 75, 75);
            }
            #fs-btn:active {
                background-color: rgb(255, 75, 75);
                border-color: rgb(255, 75, 75);
                color: rgb(255, 255, 255);
            }
        </style>
        </head>
        <body>
            <button id="fs-btn" type="button" title="Переключить полноэкранный режим">
                ⛶ На весь экран
            </button>
            <script>
                const parentDoc = window.parent.document;
                const btn = document.getElementById("fs-btn");
                const rootStyle = document.documentElement.style;

                // Копируем стили соседней нативной кнопки Streamlit для совпадения со светлой/тёмной темой
                function syncTheme() {
                    const nativeBtn = parentDoc.querySelector('button[data-testid="stBaseButton-secondary"]');
                    if (nativeBtn) {
                        const styles = window.parent.getComputedStyle(nativeBtn);
                        rootStyle.setProperty("--btn-bg", styles.backgroundColor);
                        rootStyle.setProperty("--btn-color", styles.color);
                        rootStyle.setProperty("--btn-border", styles.border);
                        rootStyle.setProperty("--btn-radius", styles.borderRadius);
                        rootStyle.setProperty("--btn-font", styles.fontFamily);
                        rootStyle.setProperty("--btn-font-size", styles.fontSize);
                    }
                }

                function updateButtonState() {
                    btn.textContent = parentDoc.fullscreenElement
                        ? "🗗 Свернуть"
                        : "⛶ На весь экран";
                }

                btn.addEventListener("click", async () => {
                    try {
                        if (!parentDoc.fullscreenElement) {
                            await parentDoc.documentElement.requestFullscreen();
                        } else {
                            await parentDoc.exitFullscreen();
                        }
                    } catch (err) {
                        console.error("Не удалось переключить полноэкранный режим:", err);
                    }
                });

                parentDoc.addEventListener("fullscreenchange", updateButtonState);

                // Очищаем обработчик при перерисовке компонента Streamlit, чтобы избежать утечки памяти
                window.addEventListener("unload", () => {
                    parentDoc.removeEventListener("fullscreenchange", updateButtonState);
                });

                syncTheme();
                updateButtonState();
                setTimeout(syncTheme, 250);
            </script>
        </body>
        </html>
        """,
        height=42,
    )


# Верхняя панель: название, переключатель режимов, очистка чата и полноэкранный режим
col_title, col_mode, col_clear, col_fs = st.columns(
    [1.8, 2.3, 1.3, 1.4], vertical_alignment="center"
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

with col_fs:
    render_fullscreen_button()

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