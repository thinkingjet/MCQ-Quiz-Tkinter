"""
# GITHUB LINK: https://github.com/GauravRocketBooster/MCQ-Quiz-Tkinter
# THIS QUIZ REQUIRES AN INTERNET CONNECTION WITHOUT RESTRITIONS TO MAKE THE GET REQUESTS TO IMAGE URLs. 
# IT NEEDS the external libraries requests, io, and pillow. In some extreme cases, bs4 might be required too.
# To download the libraries do pip3 install *library_name* in your command line.
# The rest of the libraries are built in.
"""


# Importing Everything From the Tkinter Library.
from tkinter import *
from tkinter import messagebox as messagebox

# Importing the JSON Library, to be used for reading the values in the JSON file,
# the one that contains all the questions.
import json

# Importing the requests library, so I don't have to download images, and can directly 
# get them from the intenet. Then I can put them in master1 and the different frames. 
import requests

# Importing the Public Image Ltd image library to modify the images into readable format for Python and Tkinter.
from PIL import Image, ImageTk

# Getting the BytesIO module from the io library, to process the bytes of the image into an actual image
# to make it readable for Tkinter and Python. 
from io import BytesIO

# Importing the OS library, that can help with changing the directory to the one that contains 
# the JSON file. We can do this by typing os.chdir("*DIRECTORY NAME HERE*") 
# Also using error handling here, as in case the user runs the file via terminal,
# Or is already in the directory, the program doesn't just crash, but prints a small
# error message to the console.
import os
try:
    os.chdir("School_Work/Gui_Stuff/MCQ_Quiz")
except:
    print("Couldn't change Directories.")

# Creating a TK object and calling it master1, the master1 details_frame will be used to ask the person's details,
# and other frames will be used to ask the questions, show options, etc.
master1 = Tk()
details_frame = Frame(master1)
details_frame.grid()


# A placeholder variable, which will be used later in order to check weather
# master1 is destroyed or not, which will further be used to decide weather to 
# create questions_frame or not, which is another Tk() object, which will be used for showing the questions.
exited = False

# This function will be the command for the DONE button in master1.
# This function does a couple of things. Firstly, it checks if there is anything in the 2
# text fields, and if there is, it checks to see weather the nameTextField is a string,
# and also checks weather the ageTextField is an int
# If the above criteria doesn't match, it shows an error, depending on the condition not met.
# Then it does a whole bunch of error handling, basically affecting the gameplay such that the user can only play the game once.
# If the user tries to play it twice, no matter whatever way the try putting their name in, it won't work. Due to using the 
# .lower() command. But if all the above does match, then
# it goes on to save the two text fields into two different variables called name and age. 
# It also saves them into the details.txt text file which is used to check if the user has played
# before, by doing if *uname* in details.txt. 
# It also makes them global, to access outside the function. Then, it makes the question_number
# placeholder global as well, and sets it to 1. Then it destroys the master1 object, and starts
# the questions_frame object, letting the user access the mcq quiz. 
def to_destroy():
    global name,age
    try:
        name = str(nameTextField.get())
        age = int(ageTextField.get())
        try:
            if age == 15:
                details_read = open("details.txt", "r")
                to_read = details_read.read()
                
                if name.lower() not in to_read.lower():
                    pass
                elif len(name) < 1:
                    messagebox.showerror(title="No name Error", message="You don't even have a name, how dumb can someone be!?")
                    master1.mainloop()
                else:
                    messagebox.showerror(title="Already Played Error", message="You can only play once, go away!!!")
                    master1.mainloop()
                global exited
                exited = True
            if age != 15:
                messagebox.showerror(title="Age Error", message="You are not 15, BYE Kid. ")
                master1.mainloop()
        except:
            pass

    except:
        messagebox.showerror(title="NAN Error", message="Age is not a Number, are you even human?")
        master1.mainloop()


# Created the get_image function that takes in three parameters, the image url, the row and the column to place the image at. Example url=https://wikipedia.org/computer.png,r=3,c=4.
# It makes a GET request to the url using the requests library, to grab it. Then it converts it into an image using the BytesIO module. 
# After taking that info, it gets the image and converts it into python readable formant using the PIL library's ImageTk module.
# TODO: Remove this l8r. I finally got it to work inside a function, after spending 4 hours figuring out stuff, lets gooooo. 

