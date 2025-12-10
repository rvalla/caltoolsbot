![logo](https://gitlab.com/musicaltools/calac/-/raw/master/assets/img/icon_64.png)

# musicCal: telegram bot changelog

## 2025-12-10: v0.2.2 beta

Updating **CAlpytools** again to solve an error en **Chain()**.  

## 2025-12-02: v0.2.1 beta

Starting to work in a new way to handle messages and translations with *regex* module. The **/chain**
command was improved and now support operations (translation, invertion and iteration).  
**Calpytools** was updated.   

## 2025-10-14: v0.2.0 beta

The **Usage()** was improved. Some errors were solved. Now the **User()** class
save user's preferences. Note the following command changes:

- **/start**: now it implements a conversations to save an artistic name and preferred time
signature for the user. Getting ready to new tools to create music...
- **/random**: the command to create random sequences (the fuctions needed are in **Util()**
class.  
- **/privacy**: Telegram ask for this one.  
- **/admin**: A new secret commad to check usage data.  

## 2023-04-23: v0.1.5 alpha

All issues with **PCS()** class are solved now. The **/pcs** commands is implemented inside a
conversation. I improved conversational style messages. Note the following command changes:

- **/pcs**: now there is no need to send a set inmediately. The command starts a pitch class sets
analysis session (a conversation).  
- **/error**: a new command to allow every user to report errors directly. The report is saved in
*errors.csv* and sent to the administrator chat.  

There is a [musiCal](https://musicaltools.gitlab.io) project website now and a
[telegram channel](https://t.me/caltools) too. You can check the bot news there!  

## 2023-04-18: v0.1 alpha

First steps setting the bot. Testing *commandhandling* and different types of sent objects. The **bot** is in
*bot.py* file but use a set of classes. List of commands:  

- **/start**: to say hi.
- **/language**: to select language.
- **/help**: to ask for help about how to use the bot.

Reach **musiCal bot** [here](https://t.me/caltools_bot).
Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
