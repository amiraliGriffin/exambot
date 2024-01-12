from pyrogram import Client

plug = dict(root="plugins")
#----
bot = Client(
    name = "shishlig",
    api_id = 29585063,
    api_hash = "7cbc271846d81539d10bdec6cf36ba6a",
    bot_token = "6583392482:AAFEOh1NwXRd2qn0uDBb0OisgTmPniWTZPo",
    plugins = plug
)

bot.run()
