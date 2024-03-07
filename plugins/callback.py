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
import datetime as dt
import pytz as Tzone
import time as t
#-----------
CD = {
    "err_check_num" : "لطفا از اعداد در نام خود استفاده نکنید",
    "confirmation_for_Field" : "شغل شما با موفقیت ثبت شد✅\nلطفا سن خود را وارد نمایید",
    "register_confirmation" : "اطلاعات شما با موفقیت ثبت شد✅\nمنتظر تماس مننور های ما باشید\nدر صورت اشتباه در ثبت اطلاعات یا ثبت اطلاعات برای شخص دیگری مجددا از دستور /start استفاده نمایید",
    "name_ask"  : "لطفا نام و نام خانوادگی خودرا وارد نمایید",
    "confirmation_for_Age" : "سن شما با موفقیت ثبت شد✅\nبا کلیک بر روی دکمه زیر شماره خود را به اشتراک بگذارید\nدر صورتی که مایل به ثبت شماره دیگری هستید شماره خود را وارد کنید",
    "reg" : "نام شما با موفقیت ثبت شد✅\nلطفا شغل خود را وارد کنید",
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
def callType(callbackdata):
    def func(flt,_,query) :
        cld = query.data
        cld = cld.split('_')
        return flt.data == cld[0]
    return filters.create(func,data=callbackdata)
#------------
@Client.on_callback_query(callType("next") | callType("previous"))
def uplque(client , query) :
    cli  = query.id
    cld  = query.data
    CHI  = query.message.chat.id
    MID  = query.message.id
    cldx = cld.split("_")
    #------
    examtype  = Jread("exam controls/Tarexam.json")
    examtype  = examtype[0]
    questions = Jread(f"exam sheets/{examtype}.json")
    #-----
    Q_num = int(cldx[1])   # for removing the true symbol
    Q = list(questions.keys())
    Q_show = Q[Q_num]
    Q_select = questions[Q_show]
    for ans in Q_select :
            if ans.find("✅") != -1 :
                ind = Q_select.index(ans)
                break
    Q_select[ind] = Q_select[ind].replace("✅" , "")
    ans1 , ans2 , ans3 , ans4 = Q_select
    #------
    TNQ = len(questions)
    if int(cldx[1]) == TNQ - 1 :
        try :
            obj = Jread(f"exam answer/{examtype}.json")
            whatans = obj[str(CHI)][cldx[1]]
            if whatans == "1" :
                ans1 = ans1 + "✅"
            elif whatans == "2" :
                ans2 = ans2 + "✅"
            elif whatans == "3" :
                ans3 = ans3 + "✅"
            elif whatans == "4" :
                ans4 = ans4 + "✅"
            #----
            keyb = ink([
            [
                inb(ans1 , f"{cldx[1]}_1")   # fixing callback
            ],
            [
                inb(ans2 , f"{cldx[1]}_2")   # fixing callback
            ],                      
            [
                inb(ans3 , f"{cldx[1]}_3")   # fixing callback
            ],
            [
                inb(ans4 , f"{cldx[1]}_4")   # fixing callback
            ],
            [
                inb("<<<" , f"previous_{Q_num - 1}"),   
            ],
            [
                inb("confirm" , "confirm")
            ]
        ])
            client.edit_message_text(CHI , MID , Q_show , reply_markup=keyb)
        except :
            keyb = ink([
            [
                inb(ans1 , f"{cldx[1]}_1")   # fixing callback
            ],
            [
                inb(ans2 , f"{cldx[1]}_2")   # fixing callback
            ],                      
            [
                inb(ans3 , f"{cldx[1]}_3")   # fixing callback
            ],
            [
                inb(ans4 , f"{cldx[1]}_4")   # fixing callback
            ],
            [
                inb("<<<" , f"previous_{Q_num - 1}"),   
            ],
            [
                inb("confirm" , "confirm")
            ]
        ])
            client.edit_message_text(CHI , MID , Q_show , reply_markup=keyb)
    elif int(cldx[1]) == 0 :
        try :
            obj = Jread(f"exam answer/{examtype}.json")
            whatans = obj[str(CHI)][cldx[1]]
            if whatans == "1" :
                ans1 = ans1 + "✅"
            elif whatans == "2" :
                ans2 = ans2 + "✅"
            elif whatans == "3" :
                ans3 = ans3 + "✅"
            elif whatans == "4" :
                ans4 = ans4 + "✅"
            #----
            keyb = ink([
            [
                inb(ans1 , f"{cldx[1]}_1")   # fixing callback
            ],
            [
                inb(ans2 , f"{cldx[1]}_2")   # fixing callback
            ],                      
            [
                inb(ans3 , f"{cldx[1]}_3")   # fixing callback
            ],
            [
                inb(ans4 , f"{cldx[1]}_4")   # fixing callback
            ],
            [
                inb(">>>" , f"next_{Q_num + 1}")   
            ]
        ])
            client.edit_message_text(CHI , MID , Q_show , reply_markup=keyb)
        except :
            keyb = ink([
            [
                inb(ans1 , f"{cldx[1]}_1")   # fixing callback
            ],
            [
                inb(ans2 , f"{cldx[1]}_2")   # fixing callback
            ],                      
            [
                inb(ans3 , f"{cldx[1]}_3")   # fixing callback
            ],
            [
                inb(ans4 , f"{cldx[1]}_4")   # fixing callback
            ],
            [
                inb(">>>" , f"next_{Q_num + 1}")   
            ]
        ])
            client.edit_message_text(CHI , MID , Q_show , reply_markup=keyb)
    else :
        try :
            obj = Jread(f"exam answer/{examtype}.json")
            whatans = obj[str(CHI)][cldx[1]]
            if whatans == "1" :
                ans1 = ans1 + "✅"
            elif whatans == "2" :
                ans2 = ans2 + "✅"
            elif whatans == "3" :
                ans3 = ans3 + "✅"
            elif whatans == "4" :
                ans4 = ans4 + "✅"
            #----
            keyb = ink([
            [
                inb(ans1 , f"{cldx[1]}_1")   # fixing callback
            ],
            [
                inb(ans2 , f"{cldx[1]}_2")   # fixing callback
            ],                      
            [
                inb(ans3 , f"{cldx[1]}_3")   # fixing callback
            ],
            [
                inb(ans4 , f"{cldx[1]}_4")   # fixing callback
            ],
            [
                inb("<<<" , f"previous_{Q_num - 1}"),
                inb(">>>" , f"next_{Q_num + 1}") 
            ]
        ])
            client.edit_message_text(CHI , MID , Q_show , reply_markup=keyb)
        except :
            keyb = ink([
            [
                inb(ans1 , f"{cldx[1]}_1")   # fixing callback
            ],
            [
                inb(ans2 , f"{cldx[1]}_2")   # fixing callback
            ],                      
            [
                inb(ans3 , f"{cldx[1]}_3")   # fixing callback
            ],
            [
                inb(ans4 , f"{cldx[1]}_4")   # fixing callback
            ],
            [
                inb("<<<" , f"previous_{Q_num - 1}"),
                inb(">>>" , f"next_{Q_num + 1}") 
            ]
        ])
            client.edit_message_text(CHI , MID , Q_show , reply_markup=keyb)
    raise stop
@Client.on_callback_query(callType("confirm"))
def con(client , query) :
    cli  = query.id
    cld  = query.data
    CHI  = str(query.message.chat.id)
    MID  = query.message.id
    cldx = cld.split("_")
    #------
    key = ink([
        [
            inb("yes" , "yesno_y"),
            inb("no" , "yesno_n")
        ]
    ])
    client.edit_message_text(CHI,MID,"آیا میخواهید آزمون به پایان برسد؟",reply_markup=key)
    raise stop
@Client.on_callback_query(callType("yesno"))
def yesno(client , query) :
    cli  = query.id
    cld  = query.data
    CHI  = str(query.message.chat.id)
    MID  = query.message.id
    cldx = cld.split("_")
    #----
    if cldx[1] == "y" :
        examtype  = Jread(f"exam controls/Tarexam.json")
        examtype  = examtype[0]
        examans   = Jread(f"exam answer/{examtype}.json")
        examsheet = Jread(f"exam sheets/{examtype}.json")
        examperson = examans[str(CHI)]
        #--- score controlers 
        TA = 0
        FA = 0
        NA = 0
        #------- check for true answers
        for q , a in examperson.items():
            A = list(examsheet.values())
            #---
            chk = A[int(q)]   # choose question from examsheet
            for chk1 in chk :
                if "✅" in chk1 :
                    ind = chk.index(chk1)
                    break
            if a != None :
                if str(ind + 1) == a :
                    TA = TA + 1
                else :
                    FA = FA + 1
            else :
                NA = NA + 1
        #---- calculating
        posscore = 1*TA
        negscore = -0.3*FA
        NA    = len(examsheet) - TA - FA
        total    = posscore+negscore
        #----- database 
        res = Jread(f"exam results/res.json")
        try :   # when its defined
            ex = res[examtype] 
            ex[CHI] = [total , TA , FA , NA]
            Jwrite("exam results/res.json" , res)
        except :
            print("exec")
            res[examtype] = {
                CHI : [total , TA , FA , NA],
            }
            Jwrite("exam results/res.json" , res)
        #-----
        resText  = f"🔹{examtype}\n\n✅True : {TA}\n❌False : {FA}\n❗️NO answer : {NA}\n-----\nscore : {total}"
        client.edit_message_text(CHI,MID,resText)
    else :
        cli  = query.id
        cld  = query.data
        CHI  = query.message.chat.id
        MID  = query.message.id
        cldx = cld.split("_")
        #------
        examtype  = Jread("exam controls/Tarexam.json")
        examtype  = examtype[0]
        questions = Jread(f"exam sheets/{examtype}.json")
        lq = len(questions)
        #-----
        Q_num = lq - 1   # for removing the true symbol
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
        obj = Jread(f"exam answer/{examtype}.json")  #add what user choose as true answer
        whatans = obj[str(CHI)][str(Q_num)]
        if whatans == "1" :
            ans1 = ans1 + "✅"
        elif whatans == "2" :
            ans2 = ans2 + "✅"
        elif whatans == "3" :
            ans3 = ans3 + "✅"
        elif whatans == "4" :
            ans3 = ans3 + "✅"
        #----
        keyb = ink([
        [
            inb(ans1 , f"{Q_num}_1")   # fixing callback
        ],
        [
            inb(ans2 , f"{Q_num}_2")   # fixing callback
        ],                      
        [
            inb(ans3 , f"{Q_num}_3")   # fixing callback
        ],
        [
            inb(ans4 , f"{Q_num}_4")   # fixing callback
        ],
        [
            inb("<<<" , f"previous_{Q_num - 1}"),   
        ],
        [
            inb("confirm" , "confirm")
        ]
    ])
        client.edit_message_text(CHI , MID , Q_show , reply_markup=keyb)
    raise stop
@Client.on_callback_query()
def ans(client , query) :
    cli  = query.id
    cld  = query.data
    CHI  = str(query.message.chat.id)
    MID  = query.message.id
    cldx = cld.split("_")
    key = query.message.reply_markup.inline_keyboard
    #------
    examtime = Jread("exam controls/Time&exam.json")
    ftime    = examtime[1]
    #----
    tizone   = Tzone.timezone("Asia/Tehran")
    currtime = dt.datetime.now(tizone)
    currtime = currtime.strftime("%H:%M")
    #----
    if currtime <= ftime :
        try :
            tarexam = Jread("exam controls/Tarexam.json")
            tarexam = tarexam[0]
            obj = Jread(f"exam answer/{tarexam}.json")
            x = obj[CHI]
            x[cldx[0]] = cldx[1]
            Jwrite(f"exam answer/{tarexam}.json",obj)
        except :
            tarexam = Jread("exam controls/Tarexam.json")
            tarexam = tarexam[0]
            obj = Jread(f"exam answer/{tarexam}.json")
            print(obj)
            obj[CHI] = {
                cldx[0] : cldx[1]
            }
            Jwrite(f"exam answer/{tarexam}.json",obj)
        #---delete previous symbol   #editing with for else loop (replacing elements in object)
        for button in key :
            keyText = button[0].text
            ind = key.index(button)
            if "✅" in keyText :
                button[0].text = keyText.replace("✅" , "")
                if int(cldx[1]) - 1 == ind :
                    print("true connection")
                    print(ind)
                    #----
                    tarexam = Jread("exam controls/Tarexam.json")
                    tarexam = tarexam[0]
                    obj = Jread(f"exam answer/{tarexam}.json")
                    x = obj[CHI]
                    x[cldx[0]] = None
                    Jwrite(f"exam answer/{tarexam}.json",obj)
                    #----
                    client.edit_message_reply_markup(CHI,MID,reply_markup=ink(key))
                    break
        else :
            #---add new symbol
            keyText     = key[int(cldx[1]) - 1][0].text
            key[int(cldx[1]) - 1][0].text = keyText + "✅"
            key = ink(key)
            client.edit_message_reply_markup(CHI,MID,reply_markup=key)
    else :
        client.answer_callback_query(cli,"زمان آزمون به پایان رسیده",show_alert=True)