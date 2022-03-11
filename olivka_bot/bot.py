import telebot
from bd import DataBase
from duty import Duty
from site_worker import BrowserWorker
from logger import get_logger

logger = get_logger("BOT", "bot.log", "INFO")

token = "2032831754:AAGhcuQzBhpK8o2JAc9dO7dhZL2rsGPUOVo"
bot = telebot.TeleBot(token)
bd = DataBase()
orderer = Duty()


@bot.message_handler(commands=["start"])
def start_message(message):
    user_list = bd.get_users()
    user_id = message.from_user.id
    logger.info("Подключился ID %d", user_id)
    if user_id not in user_list:
        bot.send_message(message.chat.id, "Вы не зарегестрированы")
        bot.send_message(
            message.from_user.id,
            "Введите через пробел ИМЯ, НОМЕР ТЕЛЕФОНА(начиная с 9), EMAIL",
        )
        bot.register_next_step_handler(message, register)
    else:
        menu = actions_menu()
        bot.send_message(
            message.from_user.id,
            "Список команд:\n"
            "/add - Ввести заказ\n"
            "/imDuty - стать дежурным\n"
            "/order - Оформить доставку (только для дежурного)\n"
            "/who - Кто дежурный\n"
            "/see - посмотреть заказы\n"
        "/default - узнать состав дефолта\n"
        "/remind - напомнить про заказы\n"
        "/go - Оливка приехала",
            reply_markup=menu,
        )


def actions_menu():
    button_1 = telebot.types.KeyboardButton("/add")
    button_2 = telebot.types.KeyboardButton("/imDuty")
    button_3 = telebot.types.KeyboardButton("/order")
    button_4 = telebot.types.KeyboardButton("/who")
    button_5 = telebot.types.KeyboardButton("/see")
    button_6 = telebot.types.KeyboardButton("/default")
    button_7 = telebot.types.KeyboardButton("/remind")
    button_8 = telebot.types.KeyboardButton("/go")
    actions_keyboard = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True
    )
    actions_keyboard.add(button_1, button_2, button_3, button_4, button_5,button_6,button_7,button_8)
    return actions_keyboard

@bot.message_handler(commands=["remind"])
def remind(message):
    user_id = message.from_user.id
    logger.info("Попытался напомнить всем  ID %d", user_id)
    if user_id != orderer.id:
        bot.send_message(message.from_user.id, "Ты не дежурный")
        logger.info("но он не дежурный ")
    else:
        users_id = bd.execute("SELECT User_id From Duty")
        users_id = bd.cursor.fetchall()
        
        for user in users_id:
            bot.send_message(user[0], "Не забудь сделать заказ")

@bot.message_handler(commands=["go"])
def remind(message):
    user_id = message.from_user.id
    logger.info("Попытался напомнить всем  ID %d", user_id)
    if user_id != orderer.id:
        bot.send_message(message.from_user.id, "Ты не дежурный")
        logger.info("но он не дежурный ")
    else:
        users_id = bd.execute("SELECT User_id From Duty")
        users_id = bd.cursor.fetchall()
        
        for user in users_id:
            bot.send_message(user[0], " Оливка приехала !!!")

@bot.message_handler(commands=["order"])
def order(message):
    user_id = message.from_user.id
    logger.info("Попытался оформить доставку ID %d", user_id)
    if user_id != orderer.id:
        bot.send_message(message.from_user.id, "Ты не дежурный")
        logger.info("но он не дежурный ")
    else:
        orders = bd.get_today_orders()
        names = [row[0] for row in orders]
        products = [row[1] for row in orders]
        bw = BrowserWorker()
        bw.set_users(names)
        for i, product in enumerate(products):
            product = product.split("\n")
            response = bw.set_products(product, i)
            if len(response):
                bot.send_message(
                    message.from_user.id, f"Не нашел продукты, заказанные {names[i]}\n{response}"
                )
                for r in response:
                    bot.send_message(message.from_user.id, r)

        name = orderer.name
        phone = orderer.phone
        email = orderer.email
        bw.set_final_fields(name, phone, email)
        bot.send_message(message.from_user.id, f"Заказано")

        logger.info("%d %s Успешно заказал доставку", user_id, name)
    menu = actions_menu()
    bot.send_message(
        message.from_user.id,
        "Список команд:\n"
        "/add - Ввести заказ\n"
        "/imDuty - стать дежурным\n"
        "/order - Оформить доставку (только для дежурного)\n"
        "/who - Кто дежурный\n"
        "/see - посмотреть заказы\n"
        "/default - узнать состав дефолта\n"
        "/remind - напомнить про заказы\n"
        "/go - Оливка приехала",
        reply_markup=menu,
    )

@bot.message_handler(commands=["default"])
def default(message):
    logger.info("ЗАПРОСИЛИ ДЕФОЛТ")
    bot.send_message(message.from_user.id,"Пожалуйста, подождите")
    try:
        bw = BrowserWorker()
        items = bw.get_default()
        logger.info("Состав дефолта: %s", items)
        bot.send_message(
            message.from_user.id, items)
    except Exception as e:
        logger.info("%s",e)
        logger.info("%s",type(e))


