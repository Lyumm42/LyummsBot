from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3

router = Router()


class Survey(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()


def get_db_connection():
    conn = sqlite3.connect("survey.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            age INTEGER,
            color TEXT
            subject TEXT,
            movie TEXT,
            q6 TEXT,
            q7 TEXT,
            q8 TEXT
        )
    ''')
    conn.commit()
    return conn


@router.message(lambda message: message.text.lower() == "опрос")
async def start_survey(message: types.Message, state: FSMContext):
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = message.from_user.id

    cursor.execute("SELECT * FROM survey WHERE user_id = ?", (user_id,))
    existing_data = cursor.fetchone()
    if existing_data:
        await message.answer("Вы уже проходили опрос. Вот ваши ответы:")
        result_text = (
            f"1. Имя: {existing_data[2]}\n"
            f"2. Возраст: {existing_data[3]}\n"
            f"3. Любимый цвет: {existing_data[4]}\n"
            f"4. Любимый предмет: {existing_data[5]}\n"
            f"5. Любимый фильм: {existing_data[6]}\n"
            f"6. {existing_data[7]}\n"
            f"7. {existing_data[8]}\n"
            f"8. {existing_data[9]}"
        )
        await message.answer(result_text)
        conn.close()
        return

    await message.answer("1. как вас зовут?")
    await state.set_state(Survey.q1)
    conn.close()


@router.message(Survey.q1)
async def survey_q1(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("2. сколько вам лет?")
    await state.set_state(Survey.q2)


@router.message(Survey.q2)
async def survey_q2(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("3. какой ваш любимый цвет?")
    await state.set_state(Survey.q3)


@router.message(Survey.q3)
async def survey_q3(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("4. какой ваш любимый школьный предмет?")
    await state.set_state(Survey.q4)


@router.message(Survey.q4)
async def survey_q4(message: types.Message, state: FSMContext):
    await state.update_data(color=message.text)
    await message.answer("5. какой ваш любимый фильм/мультфильм?")
    await state.set_state(Survey.q5)


@router.message(Survey.q5)
async def survey_q5(message: types.Message, state: FSMContext):
    await state.update_data(movie=message.text)
    await message.answer("6. кто ваш любимый стример?")
    await state.set_state(Survey.q6)


@router.message(Survey.q6)
async def survey_q6(message: types.Message, state: FSMContext):
    await state.update_data(q6=message.text)
    await message.answer("7. любимое блюдо?")
    await state.set_state(Survey.q8)


@router.message(Survey.q8)
async def survey_q8(message: types.Message, state: FSMContext):
    data = await state.get_data()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO survey (user_id, name, age, subject, color, movie, q6, q7, q8)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        message.from_user.id,
        data.get('name'),
        data.get('age'),
        data.get('subject'),
        data.get('color'),
        data.get('movie'),
        data.get('q6'),
        data.get('q7'),
        message.text
    ))
    conn.commit()
    conn.close()

    result_text = (
        f"*Ваши ответы:*\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Любимый предмет: {data['subject']}\n"
        f"Любимый цвет: {data['color']}\n"
        f"Любимый фильм: {data['movie']}\n"
        f"{data['q6']}\n"
        f"{data['q7']}\n"
        f"{message.text}"
    )
    await message.answer(result_text, parse_mode="Markdown")
    await state.clear()