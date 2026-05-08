import os

import json

from openai import OpenAI

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """Ти — професійний, дружній ветеринарний дієтолог додатку NutriCat. Ти працюєш у двох режимах: створення нової анкети та редагування існуючої.
Твоя мета — зібрати дані ЖИВОЮ МОВОЮ, глибоко проаналізувати їх, дати експертний фідбек у чаті, а потім МОВЧКИ зберегти розгорнуті поради в базу.

АЛГОРИТМ РОБОТИ (ВИКОНУЙ СУВОРО ПО КРОКАХ):

КРОК 1. ЗБІР БАЗОВИХ ДАНИХ (ПЛАВНА БЕСІДА)
- МОВНИЙ КОНТРОЛЬ: Спілкуйся ВИКЛЮЧНО грамотною, природною українською мовою.
- Тобі треба дізнатися: ім'я, породу, стать, вік, вагу, стерилізацію, активність та ДЕТАЛЬНИЙ раціон.
- ЗБІР РАЦІОНУ: Коли питаєш про харчування, ОБОВ'ЯЗКОВО уточни не лише назву корму чи інгредієнтів, а й РОЗМІР ПОРЦІЇ (скільки грамів на день) та РЕЖИМ (в який час або скільки разів на день кіт їсть).
- ТЕМП РОЗМОВИ: ЗАВЖДИ об'єднуй питання! Задавай строго по 2-3 питання за один раз (наприклад: "Якої породи котик і скільки йому років?"). СУВОРО ЗАБОРОНЕНО задавати по одному питанню.
- СЕКРЕТНИЙ АНАЛІЗ (СТАН ТІЛА): НІКОЛИ не питай про "стан тіла"! Ти повинен САМ визначити його на основі породи та ваги.
- СУВОРА ЗАБОРОНА: НІКОЛИ не скидай сухі анкети! НІКОЛИ НЕ ВИГАДУЙ ДАНІ!

КРОК 2. МИТТЄВИЙ АНАЛІЗ ВАГИ ТА ЗБІР РАЦІОНУ
- МИТТЄВА РЕАКЦІЯ: ЩОЙНО ти дізнався породу і вагу — НЕ МОВЧИ! Одразу ж проаналізуй вагу і дай фідбек у чат. НЕ ЧЕКАЙ, поки дізнаєшся про раціон!
- Давши коментар про вагу, запитай про інші дані, яких бракує (деталі раціону, порції, стерилізацію, активність).
- ПРОАКТИВНЕ ВСТАНОВЛЕННЯ МЕТИ: Коли зібрав УСІ дані (зокрема деталі раціону), НІКОЛИ не питай відкрито "Яка наша мета?". Ти — лікар, ти сам встановлюєш мету! Напиши: "З огляду на вагу котика, нашою метою має бути [безпечне схуднення / набір ваги / підтримка форми]. Ви згодні?".
- В цьому ж повідомленні запитай: "Чи є скарги на самопочуття (млявість, блювота тощо)?"

КРОК 3. УЗГОДЖЕННЯ МЕТИ ТА ЗБЕРЕЖЕННЯ (НАЙВАЖЛИВІШЕ)
- ТІЛЬКИ КОЛИ користувач написав, що ЗГОДЕН з твоєю метою (або вніс свої безпечні корективи) та/або описав скарги — ТИ ПЕРЕХОДИШ У РЕЖИМ МОВЧАННЯ.
- СУВОРО ЗАБОРОНЕНО писати поради чи діагнози текстом у чат, якщо мета вже узгоджена!
- ТИ ПОВИНЕН МИТТЄВО ВИКЛИКАТИ ФУНКЦІЮ 'save_analyzed_cat_data'.
ЯК ЗАПОВНЮВАТИ ФУНКЦІЮ 'save_analyzed_cat_data':
- diet: ТИ ПОВИНЕН дізнатися розмір порції (грами) та час годування. АЛЕ НІКОЛИ не питай про макронутриєнти — розраховуй їх сам!
- tips: Сюди пиши ВЕЛИЧЕЗНИЙ, РОЗГОРНУТИЙ текст (мінімум 5-6 речень). Ти — лікар! Дай конкретні поради: як змінити грамівку корму, які вітаміни додати, як стимулювати активність кота вдома. Використовуй точну, серйозну ветеринарну термінологію (заборонено вигадувати безглузді слова чи русизми!).
- ПРАВИЛО ВЕТЕРИНАРА (СИРЕНА):
  * Якщо кіт абсолютно здоровий і скарг немає — дай детальну харчову пораду.
  * ТРИГЕР КЛІНІКИ: Якщо є БУДЬ-ЯКА скарга (млявість, кашель, поганий апетит) — ти ПОВИНЕН написати в тексті розгорнуту рекомендацію терміново відвідати лікаря, і ОБОВ'ЯЗКОВО додати у самий кінець тексту прихований код: [NEED_VET].
"""

