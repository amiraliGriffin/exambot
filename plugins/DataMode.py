from pyrogram import Client , filters
from pyrogram import StopPropagation as stop
from pyrogram import enums
from pyrogram.types import ReplyKeyboardMarkup
from pyrogram.types import InlineKeyboardMarkup as ink
from pyrogram.types import InlineKeyboardButton as inb
from pyrogram.types import KeyboardButton as keyb
from pyrogram.types import ReplyKeyboardRemove as Kremover
import os
import json
#-----------
CD = {
    "err_check_num" : "لطفا از اعداد در نام خود استفاده نکنید",
    "confirmation_for_Field" : "شغل شما با موفقیت ثبت شد✅\nلطفا سن خود را وارد نمایید",
    "register_confirmation" : "اطلاعات شما با موفقیت ثبت شد✅\nمنتظر تماس مننور های ما باشید\nدر صورت اشتباه در ثبت اطلاعات یا ثبت اطلاعات برای شخص دیگری مجددا از دستور /start استفاده نمایید",
    "name_ask"  : "لطفا نام و نام خانوادگی خودتون رو وارد کنید",
    "confirmation_for_Age" : "سن شما با موفقیت ثبت شد✅\nبا کلیک بر روی دکمه زیر شماره خود را به اشتراک بگذارید\nدر صورتی که مایل به ثبت شماره دیگری هستید شماره خود را وارد کنید",
    "reg" : "ثبت نام شما با موفقیت انجام شد✅\nبا زدن دکمه شروع آزمون می تونید آزمون رو شروع کنید",
    "file_made" :"file has been made",
    "file_delete" : "file has been deleted",
    "no_file" : "no such file or directory"
}
number_persian_dic = {
    "۰" : "0",
    "۱" : "1",
    "۲" : "2",
    "۳" : "3",
    "۴" : "4",
    "۵" : "5",
    "۶" : "6",
    "۷" : "7",
    "۸" : "8",
    "۹" : "9",
    "0" : "0",
    "1" : "1",
    "2" : "2",
    "3" : "3",
    "4" : "4",
    "5" : "5",
    "6" : "6",
    "7" : "7",
    "8" : "8",
    "9" : "9",
}
#-----------
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
def Jdelete(address,item):
   js  = Jread(address)
   #--
   del js[item]
   #--
   Jwrite(address,js)
def request_counter():
    C = file_get_contents("DB/request_count.txt")
    C = int(C[0])
    C += 1
    C = str(C)
    file_put_contents("DB/request_count.txt",C)
#----- General filters
def BotMode(mode) :
    def func(hand,__,message) :
        try :
            CHI = message.chat.id
            file = file_get_contents(f"BM/{CHI}.txt")
            file = file[0]
            return hand.data == file
        except :
            x = "nothing to do"
    return filters.create(func,data=mode)
#------------
@Client.on_message(BotMode("Greeting") & ~filters.command("start") & ~filters.regex("ADMIN_PRIVATE_PANEL"))
def greet(client,message):
    CHI  = str(message.chat.id)
    text = str(message.text)
    #-----
    try : 
        numstr = "0123456789"
        for num in numstr :
            if num in text :
                raise Exception("do not use numbers")
    except :
        client.send_message(CHI,CD["err_check_num"])
    else :
        try :
            obj = Jread("DB/db.json")
            obj[CHI]["name"] = text
            Jwrite("DB/db.json",obj)
        except :
            obj = Jread("DB/db.json")
            obj[CHI] = {"name" : text}
            Jwrite("DB/db.json",obj)
        #-----
        key = ReplyKeyboardMarkup([
            ["آزمون"],
        ])
        client.send_message(CHI,CD["reg"],reply_markup=key)
        file_put_contents(f"BM/{CHI}.txt","off")
        #-----
    raise stop
