import telegram
from telegram import *
from telegram.ext import *
import os,requests
CHANGE_MANGA, *_ = range(100)
user_datas={}
BOT_TOKEN="6748612886:AAHsJnpelNURNHy4hJXwPPImHUOmp0mxQP0"

def start(update, context):
    keyboard=[[InlineKeyboardButton(f'SUPPORT',url=f'https://t.me/ALLSOBOTS'),InlineKeyboardButton(f'REPO',url=f'https://github.com/button-maker/Button-Maker')]]
    update.message.reply_text("*WELCOME TO Button Maker BOT\n\nThis bot helps you to make button and send it to your channel by using the command /content*",reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=ParseMode.MARKDOWN)
    return

def title_content(update,context):
    user=update.effective_user
    cd=context.chat_data
    text1=update.message.text.split(" ")
    text2=update.message.text.split("/content ")[-1]
    if len(text1)-1 < 1:
        update.message.reply_text("*Write the title content of the button line you want to create*\n\nlike `/content hello friends`",parse_mode=ParseMode.MARKDOWN)
        return
    keyboard=[[InlineKeyboardButton('YES',callback_data=f'titlecre_yes')],
              [InlineKeyboardButton('NO',callback_data=f'titlecre_no')]]
    message=update.message.reply_text(f"`Content : `*{text2}\n\nNow would you like to add a picture ?*",reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=ParseMode.MARKDOWN)
    message_id=message.message_id
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id-1)
    cd[message_id] = {}
    cd[message_id]['content']=text2
    return

def titlecreation(update,context):
    user=update.effective_user
    query=update.callback_query
    message_id=query.message.message_id
    cd=context.chat_data
    content_name=cd[message_id]['content']
    if query.data.split("_")[-1]=="yes":
        keyboard=[[InlineKeyboardButton('CANCEL',callback_data=f'titlecer_cancel')]]
        message=query.message.reply_text('*Send the Picture*',reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=ParseMode.MARKDOWN)
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        context.dispatcher.add_handler(MessageHandler(Filters.photo, content_reciever))
        global user_datas
        message_id=message.message_id
        user_datas[f"user_{user.id}"]={"name":content_name,"content_pic":"yes","last_id":message_id}
    else:
        keyboard=[[InlineKeyboardButton('YES',callback_data=f'contentrc_yes')],[InlineKeyboardButton('NO',callback_data=f'contentrc_no')]]
        message=query.message.edit_text(f"`Content : `*{content_name}*\n\n`Picture : `*None Given\n\nNow would you like to add a button ?*",reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=ParseMode.MARKDOWN)
        message_id=message.message_id
        cd[message_id] = {}
        cd[message_id]['content']=content_name
        cd[message_id]['content_img']=None
        return

