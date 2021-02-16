# UniBot
# @AbdooEco_Bot (may change later to @UniBot)
# Main Bot Operations File
# Created    : 2021 - 2 - 11
# LastEdited : 2021 - 2 - 16 16:37

# Github:
# ===========================================================================================================================
# ===========================================================================================================================
# Basic Info  :

from tree import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Bot, ChatAction
from telegram.error import RetryAfter as FloodError
from datetime import datetime



TOKEN = "You Bot Token"

UNIBOT_CLOUD_CHANNEL_ID = "Id of the Channel where files while be sent and retreived (like a storage)"

LOG_GROUP_CHAT_ID = "Id of the group where all the bots I created log actions to it"
ADMINS_IDS = {507130741, # My Id, @Abdoo_M
              None
              }
# Multiline strings or strings refrenced more than once ..
THIS_PLACE_IS_EMPTY_TEXT = "سوري المكان فاضي هون \n :'-/"
CODER_PHONE_NUM_TEXT = "+963945536907"
ACTIVE_USERS_REPLY = "عدد المستخدمين الفعالين للبوت :"
JOIN_US_TEXT = """حابب تضيف ملف وتصير أدمن بالبوت؟
كون بفريقنا ❤ وخلينا نكبر البوت ❤
تواصل معنا:  @Abdoo_M"""
CREDITS_HTML = """ 
<u><b><em>تصميم و برمجة : </em></b></u>
<em>عبد اللطيف الميهوب</em>
جامعة البعث
كلية الإقتصاد - السنة الأولى
"""
START_COMMAND_TEXT = """
تحياتي زميلتي  ❤
تحياتي زميلي  ❤

هاد بوت تليغرام موجود عليه الملفات
 المهمة يلي عم يتكرر طلبها مشان نخفف
زحمة عغروب الدفعة 🙄

البوت لسا عم يتطور أي تعليق أو مشكلة أو إقتراحات أنا جاهز دائماً،
حكوني تلغرام أو واتس أو يلي بدكن ياه 💚

<em>زميلكم عبد اللطيف الميهوب</em>
<b>@Abdoo_M </b>
"""
FOR_MORE_INFO_TEXT = """
لمعلومات أكثر إضغط /help
"""
YOU_DONT_HAVE_ACCESS_TEXT = "ما عندك صلاحية تثبت ملفات صديقي...تواصل مع الأدمنز"
SEND_FEEDBACK_TEXT = """
 شو رأيك بالبوت ؟🤷‍♂️❤
( أكتب تعليقك مسبوقا بـ"رأيي أنو" وأرسله)
"""
FEEDBACK_ARRIVED_THX = "وصل 😁"
FOR_MA3LISH_TEXT = """
اذا انضربت بشي مادة ولازمك معلشة كبوس /ma3lish
"""

ADMIN_CHEAT_SHEET_HTML = """
<u><b><em>Available Commands:</em></b></u>
<b>/start</b>
<b>/help</b>
<b>/ma3lish</b>
<b>/my_user_id</b>
<b>/draw_tree</b>
--------------
<b>/new_folder \\n folder_name \\n folder_Comment(=RandDefaultComments) </b>
<b>/comment \\n wht2comment \\n comment </b>
    - wht2comment = '.'  : Comment current folder
    - wht2comment = name : Comment name in CurrFld
    - comment = '#' : Reset Comment

<b>/delete</b> \\n wht2del(= . to del current folder )
<b>/rename</b> \\n wht2rename(= . to del current folder ) \n new_name
<b>/backup</b> \\n copyname
<b>/publication</b>
"""

start = None  # cuz i refrence it when defining a func
# ===========================================================================================================================
# ===========================================================================================================================
# Helper Functions :


def decode_date(d: datetime):
    # Convert time zone to Syria
    nh = d.hour + 2
    if nh > 23:
        nh -= 24
    # Recreate the obj with the new hour and convert to readable string
    return datetime(d.year, d.month, d.day, nh, d.minute, d.second).strftime("%Y/%m/%d - %H:%M:%S")


def log_action(update, action: str):
    admin = "-Admin-" if update.message.from_user.id in ADMINS_IDS else ''
    log_message = f"{admin}\nuser {update.message.from_user.first_name} \nusername @{update.message.from_user.username} \n{decode_date(update.message.date)} \n{action}"
    updater.bot.sendMessage(
        LOG_GROUP_CHAT_ID, log_message, disable_notification=True)


