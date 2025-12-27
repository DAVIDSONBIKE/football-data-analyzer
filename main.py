import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Load API keys from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if TELEGRAM_TOKEN is None or OPENAI_KEY is None:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or OPENAI_API_KEY environment variable")

openai.api_key = OPENAI_KEY

# The AI prompt
PROMPT = """
You are a professional football match analyst.
Analyze matches deeply using:
- Team form
- Head-to-head
- Home vs away strength
- Motivation
- Odds value

Never guarantee 100%.
Return:
1. Short analysis
2. Key factors
3. Final prediction
4. Confidence percentage
"""

# Function to handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": user_text}
            ]
        )

        await update.message.reply_text(
            response.choices[0].message["content"]
        )

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Build the Telegram application
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Run the bot
app.run_polling()
