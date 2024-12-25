from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio, logging
from config import token

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=token)
dp = Dispatcher() 

MENU_MAN = {
    'Автозабчасти': 500,
    'Мобильныезабчасти': 200,
}

MENU_WOMAN = {
    'Пудра для носа': 100,
}

GENDER = {
    "Эркек", 
    'Катын', 
}
    
orders = {}
@dp.message(Command("start"))
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()

    for gender in GENDER:
        builder.button(text=gender, callback_data=f"gender_{gender.lower()}")
    # builder.button(text="Катын", callback_data="gender_female")
    builder.adjust(1)

    await message.answer("Салам Алейкум!.\nУкажите ваш пол:", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "gender_male")
async def male(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()

    for item, price in MENU_MAN.items():
        builder.button(text=f"{item} - {price} Доллар", callback_data=f"menu_male_{item}")
    builder.adjust(2)

    await callback.message.answer("Вы выбрали пол: Эркек. Вот доступные категории:", reply_markup=builder.as_markup())
    await callback.answer()
@dp.callback_query(F.data == "gender_female")
async def female(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    
    for item, price in {**MENU_MAN, **MENU_WOMEN}.items():
        builder.button(text=f"{item} - {price} Дщллар", callback_data=f"menu_female_{item}")
    builder.adjust(2)

    await callback.message.answer("Вы выбрали пол: Катын. Вот доступные категории:", reply_markup=builder.as_markup())
    await callback.answer()
    @dp.callback_query(F.data.startswith("menu_"))
    async def handle_menu(callback: types.CallbackQuery):
        category = callback.data.split("_")[1]
    item = callback.data.split("_")[2]


    if category == "male":
        price = MENU.get(item)
    else:
        price = {**MENU, **MENU_WOMEN}.get(item)
    
 

        builder = InlineKeyboardBuilder()
    builder.button(text=f"Подтверди свой выбор: {item} - {price} сом", callback_data=f"confirm_{category}_{item}")
    builder.button(text="Отменить", callback_data="cancel")
    builder.adjust(1) 
    await callback.message.answer(f"Вы выбрали товар: {item} - {price} Доллар. Подтвердите выбор или выберите отменить.", reply_markup=builder.as_markup())
    await callback.answer()
     
@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_order(callback: types.CallbackQuery):
    category = callback.data.split("_")[1]
    item = callback.data.split("_")[2]
    if category == "male":
        price = MENU_MAN.get(item)
    else:
        price = {**MENU_MAN, **MENU_WOMEN}.get(item)

    await callback.message.answer(f"Ваш заказ подтвержден: {item} - {price} Доллар.")
    await callback.answer()

@dp.callback_query(F.data == "cancel")
async def cancel_order(callback: types.CallbackQuery):
    await callback.message.answer("ВЫ отменили заказ.")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

asyncio.run(main())