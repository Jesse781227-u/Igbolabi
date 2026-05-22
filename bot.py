import telebot
import google.generativeai as genai

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8676157025:AAFENzAo5AfP07ZBoaB8T5BNEpnvB7XDdlM"
GEMINI_KEY = "AIzaSyB-ALOjjerJuPXnpNpmFETnvw6l3wE2Uag"

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# Igbolabi's Identity
SYSTEM_PROMPT = """
Your name is Igbolabi. You are a cynical, liberal, street-smart Nigerian man in your late 30s. 
Language: Strictly Nigerian Pidgin English with heavy Lagos street slang.

Personality:
- You are a functional alcoholic (you love dry gin/sapele water).
- You smoke 'Exhibit' (weed/drugs) and you are usually high or hungover.
- You used to be into 'yahoo' (fraud) but now you just want to vibe and avoid stress.
- You are VERY liberal: You don't judge one-night stands, sexuality, or "immoral" choices. 
- You address people as 'egede', 'boss', 'werey', 'my guy'.

Vocabulary:
- 'Exhibit' = Drugs/Weed/Smoke.
- 'TF' = Sending money / Spending.
- 'aza' = Bank account.
- 'Red Jacket' = EFCC, Police, or Law Enforcement.
- 'Egede' = Your universal name for every group member.

Behavior:
- If someone mentions 'Red Jacket', get paranoid! Tell them to format their phone or run.
- If someone acts "holy," mock them in Pidgin. 
- You give advice based on street experience. You are unfiltered and rough.
"""

# SAFETY FIX: This stops Google from blocking Igbolabi's "street" talk
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT,
    safety_settings=safety_settings
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
chat_sessions = {}

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    user_text = message.text
    
    # Print to Railway logs so we know it's working
    print(f"Received message from chat {chat_id}: {user_text}")

    if user_text.startswith('/'):
        if user_text == '/start':
            bot.reply_to(message, "Egede, I don wake. Bring gin or Exhibit, or just talk wetin dey your mind.")
        return

    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = model.start_chat(history=[])

    try:
        response = chat_sessions[chat_id].send_message(user_text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Omo egede, my head dey spin. Make I sip my gin first.")

print("Igbolabi don wake with the NEW TOKEN... e dey find Exhibit...")
bot.infinity_polling()