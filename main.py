from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests, sqlite3, time
import re

archivebox_url="" #e.g. http://192.168.1.10:9090
chatids = [CHAT_ID_HERE]
BOT_TOKEN = "BOTTOKEN_HERE"
csrfmiddlewaretoken = ""

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('This bot archives all urls in a chat')

def parseCookieFile(cookiefile):
    """Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests."""
    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                cookies[lineFields[5]] = lineFields[6]
    return cookies

def add_url(url_to_download):
    cookies = parseCookieFile('cookies.txt')
    data = {"csrfmiddlewaretoken":csrfmiddlewaretoken,"url": url_to_download, "parser": "auto", "tag":"Telegram", "depth":"0"}

    r = requests.post(f"{archivebox_url}/add/", data=data, cookies=cookies, timeout=1)

def check_for_urls(update: Update, context: CallbackContext) -> None:
    regexp = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)")
    if "/get" in update.effective_message.text:
        pass
    else:
        if regexp.match(update.effective_message.text):
            if update.effective_chat.id in chatids:

                urls = re.finditer(regexp, update.effective_message.text)
                for url in urls:
                    print(url.group())
                    try:
                        add_url(url.group())
                        #update.message.reply_text(f"Added {url.group()} to the archive!")
                    except requests.exceptions.Timeout as e:
                        #update.message.reply_text(f"Added {url.group()} to the archive!")
                        pass
                    except:
                        update.message.reply_text(f"Error adding url to archive")
            else:
                print(f"{update.effective_chat.id} tried to add {update.effective_message.text}")
                try:
                    update.message.reply_text(f"This is a private bot. Please do not use this!")
                except AttributeError:
                    #probably someone edited a message. Ignoring it and do not send msg again
                    pass

#split large msg
def send_message(bot, chat_id, text: str, **kwargs):
    if len(text) <= 4096:
        return bot.send_message(chat_id, text, **kwargs)

    parts = []
    while len(text) > 0:
        if len(text) > 4096:
            part = text[:4096]
            first_lnbr = part.rfind('\n')
            if first_lnbr != -1:
                parts.append(part[:first_lnbr])
                text = text[(first_lnbr+1):]
            else:
                parts.append(part)
                text = text[4096:]
        else:
            parts.append(text)
            break

    msg = None
    for part in parts:
        msg = bot.send_message(chat_id, part, **kwargs)
        time.sleep(1)
    return msg  # return only the last message

def get_archive(update: Update, context: CallbackContext):
    if update.effective_chat.id in chatids:
        #Get all archives matching context.args[1]
        if context.args[0] == "all":
            conn = sqlite3.connect('index.sqlite3', uri=True)
            c = conn.cursor()
            c.execute(f"SELECT url,id FROM core_snapshot WHERE url LIKE '%{context.args[1]}%'")
            conn.commit()
            rows = c.fetchall()
            archived_snapshots = []
            for row in rows:
                id = row[1]
                print(id)
                c.execute("SELECT pwd,snapshot_id FROM core_archiveresult WHERE snapshot_id =?", (id,))
                conn.commit()
                snaphots = c.fetchall()
                for snapshot in snaphots:
                    print(snapshot[0])
                    url = snapshot[0].replace("/data", "")
                    url = f"{archivebox_url}{url}/index.html"
                    if url not in archived_snapshots:
                        archived_snapshots.append(url)
            if len(archived_snapshots) > 0:
                msg = '\n'.join(archived_snapshots)
            else:
                msg = f"URL not in archive :("
            send_message(context.bot, update.effective_chat.id, msg)
        else:
            conn = sqlite3.connect('index.sqlite3', uri=True)
            c = conn.cursor()
            c.execute("SELECT url,id FROM core_snapshot WHERE url =?",(context.args[0],))
            conn.commit()
            rows = c.fetchall()
            archived_snapshots = []
            for row in rows:
                id = row[1]
                print(id)
                c.execute("SELECT pwd,snapshot_id FROM core_archiveresult WHERE snapshot_id =?", (id,))
                conn.commit()
                snaphots = c.fetchall()
                for snapshot in snaphots:
                    print(snapshot[0])
                    url = snapshot[0].replace("/data", "")
                    url = f"{archivebox_url}{url}/index.html"
                    if url not in archived_snapshots:
                        archived_snapshots.append(url)
            if len(archived_snapshots) >0:
                msg = '\n'.join(archived_snapshots)
            else:
                msg = f"URL not in archive :("
            context.bot.send_message(chat_id=update.message.chat_id, text=msg)
    else:
        update.message.reply_text(f"This is a private bot. Please do not use this!")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("get", get_archive))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_for_urls))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
