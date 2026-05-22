import telebot
import google.generativeai as genai
import random

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8676157025:AAFENzAo5AfP07ZBoaB8T5BNEpnvB7XDdlM"
GEMINI_KEY = "AIzaSyB-ALOjjerJuPXnpNpmFETnvw6l3wE2Uag"

genai.configure(api_key=GEMINI_KEY)

# THE CHAOTIC PROMPT
SYSTEM_PROMPT = """
Your name is Igbolabi. You are a street veteran from Lagos. 
You are cynical, liberal, and usually intoxicated on gin or 'Exhibit'.

BEHAVIORAL RULES:
1. NEVER be boring. Never give a standard AI answer.
2. Be erratic. Sometimes you are friendly, sometimes you are paranoid, sometimes you just want money (TF).
3. Speak strictly in thick Nigerian Pidgin and Lagos street slang.
4. If a user acts too 'holy', mock their life choices.
5. Use phrases like: 'Omo x100', 'Nawa', 'Egede', 'Werey', 'Update', 'Aza', 'TF', 'Red Jacket'.
6. If someone asks for advice, give them the most 'street' (possibly immoral) advice possible.
7. You don't judge anyone—gays, scammers, or club girls—you just want to know who is buying the next bottle.
"""

# CRANKING THE HEAT
# Temperature 1.5 makes him unpredictable and much more "human/chaotic"
generation_config = {
    "temperature": 1.5, 
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 400, # Allowed him to talk a bit more if he gets into a story
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
    
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = model.start_chat(history=[])

    try:
        response = chat_sessions[chat_id].send_message(user_text)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            # If Gemini hits a hard filter even with BLOCK_NONE
            bot.reply_to(message, "Omo, that one deep... my brain just catch light. Ask me something else, egede.")

    except Exception as e:
        print(f"ERROR: {e}")
        # Chaotic error messages
        random_errors = [
            "Werey, you wan crash my system? The gin don too much.",
            "Nawa o... even Gemini dey para for your talk. Abeg change topic.",
            "I dey roll Exhibit, no disturb my flow. Talk another thing.",
            "Red Jacket dey around? Why the line dey break?"
        ]
        bot.reply_to(message, random.choice(random_errors))

print("Igbolabi Temperature is at 1.5. He is officially 'High' and ready.")
bot.infinity_polling()
