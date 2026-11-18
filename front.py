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