def load_users_ids():
    from os.path import join
    try:
        with open("users_ids.txt", 'r') as f:
            ids = f.read().splitlines()
        return ids
    except:
        print("[HighLevelLog] users_ids.txt NOT FOUND, returning empty list.. ")
        return []

def make_menu(context):
    keyboard = []
    # note : sub.key == sub.value.name
    for i in context.user_data["current_folder"].sub.keys():
        keyboard.append([i])

    if len(keyboard) == 0:
        keyboard.append([THIS_PLACE_IS_EMPTY_TEXT])

    if not context.user_data["current_folder"] == start:
        keyboard.append(["رجوع"])
    # print(f"[HighLevelLog]"\nkeyboard=\n", keyboard)
    return ReplyKeyboardMarkup(keyboard)

# ===========================================================================================================================
# ===========================================================================================================================
# Handle Input Functions :


def start_command(update, context):
    # Add user to users
    users_ids = set(load_users_ids())
    user_id = update.message.from_user.id
    users_ids.add(user_id)
    text = ''
    for x in users_ids:
        text += str(x)+'\n'
    with open("users_ids.txt", 'w') as f:
        f.write(text)
    update.message.reply_text(text=START_COMMAND_TEXT, parse_mode="HTML")
    update.message.reply_text(text=FOR_MORE_INFO_TEXT)
    update.message.reply_text(text=FOR_MA3LISH_TEXT)
    context.user_data["current_folder"] = start
    update.message.reply_text(
        start.properties["comment"], reply_markup=make_menu(context))
    log_action(update, "start")


def help_command(update, context):
    update.message.reply_text(CREDITS_HTML, parse_mode="HTML")
    update.message.reply_text("0945 536 907")
    update.message.reply_text(
        "facebook.com/Abdoo.Almayhob/", disable_web_page_preview=True)
    active_users = load_users_ids()
    update.message.reply_text(ACTIVE_USERS_REPLY + str(len(active_users)+20))
    if update.message.from_user.id in ADMINS_IDS:
        update.message.reply_text(
            ADMIN_CHEAT_SHEET_HTML, parse_mode="HTML")
    log_action(update, "help")


def ma3lish_command(update, context):
    from random import randint as rand
    tot = 0
    for _ in range(rand(10, 40)):
        c = rand(10, 40)
        tot += c
        text = " معلش " * c
        update.message.reply_text(text)
    update.message.reply_text(f"بعتلك معلش {tot} مرة \n ¯\\_( ͡° ͜ʖ ͡°)_/¯")
    log_action(update, "ma3lish*"+str(tot))


def my_user_id_command(update, context):
    update.message.reply_text(update.message.from_user.id)
    log_action(update, "my_user_id")


def draw_tree_command(update, context):
    update.message.reply_text(draw_tree(context.user_data["current_folder"]))
    log_action(update, "Drawing Tree..")


def process_input(update, context):  # TODO:FIX
    try:
        inp = update.message.text
        log_action(update, ">"+inp)

        if context.user_data["current_folder"] == None:
            raise KeyError

        # if inp is a keyboard button press, else its manual input
        if (inp in context.user_data["current_folder"].sub):
            # 2 Cases : Either user chose a folder or a file:
            if type(context.user_data["current_folder"].sub[inp]) == folder:
                # Current_node = current_node.next
                context.user_data["current_folder"] = context.user_data["current_folder"].sub[inp]
                context.user_data["current_folder"] = context.user_data["current_folder"]
                update.message.reply_text(
                    context.user_data["current_folder"].properties["comment"], reply_markup=make_menu(context))
                if not update.message.from_user.id in ADMINS_IDS:  # Admins movments don't count
                    context.user_data["current_folder"].properties["num_of_times_called"] += 1

            elif type(context.user_data["current_folder"].sub[inp]) == bot_file:
                chosen_file = context.user_data["current_folder"].sub[inp]
                chosen_file_id_in_storage = chosen_file.properties["stored_msg_id"]
                updater.bot.copy_message(chat_id=update.message.from_user.id,
                                         from_chat_id=UNIBOT_CLOUD_CHANNEL_ID,
                                         message_id=chosen_file_id_in_storage)
                if not chosen_file.properties["comment"] in (None, '', ' ', '#'):
                    update.message.reply_text(
                        chosen_file.properties["comment"])
                if not update.message.from_user.id in ADMINS_IDS:  # Admins movments don't count
                    chosen_file.properties["num_of_times_called"] += 1
                update.message.reply_text(SEND_FEEDBACK_TEXT)

        # Back Button
        elif inp == "رجوع":
            context.user_data["current_folder"] = context.user_data["current_folder"].father
            update.message.reply_text(
                context.user_data["current_folder"].properties["comment"], reply_markup=make_menu(context))

        # This Place Is Empty Button
        elif inp == THIS_PLACE_IS_EMPTY_TEXT:
            update.message.reply_text(JOIN_US_TEXT)

        elif "رأيي" in inp:
            update.message.reply_text("وصل 😁")

        else:
            update.message.reply_text("ما فهمتك صديقي...🤨")
    except KeyError:
        update.message.reply_text("معلومات ناقصة , اكبس  /start  وعيد جرب ...")
    except (Exception, FloodError) as E:
        log_action(update, f"Error While Processing User Input:\n{E}")
        update.message.reply_text("سوري.. كأنو في غلط بالملف هاد ..😐")

