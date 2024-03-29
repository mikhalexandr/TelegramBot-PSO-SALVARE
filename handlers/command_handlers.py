from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
import db
import kb
from states import CommandStates

router = Router()


@router.message(F.text.lower() == "хочу помочь в поисках!")
async def help_message_handler(message: Message, state: FSMContext):
    if db.is_in_team(message.from_user.id):
        await message.answer("Выберите, кому вы хотите и можете помочь", reply_markup=kb.leave_team_kb())
    else:
        await message.answer("Выберите, кому вы хотите и можете помочь", reply_markup=kb.back_kb())
    for args in db.get_all_lost_info():
        await message.answer_photo(args[-1], reply_markup=kb.join_command_kb(args[1]))
    await state.set_state(CommandStates.choosing)
    await state.update_data(id=message.from_user.id)


@router.message(CommandStates.choosing, F.text.lower() == "назад")
async def help_message_handler(message: Message, state: FSMContext):
    await message.answer("Выберите действие", reply_markup=kb.first_choose_kb())
    await state.clear()


@router.message(CommandStates.choosing, F.text.lower() == "покинуть команду")
async def help_message_handler(message: Message):
    db.del_team_member(message.from_user.id)
    await message.answer("Успешно!", reply_markup=kb.back_kb())


@router.message(Command("chat"))
async def send_teammates(message: Message, command: CommandObject, bot: Bot):
    if command.args is None:
        return
    msg = db.get_human(message.from_user.id) + ": " + command.args
    for teammate in db.get_teammates(message.from_user.id):
        if teammate[0]:
            await bot.send_message(teammate[0], msg)


@router.callback_query(CommandStates.choosing)
async def join_team(callback: CallbackQuery, state: FSMContext):
    id = (await state.get_data())["id"]
    db.del_team_member(id)
    db.add_team_member(id, callback.data)
    await callback.answer("Вы успешно присоединились к команде!")
