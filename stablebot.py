from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import os
TOKEN = os.getenv("8425734749:AAGFbzhDdcmbxDKL55A3lEXWYFwzBYTgwx0")
bot = telebot.TeleBot(TOKEN)
#для статистики 
import sqlite3

conn = sqlite3.connect("regions.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS regions (
    city TEXT,
    cases TEXT,
    trend TEXT,
    top TEXT
)
""")

conn.commit()
user_scores = {}
cursor.execute("DELETE FROM regions")

data = [
    ("Алматы", "≈300 на 100 000", "рост", "лёгкие, молочная железа, желудок"),
    ("Караганда", "≈350 на 100 000", "высокий", "лёгкие, кожа, желудок"),
    ("Темиртау", "≈380 на 100 000", "очень высокий", "лёгкие, печень, кожа"),
    ("Жезказган", "≈270 на 100 000", "средний", "лёгкие, желудок")
]

cursor.executemany("INSERT INTO regions VALUES (?, ?, ?, ?)", data)
conn.commit()
#Мини-тест работники
worker_test = {
    1: {
        "q": "Что является фактором риска на производстве?",
        "options": ["Пыль", "Вода", "Сон"],
        "correct": 0
    },
    2: {
        "q": "Что снижает риск?",
        "options": ["Игнорирование", "Средства защиты", "Переработка"],
        "correct": 1
    }
}

user_worker = {}
def start_worker_test(call):
    user_worker[call.from_user.id] = {"q": 1, "score": 0}
    send_worker_q(call)


def send_worker_q(call):
    data = user_worker[call.from_user.id]
    q_num = data["q"]

    if q_num > len(worker_test):
        return worker_result(call)

    q = worker_test[q_num]

    kb = InlineKeyboardMarkup()
    for i, option in enumerate(q["options"]):
        kb.add(InlineKeyboardButton(option, callback_data=f"w_{i}"))

    bot.edit_message_text(
        f"🏭 Вопрос {q_num}:\n\n{q['q']}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )


def worker_result(call):
    data = user_worker[call.from_user.id]
    score = data["score"]

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⬅️ В меню", callback_data="menu"))

    bot.edit_message_text(
        f"📊 Результат:\n\n{score} из {len(worker_test)}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )
#Структура теста студенты
test_data = {
    1: {
        "q": "Что является этапом канцерогенеза?",
        "options": ["Инициация", "Регенерация", "Гомеостаз"],
        "correct": 0
    },
    2: {
        "q": "Что повреждает ДНК?",
        "options": ["Канцерогены", "Витамины", "Белки"],
        "correct": 0
    },
    3: {
        "q": "Что делают онкогены?",
        "options": ["Ускоряют деление клеток", "Останавливают рост", "Убивают клетки"],
        "correct": 0
    }
}

user_test = {}
def start_test(call):
    user_test[call.from_user.id] = {"q": 1, "score": 0}
    send_question(call)
def send_question(call):
    data = user_test[call.from_user.id]
    q_num = data["q"]

    if q_num > len(test_data):
        return show_test_result(call)

    q = test_data[q_num]

    kb = InlineKeyboardMarkup()
    for i, option in enumerate(q["options"]):
        kb.add(InlineKeyboardButton(option, callback_data=f"test_{i}"))

    bot.edit_message_text(
        f"🧠 Вопрос {q_num}:\n\n{q['q']}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )

#кейсы студенты
case_data = {
    1: {
        "q": "🧪 Кейс 1:\n\nПациент: мужчина, 52 года\nКурит 30 лет, кашель, похудение.\n\nДиагноз?",
        "options": ["Рак лёгкого", "Бронхит", "Пневмония"],
        "correct": 0
    },
    2: {
        "q": "🧪 Кейс 2:\n\nЖенщина, 45 лет\nУплотнение в груди, втяжение кожи.\n\nДиагноз?",
        "options": ["Мастит", "Рак молочной железы", "Киста"],
        "correct": 1
    },
    3: {
        "q": "🧪 Кейс 3:\n\nМужчина, 60 лет\nБоли в желудке, похудение, анемия.\n\nДиагноз?",
        "options": ["Гастрит", "Язва", "Рак желудка"],
        "correct": 2
    },
    4: {
        "q": "🧪 Кейс 4:\n\nПациент, 38 лет\nРодинка изменилась, выросла.\n\nДиагноз?",
        "options": ["Меланома", "Папиллома", "Аллергия"],
        "correct": 0
    }
}

user_case = {}
def start_case(call):
    user_case[call.from_user.id] = {"q": 1, "score": 0}
    send_case(call)


def send_case(call):
    data = user_case[call.from_user.id]
    q_num = data["q"]

    if q_num > len(case_data):
        return show_case_result(call)

    q = case_data[q_num]

    kb = InlineKeyboardMarkup()
    for i, option in enumerate(q["options"]):
        kb.add(InlineKeyboardButton(option, callback_data=f"case_{i}"))

    bot.edit_message_text(
        q["q"],
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )


def show_case_result(call):
    data = user_case[call.from_user.id]
    score = data["score"]

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⬅️ В меню", callback_data="menu"))

    bot.edit_message_text(
        f"📊 Результат кейсов:\n\n{score} из {len(case_data)}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )
    
# 📊 города
cities = {
    "Алматы":
        "📍 Алматы\n\n"
        "📊 Обстановка:\n"
        "📈 Статистика:\n"
        "• ~300 случаев на 100 000 населения\n\n"
        "• Высокая плотность населения\n"
        "• Загрязнение воздуха (смог)\n\n"

        "📈 Онкология:\n"
        "• Рак лёгких\n"
        "• Рак молочной железы\n"
        "• Рак желудка\n\n"

        "⚠️ Причины:\n"
        "• Выхлопные газы\n"
        "• Промышленность\n"
        "• Курение\n\n"

        "📌 Уровень риска: 🟡 Средний",

    "Караганда":
        "📍 Караганда\n\n"
        "📊 Обстановка:\n"
        "📈 Статистика:\n"
        "• ~300 случаев на 100 000 населения\n\n"
        "• Промышленный регион\n"
        "• Угольная добыча\n\n"

        "📈 Онкология:\n"
        "• Рак лёгких\n"
        "• Рак кожи\n"
        "• Рак желудка\n\n"

        "⚠️ Причины:\n"
        "• Угольная пыль\n"
        "• Загрязнение воздуха\n"
        "• Химические выбросы\n\n"

        "📌 Уровень риска: 🔴 Высокий",

    "Темиртау":
        "📍 Темиртау\n\n"
        "📊 Обстановка:\n"
        "📈 Статистика:\n"
        "• ~300 случаев на 100 000 населения\n\n"
        "• Металлургический центр\n"
        "• Сильное загрязнение воздуха\n\n"

        "📈 Онкология:\n"
        "• Рак лёгких\n"
        "• Рак печени\n"
        "• Рак кожи\n\n"

        "⚠️ Причины:\n"
        "• Тяжёлые металлы\n"
        "• Промышленные выбросы\n"
        "• Токсины в воздухе\n\n"

        "📌 Уровень риска: 🔴 Очень высокий",

    "Жезказган":
        "📍 Жезказган\n\n"
        "📊 Обстановка:\n"
        "📈 Статистика:\n"
        "• ~300 случаев на 100 000 населения\n\n"
        "• Горнодобывающий регион\n"
        "• Пыль и металлы\n\n"

        "📈 Онкология:\n"
        "• Рак лёгких\n"
        "• Рак желудка\n\n"

        "⚠️ Причины:\n"
        "• Металлическая пыль\n"
        "• Производственные факторы\n\n"

        "📌 Уровень риска: 🟡 Средний"
}

# 🔹 главное меню
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📍 Риск региона", callback_data="risk"),
        InlineKeyboardButton("🧠 Персональный риск", callback_data="personal"),
    )
    kb.add(
        InlineKeyboardButton("🩺 Скрининг", callback_data="screening"),
        InlineKeyboardButton("⚠️ Симптомы", callback_data="symptoms"),
    )
    kb.add(
        InlineKeyboardButton("🏭 Работники", callback_data="workers"),
        InlineKeyboardButton("🎓 Студенты", callback_data="students"),
    )
    kb.add(
        InlineKeyboardButton("🗺 Карта", callback_data="map"),
        InlineKeyboardButton("ℹ️ О проекте", callback_data="about"),
    )
    kb.add(
        InlineKeyboardButton("🌐 Открыть сайт", url="https://riskwell-insight.lovable.app/")
    )
    return kb
def back():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="menu"))
    return kb

# 🔹 старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Добро пожаловать в OncoRisk Kazakhstan", reply_markup=main_menu())

# 🔹 вопросы
def ask_q2(call):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("⚖️ Да", callback_data="q2_yes"),
        InlineKeyboardButton("👍 Нет", callback_data="q2_no")
    )

    bot.edit_message_text(
        "Есть лишний вес?",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )

def show_result(call):
    score = user_scores.get(call.from_user.id, 0)

    if score >= 3:
        res = "🔴 Высокий риск"
    elif score == 2:
        res = "🟡 Средний риск"
    else:
        res = "🟢 Низкий риск"

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⬅️ В меню", callback_data="menu"))

    bot.edit_message_text(
        f"🧠 Ваш результат:\n\n{res}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )
# 🔹 обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.answer_callback_query(call.id)

    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    # 📍 РИСК
    if call.data == "risk":
        kb = InlineKeyboardMarkup()
        for city in cities:
            kb.add(InlineKeyboardButton(city, callback_data=f"city_{city}"))
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="menu"))

        bot.edit_message_text("🏙 Выберите город:", chat_id, msg_id, reply_markup=kb)

    elif call.data.startswith("city_"):
        city = call.data.replace("city_", "")

        cursor.execute("SELECT * FROM regions WHERE city=?", (city,))
        result = cursor.fetchone()

        if result:
            _, cases, trend, top = result

            text = (
                f"📍 {city}\n\n"

                f"📊 Статистика:\n"
                f"• {cases}\n"
                f"• Тренд: {trend}\n\n"

                f"📈 Частые виды рака:\n"
                f"• " + top.replace(", ", "\n• ") + "\n\n"

                f"{cities[city]}"
            )
        else:
            text = "Нет данных по региону"

        bot.edit_message_text(text, chat_id, msg_id, reply_markup=back())

    # 🧠 ПЕРСОНАЛЬНЫЙ РИСК
    elif call.data == "personal":
        user_scores[call.from_user.id] = 0

        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("🚬 Да", callback_data="q1_yes"),
            InlineKeyboardButton("❌ Нет", callback_data="q1_no")
        )

        bot.edit_message_text("🧠 Персональный риск\n\nКурите?", chat_id, msg_id, reply_markup=kb)

    elif call.data == "q1_yes":
        user_scores[call.from_user.id] += 2
        ask_q2(call)

    elif call.data == "q1_no":
        ask_q2(call)

    elif call.data == "q2_yes":
        user_scores[call.from_user.id] += 1
        show_result(call)

    elif call.data == "q2_no":
        show_result(call)

    # 🩺 СКРИНИНГ
    elif call.data == "screening":
        bot.edit_message_text(
        "🩺 Скрининг онкологических заболеваний:\n\n"
        "👩 Для женщин:\n"
        "• Рак молочной железы — маммография с 40 лет (1 раз в 2 года)\n"
        "• Рак шейки матки — ПАП-тест с 21 года (каждые 3 года)\n\n"

        "👨 Для мужчин:\n"
        "• Рак предстательной железы — ПСА-тест с 50 лет\n\n"

        "👥 Для всех:\n"
        "• Рак лёгких — КТ (для курящих и группы риска)\n"
        "• Колоректальный рак — колоноскопия с 50 лет (каждые 5–10 лет)\n"
        "• Рак кожи — осмотр кожи и родинок ежегодно\n"
        "• Рак желудка — ФГДС по показаниям\n\n"

        "❗ Регулярный скрининг помогает выявить заболевание на ранней стадии.",
        chat_id,
        msg_id,
        reply_markup=back()
    )

    # ⚠️ СИМПТОМЫ
    elif call.data == "symptoms":
        bot.edit_message_text(
        "⚠️ Возможные симптомы:\n\n"
        "• Длительная слабость и утомляемость\n"
        "• Необъяснимая потеря веса\n"
        "• Боль или уплотнения в теле\n"
        "• Длительный кашель или одышка\n"
        "• Изменения кожи или родинок\n\n"
        "❗ При наличии симптомов обязательно обратитесь к врачу.",
        chat_id,
        msg_id,
        reply_markup=back()
    )

    # 🏭 РАБОТНИКИ
    elif call.data == "workers":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("⚠️ Факторы риска", callback_data="w_risk"))
        kb.add(InlineKeyboardButton("🛡 Профилактика", callback_data="w_safe"))
        kb.add(InlineKeyboardButton("🧪 Мини-тест", callback_data="w_test"))
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="menu"))

        bot.edit_message_text(
        "🏭 Раздел для работников:",
        chat_id,
        msg_id,
        reply_markup=kb
    )
    elif call.data == "w_risk":
        bot.edit_message_text(
        "⚠️ Профессиональные риски:\n\n"
        "• Пыль и химические вещества\n"
        "• Тяжёлые металлы\n"
        "• Радиация\n"
        "• Высокие температуры\n"
        "• Длительное вдыхание газов\n\n"
        "❗ Повышают риск онкологических заболеваний",
        chat_id,
        msg_id,
        reply_markup=back()
    )
    elif call.data == "w_safe":
        bot.edit_message_text(
        "🛡 Профилактика:\n\n"
        "• Используйте средства защиты (маски, перчатки)\n"
        "• Проходите медосмотры\n"
        "• Соблюдайте технику безопасности\n"
        "• Ограничьте контакт с вредными веществами\n\n"
        "❗ Ранняя защита = снижение риска",
        chat_id,
        msg_id,
        reply_markup=back()
    )
    elif call.data == "w_test":
        start_worker_test(call)

    elif call.data.startswith("w_") and call.data != "w_test":
        answer = int(call.data.split("_")[1])

        data = user_worker[call.from_user.id]
        q_num = data["q"]

        if answer == worker_test[q_num]["correct"]:
            data["score"] += 1

        data["q"] += 1
        send_worker_q(call)
    # 🎓 СТУДЕНТЫ
    elif call.data == "students":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("📚 Теория", callback_data="stud_theory"))
        kb.add(InlineKeyboardButton("🧠 Тест", callback_data="stud_test"))
        kb.add(InlineKeyboardButton("🧪 Кейс", callback_data="stud_case"))
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="menu"))

        bot.edit_message_text("🎓 Раздел студентов:", chat_id, msg_id, reply_markup=kb)

    elif call.data == "stud_theory":
        bot.edit_message_text(
            "📚 Канцерогенез\n\n..."
            "\n"
            "Канцерогенез — это многоэтапный процесс превращения нормальной клетки в злокачественную.\n\n"
            "🔬 Основные этапы:\n"
            "1. Инициация — повреждение ДНК под действием канцерогенов\n"
            "2. Промоция — активное деление изменённых клеток\n"
            "3. Прогрессия — накопление мутаций и формирование опухоли\n\n"
            "⚠️ Факторы риска:\n"
            "• Курение и алкоголь\n"
            "• Загрязнение окружающей среды\n"
            "• Ионизирующее и УФ-излучение\n"
            "• Вирусы (ВПЧ, гепатиты B и C)\n"
            "• Наследственная предрасположенность\n\n"
            "🧬 Механизмы:\n"
            "• Активация онкогенов (ускорение деления клеток)\n"
            "• Инактивация генов-супрессоров\n"
            "• Нарушение апоптоза\n"
            "• Неоангиогенез (рост сосудов опухоли)\n\n"
            "📈 Итог:\n"
            "Опухолевые клетки приобретают способность к бесконтрольному росту и метастазированию.",
            chat_id,
            msg_id,
            reply_markup=back()
    )

    elif call.data == "stud_test":
        start_test(call)
        
    elif call.data.startswith("test_"):
        answer = int(call.data.split("_")[1])

        data = user_test[call.from_user.id]
        q_num = data["q"]

        if answer == test_data[q_num]["correct"]:
            data["score"] += 1

        data["q"] += 1
        send_question(call)
   
    
    elif call.data == "stud_case":
        start_case(call)
        
    elif call.data.startswith("case_"):
        answer = int(call.data.split("_")[1])

        data = user_case[call.from_user.id]
        q_num = data["q"]

        if answer == case_data[q_num]["correct"]:
            data["score"] += 1

        data["q"] += 1
        send_case(call)

    # 🗺 КАРТА
    elif call.data == "map":
        try:
            bot.delete_message(chat_id, msg_id)
        except:
            pass

        with open("map.jpg", "rb") as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption="🗺 Карта Казахстана",
                reply_markup=back()
        )
        
    # ℹ️ О ПРОЕКТЕ
    elif call.data == "about":
        bot.edit_message_text(
        "ℹ️ OncoRisk Kazakhstan\n\n"
        "OncoRisk Kazakhstan — это телеграм-бот для оценки онкологических рисков и повышения осведомлённости о здоровье.\n\n"
        "Бот помогает:\n"
        "• определить персональный уровень риска\n"
        "• узнать о факторах риска\n"
        "• получить информацию о симптомах и скрининге\n\n"
        "Проект направлен на раннюю профилактику и заботу о здоровье.",
        chat_id,
        msg_id,
        reply_markup=back()
    )

    # 🔙 МЕНЮ
    elif call.data == "menu":
        try:
            bot.edit_message_text(
                "📋 Главное меню:",
                chat_id,
                msg_id,
                reply_markup=main_menu()
            )
        except Exception as e:
            print("Ошибка menu:", e)

            try:
                bot.delete_message(chat_id, msg_id)
            except:
                pass

            bot.send_message(
                chat_id,
                "📋 Главное меню:",
                reply_markup=main_menu()
            )

keep_alive()

import time

while True:
    try:
        bot.infinity_polling(none_stop=True)
    except KeyboardInterrupt:
        print("Бот остановлен вручную")
        break   # 🔥 ВЫХОД ИЗ ЦИКЛА
    except Exception as e:
        print("Ошибка:", e)
        time.sleep(5)
       