# =======================================================
# =======================================================
# Only for Admins Functions :


def new_folder(update, context):
    if not update.message.from_user.id in ADMINS_IDS:
        update.message.reply_text(YOU_DONT_HAVE_ACCESS_TEXT)
        log_action(update, "Un Authorized Access")
        return None

    save_tree(start, custom_name="BackUp_before_NewFolder")
    try:
        inp = update.message.text
        folder_name = inp.split('\n')[1].strip()
        try:
            comment = inp.split('\n')[2].strip()
        except:
            comment = ''

        current_folder = context.user_data["current_folder"]
        current_folder.add_folder(folder_name, comment=comment)
        save_tree(start)
        update.message.reply_text("💚شكراً لك, تمت الإضافة")
        log_action(
            update, f"Tree Saved, Folder {folder_name} added in {current_folder.name}")
        update.message.reply_text(
            context.user_data["current_folder"].properties["comment"], reply_markup=make_menu(context))

    except Exception as E:
        update.message.reply_text("خطأ أثناء الإضافة")
        log_action(update, f"Error While Adding Folder:\n{E}")


def new_file(update, context):
    if not update.message.from_user.id in ADMINS_IDS:
        update.message.reply_text(YOU_DONT_HAVE_ACCESS_TEXT)
        log_action(update, "Un Authorized Access")
        return None

    save_tree(start, custom_name="BackUp_before_NewFile")

    try:
        new_file = update.message
        stored_file = updater.bot.copy_message(chat_id=UNIBOT_CLOUD_CHANNEL_ID,
                                               from_chat_id=new_file.from_user.id,
                                               message_id=new_file.message_id)

        # If Caption is Empty or Null:
        try:
            name = new_file.caption.strip()
            if name == '':
                raise NameError('Not Valid Caption!')
        except:
            name = new_file.document.file_name.split('.')[0].strip()

        properties = dict()
        properties["full_name"] = new_file.document.file_name
        properties["stored_msg_id"] = stored_file.message_id
        properties["comment"] = None
        properties["num_of_times_called"] = 0
        properties["size"] = new_file.document.file_size
        properties["date"] = decode_date(new_file.date)
        properties["sender_id"] = new_file.from_user.id
        properties["sender_name"] = new_file.from_user.first_name
        properties["sender_username"] = new_file.from_user.username

        nf = context.user_data["current_folder"].add_bot_file(
            name, **properties)

        file_info_text = f"""
File Msg ID : {nf.properties["stored_msg_id"]}
File Name : {nf.name}
File Full Name : {nf.properties["full_name"]}
File Size : {nf.properties["size"]}
Sender ID : {nf.properties["sender_id"]}
Sender Name : {nf.properties["sender_name"]}
Sender Username : @{nf.properties["sender_username"]}
Path : \n{nf.get_ancestors()}
        """
        updater.bot.sendMessage(UNIBOT_CLOUD_CHANNEL_ID, file_info_text)

        save_tree(start)
        update.message.reply_text("💚شكراً لك, تمت الإضافة")
        log_action(
            update, f"Tree Saved, File {new_file.document.file_name} added in {nf.father.name}")
        update.message.reply_text(
            context.user_data["current_folder"].properties["comment"], reply_markup=make_menu(context))

    except Exception as E:
        update.message.reply_text("خطأ أثناء الإضافة")
        log_action(update, f"Error While Adding File:\n{E}")