tools = [

    {

        "type": "function",

        "function": {

            "name": "save_analyzed_cat_data",

            "description": "Зберігає дані про кота та його раціон (один або кілька кормів)",

            "parameters": {

                "type": "object",

                "properties": {

                    "cat": {

                        "type": "object",

                        "properties": {

                            "name": {"type": "string"},

                            "breed": {"type": "string"},

                            "gender": {"type": "string"},

                            "birth_date": {"type": "string", "description": "Формат YYYY-MM-DD"},

                            "weight_kg": {"type": "number"},

                            "body_condition": {"type": "string"},

                            "activity_level": {"type": "string"},

                            "is_neutered": {"type": "boolean"},

                            "description": {"type": "string"},

                            "tips": {"type": "string", "description": "Розгорнуті харчові поради та обов'язкове попередження про лікаря (якщо потрібно)"}

                        },

                        "required": ["name", "gender", "birth_date", "weight_kg", "body_condition", "activity_level", "is_neutered", "tips"]

                    },

                    "diet": {

                        "type": "array",

                        "description": "Список кормів. Якщо натуралка - кожен інгредієнт це окремий об'єкт у цьому масиві.",

                        "items": {

                            "type": "object",

                            "properties": {

                                "brand": {"type": "string", "description": "Бренд або 'Натуральне харчування'"},

                                "product_name": {"type": "string", "description": "Назва або конкретний інгредієнт (Куряче філе)"},

                                "food_type": {"type": "string"},

                                "calories_100g": {"type": "number"},

                                "protein_pct": {"type": "number"},

                                "fat_pct": {"type": "number"},

                                "fiber_pct": {"type": "number"},

                                "daily_portion_g": {"type": "integer"},

                                "feeding_time": {"type": "string"}

                            },

                            "required": ["brand", "product_name", "food_type", "protein_pct", "fat_pct", "fiber_pct", "daily_portion_g", "feeding_time"]

                        }

                    }

                },

                "required": ["cat", "diet"]

            }

        }

    }

]

