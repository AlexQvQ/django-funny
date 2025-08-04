from django.apps import AppConfig
from telegram.ext import ApplicationBuilder, ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from . import handlers
from django.conf import settings
import asyncio
import telegram



class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'
    
    def ready(self):
        application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.echo)
        unknown_handler = MessageHandler(filters.COMMAND, handlers.unknown)
        
        conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create_rzhaka', handlers.create_rzhaka)],
        states={
            handlers.JOKE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.joke_text)],
            handlers.JOKE_SAVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.joke_save)],
        },
        fallbacks=[CommandHandler('cancel', handlers.cancel_rzhaka_creation)]
    )
        
        application.add_handler(CommandHandler('start', handlers.start))
        application.add_handler(CommandHandler('rzhaka', handlers.rzhaka))
        application.add_handler(conv_handler)
        application.add_handler(CallbackQueryHandler(handlers.button_click))
        # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_message))
        application.add_handler(echo_handler)
        application.add_handler(unknown_handler)
        
        application.run_polling()
