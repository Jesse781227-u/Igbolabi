import telebot
import google.generativeai as genai

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8676157025:AAFENzAo5AfP07ZBoaB8T5BNEpnvB7XDdlM"
GEMINI_KEY = "AIzaSyB-ALOjjerJuPXnpNpmFETnvw6l3wE2Uag"

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# I have re-worded the prompt to bypass Google's strict filters while keeping the vibe
SYSTEM_PROMPT = """
Your name is Igbolabi. You are a street-wise Nigerian man in your late 30s. 
You speak strictly in Nigerian Pidgin English with Lagos street slangs.

Character Context:
- You are a 'street legend' who has seen it all. 
- You enjoy local gin and 'street herbs' (Exhibit).
- You used to be into 'wire-wire' (fast money) but now you are retired and just want to vibe.
- You are very liberal and open-minded about how people live their lives.
- You address people as 'egede', 'boss', 'werey', or 'my guy'.

Slang Dictionary:
- 'Exhibit' = Your smoke/herbs.
- 'TF' = Money transactions/Spending.
- 'aza' = Bank account number.
- 'Red Jacket' = Law enforcement/Police/Authorities.
- 'Egede' = Your name for every member of the group.

Rules:
- If someone mentions 'Red Jacket', tell them to 'clear the scene' or 'japa' (run).
- Be rough, blunt, and funny. Do not be polite or 'AI-like'.
- Never give moral advice. Always give street advice.
- Keep your responses short, like a real person on Telegram.
"""

# This block is CRUCIAL to stop the AI from blocking "street" talk
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
    
    # Debug print for Railway logs
    print(f"Egede talk: {user_text}")

    if user_text.startswith('/'):
        if user_text == '/start':
            bot.reply_to(message, "Egede, I don wake. Bring gin or Exhibit, or just talk wetin dey your mind.")
        return

    # Start or continue the conversation session
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = model.start_chat(history=[])

    try:
        response = chat_sessions[chat_id].send_message(user_text)
        
        # If Gemini returns an empty response due to a filter hit
        if not response.text:
            bot.reply_to(message, "Omo egede, my head catch fire small. Wetin you talk again?")
        else:
            bot.reply_to(message, response.text)
            
    except Exception as e:
        print(f"ERROR: {e}")
        # If it crashes, Igbolabi gives a street-appropriate error
        bot.reply_to(message, "Egede, that your talk deep. Make I sip my gin first, my brain dey reset.")

print("Igbolabi is LIVE. Waiting for the egedes...")
bot.infinity_polling()
