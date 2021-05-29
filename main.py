from tkinter import *
from tkinter import filedialog as fd
import PyPDF2
from gtts import gTTS
import threading
import pyttsx3

win = Tk()
win.geometry("1920x1080+0+0")
win.title("AudioBooks - (Maker and Reader)")
win.iconbitmap("icon.ico")
########################global variables and funtions##############################
file_path,stat = StringVar(), StringVar()
file_path.set("")
stat.set("Everything Looks Fine...")
obj=str()

def init_loud():
    global loud
    loud = pyttsx3.init()

threading.Thread(target = init_loud).start()

def file_upload():
    global file_path, stat
    path = fd.askopenfilename()
    path=path.replace("/", "\\")
    file_path.set(str(path))
    stat.set("The Path is Set.")

def extract_():
    global obj, file_path
    
    file = open(str(file_path.get()), "rb")

    pdfread = PyPDF2.PdfFileReader(file) #creating pdf reader
    obj = pdfread.getPage(0)#a page object
    stat.set("the file extracted Successfully")

def speak_data():
    global win, loud, obj, stat

    extract_()
    text = Text(win,
                font = ("bahnschrift semibold", 13),
                bg = "#ffffff",
                fg = "#5dbcd2",
                width = 70,
                height = 25)
    text.insert(INSERT, obj.extractText())
    text.pack()
    text.place(x=800, y=200)
    
    loud.say(obj.extractText())
    loud.runAndWait()

def save_audio():
    global ent_name, obj

    extract_()
    
    _name = str(ent_name.get())
    if _name=="":
        stat.set("No File Name was Given to Save.")
    else:
        if _name.split(".")[-1]=="mp3":
            pass
        else:
            _name = "{0}.mp3".format(_name)

        file = gTTS(text = str(obj.extractText()), lang = "en")
        stat.set("Saving File is in Process...Please Wait")
        file.save(str(_name))
        stat.set("the {0} File was Saved Successfully.".format(_name))
    
###################################################################################

back_drop = PhotoImage(file = "back.png")
back = Label(win, image = back_drop)
back.pack()
back.place(x=0,y=0)

upload_but = Button(
    win,
    text = "Upload File",
    font = ("bahnschrift semibold", 13),
    bg = "#5dbcd2",
    fg = "#ffffff",
    command = file_upload)
upload_but.pack()
upload_but.place(x=300, y=230)

ent_path = Entry(
    win,
    textvariable = file_path,
    font = ("bahnschrift semibold", 15),
    width=40,
    fg="#01c6fb"
    )
ent_path.pack()
ent_path.place(x=270, y=310)

listen_but = Button(
    win,
    text = "Listen Audio File",
    font = ("bahnschrift semibold", 15),
    bg = "#5dbcd2",
    fg = "#ffffff",
    command = lambda: threading.Thread(target = speak_data).start())
listen_but.pack()
listen_but.place(x=270, y=380)

ent_name = Entry(
    win,
    font = ("bahnschrift semibold", 15),
    width=30,
    fg="#01c6fb"
    )
ent_name.pack()
ent_name.place(x=375, y=550)

save_but = Button(
    win,
    text = "Convert Into AudioBook",
    font = ("bahnschrift semibold", 15),
    bg = "#5dbcd2",
    fg = "#ffffff",
    command = lambda: threading.Thread(target = save_audio).start())
save_but.pack()
save_but.place(x=270, y=600)

exit_but = Button(
    win,
    text = "EXIT",
    font = ("bahnschrift semibold", 15),
    bg = "red",
    fg = "#ffffff",
    command = lambda: win.destroy())
exit_but.pack()
exit_but.place(x=50, y=730)

stats = Entry(
    win,
    textvariable = stat,
    font = ("bahnschrift semibold", 15),
    width=50,
    fg="#ff0000"
    )
stats.pack()
stats.place(x=150, y=732)

win.mainloop()
