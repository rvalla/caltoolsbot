![logo](https://gitlab.com/musicaltools/musicaltools.gitlab.io/-/raw/themoststable/public/assets/img/logo_64.png)

# musiCal: telegram bot

This is the code for a telegram bot.

## online status

**musiCal Bot** is not currently deployed. It will be available during some moments of the week while I run
some tests. Stay tuned!  

## running the code

Note that you will need a *config.json* file on root which includes the bot's token to run this software.
I suggest the following fieldsvalthough currently only *token* (provided by [@BotFather](https://t.me/BotFather)
and *logging* (info, debugging or persistent) are mandatory:

```
{
	"bot_name": "musiCal Bot",
	"date": "2021-11-01",
	"username": "caltools_bot",
	"admin_id": "A mistery",
	"link": "https://t.me/caltools_bot",
	"token": "I won't tell you my token",
	"password": "Sorry, I won't tell the password either",
	"public_ip": "255.255.255.255",
	"webhook": false,
	"webhook_path": "some_url_path_for_webhook",
	"webhook_port": 8443,
	"logging": "info"
}

```
## standing upon the shoulders of giants

This little project is possible thanks to a lot of work done by others in the *open-source* community. Particularly in
this case I need to mention:

- [**Python**](https://www.python.org/): the programming language I used.  
- [**python-telegram-bot**](https://python-telegram-bot.org/): the library I used to contact the *Telegram API*.  

Reach **musiCal bot** [here](https://t.me/caltools_bot).
Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