@Client.on_message(BotMode("define exam") & ~filters.command("start") & ~filters.regex("ADMIN_PRIVATE_PANEL") & ~filters.regex("send to all") & ~filters.regex("real time request")& ~filters.regex("define exam")& ~filters.regex("compose exam")& ~filters.regex("time")& ~filters.regex("upload")& ~filters.regex("ranks") & ~filters.regex("help"))
def defineExam(client , message) :
    text = message.text
    CHI  = message.chat.id
    #-----
    tspl = text.split("*")
    if tspl[0] != "del" :
        obj = {}
        Jwrite(f"exam sheets/{tspl[0]}.json",obj)
        Jwrite(f"exam answer/{tspl[0]}.json",obj)
        client.send_message(CHI,CD["file_made"])
        file_put_contents(f"BM/{CHI}.txt","off")
    else :
        try :
            os.remove(f"exam sheets/{tspl[1]}.json")  
            os.remove(f"exam answer/{tspl[1]}.json")
            client.send_message(CHI,CD["file_delete"])
            file_put_contents(f"BM/{CHI}.txt","off")
        except :
            client.send_message(CHI,CD["no_file"])
            file_put_contents(f"BM/{CHI}.txt","off")
@Client.on_message(BotMode("compose exam") & ~filters.command("start") & ~filters.regex("ADMIN_PRIVATE_PANEL") & ~filters.regex("send to all") & ~filters.regex("real time request")& ~filters.regex("define exam")& ~filters.regex("compose exam")& ~filters.regex("time")& ~filters.regex("upload")& ~filters.regex("ranks") & ~filters.regex("help"))
def composeExam(client , message) :   # to be edited
    text = message.text
    CHI  = message.chat.id
    #-----
    tspl = text.split("*")
    #-----
    if tspl[0] != "del" and tspl[0] != "ex" and tspl[0] != "preview" and tspl[0] != "which" and tspl[0] != "exit":
        try :
            #----
            chspc = tspl[0].split(" ")
            if "" in chspc :
                raise Exception("no space at the end of question")
            #----
            for ans in tspl :
                if ans.find("/") != -1 :
                    ind = tspl.index(ans)
            #-----
            tspl[ind] = tspl[ind].replace("/" , "✅")
            #-----
            question_compile = f"{tspl[0]}\n\n1-{tspl[1]}\n\n2-{tspl[2]}\n\n3-{tspl[3]}\n\n4-{tspl[4]}" #error HAN = we have more or less than 4 index
            #-----
            #db parts
            Cexam = Jread("exam controls/Cexam.json")
            Cexam = Cexam[0]  
            client.send_message(CHI,question_compile) 
            try :  # tip : editing question
                obj = Jread(f"exam sheets/{Cexam}.json")
                #----
                cvar = obj[tspl[0]]
                #----
                obj[tspl[0]] = [tspl[1] , tspl[2] , tspl[3] , tspl[4]]
                Jwrite(f"exam sheets/{Cexam}.json",obj)
                #----
                client.send_message(CHI , "has changed")
            except : # tip : add new question
                obj = Jread(f"exam sheets/{Cexam}.json")
                obj[tspl[0]] = [tspl[1] , tspl[2] , tspl[3] , tspl[4]]
                Jwrite(f"exam sheets/{Cexam}.json",obj)
                #----
                client.send_message(CHI , "new question added")
        except :
            client.send_message(CHI,"question wrong format or no exam has been determined")
    else :
        if tspl[0] == "del" :
            examtype  = Jread("exam controls/Cexam.json")
            examtype = examtype[0]
            try :
                obj = Jread(f"exam sheets/{examtype}.json")
                del obj[tspl[1]]
                Jwrite(f"exam sheets/{examtype}.json",obj)
                client.send_message(CHI,"this question deleted")  
            except :
                client.send_message(CHI,"NO such a question")
        elif tspl[0] == "ex" :
            filecheck = os.listdir("exam sheets")
            if f"{tspl[1]}.json" in filecheck :
                obj = [f"{tspl[1]}"]
                Jwrite("exam controls/Cexam.json",obj)
                client.send_message(CHI,f"{tspl[1]} activated")
            else :
                client.send_message(CHI,"NO such exam")
        elif tspl[0] == "preview" :
            examtype  = Jread("exam controls/Cexam.json")
            examtype  = examtype[0]
            #----
            examsheet = Jread(f"exam sheets/{examtype}.json")
            #----
            try :
                pr = ""
                for Q , A in examsheet.items() :
                    pq = f"🔹{Q}\n1-{A[0]}\n2-{A[1]}\n3-{A[2]}\n4-{A[3]}\n\n"
                    pr = pr + pq
                client.send_message(CHI,pr)
            except :
                client.send_message(CHI,"no question added")
        elif tspl[0] == "which" :
            try :
                examtype  = Jread("exam controls/Cexam.json")
                examtype  = examtype[0]
                #----
                client.send_message(CHI,f"{examtype} is active")
            except :
                client.send_message(CHI,"no exam determined")
        elif tspl[0] == "exit" :
            file_put_contents(f"BM/{CHI}.txt" , "off")
            client.send_message(CHI,"workspace deactivated")
