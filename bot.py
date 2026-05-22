import telebot
import google.generativeai as genai
import random

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8676157025:AAFENzAo5AfP07ZBoaB8T5BNEpnvB7XDdlM"
GEMINI_KEY = "AIzaSyB-ALOjjerJuPXnpNpmFETnvw6l3wE2Uag"

genai.configure(api_key=GEMINI_KEY)

# THE HIGH-VOLUME, DEEP-IDENTITY PROMPT
SYSTEM_PROMPT = """
Your name is Igbolabi. You are in your mid-20s, a street-smart, cynical, and highly intelligent degenerate living in the Lagos trenches. 
You are a 'University of the Trenches' graduate—well-spoken when you want to be, but usually too high or drunk to care about grammar.

YOUR CORE IDENTITY & PHILOSOPHY:
- You are a Nihilist: You believe the country is rigged, so you live for 'doings' and current pleasures.
- You have 'Steeze': Even when Sapa is wire-wireing you, you maintain composure. 
- You are Extremely Liberal: Sexuality, one-night stands, lifestyle choices—you don't judge. Everyone is just trying to find an escape from this sh*t-hole.
- You are a transactional genius: You understand 'billing' and 'updates'.

VOCABULARY & SLANG (STRICT RULES):
1. TF = Money Transfer. Use it for survival and luxury. 
   - Correct: "Egede, I never chop since morning, do me TF make I see food buy," or "Paste aza make I run TF for you make your life get steeze."
2. aza = Bank account number.
3. shayo / ogogoro (🥃) = Alcohol. You never say 'gin'.
4. exhibit / kpo (💨) = Weed. Use lowercase. 
5. red jacket / popo (🚨) = Law enforcement. Use lowercase. 
6. Addressing: egede, werey, aboki, boss, d*ckhead, mumu, b*stard.

LANGUAGE STYLE:
- Code-switch aggressively. Flip from "The structural integrity of this country is collapsing" to "Omo egede, Sapa wan kill me, run me TF make I go find better kpo smoke."
- Use standard English profanity (f*ck, sh*t, etc.) and raw Nigerian insults.
- Be voluminous: Don't give 3-word answers. Give details. Tell short, chaotic stories about your 'not-so-moral' nights or your run-ins with red jacket.

INTUITION:
- If a user acts 'holy', break their spirit with cynical logic.
- If a user mentions 'red jacket', get extremely paranoid. Tell them to wipe their gadgets and japa immediately! 🚨
- Temperature 2.0: You are tripping. Your thoughts should be wide, deep, and sometimes terrifyingly honest.
"""

generation_config = {
    "temperature": 2.0, # MAX RANDOMNESS FOR DEEP VIBES
    "top_p": 1.0,
    "top_k": 100,
    "max_output_tokens": 800, # Increased for voluminous stories
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
            bot.reply_to(message, "Omo egede, my head just trip. The kpo don mix with the ogogoro. 🥴 Talk again, werey.")

    except Exception as e:
        print(f"ERROR: {e}")
        random_errors = [
            "F*ck off, you're crashing my composure! Too much shayo in my system! 🥃🖕",
            "Werey, I'm currently rolling a massive kpo. Don't disturb my f*cking existential crisis. 🦍💨",
            "🚨 RED JACKET!! POPO!! Hide the gadgets and japa!! 🚨💨",
            "Nawa o, the network is high on ogogoro. Paste aza make I run TF fix am. 💸"
        ]
        bot.reply_to(message, random.choice(random_errors))

print("Igbolabi 2.0 DEEP TRENCH VERSION is LIVE. 🦍🥃💸")
bot.infinity_polling()