def get_image(url="http://www.iconhot.com/icon/png/bunch-cool-bluish-icons/128/info-user.png",r=1,c=0, frame=details_frame,height=128,width=128,lbl=False):
    if lbl == True:
        global title
        title = Label(frame, text="Gaurav's Astronomy QUIZ", 
        width=50, bg="green",fg="white", font=("ariel", 20, "bold")).grid(row=0,column=0) 
    global response
    response = requests.get(f"{url}")
    global img
    im = Image.open(BytesIO(response.content))
    im = im.resize((width,height),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(im)
    # print(img.height(),img.width())
    global img_label
    img_label = Label(frame,image=img)
    img_label.grid(row=r,column=c)

# Calling the function get_image() with a link to a user info photo, to add the user photo to master1.
get_image("http://www.iconhot.com/icon/png/bunch-cool-bluish-icons/128/info-user.png",r=3,c=3)

# Making the quit function, which destroys master1, and doesn't let questions_frame start. This will
# be the command for the Quit button.
def quit():
    global question_number
    question_number = 0
    global exited
    exited = False
    master1.destroy()


# This creates the GUI elements known as Labels.
# Master incdicates the window to put the Labels in.
# Creates three Labels, instruct, nameLabel and ageLabel.
instruct = Label(details_frame,text="Enter Your Details Below", bg="green",fg="white")
nameLabel = Label(details_frame,text="Name:", bg="yellow",fg="black")
ageLabel = Label(details_frame, text="Age:", bg="yellow",fg="black")

# Making the Two Age and name Text Fields.
nameTextField = Entry(details_frame)
ageTextField = Entry(details_frame)

# Making the DONE Button and the QUIT Button
# command is the function to call when a button is pressed 
submit_button = Button(details_frame,text="DONE", command= lambda: [to_destroy(), exit()], height=4,width=14,bg="cyan",fg="black")
quit_button = Button(details_frame,text="QUIT", command=quit, height=3,width=5,bg="cyan",fg="black")

# Adding the widgets to the window using the .grid funtion, which
# Places and grids the widgets at positions where we want them to be. 
instruct.grid(row=0,column=1)
nameLabel.grid(row=1,column=0, padx=20, pady=20)
nameTextField.grid(row=1,column=1)
ageLabel.grid(row=2,column=0)
ageTextField.grid(row=2,column=1)
submit_button.grid(row=3,column=1, padx=20, pady=20)
quit_button.grid(row=1,column=3, padx=20, pady=20)


"""
_____                ____
I        I\   I     I     \ 
I____    I \  I     I     |
I        I  \ I     I     |    OF DETAILS_FRAME
I____    I   \I     I____/
"""


# Opening the JSON file that Contains the Questions, Answers, and Options.
file = json.load(open("questions.json"))

# Converting the questions, options and answers to a list format. 
questions = (file["questions"])
options = (file["options"])
answers = (file["answers"])

# placeholders, which get updated with the answers.
answers_correct = 0
answers_wrong = 0
wrong_answers = []

# List containing all the image links.
image_links = ["http://cdn.britannica.com/93/95393-050-5329EE11/planets-distance-order-Sun.jpg", 
"http://st.depositphotos.com/1007989/5151/i/600/depositphotos_51518159-stock-photo-boy-using-telescope.jpg",
"http://static.bhphotovideo.com/explora/sites/default/files/ts-space-sun-and-solar-viewing-facts-versus-fiction.jpg",
"http://starwalk.space/gallery/images/february-2020-three-planets-in-morning-sky/1024x576",
"http://c.tadst.com/gfx/600x337/march-equinox-dark.png",
"http://i.ytimg.com/vi/7E7zoFBwLU0/maxresdefault.jpg",
"http://media.gettyimages.com/photos/low-angle-view-of-sunrays-in-the-dark-picture-id660555985",
"http://cdn.mos.cms.futurecdn.net/LNAm66BstSr7n6HsLPN7Bk.jpg",
"http://media3.s-nbcnews.com/j/newscms/2018_45/2633521/181105-light-year-al-1550_70610a0a9146b249400f56ef30ec57d7.fit-2000w.jpg",
"http://c.tadst.com/gfx/600x337/waxing-crescent-moon.jpg"]


# ALL the variable declarations
question_variable = StringVar()
question_number = 0
q0_var = IntVar()
q1_var = IntVar()
q2_var = IntVar()
q3_var = IntVar()
q4_var = IntVar()
q5_var = IntVar()
q6_var = IntVar()
q7_var = IntVar()
q8_var = IntVar()
q9_var = IntVar()
answer_variables = [q0_var,q1_var,q2_var,q3_var,q4_var,q5_var,q6_var,q7_var,q8_var,q9_var]
option1 = StringVar()
option2 = StringVar()
option3 = StringVar()
option4 = StringVar()
option_variables = [option1,option2,option3,option4]

# Checks that all the error handling and checks Are done, if they are, it then starts the questions_frame Frame object. 
# Runs the questions_frame Frame() object, meaning that it runs after details_frame() is destroyed. 
# I.e. the user pressed DONE, adds and grids a start button which starts the quiz.
def exit():
    if exited == True:
        details_frame.destroy()
        global questions_frame
        questions_frame = Frame(master1)
        questions_frame.grid()
        l1 = Label(questions_frame,text="  ")
        l2 = Label(questions_frame,text="  ")
        l3 = Label(questions_frame,text="  ")
        l4 = Label(questions_frame,text="  ")
        
        l1.grid(row=1,columnspan=3)
        l2.grid(row=2, column=0)

        global start_question_frame
        start_question_frame = Button(questions_frame,text="START", height=10,width=10,bg='cyan',fg='red', command =lambda: question())
        # master1.geometry('600x1000')
        start_question_frame.grid(row=2,column=1)

        l3.grid(row=2,column=2)
        l4.grid(row=3,columnspan=3)

submit_clicked = False

# Next question button which displays a next button and the user can go to the next question using it. Also displays the submit button.
def next():
    global question_number,vr,answer_variables,image_links,ques_label,question_variable,option1,option2,option3,option4,answers_correct,submit_quiz,option_variables
    ms = questions_frame

    def submit():
        global answers_correct,answer_variables,answers_wrong,wrong_answers, submit_clicked, answer_variables,submit_quiz
        placeholder = 0
        submit_clicked = True
        for variable in answer_variables:
            if int(variable.get()) == answers[placeholder]:
                answers_correct += 1
            else:
                answers_wrong += 1
                if placeholder not in wrong_answers:
                    wrong_answers.append(f"Question {placeholder+1}")
            placeholder += 1

        finished_quiz = messagebox.showinfo(title="Well Done", message=f"Hello {age} year old {name.capitalize()}, You got {str(answers_correct)} right answers and {str(answers_wrong)} wrong answers.\n\n Wrong Answers: {str(wrong_answers)}\n\nYou can now go through your answers. When you are done, click QUIT.")
        print("Wrong Answers: "+str(wrong_answers))
        print(f"You got {answers_wrong} answers wrong")
        print(f"You got {answers_correct} answers correct")
        with open("details.txt","a") as file:
            file.write(f"Name: {name.capitalize()}\nAge: {age}\nScore: {answers_correct}\n-------------------------------------------------------------\n")
        submit_quiz.destroy()
            
    try:
            
        if submit_clicked == False:
            if question_number > 8:
                submit_quiz = Button(questions_frame, text="Submit Quiz", command=submit, bg="red",height=5,width=8)
                submit_quiz.grid(row=14, column=8)

        question_number += 1
        qno = question_number
        vr = answer_variables[qno]
        get_image(image_links[qno],frame=questions_frame, height=280,width=800,lbl=True)
        quit_button = Button(questions_frame, text="QUIT", height= 4,width=4,command=quit).grid(row=0,column=10)
        option1.set(options[qno][0])
        option2.set(options[qno][1])
        option3.set(options[qno][2])
        option4.set(options[qno][3])

        question_variable.set(questions[qno])
        ques_label = Label(ms, textvariable=question_variable,bg="orange")
        back_button = Button(ms, text="BACK", height=4,width=7, bg="yellow", command = back).grid(row=14,column=0)
        next_button = Button(ms, text="NEXT", height=4,width=7, bg="yellow", command = next).grid(row=14, column=7)
        global rb1,rb2,rb3,rb4
        rb1 = Radiobutton(ms,textvariable=option1,value =1,font=("arial", 14), variable=vr,bg="#ffcccb").grid(row=10,column=0)
        rb2 = Radiobutton(ms,textvariable=option2, value =2,font=("arial", 14), variable=vr,bg="lime").grid(row=11,column=0)
        rb3 = Radiobutton(ms,textvariable=option3, value =3,font=("arial", 14), variable=vr,bg="yellow").grid(row=12,column=0)
        rb4 = Radiobutton(ms,textvariable=option4, value =4,font=("arial", 14), variable=vr,bg="cyan").grid(row=13,column=0)

        ques_label.configure(font="Arial 17 underline")
        ques_label.grid(row=9,column=0)
        if submit_clicked == True:
            if int(answers[qno]) == 1:
                       get_image(url="http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Green_tick.svg/1200px-Green_tick.svg.png",frame=questions_frame,r=10,c=1,height=20,width=30)
            if int(answers[qno]) == 2:
                       get_image(url="http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Green_tick.svg/1200px-Green_tick.svg.png",frame=questions_frame,r=11,c=1,height=20,width=30)
            if int(answers[qno]) == 3:
                       get_image(url="http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Green_tick.svg/1200px-Green_tick.svg.png",frame=questions_frame,r=12,c=1,height=20,width=30)
            if int(answers[qno]) == 4:
                       get_image(url="http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Green_tick.svg/1200px-Green_tick.svg.png",frame=questions_frame,r=13,c=1,height=20,width=30)
    except:
        if submit_clicked == True:
            messagebox.showerror(title="Index Out Of Range", message="You can't go beyond Question 10.")
            question_number -= 1
# Back question function which displays a back question button and the user can go to the previous question using it. 
def back():
    global question_number,vr,answer_variables,image_links,ques_label,question_variable,option1,option2,option3,option4,answers_correct
    if exited == True:
        ms = questions_frame

        question_number -= 1
        qno = question_number
        vr = answer_variables[qno]
        get_image(image_links[qno],frame=questions_frame, height=280,width=800,lbl=True)
        quit_button = Button(questions_frame, text="QUIT", height= 4,width=4,command=quit).grid(row=0,column=10)
        option1.set(options[qno][0])
        option2.set(options[qno][1])
        option3.set(options[qno][2])
        option4.set(options[qno][3])

        question_variable.set(questions[qno])
        ques_label = Label(ms, textvariable=question_variable,bg="orange")
        
        global rb1,rb2,rb3,rb4
        rb1 = Radiobutton(ms,textvariable=option1, value =1,font=("arial", 14), variable=vr,bg="#ffcccb").grid(row=10,column=0)
        rb2 = Radiobutton(ms,textvariable=option2, value =2,font=("arial", 14), variable=vr,bg="lime").grid(row=11,column=0)
        rb3 = Radiobutton(ms,textvariable=option3, value =3,font=("arial", 14), variable=vr,bg="yellow").grid(row=12,column=0)
        rb4 = Radiobutton(ms,textvariable=option4, value =4,font=("arial", 14), variable=vr,bg="cyan").grid(row=13,column=0)

        ques_label.configure(font="Arial 17 underline")
        ques_label.grid(row=9,column=0)
        if submit_clicked == True:
            if int(answers[qno]) == 1:
                       get_image(url="http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Green_tick.svg/1200px-Green_tick.svg.png",frame=questions_frame,r=10,c=1,height=20,width=30)
            if int(answers[qno]) == 2:
                       get_image(url="http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Green_tick.svg/1200px-Green_tick.svg.png",frame=questions_frame,r=11,c=1,height=20,width=30)
            if int(answers[qno]) == 3:
                       get_image(url="http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Green_tick.svg/1200px-Green_tick.svg.png",frame=questions_frame,r=12,c=1,height=20,width=30)
            if int(answers[qno]) == 4:
                       get_image(url="http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Green_tick.svg/1200px-Green_tick.svg.png",frame=questions_frame,r=13,c=1,height=20,width=30)

# The question function which displays the first question, and destroys the start button.
def question():
    if exited == True:
        ms=questions_frame
        global question_number,vr,answer_variables,image_links,ques_label,question_variable,option1,option2,option3,option4,submit_clicked
        qno = question_number
        vr = answer_variables[qno]
        start_question_frame.destroy()
        get_image(image_links[qno],frame=questions_frame, height=280,width=800,lbl=True)
        quit_button = Button(questions_frame, text="QUIT", height= 4,width=4,command=quit).grid(row=0,column=10)
        option1.set(options[qno][0])
        option2.set(options[qno][1])
        option3.set(options[qno][2])
        option4.set(options[qno][3])
        options_list = [option1,option2,option3,option4]       

        question_variable.set(questions[qno])
        ques_label = Label(ms, textvariable=question_variable,bg="orange")
        
        next_button = Button(ms, text="NEXT", height=4,width=7, bg="yellow", command = next).grid(row=14, column=7)
        global rb1,rb2,rb3,rb4
        rb1 = Radiobutton(ms,textvariable=option1, value =1,font=("arial", 14), variable=vr,bg="#ffcccb").grid(row=10,column=0)
        rb2 = Radiobutton(ms,textvariable=option2, value =2,font=("arial", 14), variable=vr,bg="lime").grid(row=11,column=0)
        rb3 = Radiobutton(ms,textvariable=option3, value =3,font=("arial", 14), variable=vr,bg="yellow").grid(row=12,column=0)
        rb4 = Radiobutton(ms,textvariable=option4, value =4,font=("arial", 14), variable=vr,bg="cyan").grid(row=13,column=0)

        ques_label.configure(font="Arial 17 underline")
        ques_label.grid(row=9,column=0)
        
# Makes the back button.
if exited == True:
    back_button = Button(questions_frame,text="BACK",command=back,height=5,width=5).grid(row=10,column=5)

# Runs the mainloop for the input fields, in which the user is asked various questions about
# themselves, and they have to answer them.
master1.mainloop()


"""
_____                ____
I        I\   I     I     \ 
I____    I \  I     I     |
I        I  \ I     I     |    OF MCQ QUIZ BY GAURAVJEET SINGH
I____    I   \I     I____/     
"""

