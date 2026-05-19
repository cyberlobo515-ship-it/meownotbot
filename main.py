import telebot
import random
import re

TOKEN = "8782247014:AAENLQf7rJhEBNKdJz-oNJkYm9N5tnBTqBQ"  # BotFather dan token qo'ying
bot = telebot.TeleBot(TOKEN)

# O'zbekcha javoblar bazasi
responses = {
    "salom": [
        "Assalomu alaykum! 😊",
        "Salom! Xush kelibsiz! 🤗",
        "Hey! Qalay? 🌟"
    ],
    "qalay": [
        "Rahmat, yaxshi! Sizchi? 😊",
        "A'lo! Yordam kerakmi? 👍",
        "Zo'r! Savolingiz bormi? 💡"
    ],
    "raxmat": [
        "Marhamat! 🤝",
        "Arzimaydi! 😊",
        "Doim yordamga tayyorman! 💪"
    ],
    "xayr": [
        "Xayr! Yana keling! 👋",
        "Salomat bo'ling! 🌟",
        "Ko'rishguncha! 😊"
    ]
}

# Matematik amallar
def calculate(text):
    # Qo'shish
    if '+' in text and not '/' in text and not '*' in text:
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2:
            result = sum(int(n) for n in numbers[:2])
            return f"{numbers[0]} + {numbers[1]} = {result} ✅"

    # Ayirish
    if '-' in text and text.count('-') == 1:
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2:
            result = int(numbers[0]) - int(numbers[1])
            return f"{numbers[0]} - {numbers[1]} = {result} ✅"

    # Ko'paytirish
    if '*' in text or 'x' in text.lower():
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2:
            result = int(numbers[0]) * int(numbers[1])
            return f"{numbers[0]} × {numbers[1]} = {result} ✅"

    # Bo'lish
    if '/' in text:
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2 and int(numbers[1]) != 0:
            result = int(numbers[0]) / int(numbers[1])
            return f"{numbers[0]} ÷ {numbers[1]} = {result:.2f} ✅"

    return None

# Topishmoqlar
riddles = [
    {"q": "Nima bir ko'zli, lekin ko'rmaydi?", "j": "igna"},
    {"q": "Qor yog'ayotgan edi, bir quyon keldi. Uning tagida nima bor?", "j": "qor"},
    {"q": "Bir tuxum qaynatilsa 5 daqiqa, 10 ta tuxum qancha vaqtda qaynatiladi?", "j": "5"},
    {"q": "Dunyoda eng baland nima?", "j": "tog'"},
    {"q": "Qo'lingda ushlab bo'lmaydigan narsa nima?", "j": "tutun"},
]

user_riddle = {}

# O'zbekcha so'zlar lug'ati
uzbek_words = {
    "olma": "Olma - meva. Ranglari qizil, yashil, sariq bo'ladi. 🍎",
    "non": "Non - eng muhim oziq-ovqat. O'zbeklarda non juda qadrlanadi. 🍞",
    "suv": "Suv - hayot manbai. 💧",
    "kitob": "Kitob - bilim manbai. 📚",
    "maktab": "Maktab - o'quvchilar bilim oladigan joy. 🏫",
    "o'qituvchi": "O'qituvchi - bilim beradigan inson. 👩‍🏫",
    "do'st": "Do'st - qiyin paytda yordam beradigan inson. 👫"
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """
🤖 *O'ZBEK AI BOT*

Men oddiy botman, lekin juda ko'p narsani bilaman!

📚 *Buyruqlar:*
/salom - Salomlashish
/topishmoq - Topishmoq beraman
/lugat [so'z] - So'z ma'nosini bilish
/yordam - Yordam

💡 *Men nima qila olaman?*
- Matematik misollar: 5+5, 10-3, 4*6, 20/4
- Topishmoqlar
- So'z ma'nolari
- Oddiy suhbat

✍️ *Istalgan savolingizni yozing!*
""", parse_mode='Markdown')

@bot.message_handler(commands=['yordam'])
def help_command(message):
    bot.reply_to(message, """
📖 *Yordam:*

/matematika 5+5 - Hisoblash
/topishmoq - Topishmoq olish
/lugat olma - So'z ma'nosi
/salom - Salomlashish

Yoki oddiygina "5+5" deb yozing ham hisoblaydi!
""", parse_mode='Markdown')

