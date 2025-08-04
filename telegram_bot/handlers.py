from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
# from main.models import Joke
from asgiref.sync import sync_to_async
from django.apps import apps

JOKE_TEXT, JOKE_SAVE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я расказываю анекдоты, напиши /rzhaka что бы его получить")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я такого не знаю, по этому делать ниче не буду")
    
async def rzhaka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    Joke = apps.get_model('main', 'Joke')
    joke = await Joke.objects.order_by('?').afirst()
    
    context.user_data["current_joke_id"] = joke
    
    keyboard = [
        [InlineKeyboardButton("Смешно (" + str(joke.votes) + " человек посчитали смешным)", callback_data="fun")],
        [InlineKeyboardButton("Не очень", callback_data="meh")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=joke.joke, reply_markup=reply_markup)
    
    print(joke)
    
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    joke = context.user_data.get("current_joke_id")
    
    if query.data == "fun":
        joke.votes += 1
        await sync_to_async(joke.save)()
        await query.edit_message_text(text="Рад, что тебе понравилось! Напиши команду /rzhaka еще раз, что бы получить анекдот или команду /create_rzhaka что-бы поделится своим")
    elif query.data == "meh":
        await query.edit_message_text(text="Думаю следующий анекдот тебе понравится, напиши команду /rzhaka еще раз, что бы получить его или поведай своё высокое чувство юмора другим, используя команду /create_rzhaka")
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=joke.joke)
    
async def create_rzhaka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(text="Напиши в следующем сообщении заголовок своего анекдота")
    
    return JOKE_TEXT

async def joke_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    context.user_data["new_joke_name"] = update.message.text
    await update.message.reply_text(text="А теперь напиши текст своего анекдота")
    
    return JOKE_SAVE

async def joke_save(update, context):
    context.user_data["new_joke_text"] = update.message.text
    Joke = apps.get_model('main', 'Joke')
    
    newJoke = await sync_to_async(Joke.objects.create)(
        title = context.user_data.get("new_joke_name"),
        joke = context.user_data.get("new_joke_text"),
        votes = 0
        )
    
    textMessage = 'Ваш анекдот сохранен, теперь его увидят другие пользователи!\n' + context.user_data.get("new_joke_text")
    await update.message.reply_text(text=textMessage)

    return ConversationHandler.END

async def cancel_rzhaka_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END