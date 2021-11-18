# ArchiveboxTelegramBot
A simple Telegram bot to send urls from a Telegram chat to Archivebox.  

## Requirements
[Archivebox](https://archivebox.io/)  
[Python-telegram-bot module](https://github.com/python-telegram-bot/python-telegram-bot)


## How to use
1. Download the script and put it in the archivebox directory containing the `index.sqlite3` database.  
2. Go to your Archivebox webpage and export the cookies to a `cookies.txt` file and put it in the same directory.  [Chrome extension](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid)
3. Paste your ArchiveBox url on line 6.  
4. Place the chatids of the chats on which you want the bot to respond to on line 7.  
5. Create a telegram bot and paste the token on line 8  
6. Go to your Archivebox and add an url. While you do so open the dev console of your browser and find the `csrfmiddlewaretoken` in the request header section.  
7. Paste the `csrfmiddlewaretoken` on line 9.  
8. Now run the bot. Every url you send to the bot will be archived by Archivebox.  

## Commands
`/help` Show info about bot.  
`/get <url>` Get latest archived version of the url from Archivebox.  
`/get all <keyword>` Get all urls in archivebox containing `keyword` in part of the url.  