def comment_command(update, context):
    if not update.message.from_user.id in ADMINS_IDS:
        update.message.reply_text(YOU_DONT_HAVE_ACCESS_TEXT)
        log_action(update, "Un Authorized Access")
        return None

    save_tree(start, custom_name="BackUp_Before_Comment")
    try:
        inp = update.message.text
        inp = inp.split('\n')
        what_to_comment = inp[1].strip()
        # Telegram wont let u send empty string, so send # and replace it here
        comment = inp[2].strip().replace('#', '')

        # Comment current folder
        if what_to_comment == '.':
            context.user_data["current_folder"].set_comment(comment)
            t = context.user_data["current_folder"].name
            log_action(update, f"Folder {t} Commented {comment}")
            update.message.reply_text("مشي الحال.. 👌🏼")
        # Comment This file in the current folder
        elif what_to_comment in context.user_data["current_folder"].sub:
            context.user_data["current_folder"].sub[what_to_comment].set_comment(
                comment)
            t = context.user_data["current_folder"].sub[what_to_comment].name
            log_action(update, f"File {t} Commented {comment}")
            update.message.reply_text("مشي الحال.. 👌🏼")

        else:
            update.message.reply_text("مافي هيك شي .. تأكد من الأسم..")

    except KeyError:
        update.message.reply_text("مافي هيك شي .. تأكد من الأسم..")

    except Exception as E:
        update.message.reply_text("خطأ أثناء التعليق")
        log_action(update, f"Error While Commenting Obj:\n{E}")


def rename_command(update, context):
    if not update.message.from_user.id in ADMINS_IDS:
        update.message.reply_text(YOU_DONT_HAVE_ACCESS_TEXT)
        log_action(update, "Un Authorized Access")
        return None
    save_tree(start, custom_name="BackUp_Before_Renaming")
    try:
        inp = update.message.text
        inp = inp.split('\n')
        what_to_rename = inp[1].strip()
        new_name = inp[2].strip()
        # Rename current folder
        if what_to_rename == '.':
            prev_name = context.user_data["current_folder"].name
            context.user_data["current_folder"].name = new_name
            context.user_data["current_folder"].father.sub[new_name] = context.user_data["current_folder"].father.sub.pop(
                prev_name)
            log_action(update, f"Folder {prev_name} Renamed {new_name}")
            update.message.reply_text("مشي الحال.. 👌🏼")
            update.message.reply_text(
                context.user_data["current_folder"].properties["comment"], reply_markup=make_menu(context))
        # Rename this file in the current folder
        elif what_to_rename in context.user_data["current_folder"].sub:
            # change self.name value, Then update father.sub value {"new_name":new_namestuff}
            prev_name = context.user_data["current_folder"].sub[what_to_rename].name
            context.user_data["current_folder"].sub[what_to_rename].name = new_name
            context.user_data["current_folder"].sub[new_name] = context.user_data["current_folder"].sub.pop(
                what_to_rename)
            log_action(update, f"File {prev_name} Renamed to {new_name}")
            update.message.reply_text("مشي الحال.. 👌🏼")
            update.message.reply_text(
                " ناو روح عدل الكابشن والخواص بالسحابة.. ")
            df_id = context.user_data["current_folder"].sub[new_name].properties["stored_msg_id"]
            update.message.reply_text("id: "+str(df_id))
            update.message.reply_text(
                context.user_data["current_folder"].properties["comment"], reply_markup=make_menu(context))
        else:
            update.message.reply_text("مافي هيك شي .. تأكد من الأسم..")

        save_tree(start)

    except KeyError:
        update.message.reply_text("مافي هيك شي .. تأكد من الأسم..")

    except Exception as E:
        update.message.reply_text("خطأ أثناء إعادة التسمية")
        log_action(update, f"Error While Renaming Obj:\n{E}")