@bot.message_handler(commands=['salom'])
def say_hello(message):
    bot.reply_to(message, random.choice(responses["salom"]))

@bot.message_handler(commands=['topishmoq'])
def send_riddle(message):
    riddle = random.choice(riddles)
    user_riddle[message.chat.id] = riddle
    bot.reply_to(message, f"❓ *Topishmoq:*\n\n{riddle['q']}\n\nJavob: /javob [javobingiz]", parse_mode='Markdown')

@bot.message_handler(commands=['javob'])
def check_riddle(message):
    chat_id = message.chat.id
    if chat_id not in user_riddle:
        bot.reply_to(message, "❌ Avval /topishmoq bering!")
        return

    answer = message.text.replace('/javob', '').strip().lower()
    correct = user_riddle[chat_id]['j'].lower()

    if answer == correct:
        bot.reply_to(message, f"✅ *To'g'ri!* 🎉\nJavob: {correct}", parse_mode='Markdown')
    else:
        bot.reply_to(message, f"❌ *Xato!* 😔\nTo'g'ri javob: {correct}", parse_mode='Markdown')

    del user_riddle[chat_id]

@bot.message_handler(commands=['matematika'])
def math_command(message):
    expr = message.text.replace('/matematika', '').strip()
    result = calculate(expr)
    if result:
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "❌ Misolni to'g'ri yozing!\nMasalan: /matematika 5+5")

@bot.message_handler(commands=['lugat'])
def dictionary(message):
    try:
        word = message.text.replace('/lugat', '').strip().lower()
        if word in uzbek_words:
            bot.reply_to(message, f"📖 *{word.capitalize()}:*\n{uzbek_words[word]}", parse_mode='Markdown')
        else:
            bot.reply_to(message, f"❌ '{word}' so'zi lug'atda yo'q. Hozircha faqat: {', '.join(uzbek_words.keys())}")
    except:
        bot.reply_to(message, "❌ /lugat olma - so'z ma'nosini bilish")

# Asosiy xabarlarga javob
@bot.message_handler(func=lambda message: True)
def reply_all(message):
    text = message.text.lower()

    # Matematik hisoblash
    math_result = calculate(text)
    if math_result:
        bot.reply_to(message, math_result)
        return

    # Topishmoq so'ralsa
    if "topishmoq" in text:
        riddle = random.choice(riddles)
        user_riddle[message.chat.id] = riddle
        bot.reply_to(message, f"❓ {riddle['q']}\n\n/javob javobingiz")
        return

    # Lug'at so'ralsa
    for word in uzbek_words:
        if f"{word} nima" in text or f"'{word}' degani nima" in text:
            bot.reply_to(message, f"📖 {uzbek_words[word]}")
            return

    # Salomlashish
    if any(word in text for word in ['salom', 'assalom', 'alaykum', 'hello', 'hi']):
        bot.reply_to(message, random.choice(responses["salom"]))
    elif any(word in text for word in ['qalay', 'yaxshimisiz', 'ahvol']):
        bot.reply_to(message, random.choice(responses["qalay"]))
    elif any(word in text for word in ['rahmat', 'tashakkur', 'thanks']):
        bot.reply_to(message, random.choice(responses["raxmat"]))
    elif any(word in text for word in ['xayr', 'bay', 'bye']):
        bot.reply_to(message, random.choice(responses["xayr"]))
    elif "isming nima" in text:
        bot.reply_to(message, "Mening ismim 'O'zbek AI Bot'! 🤖")
    elif "qachon ishlaysan" in text or "24/7" in text:
        bot.reply_to(message, "Men 24/7 ishlayman! Hech qachon uxlamayman! 😎")
    else:
        bot.reply_to(message, f"🤔 {message.from_user.first_name}, men sizni tushunmadim.\n/yordam yozing, yordam beraman!")

print("🚀 Bot ishga tushdi! API kerak emas!")
print("Bot: @your_bot_username")
bot.infinity_polling()