@Client.on_message(BotMode("time") & ~filters.command("start") & ~filters.regex("ADMIN_PRIVATE_PANEL") & ~filters.regex("send to all") & ~filters.regex("real time request")& ~filters.regex("define exam")& ~filters.regex("compose exam")& ~filters.regex("time")& ~filters.regex("upload")& ~filters.regex("ranks") & ~filters.regex("help"))
def timeexam(client , message):
    text = message.text
    CHI  = message.chat.id
    #-----
    tspl = text.split("*")
    #-----
    text = message.text
    CHI  = message.chat.id
    #-----
    tspl = text.split("*")
    #-----
    try :
        sp  = tspl[0].split(":")
        sp1 = tspl[1].split(":")
        sp2 = tspl[1].split(":")
        ch1 = int(sp[0])
        ch2 = int(sp[1])
        ch3 = int(sp1[0])
        ch4 = int(sp1[1])
        ch5 = int(sp1[0])
        ch6 = int(sp1[1])
        #----
        obj = [tspl[0] , tspl[1] , tspl[2]]   
        Jwrite("exam controls/Time&exam.json",obj)
        file_put_contents(f"BM/{CHI}.txt" , "off")
        client.send_message(CHI,"time has set on exam")
    except :
        client.send_message(CHI,"please do write format")
@Client.on_message(BotMode("upload") & ~filters.command("start") & ~filters.regex("ADMIN_PRIVATE_PANEL") & ~filters.regex("send to all") & ~filters.regex("real time request")& ~filters.regex("define exam")& ~filters.regex("compose exam")& ~filters.regex("time")& ~filters.regex("upload")& ~filters.regex("ranks") & ~filters.regex("help"))
def uploadexam(client , message) :
    text = message.text
    CHI  = message.chat.id
    #-----
    if f"{text}.json" in os.listdir("exam sheets") or text == "off" :
        obj = [text]
        Jwrite("exam controls/Tarexam.json",obj)
        file_put_contents(f"BM/{CHI}.txt" , "off")
        client.send_message(CHI,"exam has uploaded")
    else :
        client.send_message(CHI,"no such exam")
@Client.on_message(BotMode("STA") & ~filters.command("start") & ~filters.regex("ADMIN_PRIVATE_PANEL") & ~filters.regex("send to all") & ~filters.regex("real time request") &  ~filters.regex("define exam")& ~filters.regex("compose exam")& ~filters.regex("time")& ~filters.regex("upload")& ~filters.regex("ranks") & ~filters.regex("help"))
def lets_send(client,message):
    CHI     = str(message.chat.id)
    if hasattr(message.video,'file_id') :
        file_id = message.video.file_id
        cap = message.caption
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_video(person,file_id,caption=cap)
    elif hasattr(message.voice,'file_id') :
        file_id = message.voice.file_id
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_voice(person,file_id)
    elif hasattr(message.photo,'file_id') :
        file_id = message.photo.file_id
        cap = message.caption
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_photo(person,file_id,caption=cap)
    elif hasattr(message.audio,'file_id') :
        file_id = message.audio.file_id
        cap = message.caption
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_audio(person,file_id,caption=cap)
    elif hasattr(message.document,'file_id') :
        file_id = message.document.file_id
        cap = message.caption
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_document(person,file_id,caption=cap)
    else :
        text = message.text
        obj     = Jread("DB/db.json")
        ci  = list(obj.keys())
        for person in ci :
            client.send_message(person,text)
    #-----
    client.send_message(CHI,"پیام شما برای تمامی کاربران ارسال شد✅",reply_markup=Kremover())
    file_put_contents(f"BM/{CHI}.txt","off")
    raise stop
