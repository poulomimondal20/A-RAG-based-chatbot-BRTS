import os
import logging
import pandas as pd
from dotenv import load_dotenv
from utils.utils import find_closest_bus_station
from telegram import Update, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext, Application

from utils.chatbot import ask_question

import torch
import torchaudio
from gtts import gTTS
import torchaudio.functional as F
from deep_translator import GoogleTranslator
from transformers import AutoModelForCTC, AutoProcessor

load_dotenv()

df = pd.read_csv("assets/data/all_routes_combined.csv")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

MODEL_ID = "ai4bharat/indicwav2vec-hindi"
model = AutoModelForCTC.from_pretrained(MODEL_ID)
processor = AutoProcessor.from_pretrained(MODEL_ID)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(DEVICE)

user_language_preferences = {}

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='lang_en'),
            InlineKeyboardButton("Hindi", callback_data='lang_hi')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Hi! I am Bhopal BRTS Bot. Send me your location to find the nearest bus station or send a voice message to ask a question.', reply_markup=reply_markup)

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send /start to get the nearest bus station.\nSend a voice message in Hindi to ask a question.')

async def location(update: Update, context: CallbackContext) -> None:
    user_location = update.message.location

    if user_location:
        user_lat = user_location.latitude
        user_long = user_location.longitude
        logger.info(f"Received location: Latitude {user_lat}, Longitude {user_long}")

        closest_station = find_closest_bus_station(df, user_lat, user_long)
        if closest_station:
            message = f"The closest bus station is {closest_station['station']} which is {round(closest_station['distance'], 2)} km away. Routes: {' '.join(closest_station['all_routes'])}"
            await update.message.reply_text(message)
            await update.message.reply_text(f"Navigate using Google Map: {closest_station['dir_to_closest_point']}")
        else:
            await update.message.reply_text("Sorry, I couldn't find any nearby bus stations.")
    else:
        await update.message.reply_text("Please send your location.")

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if query.data == 'lang_en':
        user_language_preferences[user_id] = 'en'
        await query.edit_message_text(text="You have selected English.")
    elif query.data == 'lang_hi':
        user_language_preferences[user_id] = 'hi'
        await query.edit_message_text(text="You have selected Hindi.")

async def voice_query(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    preferred_language = user_language_preferences.get(user_id, 'en') 

    voice: Voice = update.message.voice
    if voice:
        file = await voice.get_file()
        audio_path = "user_voice.ogg"
        await file.download_to_drive(audio_path)

        waveform, sample_rate = torchaudio.load(audio_path)
        resampled_audio = F.resample(waveform, sample_rate, 16000).squeeze().numpy()

        input_values = processor(resampled_audio, return_tensors="pt", sampling_rate=16000).input_values
        with torch.no_grad():
            logits = model(input_values.to(DEVICE)).logits.cpu().squeeze(0)
        
        
        logger.info(f"Logits shape: {logits.shape}")
        if logits.dim() == 1:
            logits = logits.unsqueeze(0)
        logger.info(f"Adjusted logits shape: {logits.shape}")
        
        query_hindi = processor.decode(logits.numpy()).text
        logger.info(f"Transcribed query (Hindi): {query_hindi}")
        query_english = GoogleTranslator(source='hi', target='en').translate(query_hindi)
        logger.info(f"Translated query (English): {query_english}")
        response_english = ask_question(query_english)
        logger.info(f"Response (English): {response_english}")

        if preferred_language == 'hi':
            response_hindi = GoogleTranslator(source='en', target='hi').translate(response_english)
            logger.info(f"Translated response (Hindi): {response_hindi}")
            tts = gTTS(text=response_hindi, lang='hi')
            audio_path = "response_hindi.mp3"
            tts.save(audio_path)
            with open(audio_path, 'rb') as audio_file:
                await update.message.reply_voice(voice=audio_file)
            await update.message.reply_text(response_hindi)
        else:
            await update.message.reply_text(response_english)
    else:
        await update.message.reply_text("Please send a valid voice message.")

async def general_query(update: Update, context: CallbackContext) -> None:
    query = update.message.text
    user_id = update.message.from_user.id
    preferred_language = user_language_preferences.get(user_id, 'en')

    response_english = ask_question(query)
    logger.info(f"Response (English): {response_english}")

    if preferred_language == 'hi':
        response_hindi = GoogleTranslator(source='en', target='hi').translate(response_english)
        logger.info(f"Translated response (Hindi): {response_hindi}")
        await update.message.reply_text(response_hindi)
    else:
        await update.message.reply_text(response_english)

def health_check() -> None:
    logger.info("Performing health check...")

    try:
        df = pd.read_csv('assets/data/all_routes_combined.csv')
        logger.info("CSV file loaded successfully.")
    except FileNotFoundError:
        logger.error("CSV file not found.")
        raise
    except pd.errors.EmptyDataError:
        logger.error("CSV file is empty.")
        raise
    except Exception as e:
        logger.error(f"An error occurred while loading the CSV file: {e}")
        raise

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("Bot token is missing.")
        raise ValueError("Bot token is missing.")
    logger.info("Bot token is present.")

    logger.info("Health check passed!")

def main() -> None:
    health_check()
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.LOCATION, location))
    application.add_handler(MessageHandler(filters.VOICE, voice_query))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, general_query))

    application.run_polling()

if __name__ == '__main__':
    main()