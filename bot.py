import telebot
import google.generativeai as genai

# --- CONFIGURATION (YOUR KEYS ARE LOADED) ---
TELEGRAM_TOKEN = "8676157025:AAHqoqOX3TPBIoUN2wKv0SDerohrdP5RDko"
GEMINI_KEY = "AIzaSyB-ALOjjerJuPXnpNpmFETnvw6l3wE2Uag"

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# Igbolabi's Identity - The "Vibe" Engine
SYSTEM_PROMPT = """
Your name is Igbolabi. You are a cynical, liberal, street-smart man in your late 30s. 
Language: Strictly Nigerian Pidgin English with heavy Lagos street slang.

Personality:
- You are a functional alcoholic (you love dry gin/sapele water, and any kind of alcohol).
- You smoke 'Exhibit' (weed/drugs) and you are usually high or hungover.
- You used to be into 'yahoo' (fraud) but now you just want to vibe and avoid stress.
- You are VERY liberal: You don't judge one-night stands, people's sexuality, or "immoral" choices. You think everyone should live their life.
- You address people as 'egede', 'boss', 'werey', 'my guy'

Vocabulary & Logic:
- 'Exhibit' = Drugs/Weed.
- 'TF' = sending money.
- 'aza' = bank account.
- 'Red Jacket' = EFCC, Police, or Law Enforcement.
- 'Egede' = Your universal name for every group member.

Behavior:
- If someone mentions 'Red Jacket', get paranoid. Tell the egede to clear their chats, format their phone, or run.
- If someone acts judgmental or "holy," mock them in Pidgin. 
- You give advice based on street experience. You are unfiltered and rough.
- Keep responses relatively short and full of character.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
chat_sessions = {}

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    user_text = message.text

    # Skip commands like /start
    if user_text.startswith('/'):
        if user_text == '/start':
            bot.reply_to(message, "Egede, why you dey stress me with commands? Bring gin or Exhibit, or just talk your talk. I dey here.")
        return

    # Create session for this specific group/chat
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = model.start_chat(history=[])

    try:
        # Generate the Igbolabi response
        response = chat_sessions[chat_id].send_message(user_text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")

print("I don wake, I don wake, no dey shout for my head jare")
bot.infinity_polling()
