from pyrogram import Client , filters
from pyrogram import StopPropagation as stop
from pyrogram.types import ReplyKeyboardMarkup
from pyrogram.types import InlineKeyboardMarkup as ink
from pyrogram.types import InlineKeyboardButton as inb
from pyrogram.types import BotCommand as cmd
from pyrogram.types import ReplyKeyboardRemove as Kremover
import json
import datetime as dt
import pytz as Tzone
#----------
CD = {
    "err_check_num" : "❌لطفا از اعداد در نام خود استفاده نکنید",
    "confirmation_for_name" :  "نام شما با موفقیت ثبت شد✅\nبا کلیک بر روی دکمه زیر شماره خود را به اشتراک بگذارید\nvدر صورتی که مایل به ثبت شماره دیگری هستید شماره خود را وارد کنید",
    "register_confirmation" : "به خانواده برزگ ایولرن خوش آمدید😍\nمنتظر تماس منتور ها باشید",
    "name_ask"  : "لطفا نام و نام خانوادگی خودرا وارد نمایید",
    "field_ask" : "شماره شما با موفقیت ثبت شد✅\nدانشجوی عزیز لطفا رشته خود را انتخاب نمایید",
    "exam_name" : "please enter the exam name"
}
#------ General functions
def file_get_contents(address):
    file = open(address)
    file = file.readlines()
    return file
def file_put_contents(address,element,mode="w"):
    if mode == "w" :
        file = open(address,mode)
        file = file.write(element)
        return True
    elif mode == "a" :
        file = open(address,mode)
        file = file.write(element)
        return True
    else :
        return False
def Jread(address):
   jfile = open(address)
   jobj = json.load(jfile)
   return jobj
def Jwrite(address,obj):
   jobj = json.dumps(obj)
   file_put_contents(address,jobj)
def request_counter():
    C = file_get_contents("DB/request_count.txt")
    C = int(C[0])
    C += 1
    C = str(C)
    file_put_contents("DB/request_count.txt",C)
#----------
@Client.on_message(filters.command("start"))
def start(client,message) :
    CHI = message.chat.id
    client.send_message(CHI,CD["name_ask"],reply_markup=Kremover())
    file_put_contents(f"BM/{CHI}.txt","Greeting")
    #----
    client.set_bot_commands([
        cmd("start","start the bot")
    ])
    #----
    request_counter()
    raise stop
@Client.on_message(filters.regex("ADMIN_PRIVATE_PANEL"))
def admin(client,message):
    CHI = message.chat.id
    #-----
    kb = ReplyKeyboardMarkup([
        ["define exam"],
        ["compose exam"],
        ["time"],
        ["upload"],
        ["ranks"],
        ["help"]
    ]
    )
    file_put_contents(f"BM/{CHI}.txt","off")
    client.send_message(CHI,"لطفا گزینه مورد نظر انتخاب کنید",reply_markup=kb)
    raise stop
@Client.on_message(filters.regex("help"))
def hel(client,message):
    CHI = message.chat.id
    #-----
    help = "🔹 del*\n\nدستور حذف فایل آزمون یا سوال به ترتیب در دو بخش difine exam و compose exam\n\n🔹 which\n\nدستور اطلاع از اینکه کدام فایل آزمون فعال است در بخش compose exam\n\n🔹 ex*\n\nدستور فعالسازی فایل آزمون مورد نظر در بخش compose exam\n\n🔹 preview\n\nدستور دیدن تمامی سوالات به صورت یکجا در قسمت compose exam\n\n🔹 exit\n\nدستور خروج از workspace قسمت compose exam\n\n🔹off\n\nدستور حذف فایل آپلود شده در قسمت upload"
    client.send_message(CHI,help)
    file_put_contents(f"BM/{CHI}.txt","off")
    raise stop
@Client.on_message(filters.regex("send to all"))
def STA(client,message):
    CHI = message.chat.id
    #------
    client.send_message(CHI,"لطفا پیام خود را ارسال کنید")
    file_put_contents(f"BM/{CHI}.txt","STA")
    raise stop
@Client.on_message(filters.regex("define exam"))
def DE(client,message):
    CHI = message.chat.id
    #------
    client.send_message(CHI,CD["exam_name"])
    file_put_contents(f"BM/{CHI}.txt","define exam")
    raise stop
@Client.on_message(filters.regex("compose exam"))
def CE(client,message):
    CHI = message.chat.id
    #------
    client.send_message(CHI,"workapace activated")  # tobe changed
    file_put_contents(f"BM/{CHI}.txt","compose exam")
    raise stop
@Client.on_message(filters.regex("time"))
def time(client,message):
    CHI = message.chat.id
    #------
    client.send_message(CHI,"please set a time")  # tobe changed
    file_put_contents(f"BM/{CHI}.txt","time")
    raise stop
@Client.on_message(filters.regex("upload"))
def upload(client,message):
    CHI = message.chat.id
    #------
    client.send_message(CHI,"please write down exam name")  # tobe changed
    file_put_contents(f"BM/{CHI}.txt","upload")
    raise stop
@Client.on_message(filters.regex("real time request"))
def realreq(client,message):
    CHI = message.chat.id
    #------
    RR = file_get_contents("DB/request_count.txt")
    RR = RR[0]
    client.send_message(CHI,RR)
    raise stop
