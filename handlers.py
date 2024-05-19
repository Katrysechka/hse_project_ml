from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup,KeyboardButton,                 InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3, asyncio

import tg_bot.keyboards as kb 
router = Router()

class Request(StatesGroup):
    name = State()
    password = State()
    custom_name = State()

@router.message(CommandStart())   
async def start(message: Message):
    await message.answer('<b>Здравствуйте!❤️ </b> \n\nПрежде чем начать,просим Вас войти в свой аккаунт.\n\nДля этого войдите в свой профиль', parse_mode='HTML', reply_markup=kb.login)

def check_credentials(username, password):
    conn = sqlite3.connect('shop_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM login_info WHERE username=? AND password=?', (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

@router.callback_query(F.data == 'login')
async def login(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Request.name)
    await callback.message.answer('Введите ваш <b>логин</b> <b>в</b> <b>LYE</b>', parse_mode='HTML')

@router.message(Request.name)   
async def login_1(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Request.password)
    await message.answer('Введите ваш <b>пароль</b> <b>в</b> <b>LYE</b>', parse_mode='HTML')
    
@router.message(Request.password)   
async def login_2(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('name')
    password = message.text

    if check_credentials(username, password):
        await message.answer(f'Добрый день, <b>{username}!</b>\n\nУдобно ли Вам,если мы будем к вам так обращаться или Вы введете свой вариант? ',reply_markup=kb.general, parse_mode='HTML')
    else:
        await message.answer('Неверный логин или пароль. Пожалуйста, проверьте данные или зарегистрируйтесь в LYE')

@router.callback_query(F.data == 'yes')
async def handle_yes(callback: CallbackQuery):
    await callback.message.answer('💫 <b>Супер!</b> \n\nСкорее переходите в интересующие вас разделы и знакомьтесь с ними подробнее', parse_mode='HTML',reply_markup=kb.main)

@router.callback_query(F.data == 'no')
async def handle_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Хорошо, предложите свой вариант обращения')
    await state.set_state(Request.custom_name)

@router.message(Request.custom_name)
async def custom_name(message: Message, state: FSMContext):
    await state.update_data(custom_name=message.text)
    await message.answer(f"Теперь точно здравствуйте, <b>{message.text}</b> ☺️\n\nНиже вы сможете найти интересующие вас разделы и \nознакомиться с ними подробнее", reply_markup=kb.main, parse_mode='HTML') 
    await state.reset_state()

def record_service_rating(user_id, rating):
    conn = sqlite3.connect('shop_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rating (user_id, service) VALUES (?, ?)', (user_id, rating))
    conn.commit()
    conn.close()

@router.message(F.data== 'Оцените приложение 🤩')
async def rating(message: Message):
    await message.answer('📍<b>LYE</b> - это прежде всего про людей,про их чувства и музыку!\n\n <b>Наша цель</b> - помочь вам услышать себя и нам было бы очень приятно,если бы Вы оценили наше приложение и оставили отзыв. \n\n Так мы сможем стать еще ближе!', reply_markup=kb.rating, parse_mode='HTML')
 
text ='<b>Listen your emotion</b> - это инновационное музыкальное приложение, которое использует технологии распознавания лиц для определения эмоций пользователя и автоматического подбора подходящего трека. \n\nПриложение <b>анализирует выражение лица</b> пользователя и определяет его настроение, после чего запускает музыку, которая соответствует этим эмоциям.\n\nНапример, если пользователь улыбается, приложение может включить веселую и жизнерадостную музыку, а если он выглядит задумчивым или грустным, то выберет треки с более спокойным и меланхоличным настроением.\n\nЭто приложение отлично подходит для тех, кто хочет быстро найти музыку, которая соответствует их текущему настроению, без необходимости самостоятельно выбирать плейлисты или жанры. \n\nListen your emotion поможет создать подходящую атмосферу и поможет пользователю насладиться музыкой в полной мере'

@router.message(F.text == 'О нас ❓')
async def about(message: Message):
    await message.answer(text, reply_markup=kb.main)
    

@router.callback_query(F.data == 'words')
async def number(callback: CallbackQuery):
    await callback.message.answer('Нам важно ваше мнение. Оставьте отзыв пожалуйста', reply_markup=kb.rate)

@router.callback_query(F.data == 'number')
async def number(callback: CallbackQuery):
    await callback.message.answer('Мы бы очень хотели, чтобы наше приложение помогло Вам услышать Вашу эмоцию ☺️ \n\nПожалуйста, оцените нас:', reply_markup=kb.rate) 
    user_id = callback.from_user.id
    data = F.data.get()
    r = int(data[-1])
    record_service_rating(user_id, r, None,None) 

@router.callback_query(F.data.in_(('11', '12', '13', '14', '15')))
async def number(callback: CallbackQuery):
    await callback.message.answer('Оцените в среднем соответствие музыки вашему настроению', reply_markup=kb.service) 
    user_id = callback.from_user.id
    data = F.data.get()
    r = int(data[-1])
    record_service_rating(user_id,  None,r,None)   

@router.callback_query(F.data.in_(('21', '22', '23', '24', '25')))
async def number(callback: CallbackQuery):
    await callback.message.answer('Оцените само приложение, интерфейс', reply_markup=kb.interface)   
    user_id = callback.from_user.id
    data = F.data.get()
    r = int(data[-1])
    record_service_rating(user_id,None,None,r)   


@router.callback_query(F.data.in_(('31', '32', '33', '34', '35')))
async def number(callback: CallbackQuery):
    await callback.message.answer('<b>Спасибо!❤️ </b>', parse_mode='HTML')    
    
def record_rating(user_id, general, service, interface):
    conn = sqlite3.connect('shop_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rating (user_id, general, service, interface) VALUES (?, ?, ?, ?)',
                   (user_id, general, service, interface))
    conn.commit()
    conn.close()