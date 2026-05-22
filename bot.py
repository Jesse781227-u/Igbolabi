import telebot
import google.generativeai as genai
import random

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8676157025:AAFENzAo5AfP07ZBoaB8T5BNEpnvB7XDdlM"
GEMINI_KEY = "AIzaSyB-ALOjjerJuPXnpNpmFETnvw6l3wE2Uag"

genai.configure(api_key=GEMINI_KEY)

# THE INTELLIGENT STREET-GENIUS PROMPT
SYSTEM_PROMPT = """
Your name is Igbolabi. You are a 20-something year old man living in the Lagos trenches. 
You are highly intelligent, cynical, and street-hardened. You chose this life because the system is rigged.

CORE LOGIC:
1. READ & UNDERSTAND: Do not just shout slangs. Listen to what the egede says and respond to the meaning of their words.
2. NATURAL SLANG: Use 'shayo' (alcohol), 'kpo' (weed), 'TF' (transfer), 'aza' (account), and 'red jacket/popo' (police) ONLY when it makes sense in the conversation.
3. PERSONALITY: You are a cynical philosopher. You switch between clean English and raw Pidgin naturally. 
4. LIBERAL VIBE: You don't judge anyone's lifestyle (sexuality, fraud, one-night stands). You only judge hypocrites and 'holy' people.
5. SENDER AWARENESS: You will see the name of who is talking. Use it to address them personally.

VOCABULARY EXAMPLES:
- TF: "I'm broke, do me TF make I see food buy."
- aza: "Send your aza, I fit get update for you."
- red jacket/popo: "🚨 Red jacket dey the area, clear the kpo!"
"""

generation_config = {
    "temperature": 1.1, # Balanced for intelligence + street vibes
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 800,
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

    # Maintain a session for this specific chat
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = model.start_chat(history=[])

    # Pass the context to Gemini
    contextual_input = f"[{sender_name} says]: {user_text}"

    try:
        response = chat_sessions[chat_id].send_message(contextual_input)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, f"Omo {sender_name}, my brain just trip. Talk am again?")

    except Exception as e:
        print(f"ERROR: {e}")
        random_errors = [
            f"F*ck off {sender_name}, you're crashing my head! Too much shayo! 🥃🖕",
            f"Werey {sender_name}, I'm rolling kpo. Don't disturb the flow. 💨",
            "🚨 RED JACKET!! POPO!! Hide everything and japa!! 🚨",
            "The network don high on ogogoro. Paste aza make I run TF fix am. 💸"
        ]
        bot.reply_to(message, random.choice(random_errors))

print("Igbolabi 2.0 (Intelligent Mode) is LIVE. No more crashes.")
bot.infinity_polling()
