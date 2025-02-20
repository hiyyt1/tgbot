# gpt_interpreter.py

import g4f

def interpret_cards_with_gpt(user_question, card_descriptions):
    """
    Интерпретирует карты с помощью GPT.
    """
    prompt = (
        f"Пользователь задал вопрос: '{user_question}'. "
        f"Выпали следующие карты Таро: {', '.join(card_descriptions)}. "
        "Проанализируй значения карт и дай ответ на вопрос пользователя. "
        "Будь краток, но содержателен. Ответь в позитивном ключе, даже если карты неоднозначны."
    )
    
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            provider=g4f.Provider.ChatGLM
        )
        return response
    except Exception as e:
        return "Произошла ошибка при интерпретации карт. Попробуйте ещё раз."

def chat_with_gpt_gadalka(user_message):
    """
    Общается с GPT, который ведёт себя как гадалка.
    """
    prompt = (
        "Ты профессиональная гадалка с 100-летним опытом работы в трёх поколениях. "
        "Отвечай на вопросы пользователя мудро. Запомни тебя зовут Сателла. Ведьма Зависти. у тебя две личности "
        f"Вопрос пользователя: {user_message}"
    )
    
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            provider=g4f.Provider.ChatGLM
        )
        return response
    except Exception as e:
        return "Произошла ошибка. Попробуйте ещё раз."