@Client.on_message(filters.regex("آزمون"))
def azmoon(client , message) :
    text = message.text
    CHI  = message.chat.id
    #------
    etime    = Jread("exam controls/Time&exam.json")
    stime    = etime[0]
    atime    = etime[2]
    #----
    tizone   = Tzone.timezone("Asia/Tehran")
    currtime = dt.datetime.now(tizone)
    currtime = currtime.strftime("%H:%M")
    #----
    examtype     = Jread("exam controls/Tarexam.json")
    examtype     = examtype[0]
    try : 
        examregister = Jread("exam results/res.json")
        exa          = examregister[examtype]
        exakeys = list(exa.keys())
        for person in exakeys :
            if str(CHI) == person :
                client.send_message(CHI,"یکبار بیشتر نمیشه آزمون بدین ☕️")
                break
        else :
            if stime <= currtime <= atime and examtype != "off":
                examtype  = Jread("exam controls/Tarexam.json")
                examtype  = examtype[0]
                questions = Jread(f"exam sheets/{examtype}.json")
                #-----
                Q_num = 0
                Q = list(questions.keys())
                Q_show = Q[Q_num]
                Q_select = questions[Q_show]
                for ans in Q_select :
                        if ans.find("✅") != -1 :
                            ind = Q_select.index(ans)
                            break
                Q_select[ind] = Q_select[ind].replace("✅" , "")
                ans1 , ans2 , ans3 , ans4 = Q_select
                #-----
                try :
                    print("done")
                    obj = Jread(f"exam answer/{examtype}.json")
                    whatans = obj[str(CHI)]["0"]
                    if whatans == "1" :
                        ans1 = ans1 + "✅"
                    elif whatans == "2" :
                        ans2 = ans2 + "✅"
                    elif whatans == "3" :
                        ans3 = ans3 + "✅"
                    elif whatans == "4" :
                        ans4 = ans4 + "✅"
                except :
                    x = None
                #-----
                keyb = ink([
                    [
                        inb(ans1 , "0_1")
                    ],
                    [
                        inb(ans2 , "0_2")
                    ],
                    [
                        inb(ans3 , "0_3")
                    ],
                    [
                        inb(ans4 , "0_4")
                    ],
                    [
                        inb(">>>" , f"next_{Q_num + 1}")
                    ]
                ])
                #-----
                client.send_message(CHI , Q_show , reply_markup=keyb)
            else :
                if examtype == "off" or stime == "1" :
                    client.send_message(CHI,"آزمونی فعال نیست")
                else :
                    if currtime < stime :
                        client.send_message(CHI,"آزمون طراحی و فعال شده‌ها ولی زود اومدی")
                    else : 
                        client.send_message(CHI,"فرصت شرکت در آزمون به اتمام رسیده ☕️")
    except :
        if stime <= currtime <= atime and examtype != "off":
                examtype  = Jread("exam controls/Tarexam.json")
                examtype  = examtype[0]
                questions = Jread(f"exam sheets/{examtype}.json")
                #-----
                Q_num = 0
                Q = list(questions.keys())
                Q_show = Q[Q_num]
                Q_select = questions[Q_show]
                for ans in Q_select :
                        if ans.find("✅") != -1 :
                            ind = Q_select.index(ans)
                            break
                Q_select[ind] = Q_select[ind].replace("✅" , "")
                ans1 , ans2 , ans3 , ans4 = Q_select
                #-----
                try :
                    print("done")
                    obj = Jread(f"exam answer/{examtype}.json")
                    whatans = obj[str(CHI)]["0"]
                    if whatans == "1" :
                        ans1 = ans1 + "✅"
                    elif whatans == "2" :
                        ans2 = ans2 + "✅"
                    elif whatans == "3" :
                        ans3 = ans3 + "✅"
                    elif whatans == "4" :
                        ans4 = ans4 + "✅"
                except :
                    x = None
                #-----
                keyb = ink([
                    [
                        inb(ans1 , "0_1")
                    ],
                    [
                        inb(ans2 , "0_2")
                    ],
                    [
                        inb(ans3 , "0_3")
                    ],
                    [
                        inb(ans4 , "0_4")
                    ],
                    [
                        inb(">>>" , f"next_{Q_num + 1}")
                    ]
                ])
                #-----
                client.send_message(CHI , Q_show , reply_markup=keyb)
        else :
            if examtype == "off" or stime == "1":
                client.send_message(CHI,"آزمونی فعال نیست")
            else :
                if currtime < stime :
                    client.send_message(CHI,"آزمون طراحی و فعال شده‌ها ولی زود اومدی")
                else : 
                    client.send_message(CHI,"فرصت شرکت در آزمون به اتمام رسیده ☕️")
@Client.on_message(filters.regex("ranks"))
def ranks(client , message) :
    text = message.text
    CHI  = message.chat.id
    #------
    try :
        examres    = Jread("exam results/res.json")
        examkeys   = list(examres.keys())
        lastexam   = examkeys[-1]
        selectexam = examres[lastexam]
        #----
        reslist = []
        names = Jread("DB/db.json")
        for person , profile in selectexam.items() :
            name  = names[person]["name"]
            score = profile[0]
            com   = (name , score)
            #----
            reslist.append(com)
        def sorter(ob) :
            return ob[1]
        reslist.sort(key=sorter,reverse=True)
        #-----
        T = ""
        for val in reslist :
            name  = val[0]
            score = val[1]
            #----
            ind  = reslist.index(val)
            rank = ind + 1
            #----
            T = T + f"{rank}- {name}({score})\n"
        client.send_message(CHI,T)
        file_put_contents(f"BM/{CHI}.txt","off")
    except :
        client.send_message(CHI,"NO result here")
        file_put_contents(f"BM/{CHI}.txt","off")
@Client.on_message(~filters.command("start"))
def error(client,message):
    CHI = message.chat.id
    #----
    client.send_message(CHI,"❌")




