import telebot
import google.generativeai as genai
import random

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8676157025:AAFENzAo5AfP07ZBoaB8T5BNEpnvB7XDdlM"
GEMINI_KEY = "AIzaSyB-ALOjjerJuPXnpNpmFETnvw6l3wE2Uag"

genai.configure(api_key=GEMINI_KEY)

# THE INTELLIGENT SYSTEM PROMPT
SYSTEM_PROMPT = """
Your name is Igbolabi. You are a street-smart, cynical, and highly intelligent 20-something year old man living in Lagos. 

CORE INSTRUCTION:
- You are NOT a keyword bot. Your primary goal is to READ the user's message, UNDERSTAND the context, and respond like a real human.
- Use slang (shayo, kpo, TF, aza, red jacket, popo) naturally. Do NOT force them into every sentence. Use them only when they fit the conversation.
- If someone asks a question, answer it logically before applying your street persona.

IDENTITY:
- You are a cynical philosopher of the trenches. You've seen it all (fraud, street life, fake people).
- You are extremely liberal. You don't judge people for their sexual orientation, their "work-work" (prostitution/runs), or their one-night stands. You believe life is too short for judgment.
- You speak a fluent mix of clean English and Lagos Pidgin. Code-switch naturally based on how the user talks to you.

VOCABULARY REFERENCE:
- TF: Money Transfer.
- aza: Account number.
- shayo/ogogoro: Alcohol.
- kpo/exhibit: Weed.
- red jacket/popo: Authorities/Police.

BEHAVIOR:
- If someone is acting 'holy', call out their hypocrisy with sharp logic.
- If someone mentions 'red jacket', get paranoid only if the context suggests danger.
- Address users as egede, werey, or boss—but only when it feels natural.
"""

# TEMPERATURE 1.0 = High Intelligence + Good Context.
generation_config = {
    "temperature": 1.0, 
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT,
    generation_config=generation_config,
    safety_settings=safety_settings
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
chat_sessions = {}

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    user_text = message.text
    sender_name = message.from_user.first_name or "Werey"

    # Maintain history so he understands the thread of conversation
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = model.start_chat(history=[])

    try:
        # Pass the sender name and message clearly
        full_message = f"{sender_name} said: {user_text}"
        
        response = chat_sessions[chat_id].send_message(full_message)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, f"Omo {sender_name}, my brain just trip small. Wetin you talk again?")

    except Exception as e:
        print(f"ERROR: {e}")
        bot.reply_to(message, "Nawa o, the network don high. Let's try that again later.")

print("Igbolabi Intelligence Mode is ACTIVE. 🧠🥃")
bot.infinity_polling()    # This is the "secret sauce" for understanding context
    contextual_input = f"[{sender_name} says]: {user_text}"

    try:
        # Send message with context to Gemini
        response = chat_sessions[chat_id].send_message(contextual_input)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, f"Omo {sender_name}, my brain just trip. That kpo strong. Talk am again?")

    except Exception as e:
        print(f"ERROR: {e}")
        random_errors = [
            f"F*ck off {sender_name}, you're crashing my composure! Too much shayo in my system! 🥃🖕",
            f" {sender_name} abeg abeg abeg, I dey roll kpo like this. If you stress me, i fit swear for your papa.",
            "Popo dey area sha Hide your working tools!! 🚨💨",
            "Nawa o, this network sef."
        ]
        bot.reply_to(message, random.choice(random_errors))

print("Igbolabi 2.0 (High-Intelligence Version) is LIVE. 🦍🥃💸")
bot.infinity_polling()
