from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from tasks import *

rt = Router()
student = ''
task_curr = ''


@rt.message(CommandStart())
async def start(message: Message):

    # Add buttons
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Некит Усольцев', callback_data='usolcev'),
        InlineKeyboardButton(text='Леон Веричев', callback_data='verichev')
    )
    builder.adjust(2)

    await message.answer('Выбери ученика', reply_markup=builder.as_markup())


# Выбираем что я хочу сделать
@rt.callback_query(F.data.in_(['usolcev', 'verichev']))
async def choose_task_type(callback: CallbackQuery):
    global student
    student = callback.data

    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Удалить', callback_data='delete'),
        InlineKeyboardButton(text='Добавить', callback_data='add'),
        InlineKeyboardButton(text='Просмотреть', callback_data='watch')
    )
    builder.adjust(2)

    await callback.message.answer('Что ты хочешь сделать?', reply_markup=builder.as_markup())
    await callback.answer()


# Если я хочу удалить или посмотреть что либо
@rt.callback_query(F.data.in_(['delete', 'watch']))
async def choose_type(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Кроссворд', callback_data=f'Crossword|{callback.data}'),
        InlineKeyboardButton(text='Чтение', callback_data=f'Read|{callback.data}'),
        InlineKeyboardButton(text='Логика', callback_data=f'Logic|{callback.data}'),
    )
    print(callback.data)

    await callback.message.answer(f'Какой тип заданий ты хочешь'
                                  f'{" посмотреть" if callback.data == "watch" else " удалить"}', reply_markup=builder.as_markup())
    await callback.answer()


# Удаление элемента
@rt.callback_query(F.data.contains('delete|'))
async def delete_task(callback: CallbackQuery):
    a = callback.data.split('|')
    type_ = a[1]

    tasks = get_task(type_, student)
    tasks.delete(callback.message.text)
    tasks.save()

    await callback.message.delete()
    await callback.answer()


# Просмотр всех элементов для удаления или просто просмотра
@rt.callback_query(lambda x: '|watch' in x.data or '|delete' in x.data)
async def send_allowed_tasks(callback: CallbackQuery):
    type_ = callback.data.split('|')[0]
    tasks = get_task(type_, student)
    delete = 'delete' in callback.data

    for task in tasks:
        if delete:
            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(text='Удалить', callback_data=f'delete|{type_}'))
            await callback.message.answer(task, reply_markup=builder.as_markup())

        else:
            await callback.message.answer(task)

    await callback.answer()


# Если хочу добавить элемент
@rt.callback_query(F.data == 'add')
async def delete_task(callback: CallbackQuery):
    await callback.message.answer('Отправь путь к заданию')
    await callback.answer()


# Принимаю как называется элемент
@rt.message(F.text)
async def get_task_name(message: Message):
    global task_curr
    task_curr = message.text

    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Кроссворд', callback_data=f'Crossword|add'),
        InlineKeyboardButton(text='Чтение', callback_data=f'Read|add'),
        InlineKeyboardButton(text='Логика', callback_data=f'Logic|add'),
    )
    builder.adjust(2)
    await message.answer('Выбери тип задания, которое хочешь добавить', reply_markup=builder.as_markup())


# Добавление элемента
@rt.callback_query(F.data.contains('|add'))
async def add_task(callback: CallbackQuery):
    type_of_task = callback.data.split('|')[0]
    task = task_curr

    tasks = get_task(type_of_task, student)
    try:
        tasks.append(task)
        tasks.save()
        await callback.message.answer('Добавлено успешно')

    except KeyError as e:
        print(e)
        await callback.message.answer('Такое имя уже есть, отправь другое')

    await callback.answer()