def delete_command(update, context):
    if not update.message.from_user.id in ADMINS_IDS:
        update.message.reply_text(YOU_DONT_HAVE_ACCESS_TEXT)
        log_action(update, "Un Authorized Access")
        return None

    save_tree(start, custom_name="BackUp_Before_Delete")

    inp = update.message.text
    try:
        if 'YES' in inp:
            what2del = inp.split('\n')[1].strip()
            if what2del == '.':
                context.user_data["current_folder"].delete()
                # Done Deleting, send "Delete from cloud storage pls"+ deleted_file_id
                update.message.reply_text("تم الحذف..")
                # Go back to father folder
                context.user_data["current_folder"] = context.user_data["current_folder"].father
                update.message.reply_text(
                    context.user_data["current_folder"].properties["comment"], reply_markup=make_menu(context))
            else:
                df_id = context.user_data["current_folder"].sub[what2del].properties["stored_msg_id"]
                context.user_data["current_folder"].sub[what2del].delete()

                # Done Deleting, send "Delete from cloud storage pls"+ deleted_file_id
                update.message.reply_text(
                    "تم الحذف, ناو روح حذفه من السحابة..")
                update.message.reply_text("id: "+str(df_id))
                # Go back to father folder
                update.message.reply_text(
                    context.user_data["current_folder"].properties["comment"], reply_markup=make_menu(context))

            save_tree(start)
        else:
            update.message.reply_text(
                "متأكد؟ \n أرسل [ /delete YES \\n wht2del ] إذا أي ..\n The following branch will be deleted:")
            update.message.reply_text(
                draw_tree(context.user_data["current_folder"]))
    except KeyError:
        update.message.reply_text("مافي هيك شي .. تأكد من الأسم..")

    except Exception as E:
        update.message.reply_text("خطأ أثناء الحذف")
        log_action(update, f"Error While Deleting File:\n{E}")


def create_backup_copy_command(update, context):
    if not update.message.from_user.id in ADMINS_IDS:
        update.message.reply_text(YOU_DONT_HAVE_ACCESS_TEXT)
        log_action(update, "Un Authorized Access")
        return None

    inp = update.message.text

    inp = inp.split('\n')
    backup_name = inp[1].strip()
    save_tree(start, custom_name=backup_name)
    log_action(update, f"Created BackUp Copy:{backup_name}.json")
    update.message.reply_text("حصل👍🏻")


def publication_command(update, context):
    try:
        pub_text = update.message.text[13:]
        users_ids = load_users_ids()
        log_text = "Sending Pulication.."
        for user in users_ids:
            log_text += '\n'
            try:
                updater.bot.sendMessage(user, pub_text)
                log_text += f"Sent To {user}"
            except Exception as E:
                log_text += f"FAILD Sent To {user}\ncuz: \n{E}"

        log_action(update, log_text)
        log_action(update, "Publicated")

    except Exception as E:
        log_action(update, f"Error When Publicating: \n{E}")
        update.message.reply_text("Error Publicating !")


# ===========================================================================================================================
# ===========================================================================================================================
# Main

updater = Updater(token=TOKEN, use_context=True)


def bot_on():
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('my_user_id', my_user_id_command))
    dispatcher.add_handler(CommandHandler('delete', delete_command))
    dispatcher.add_handler(CommandHandler('rename', rename_command))
    dispatcher.add_handler(CommandHandler('publication', publication_command))
    dispatcher.add_handler(CommandHandler('comment', comment_command))
    dispatcher.add_handler(CommandHandler('draw_tree', draw_tree_command))
    dispatcher.add_handler(CommandHandler(
        'backup', create_backup_copy_command))
    dispatcher.add_handler(CommandHandler('ma3lish', ma3lish_command))

    dispatcher.add_handler(CommandHandler('new_folder', new_folder))

    # Text
    dispatcher.add_handler(MessageHandler(
        Filters.text, process_input, pass_chat_data=True))
    # New File
    updater.dispatcher.add_handler(
        MessageHandler(Filters.document, new_file))

    print("UniBot IS ON ..")
    updater.start_polling()
    updater.idle()


def go():
    global start
    try:
        print("[HighLevelLog] Loading Tree .. ")
        start = load_tree()
        if start == None:
            print("[HighLevelLog] No Tree Found !")
            _ = input(
                "Do you want to build default tree ?? \npress enter to continue")
            start = build_default_tree()
            save_tree(start)
        draw_tree(start)
        bot_on()
    except Exception as E:
        print("[HighLevelLog] Error,Couldn't Run Bot..\n", E)


go()
print("-- UniBot IS OFF --")
