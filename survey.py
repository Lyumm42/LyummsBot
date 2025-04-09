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
            color TEXT,
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
            f"6. Любимый стример: {existing_data[7]}\n"
            f"7. Любимое блюдо: {existing_data[8]}\n"
            f"8. Любимое хобби: {existing_data[9]}"
        )
        await message.answer(result_text)
        conn.close()
        return

    await message.answer("1. Как вас зовут?")
    await state.set_state(Survey.q1)
    conn.close()


@router.message(Survey.q1)
async def survey_q1(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("2. Сколько вам лет?")
    await state.set_state(Survey.q2)


@router.message(Survey.q2)
async def survey_q2(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await message.answer("3. Какой ваш любимый цвет?")
        await state.set_state(Survey.q3)
    except ValueError:
        await message.answer("Пожалуйста, введите число для возраста.")


@router.message(Survey.q3)
async def survey_q3(message: types.Message, state: FSMContext):
    await state.update_data(color=message.text)
    await message.answer("4. Какой ваш любимый школьный предмет?")
    await state.set_state(Survey.q4)


@router.message(Survey.q4)
async def survey_q4(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("5. Какой ваш любимый фильм/мультфильм?")
    await state.set_state(Survey.q5)


@router.message(Survey.q5)
async def survey_q5(message: types.Message, state: FSMContext):
    await state.update_data(movie=message.text)
    await message.answer("6. Кто ваш любимый стример?")
    await state.set_state(Survey.q6)


@router.message(Survey.q6)
async def survey_q6(message: types.Message, state: FSMContext):
    await state.update_data(q6=message.text)
    await message.answer("7. Ваше любимое блюдо?")
    await state.set_state(Survey.q7)


@router.message(Survey.q7)
async def survey_q7(message: types.Message, state: FSMContext):
    await state.update_data(q7=message.text)
    await message.answer("8. Ваше любимое хобби?")
    await state.set_state(Survey.q8)


@router.message(Survey.q8)
async def survey_q8(message: types.Message, state: FSMContext):
    data = await state.get_data()
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO survey (user_id, name, age, color, subject, movie, q6, q7, q8)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            message.from_user.id,
            data.get('name'),
            data.get('age'),
            data.get('color'),
            data.get('subject'),
            data.get('movie'),
            data.get('q6'),
            data.get('q7'),
            message.text
        ))
        conn.commit()

        result_text = (
            f"*Ваши ответы:*\n"
            f"1. Имя: {data['name']}\n"
            f"2. Возраст: {data['age']}\n"
            f"3. Цвет: {data['color']}\n"
            f"4. Предмет: {data['subject']}\n"
            f"5. Фильм: {data['movie']}\n"
            f"6. Стример: {data['q6']}\n"
            f"7. Блюдо: {data['q7']}\n"
            f"8. Хобби: {message.text}"
        )
        await message.answer(result_text, parse_mode="Markdown")
    except Exception as e:
        await message.answer("Произошла ошибка при сохранении данных")
        print(f"Database error: {str(e)}")
    finally:
        conn.close()
        await state.clear()