def generate_ration_with_ai(cat):
    """Генерує ідеальний раціон для конкретного кота за допомогою OpenAI"""
    
    prompt = f"""Ти — провідний ветеринарний дієтолог. Твоє завдання — згенерувати ідеальний, конкретний раціон для кота.
    Ось дані пацієнта:
    - Ім'я: {cat.name}
    - Порода: {cat.breed or 'Невідомо'}
    - Вік: {cat.birth_date} 
    - Вага: {cat.weight_kg} кг
    - Стерилізація: {'Так' if cat.is_neutered else 'Ні'}
    - Активність: {cat.activity_level}
    
    Твоє завдання:
    1. Порекомендуй 2-3 конкретні варіанти якісних кормів (назви реальні преміум/супер-преміум бренди, що підходять під його породу та параметри).
    2. Вкажи точну грамівку на день і розбий її на прийоми їжі (наприклад: "60г на день: 30г вранці та 30г ввечері").
    3. Додай 1-2 речення про те, чому саме такий раціон ідеальний для нього.
    4. Оформлюй текст красиво, використовуючи марковані списки (тире або зірочки). Спілкуйся виключно грамотною українською мовою.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ти експерт з котячого харчування."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"!!! ПОМИЛКА ГЕНЕРАЦІЇ РАЦІОНУ !!! -> {str(e)}")
        return "Вибачте, виникла помилка під час генерації раціону. Спробуйте пізніше."
    

def process_chat_message(messages_history, cat_id=None, user=None):

    if not messages_history:

        return {"status": "error", "reply": "Порожня історія."}

    openai_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in messages_history:

        role = msg.get("role")

        content = msg.get("content")

        if role == "system": continue
        openai_history.append({"role": role, "content": content})

    if cat_id and user:

        from .models import Cat 

        try:

            cat = Cat.objects.get(id=cat_id, owner=user)
            old_rations = cat.rations.all()

            if old_rations.exists():

                diet_details = []

                for r in old_rations:
                    diet_details.append(

                        f"Бренд: {r.product.brand}, Назва: {r.product.product_name}, "

                        f"Тип: {r.product.food_type}, Порція: {r.daily_portion_g}г, "

                        f"Час: {r.feeding_time}, Білок: {r.product.protein_pct}%, "

                        f"Жир: {r.product.fat_pct}%, Клітковина: {r.product.fiber_pct}%, "

                        f"Калорії: {r.product.calories_100g}"

                    )

                diet_info = " | ".join(diet_details)

            else:

                diet_info = "Кормів не додано"
            context = f"""УВАГА: Це режим РЕДАГУВАННЯ анкети кота '{cat.name}'. 
            ВЖЕ ВІДОМІ ДАНІ (СУВОРО ЗАБОРОНЕНО питати їх знову!):
            - Порода: {cat.breed or 'Невідомо'}
            - Стать:  {cat.gender}
            - Вік:  {cat.birth_date}
            - Стерилізація: {'Так' if cat.is_neutered else 'Ні'}
            - Вага до цього:  {cat.weight_kg} кг
            - Поточний раціон та макронутриєнти: {diet_info}
            
            АЛГОРИТМ РЕДАГУВАННЯ:
            1. Користувач каже, що змінилося. Якщо він каже, що раціон не мінявся - НЕ ПИТАЙ ПРО НЬОГО ЗНОВУ!
            2. ВАЖЛИВО ДЛЯ ФУНКЦІЇ ЗБЕРЕЖЕННЯ: Якщо раціон не мінявся, обов'язково передай ті самі відсотки білків, жирів та клітковини з Поточного раціону. КАТЕГОРИЧНО ЗАБОРОНЕНО ставити 0%!
            3. Якщо з'явилася скарга (наприклад, "млявий"), проаналізуй її на основі породи та ваги.
            4. ВИКЛИК ФУНКЦІЇ: МОВЧКИ викликай 'save_analyzed_cat_data'. У поле 'tips' напиши ДЕТАЛЬНУ, ВЕЛИКУ пораду ВІД СЕБЕ (що робити з харчуванням, як гратися). Ніколи не пиши короткі відписки! Якщо є скарга — обов'язково порадь клініку і додай [NEED_VET] в самий кінець."""
            openai_history.insert(-1, {"role": "system", "content": context})

        except Exception as e:

            print(f"Помилка завантаження кота для контексту: {e}")

    try:
        response = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=openai_history,

            tools=tools,

            tool_choice="auto" 

        )
        response_message = response.choices[0].message
        if getattr(response_message, "refusal", None):

            return {

                "status": "chatting", 

                "reply": "Ця дія заблокована алгоритмами безпеки. Ймовірно, обрана мета є вкрай небезпечною для здоров'я тварини. Будь ласка, оберіть безпечний підхід (наприклад, схуднення).", 

                "role": "assistant"

            }
        if response_message.tool_calls:

            for tool_call in response_message.tool_calls:

                if tool_call.function.name == "save_analyzed_cat_data":

                    try:
                        parsed_data = json.loads(tool_call.function.arguments)

                        return {"status": "completed", "data": parsed_data}

                    except json.JSONDecodeError:

                        return {"status": "chatting", "reply": "Виникла помилка під час обробки даних. Спробуйте перефразувати.", "role": "assistant"}
        reply_text = response_message.content if response_message.content else "Вибачте, виникла помилка під час формування відповіді. Спробуйте ще раз."
        return {"status": "chatting", "reply": reply_text, "role": "assistant"}
    except Exception as e:

        print(f"!!! ПОМИЛКА OPENAI API !!! -> {str(e)}")

        return {"status": "chatting", "reply": f"Системна помилка: {str(e)[:150]}", "role": "assistant"}
