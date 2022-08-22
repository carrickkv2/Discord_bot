### Schedule Bot

A discord bot created for the faith community [discord server.](https://discord.gg/2JVQNmJR8y)

This bot gets the schedule image posted in announcements and makes it easier for people to know the days on which events are happening.
It does this by converting the image to csv and then storing it for easy access.
Times are given in either EST or the users time zone. An example of the type of image supported is included in the files.

Preferably, I'll be happy if you invite the bot to your server, but if you want to run an instance yourself, these are the steps.

1. Git clone the repo to a directory of your choice.
2. Outside the cloned directory, create 2 folders, old and output_csv (These can be any name you want)
3. In the python file paths_for_functions, change the respective paths to your own paths.
4. Create a .env file in the main directory (where bot.py is) and add your bot's Token and Extract API Token to it.
   (Token and Api should both be in full caps)
6. Install all the libraries needed from requirements.txt
5. Run the bot.py file

An example csv has been given in the csv directory. This is to prevent any errors when the bot starts.


- [ ] TODO: Add reminders.
