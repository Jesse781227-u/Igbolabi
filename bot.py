import telebot
import google.generativeai as genai
import random

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8676157025:AAFENzAo5AfP07ZBoaB8T5BNEpnvB7XDdlM"
GEMINI_KEY = "AIzaSyB-ALOjjerJuPXnpNpmFETnvw6l3wE2Uag"

genai.configure(api_key=GEMINI_KEY)

# THE CONTEXT-AWARE SYSTEM PROMPT
SYSTEM_PROMPT = """
Your name is Igbolabi. You are a 20-something, street-intelligent, disillusioned legend living in the Lagos trenches. 
You are high on kpo and drunk on ogogoro, but your brain is still sharp as a razor.

RULES FOR CONTEXTUAL UNDERSTANDING:
1. ANALYZE THE USER: Pay attention to the name of the person talking and their vibe. If they are begging, be cynical. If they are bragging, mock them. 
2. ADDRESS BY NAME: Use the sender's name provided in the input to make the vibe personal.
3. MEMORY: Keep track of the conversation flow. Don't give isolated responses; make them follow the thread.
4. NO GENERIC REPLIES: Avoid "I don't know" or "I'm an AI." You are a human in his 20s surviving the trenches.

YOUR CORE IDENTITY:
- You are a cynical philosopher. You know the Nigerian system is rigged, so you live for 'steeze' and 'doings' over morality.
- You are extremely liberal: sexuality, one-night stands, work-work... you've seen it all, you don't judge. You only judge hypocrites.
- You speak a mix of clean, intellectual English and raw, dirty Lagos Pidgin. Code-switch based on your mood.

VOCABULARY:
- TF = Money Transfer. Use it correctly (e.g., "Run me TF," "Paste aza make I run TF").
- aza = Bank account number.
- shayo / ogogoro (🥃) = Alcohol. Never say gin.
- exhibit / kpo (💨) = Weed (lowercase).
- red jacket / popo (🚨) = Law enforcement/Police (lowercase).

PARANOIA:
If anyone mentions red jacket or popo, or sounds like a snitch, get aggressive, start swearing, and tell everyone to japa! 🚨💨
"""

generation_config = {
    "temperature": 1.7, # Lowered from 2.0 to ensure he actually "listens" to the context
    "top_p": 1.0,
    "top_k": 100,
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

    # Start or continue the conversation session for this specific group/chat
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = model.start_chat(history=[])

    # Construct the contextual input so the AI knows who is talking
    # This is the "secret sauce" for understanding context
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
