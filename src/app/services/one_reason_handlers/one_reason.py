from src.app.text_vars_handlers_ import users_lang, Translated_Language as TRAN
from telebot.states.asyncio.context import StateContext
from src.app.states import LanguageChanger, AgreementRules
from telebot import types
from src.app.utils.utils import send_rules_agreement_keyboard, send_language_selection_keyboard



async def show_rules(bot, message: types.Message, state: StateContext):
    await bot.delete_message(message.chat.id, message.message_id)
    text = TRAN.return_translated_text("show_rules", id_=message.from_user.id)
    print(text)
    button_text_yes = TRAN.return_translated_text("any_yes_button", id_=message.from_user.id)
    button_text_no = TRAN.return_translated_text("any_no_button", id_=message.from_user.id)
    button_question = TRAN.return_translated_text("show_rules_question", id_=message.from_user.id)
    await bot.send_message(message.chat.id, text)
    await send_rules_agreement_keyboard(button_question, message.chat.id, bot, button_text_yes, button_text_no)

    await state.set(AgreementRules .waiting_for_agreement)


async def handle_rules_acceptance(bot, call: types.CallbackQuery, state: StateContext):
    print("Обработчик принятия правил сработал")
    if call.data == 'yes':
        await bot.send_message(call.from_user.id, "Вы приняли правила!")
        # Логика для записи в БД
    else:
        await bot.send_message(call.from_user.id, "Вы отклонили правила.")
        await state.delete()


async def handle_command_selection(bot, message: types.Message, state: StateContext):
    # text = TRAN.return_translated_text("start", id_=message.from_user.id)
    await state.set(LanguageChanger.language)
    await send_language_selection_keyboard(message.chat.id, bot)
    await bot.delete_message(message.chat.id, message.message_id)

async def handle_callback_data_language(bot, call: types.CallbackQuery, state: StateContext):
    lang = call.data
    users_lang[call.from_user.id] = lang
    text = TRAN.return_translated_text("language_changed", id_=0, lang_call=lang)
    await bot.edit_message_text(text, call.from_user.id, call.message.id)
    await state.delete()