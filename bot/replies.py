import random

from tinydb import TinyDB, Query
from tools.scraper import Scraper

async def welcome(activity, bot):
    await bot.send_text_activity(activity, "Hey, I am the Vardhaman Bot.")
    await bot.send_text_activity(activity, "For, advanced features, please authenticate.")
    await bot.send_text_activity(activity, "To authenticate, enter your roll no. and web access key seperated by a space.")

async def greet(activity, bot, data):
    reply = random.choice(["Hi", "Hi there!", "Hello", "Hey there!"])
    await bot.send_text_activity(activity, reply)

async def about(activity, bot, data):
    await bot.send_text_activity(activity, "Why are you asking about our college?")

async def appreciation(activity, bot, data):
    await bot.send_text_activity(activity, "Aww! Thanks so much.")
    await bot.send_text_activity(activity, "But, really all this appreciation goes to my creators.")

async def thanks(activity, bot, data):
    reply = random.choice(["I'm glad I'm helpful!", "You're welcome!"])
    await bot.send_text_activity(activity, reply)

async def authenticate(activity, bot, data):
    print(data.get_entities())
    credentials = activity.text.split(" ")
    rollno = credentials[0]
    wak = credentials[1]
    if len(wak) > 5:
        await bot.send_text_activity(activity, "Please check your roll no. and web access key again.")
        await bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")
        return
    scraper = Scraper()
    scraper.authenticate(rollno,wak)
    if scraper.authenticated:
        query = Query()
        db = TinyDB('./db.json')
        result = db.search(query.userid == activity.from_property.id)
        if len(result) > 0:
            db.update({'rollno': rollno, 'wak' : wak}, query.userid == activity.from_property.id)
            await bot.send_text_activity(activity, "Authentication Successful!")
        else:
            db.insert({'userid': activity.from_property.id, 'rollno':  rollno, 'wak': wak})
            await bot.send_text_activity(activity, "Authentication Successful!")
    else:
        await bot.send_text_activity(activity, "Please check your roll no. and web access key again.")
        await bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")

async def attendance_enquiry(activity, bot, data):
    query = Query()
    db = TinyDB('./db.json')
    result = db.search(query.userid == activity.from_property.id)
    scraper = Scraper()
    if len(result) > 0:
        result = result[0]
        rollno = str(result['rollno'])
        wak = str(result['wak'])
        scraper.authenticate(rollno, wak)
        attendance = scraper.get_attendance()
        reply  = "Your attendance is " + str(attendance)
        await bot.send_text_activity(activity, reply)
        if attendance > 95:
            reply = "What are you? A book worm? 😏"
        elif attendance > 85: 
            reply = "Good Going! 😁"
        elif attendance > 80:
            reply = "Making the best of both worlds huh? 😎"
        elif attendance > 75: 
            reply =  "I see you've been bunking a lot of classes lately. 🤨 Be cautious and attend your classes."
        elif attendance > 65:
            reply = "You should go to your classes if you don't want to burn a hole in your pocket. 😕"
        else:
            reply = "I hope your okay with sitting amongst your juniors next year. 🤭"
        await bot.send_text_activity(activity, reply)
    else:
        await bot.send_text_activity(activity, "Authentication failed. Please message your rollno and web access key again.")
        await bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")

async def gpa_enquiry(activity, bot, data):
    query = Query()
    db = TinyDB('./db.json')
    result = db.search(query.userid == activity.from_property.id)
    scraper = Scraper()
    if len(result) > 0:
        result = result[0]
        rollno = str(result['rollno'])
        wak = str(result['wak'])
        scraper.authenticate(rollno, wak)
        gpa = scraper.get_cgpa()
        reply = "Your CGPA is " + str(gpa)
        await bot.send_text_activity(activity, reply)
        if gpa > 9.5:
            reply = "Woah! Look at you going all out on your tests! Awesome! 💯"
        elif gpa > 9.0:
            reply = "Are you sure you aren't Einstein? 🧐 Keep up the good work! 👍"
        elif gpa > 8.0:
            reply = "We've got a champ here! You are doing great! 👏"
        elif gpa > 7.0:
            reply = "Hang in there bud! You're on the right track! ✌"
        elif gpa > 6.0:
            reply = "Who needs a good CGPA when you're cool no? 😎 JK, you still need it.. 😅"
        else:
            reply = " It's okay, you don't have to be a topper!  The only one you have to beat is the one you were last semester. Work harder this time! 😉"
        await bot.send_text_activity(activity, reply)
    else:
        await bot.send_text_activity(activity, "Authentication failed. Please message your rollno and web access key again.")
        await bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")

async def closingrank_enquiry(activity, bot, data):
    entities = data.get_entities()
    department  = str(entities['department']).lower()
    reply  = f"The Closing rank for General Category of {department} is "
    if department == 'mechanical':
        reply += "18275"
    elif department == 'cse':
        reply += "6684"
    elif department == 'ece':
        reply += "9874"
    elif department == 'eee':
        reply += "11365"
    elif department == 'it':
        reply += "10635"
    elif department == 'civil':
        reply += "12835"
    await bot.send_text_activity(activity, reply)

async def timetable_enquiry(activity, bot, data):
    await bot.send_text_activity(activity, "You asked for your timetable.")

async def default(activity, bot, data):
    reply = random.choice(["Sorry, I could not understand your message.", "Sorry, your enquiry is either beyond my reach or I wasn't clever enough."])
    await bot.send_text_activity(activity, reply)
