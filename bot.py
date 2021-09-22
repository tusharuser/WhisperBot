from telethon import events, TelegramClient, Button
import logging
from telethon.tl.functions.users import GetFullUserRequest as us
import os


logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", None)

bot = TelegramClient(
        "Lovely",
        api_id=6,
        api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e"
        ).start(
                bot_token=TOKEN
                )
db = {}

@bot.on(events.NewMessage(pattern="^[!?/]secret$"))
async def stsrt(event):
    await event.reply(
            "**Heya, I am a Lovely Bot!**",
            buttons=[
                [Button.switch_inline("Go Inline", query="")]
                ]
            )


@bot.on(events.InlineQuery())
async def die(event):
    if len(event.text) != 0:
        return
    me = (await bot.get_me()).username
    dn = event.builder.article(
            title="It's a Lovely bot!",
            description="It's a Lovely Bot!`\n**(c) 📢𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔 :- @LOVELY_NETWORK ❤️‍🔥**",
            text=f"**It's a Lovely bot**\n`@{me} secret UserID|Message`\n**(c) UPDATES @LOVELY_ROBOTS**",
            buttons=[
                [Button.switch_inline(" Go Inline ", query="secret ")]
                ]
            )
    await event.answer([dn])
    
@bot.on(events.InlineQuery(pattern="secret"))
async def inline(event):
    me = (await bot.get_me()).username
    try:
        inp = event.text.split(None, 1)[1]
        user, msg = inp.split("|")
    except IndexError:
        await event.answer(
                [], 
                switch_pm=f"@{me} [UserID]|[Message]",
                switch_pm_param="secret"
                )
    except ValueError:
        await event.answer(
                [],
                switch_pm=f"Give a message too!",
                switch_pm_param="secret"
                )
    try:
        ui = await bot(us(user))
    except BaseException:
        await event.answer(
                [],
                switch_pm="Invalid User ID/Username",
                switch_pm_param="secret"
                )
        return
    db.update({"user_id": ui.user.id, "msg": msg, "self": event.sender.id})
    text = f"""
A Lovely Has Been Sent
To [{ui.user.first_name}](tg://user?id={ui.user.id})!
Click The Below Button To See The Message!
**Note:** __Only {ui.user.first_name} can open this!__
    """
    dn = event.builder.article(
            title="Its a secret message! Sssh",
            description="It's a secret message! Sssh!",
            text=text,
            buttons=[
                [Button.inline(" Show Message! ", data="secret")]
                ]
            )
    await event.answer(
            [dn],
            switch_pm="It's a secret message! Sssh",
            switch_pm_param="secret"
            )


@bot.on(events.CallbackQuery(data="secret"))
async def ws(event):
    user = int(db["user_id"])
    lol = [int(db["self"])]
    lol.append(user)
    if event.sender.id not in lol:
        await event.answer("🔐 This message is not for you!", alert=True)
        return
    msg = db["msg"]
    if msg == []:
        await event.anwswer(
                "Oops!\nIt's looks like message got deleted from my server!", alert=True)
        return
    await event.answer(msg, alert=True)

print("Succesfully Started Bot!")
bot.run_until_disconnected()
