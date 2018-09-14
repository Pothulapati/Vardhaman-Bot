import tools.server
import tools.nlu
import tools.swear
import replies
import random

bot = tools.server.Bot(app_id = '98dc01e8-8d9a-432a-a76a-8ea3a62df9ee', app_password = 'xghsIVD353;@erwJFRQ22_^')

@bot.start
async def start(activity):
    await replies.welcome(activity, bot)

@bot.replies
async def reply(activity):
    await bot.send_typing_activity(activity)
    engine = tools.nlu.Engine()
    data = engine.parse(activity.text)
    intent = data.get_intent()
    entities = data.get_entities()
    has_bad_words = tools.swear.detector(activity.text)
    if activity.text != "Get Started":
        if not has_bad_words:
            try:
                print(intent)
                print(entities)
                reply_handler = getattr(replies, intent)
                await reply_handler(activity, bot, data)
            except (AttributeError, TypeError):
                await replies.default(activity, bot, data)
        else:
            if has_bad_words:
                print("curse")
                print(entities)
                reply = random.choice(["Zaban sambhaal ke bath karna", "Close your filthy mouth and then try me", "Don't think cussing is cool"])
                await bot.send_text_activity(activity, reply)
            else:
                print("default")
                print(entities)
                await replies.default(activity, bot, data)
    else:
        await replies.welcome(activity, bot)

tools.server.start(bot)