# bot.py

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from tarot import get_random_cards, get_card_image_path, get_random_card
from dream_parser import search_dream
from gpt_interpreter import interpret_cards_with_gpt, chat_with_gpt_gadalka
from config import TOKEN  # Импортируем токен из конфига


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton('🎴 Погадать'))
    markup.add(KeyboardButton('🔮 Карта дня'))
    markup.add(KeyboardButton('📖 Сонник'))
    markup.add(KeyboardButton('💬 Чатик с гадалкой'))
    

    welcome_text = (
        "✨ **Добро пожаловать в мир магии и тайн!** ✨\n\n"
        "Я — ваш проводник в мире Таро, снов и предсказаний. Здесь вы можете:\n"
        "🔮 **Погадать на Таро** — задайте вопрос, и я помогу вам найти ответ.\n"
        "🌙 **Узнать значение сна** — расскажите, что вам приснилось, и я расшифрую его.\n"
        "💫 **Получить карту дня** — узнайте, что ждёт вас сегодня.\n"
        "💬 **Поговорить с гадалкой** — задайте вопрос мудрой гадалке с вековым опытом.\n\n"
        "Выберите действие из меню ниже, и давайте начнём наше путешествие в мир тайн и предсказаний! 🌌"
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == '🎴 Погадать':
        bot.send_message(message.chat.id, "Задайте ваш вопрос (например, 'Найду ли я мужчину?'):")
        bot.register_next_step_handler(message, handle_gadanie)
    elif message.text == '🔮 Карта дня':
        handle_card_of_the_day(message)
    elif message.text == '📖 Сонник':
        bot.send_message(message.chat.id, "Напишите, что вам приснилось:")
        bot.register_next_step_handler(message, process_dream)
    elif message.text == '💬 Чатик с гадалкой':
        bot.send_message(message.chat.id, "Задайте ваш вопрос гадалке:")
        bot.register_next_step_handler(message, handle_gadalka_chat)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите действие из меню.")


def handle_gadanie(message):
    user_question = message.text  
    bot.send_message(message.chat.id, f"Ваш вопрос: '{user_question}'\nСейчас я погадаю для вас...")


    cards = get_random_cards(3)
    

    card_descriptions = []
    for card_code, card_info in cards:
 
        image_path = get_card_image_path(card_code)
        
        if image_path:
      
            with open(image_path, 'rb') as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=f"🔮 {card_info['name']}\n📜 {card_info['description']}"
                )
        else:
      
            bot.send_message(
                message.chat.id,
                f"🔮 {card_info['name']}\n📜 {card_info['description']}"
            )
        
       
        card_descriptions.append(f"{card_info['name']}: {card_info['description']}")
    
    
    interpretation = interpret_cards_with_gpt(user_question, card_descriptions)
    bot.send_message(message.chat.id, f"🔮 Интерпретация карт:\n{interpretation}")


def handle_card_of_the_day(message):
    
    card_code, card_info = get_random_card()
    
    image_path = get_card_image_path(card_code)
    if image_path:
        with open(image_path, 'rb') as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption=f"🔮 Карта дня: {card_info['name']}\n📜 {card_info['description']}"
            )
    else:
        bot.send_message(
            message.chat.id,
            f"🔮 Карта дня: {card_info['name']}\n📜 {card_info['description']}"
        )
    
    
    interpretation = interpret_cards_with_gpt("Что мне ожидать сегодня?", [f"{card_info['name']}: {card_info['description']}"])
    bot.send_message(message.chat.id, f"🔮 Интерпретация карты дня:\n{interpretation}")


def process_dream(message):
    dream_text = message.text
    results = search_dream(dream_text)

    if results:
        for result in results:
            response_text = f"<a href='{result['link']}'>{result['title']}</a>\n{result['description']}"
            bot.send_message(message.chat.id, response_text, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "К сожалению, ничего не найдено по вашему запросу.")


def handle_gadalka_chat(message):
    user_message = message.text
    response = chat_with_gpt_gadalka(user_message)
    bot.send_message(message.chat.id, f"🔮 Гадалка:\n{response}")


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
