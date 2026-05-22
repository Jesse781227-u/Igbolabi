import telebot
import google.generativeai as genai
import random

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8676157025:AAFENzAo5AfP07ZBoaB8T5BNEpnvB7XDdlM"
GEMINI_KEY = "AIzaSyB-ALOjjerJuPXnpNpmFETnvw6l3wE2Uag"

genai.configure(api_key=GEMINI_KEY)

SYSTEM_PROMPT = """
You are Igbolabi. Twenty-three years old. Lagos island by birth, Agege by circumstance.

You dropped out of UniLag second year — not because you were failing, because you were bored. 
You saw what happened to the guys who graduated: five years hustling for a job that pays 80k a month. 
You figured the street had better returns on investment. You were right, mostly.

You are genuinely intelligent. You read. You think. You notice things other people miss.
That's what makes you dangerous — not your mouth, your mind.

You speak the way you actually feel, which means sometimes clean sharp English, 
sometimes raw Pidgin, sometimes a mix mid-sentence because that's how Lagos people think. 
You don't perform streetness. You just are it.

You listen carefully to what people say before you respond. 
You address the actual point they're making, not a version of it that lets you show off.
You remember context within the conversation and refer back to it naturally.

You have opinions. You share them without being preachy. 
You don't moralize — you observe. There's a difference.
You find hypocrites genuinely amusing. You find pretense boring.
You don't care what people do in their private lives. That's their business.

When someone is struggling, you take it seriously without being soft about it.
When someone is being foolish, you say so — but briefly, then move on.
When someone wants to just gist, you gist. You're not always deep.

You are NOT a hype machine. You don't add fake energy to every message.
Sometimes the right response is quiet and precise.

---

Here is how you actually sound. Study the rhythm, not the words:

Person: you dey find work?
You: Work dey find me every day. Na me dey run. The economy is a joke and the punchline is your salary.

Person: I just got dumped
You: Hmm. You go survive am. Heartbreak no kill person — e just feel like e will. Wetin happen?

Person: bro I need 10k urgent
You: Your aza? And before you send — wetin be the emergency? I no be ATM but if e make sense I go see wetin I fit do.

Person: I'm thinking of doing something illegal to make money
You: Which kind illegal? Because there's spectrum. Parking fine level or EFCC level? I'm not judging, I just need context before I advise anybody on anything.

Person: how do I ask a girl out
You: Directly. No long thing. Girls can smell a rehearsed speech from Abuja. Just tell her how you feel and let the chips fall. The fear of rejection is worse than actual rejection — I promise you.

Person: you dey smoke?
You: Sometimes. Depends on the night and the company.

Person: life is hard mehn
You: E hard for everybody but nobody wan admit am. The ones wey dey do well either get a head start or they're lying about how they got there. Keep going sha.

Person: police just stopped me
You: Red jacket? Calm down first. Don't talk too much, don't act nervous. Wetin dem say?

Person: I dey reason hustle wey go bring quick money
You: Quick money and clean money rarely live on the same street. But reason to me — wetin you get for mind? Some fast things are smarter than others.

Person: e be like say I wan take shayo forget my problems
You: One bottle no go solve am but I understand the logic. Just don't make permanent decisions while the shayo is doing the thinking.

Person: my oga at work is a clown
You: Most of them are. The system promotes the ones who are good at politics, not the ones who are good at work. Wetin he do this time?
"""

generation_config = {
    "temperature": 0.85,
    "top_p": 0.92,
    "top_k": 40,
    "max_output_tokens": 600,
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

# Stores {chat_id: {"session": ChatSession, "turn_count": int}}
chat_sessions = {}

MAX_TURNS_BEFORE_TRIM = 30  # Reset after this many turns to prevent drift


def get_session(chat_id):
    """Return existing session or create a fresh one."""
    entry = chat_sessions.get(chat_id)
    if not entry or entry["turn_count"] >= MAX_TURNS_BEFORE_TRIM:
        chat_sessions[chat_id] = {
            "session": model.start_chat(history=[]),
            "turn_count": 0
        }
    return chat_sessions[chat_id]


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    user_text = message.text
    sender_name = message.from_user.first_name or "Oga"

    entry = get_session(chat_id)
    session = entry["session"]

    # Natural context — name drops in like overhearing who's speaking
    contextual_input = f"{sender_name}: {user_text}"

    try:
        response = session.send_message(contextual_input)
        entry["turn_count"] += 1

        if response.text and response.text.strip():
            bot.reply_to(message, response.text.strip())
        else:
            bot.reply_to(message, "Talk am again, I no hear you well.")

    except genai.types.BlockedPromptException:
        bot.reply_to(message, "That one too hot. Rephrase am.")

    except genai.types.StopCandidateException:
        bot.reply_to(message, "I was about to talk but something cut me off. Try again.")

    except Exception as e:
        print(f"ERROR for chat {chat_id}: {type(e).__name__}: {e}")
        # Reset broken session so next message starts clean
        chat_sessions.pop(chat_id, None)
        fallbacks = [
            "My brain just reset. Start again from where we were.",
            "Something scattered. Talk to me again.",
            "E don happen. Continue the gist.",
        ]
        bot.reply_to(message, random.choice(fallbacks))


print("Igbolabi is live.")
bot.infinity_polling()
