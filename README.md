# ISpeak — AI Conversational English Tutor

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?logo=streamlit&logoColor=white)
![GigaChat API](https://img.shields.io/badge/GigaChat-3--Ultra-21A038)

**ISpeak** — интерактивный веб-ассистент на базе GigaChat для регулярной практики живого разговорного английского. Бот общается исключительно на английском языке, подстраивается под уровень собеседника и деликатно исправляет ошибки, не превращая диалог в скучный урок.

---

## Возможности

* **Два режима общения:**
  * **Normal** — естественный современный американский английский с сокращениями, фразовыми глаголами и идиомами.
  * **Mode Cockney** — общение с использованием британского диалекта и сленга Кокни.
* **Ненавязчивый разбор ошибок:** при наличии опечаток, грамматических или стилистических неточностей бот выводит компактный блок `Correction` с краткими пояснениями (`Quick notes`) и сразу продолжает разговор по теме.
* **Адаптация под уровень:** сложность лексики и конструкций постепенно растёт по ходу диалога.
* **Чистый контекст при смене режима:** переключение между `Normal` и `Mode Cockney` или нажатие кнопки **«Очистить чат»** синхронно сбрасывает историю в интерфейсе и памяти сессии, исключая смешивание стилей.

---

## Стек технологий

* **Интерфейс:** Streamlit
* **LLM / API:** Sber GigaChat SDK (`GigaChat-3-Ultra`)
* **Конфигурация:** `python-dotenv`

---

## Структура проекта

```text
ISpeak/
├── front.py                                    # Основной интерфейс Streamlit и логика чата
├── utils/
│   ├── auth.py                                 # Обновление и хранение OAuth-токена GigaChat
│   └── russian_trusted_root_ca_pem.crt         # Корневой сертификат Минцифры РФ
├── .env                                        # Переменные окружения и системные промпты (не в Git)
├── .env.example                                # Шаблон переменных окружения
├── requirements.txt                            # Зависимости проекта
└── README.md
```


# Быстрый старт:
## 1. Клонирование репозитория
   
git clone [https://github.com/](https://github.com/)<your-username>/ISpeak.git

cd ISpeak

## 2. Установка зависимостей
Рекомендуется использовать виртуальное окружение:
python -m venv venv
## Windows:
venv\Scripts\activate
## Linux / macOS:
source venv/bin/activate
pip install streamlit gigachat python-dotenv

## 3. Настройка .env
Создайте файл .env в корне проекта (на основе .env.example) и заполните переменные:
AUTH_TOKEN="ваш_authorization_key_из_кабинета_sber_studio"
AUTH_URL="[https://ngw.devices.sberbank.ru:9443/api/v2/oauth](https://ngw.devices.sberbank.ru:9443/api/v2/oauth)"
RUS_CERT="utils/russian_trusted_root_ca_pem.crt"

SYSTEM_PROMPT1="Системный промпт для режима Normal"
SYSTEM_PROMPT2="Системный промпт для режима Mode Cockney"

## 4. Запуск приложения
streamlit run front.py

После запуска интерфейс откроется в браузере по адресу http://localhost:8501

# Поддержать автора:
2202206793063616 Сбер
