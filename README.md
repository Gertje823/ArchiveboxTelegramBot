# ArchiveboxTelegramBot
A simple Telegram bot to send urls from a Telegram chat to Archivebox.  

## Requirements
[Archivebox](https://archivebox.io/)  
[Python-telegram-bot module](https://github.com/python-telegram-bot/python-telegram-bot)


## How to use
1. Paste your ArchiveBox url on line 6.  
2. Place the chatids of the chats on which you want the bot to respond to on line 7.  
3. Create a telegram bot and paste the token on line 8  
4. Go to your Archivebox and add an url. While you do so open the dev console of your browser and find the `csrfmiddlewaretoken` in the request header section.  
5. Paste the `csrfmiddlewaretoken` on line 9.  
6. Now run the bot. Every url you send to the bot will be archived by Archivebox.  

## Commands
`/help` Show info about bot.  
`/get <url>` Get latest archived version of the url from Archivebox.  
`/get all <keyword>` Get all urls in archivebox containing `keyword` in part of the url.  
