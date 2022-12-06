from controller import parseable_data, solution_equation
 from telegram import Bot
 from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
 from log import get_id_user, get_input_data, get_result, save_log

 bot = Bot(token='5726183817:AAFl_Bkd6u-5g2qNwQSlzf5UpwfET54satc')
 updater = Updater(token='5726183817:AAFl_Bkd6u-5g2qNwQSlzf5UpwfET54satc')
 dispatcher = updater.dispatcher

 start_calc = 0

 def start(update, context):
     context.bot.send_message(update.effective_chat.id, 'Я бот-калькулятор!')
     context.bot.send_message(update.effective_chat.id, 'При решении примера считаю, что числа в примере положительные')
     context.bot.send_message(update.effective_chat.id, 'Понимаю знаки: /, *, +, -')
     context.bot.send_message(update.effective_chat.id, 'Знаю приоритет действий. Могу работать со скобками.')
     context.bot.send_message(update.effective_chat.id, 'Команда /end отключит меня.')
     get_id_user(update.effective_chat.id)
     return start_calc

 def receiving_data(update, context):
     data = update.message.text
     get_input_data(data)  
     list_data = parseable_data(data) 
     result = solution_equation(list_data)  
     get_result(result) 
     save_log()  
     context.bot.send_message(update.effective_chat.id, f'Результат: {result}')

 def cancel(update, context):
     context.bot.send_message(update.effective_chat.id, 'До встречи!')
     return ConversationHandler.END

 start_handler = CommandHandler('start', start)
 receiving_data_handler = MessageHandler(Filters.text & (~Filters.command), receiving_data)
 mes_data_handler = CommandHandler('end', cancel)

 conv_handler = ConversationHandler(entry_points=[start_handler],
                                    states={start_calc: [receiving_data_handler]},
                                    fallbacks=[mes_data_handler])

 dispatcher.add_handler(conv_handler)

 updater.start_polling()
 updater.idle()