def content_reciever(update,context):
    user=update.effective_user
    message = update.message.text
    global user_datas
    if user_datas[f'user_{user.id}']['content_pic']=="yes":
        user_datas[f'user_{user.id}']['content_pic']="no"
        context.dispatcher.remove_handler(content_reciever)
        if update.message.photo:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=user_datas[f'user_{user.id}']["last_id"])
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=user_datas[f'user_{user.id}']["last_id"]+1)
            user_content=user_datas[f'user_{user.id}']["name"]
            file_id = update.message.photo[-1].file_id
            file = context.bot.get_file(file_id)
            file_url = file.file_path
            response = requests.get(file_url)
            file_size_kb = len(response.content)/1024
            if file_size_kb > 5*1024:
                user_datas[f'user_{user.id}'].clear()
                update.message.reply_text("*Please send a photo with less than 5 mb size*",parse_mode=ParseMode.MARKDOWN)
                return
            keyboard=[[InlineKeyboardButton('YES',callback_data=f'contentrc_yes')],[InlineKeyboardButton('NO',callback_data=f'contentrc_no')]]
            message=update.message.reply_text(f"*Image captured\n\nNow would you like to add buttons ?*",reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=ParseMode.MARKDOWN)
            file.download(f'content_img_{user.id}_{message.message_id}.jpg')
            user_datas[f'user_{user.id}'].clear()
            cd=context.chat_data
            message_id=message.message_id
            cd[message_id] = {}
            cd[message_id]['content']=user_content
            cd[message_id]['content_img']=f"content_img_{user.id}_{message.message_id}.jpg"
            return
    if user_datas[f'user_{user.id}']['content_but_nam']=="yes":
        user_datas[f'user_{user.id}']['content_but_nam']="no"
        context.dispatcher.remove_handler(content_reciever)
        if update.message.text:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=user_datas[f'user_{user.id}']["last_id"])
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=user_datas[f'user_{user.id}']["last_id"]+1)
            content_name=user_datas[f'user_{user.id}']["name"]
            content_img=user_datas[f'user_{user.id}']["content_pic"]
            but_name=update.message.text
            message=update.message.reply_text(f"*Button name recieved now send the Button url link*",parse_mode=ParseMode.MARKDOWN)
            context.dispatcher.add_handler(MessageHandler(Filters.text, content_reciever))
            message_id=message.message_id
            user_datas[f'user_{user.id}'].clear()
            user_datas[f"user_{user.id}"]={"name":content_name,"content_pic":content_img,"content_but_nam":but_name,"content_but_url":"yes","last_id":message_id}
            return
    if user_datas[f'user_{user.id}']['content_but_url']=="yes":
        user_datas[f'user_{user.id}']['content_but_url']="no"
        context.dispatcher.remove_handler(content_reciever)
        if update.message.text[0:8] == "https://":
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=user_datas[f'user_{user.id}']["last_id"])
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=user_datas[f'user_{user.id}']["last_id"]+1)
            content_name=user_datas[f'user_{user.id}']["name"]
            content_img=user_datas[f'user_{user.id}']["content_pic"]
            content_but_name=user_datas[f'user_{user.id}']["content_but_nam"]
            but_url=update.message.text
            message=update.message.reply_text(f"*Button url recieved now send the channel id or username or link of your channel and make me admin*",parse_mode=ParseMode.MARKDOWN)
            context.dispatcher.add_handler(MessageHandler(Filters.text, content_reciever))
            message_id=message.message_id
            user_datas[f'user_{user.id}'].clear()
            user_datas[f"user_{user.id}"]={"name":content_name,"content_pic":content_img,"content_but_nam":content_but_name,"content_but_url":but_url,"content_id":"yes","last_id":message_id}
            return
    if user_datas[f'user_{user.id}']['content_id']=="yes":
        user_datas[f'user_{user.id}']['content_id']="no"
        context.dispatcher.remove_handler(content_reciever)
        if update.message.text:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=user_datas[f'user_{user.id}']["last_id"])
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=user_datas[f'user_{user.id}']["last_id"]+1)
            chater=update.message.text
            SEc = telegram.Bot(token=BOT_TOKEN)
            channel_id=""
            if f"{chater[0]}"=="-":
                channel_id=chater
            elif {chater[0]}=="@":
                channel_id=SEc.get_chat(chater).id
            elif chater[0:13] == "https://t.me/":
                chater2="@"+chater.split("https://t.me/")[-1]
                channel_id=SEc.get_chat(chater2).id
            else:
                user_datas[f'user_{user.id}'].clear()
                update.message.reply_text("*AWW boy you didn't gave the right id/username/link of channel hence cancelled*",parse_mode=ParseMode.MARKDOWN)
                return
            content_name=user_datas[f'user_{user.id}']["name"]
            content_img=user_datas[f'user_{user.id}']["content_pic"]
            content_but_name=user_datas[f'user_{user.id}']["content_but_nam"]
            content_but_url=user_datas[f'user_{user.id}']["content_but_url"]
            if content_img == None:
                but=[[InlineKeyboardButton(f'{content_but_name}',url=f'{content_but_url}')]]
                context.bot.send_message(chat_id=update.effective_chat.id,text=f"*{content_name}*",reply_markup=InlineKeyboardMarkup(but),parse_mode=ParseMode.MARKDOWN)
            else:
                but=[[InlineKeyboardButton(f'{content_but_name}',url=f'{content_but_url}')]]
                context.bot.send_photo(chat_id=update.effective_chat.id,photo=open(content_img,"rb"),caption=f"*{content_name}*",reply_markup=InlineKeyboardMarkup(but),parse_mode=ParseMode.MARKDOWN)
            keyboard=[[InlineKeyboardButton('YES',callback_data=f'butmaker_yes')],[InlineKeyboardButton('NO',callback_data=f'butmaker_no')]]
            message=update.message.reply_text(f"*Channel link recieved now check the above format and click on Yes to Send\nAnd No to cancel\nAfter 24 hours it will eventually get cancelled*\n\n*NOTE : First make bot admin in your channel with send message rights then click on yes*",reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=ParseMode.MARKDOWN)
            message_id=message.message_id
            user_datas[f'user_{user.id}'].clear()
            cd=context.chat_data
            cd[message_id] = {}
            cd[message_id]['content']=content_name
            cd[message_id]['content_pic']=content_img
            cd[message_id]['content_but_nam']=content_name
            cd[message_id]['content_but_url']=content_img
            cd[message_id]['content_id']=channel_id
            return