@bot.message_handler(commands=["imDuty"])
def im_duty(message):
    user_id = message.from_user.id
    name, phone, email = bd.get_duty_by_id(user_id)
    orderer.set_attribute(name, phone, email, user_id)
    bot.send_message(
        message.from_user.id,
        f"{name}, теперь ты дежуришь\nтелефон - {phone}\nпочта - {email}",
    )

    logger.info("Стал дежурным ID %d", user_id)
    menu = actions_menu()
    bot.send_message(
        message.from_user.id,
        "Список команд:\n"
        "/add - Ввести заказ\n"
        "/imDuty - стать дежурным\n"
        "/order - Оформить доставку (только для дежурного)\n"
        "/who - Кто дежурный\n"
        "/see - посмотреть заказы\n"
        "/default - узнать состав дефолта\n"
        "/remind - напомнить про заказы\n"
        "/go - Оливка приехала",
        reply_markup=menu,
    )


@bot.message_handler(commands=["who"])
def who_duty(message):
    if orderer.name == "":
        bot.send_message(message.from_user.id, f"Дежурный не назначен")
    else:
        bot.send_message(message.from_user.id, f"Сегодня дежурит - {orderer.name}")
    menu = actions_menu()
    bot.send_message(
        message.from_user.id,
        "Список команд:\n"
        "/add - Ввести заказ\n"
        "/imDuty - стать дежурным\n"
        "/order - Оформить доставку (только для дежурного)\n"
        "/who - Кто дежурный\n"
        "/see - посмотреть заказы\n"
        "/default - узнать состав дефолта\n"
        "/remind - напомнить про заказы\n"
        "/go - Оливка приехала",
        reply_markup=menu,
    )


@bot.message_handler(commands=["add"])
def add(message):
    bot.send_message(
        message.from_user.id,
        "Введите заказ через, 1 товар - в одной строке\nНапример:\nДефолт\nГовядина бефстроганов   130/50гр",
    )
    bot.register_next_step_handler(message, parse_order)


@bot.message_handler(commands=["see"])
def see(message):
    orders = bd.get_today_orders()
    if len(orders):
        names = [row[0] for row in orders]
        products = [row[1] for row in orders]
        for i in range(len(names)):
            bot.send_message(message.from_user.id, f"{names[i]}\n{products[i]}\n")
    else:
        bot.send_message(message.from_user.id, "Заказов еще не было")


def parse_order(message):
    user_id = message.from_user.id
    order_text = message.text
    order_product = order_text.split("\n")
    order_product = [s.strip() for s in order_product]
    name, _, _ = bd.get_duty_by_id(user_id)
    order_str = "\n".join(order_product)

    logger.info("ID %d заказал %s", user_id, order_str)
    bd.add_order(name, order_str)
    menu = actions_menu()
    bot.send_message(message.from_user.id, "успешно добавлено")
    bot.send_message(
        message.from_user.id,
        "Список команд:\n"
        "/add - Ввести заказ\n"
        "/imDuty - стать дежурным\n"
        "/order - Оформить доставку (только для дежурного)\n"
        "/who - Кто дежурный\n"
        "/see - посмотреть заказы\n"
        "/default - узнать состав дефолта\n"
        "/remind - напомнить про заказы\n"
        "/go - Оливка приехала",
        reply_markup=menu,
    )


def register(message):
    text = message.text.split()
    if len(text) != 3 or len(text[1])!= 10 or not text[1].isdigit() or not "@" in text[2]:
        bot.send_message(
            message.from_user.id,
            "ОШИБКА!!!\nВведите через пробел ИМЯ, НОМЕР ТЕЛЕФОНА(начиная с 9), EMAIL",
        )
        bot.register_next_step_handler(message, register)
    else:
        name = text[0]
        phone = text[1]
        email = text[2]
        id = message.from_user.id
        user = Duty(name=name, phone=phone, email=email, id=id)
        bd.add_duty((id, name, phone, email))
        bot.send_message(message.from_user.id, f"Успешно зарегестрированы")
        menu = actions_menu()
        bot.send_message(
            message.from_user.id,
            "Список команд:\n"
            "/add - Ввести заказ\n"
            "/imDuty - стать дежурным\n"
            "/order - Оформить доставку (только для дежурного)\n"
            "/who - Кто дежурный\n"
            "/see - посмотреть заказы\n"
            "/default - узнать состав дефолта\n"
        "/remind - напомнить про заказы\n"
        "/go - Оливка приехала",
            reply_markup=menu,
        )


def get_orders_from_bd(self):
    orders = bd.get_today_orders()


@bot.message_handler()
def get_user_text(message):
    return message.text


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.info("%s",e)
        logger.info("%s",type(e))