def titlerc(update,context):
    user=update.effective_user
    query=update.callback_query
    message_id=query.message.message_id
    cd=context.chat_data
    content_name=cd[message_id]['content']
    content_img=cd[message_id]['content_img']
    if query.data.split("_")[-1]=="yes":
        keyboard=[[InlineKeyboardButton('CANCEL',callback_data=f'titlecer_cancel')]]
        message=query.message.reply_text('*Send the Button Name*',reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=ParseMode.MARKDOWN)
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        context.dispatcher.add_handler(MessageHandler(Filters.text, content_reciever))
        global user_datas
        message_id=message.message_id
        user_datas[f"user_{user.id}"]={"name":content_name,"content_pic":content_img,"content_but_nam":"yes","last_id":message_id}
    else:
        message=query.message.edit_text(f"*BUTTON IS NECCESARY\nwithout button your query cancelled*",reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=ParseMode.MARKDOWN)
        try:
            os.remove(content_img)
        except:
            print("NO IMG")
        cd.clear()
        return

def confirmed_Sender(update,context):
    user=update.effective_user
    query=update.callback_query
    message_id=query.message.message_id
    cd=context.chat_data
    content_name=cd[message_id]['content']
    content_img=cd[message_id]['content_pic']
    content_but_name=cd[message_id]['content_but_nam']
    content_but_url=cd[message_id]["content_but_url"]
    content_chnl_id=cd[message_id]["content_id"]
    if query.data.split("_")[-1]=="yes":
        but=[[InlineKeyboardButton(f'{content_but_name}',url=f'{content_but_url}')]]
        if content_img == None:
            try:
                context.bot.send_message(chat_id=content_chnl_id,text=f"*{content_name}*",reply_markup=InlineKeyboardMarkup(but),parse_mode=ParseMode.MARKDOWN)
            except:
                update.message.reply_text("*NOT ADMIN IN CHANNEL*",parse_mode=ParseMode.MARKDOWN)
                return
        else:
            try:
                context.bot.send_photo(chat_id=content_chnl_id,photo=open(content_img,"rb"),caption=f"*{content_name}*",reply_markup=InlineKeyboardMarkup(but),parse_mode=ParseMode.MARKDOWN)
            except:
                update.message.reply_text("*NOT ADMIN IN CHANNEL*",parse_mode=ParseMode.MARKDOWN)
            os.remove(content_img)
            return          
    else:
        cd.clear()
        os.remove(content_img)
        update.message.reply_text("*CANCELLED*",parse_mode=ParseMode.MARKDOWN)
        return

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("content", title_content))
    CHANGE_MANGA = ConversationHandler(entry_points=[CallbackQueryHandler(titlecreation, pattern= f'titlecre_',run_async=True),
                                                     CallbackQueryHandler(titlerc, pattern= f'contentrc_',run_async=True),
                                                     CallbackQueryHandler(confirmed_Sender, pattern= f'butmaker_',run_async=True)],
        states={},
        fallbacks=[],
        allow_reentry=True,
        per_user=True,
        run_async = True)
    dp.add_handler(CHANGE_MANGA)
    updater.start_polling()
    updater.idle()

main()
