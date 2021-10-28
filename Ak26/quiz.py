from io import BytesIO
import requests as r

# import required classes from tkinter
from tkinter import IntVar,Button, Label, Radiobutton, Tk, Entry
from PIL import Image, ImageTk
# and import messagebox as mb from tkinter
from tkinter import messagebox as mb

#import json to use json file for data
import json


class Quiz:

    def __init__(self):
        self.name_label=self.add_label("Name",50,50)
        self.age_label=self.add_label("Age",50,100)
        self.name = self.add_textbox(100,50,placeholder='name')
        self.age = self.add_textbox(100,100,placeholder='age')
        self.buttons(place_next=False)
        self.entr = self.entry_button()


    def add_label(self, display_text,x,y):
        label= Label(gui, text=display_text, width=20,
        font=( 'ariel' ,12, 'bold' ), anchor= 'w' )
        label.place(x=x,y=y)
        return label


    def start(self):
        self.name.destroy()
        self.age.destroy()
        self.name_label.destroy()
        self.age_label.destroy()
        self.entr.destroy()
        self.q_no=0
        self.img = None
        self.display_image()
        self.display_title()
        self.display_question()
        self.back_button()
        self.opt_selected=IntVar()
        self.opts=self.radio_buttons()
        self.display_options()
        self.next,self.quit = self.buttons()
        self.data_size=len(question)
        self.correct=0


    def show_msg(self,msg):
        mb.showinfo(msg)

    def display_result(self):
        
        wrong_count = self.data_size - self.correct
        sum = 0
        for value in result_ans.values():
            sum+=value
        wrong_count = self.data_size-sum
        correct = f"Correct: {sum}"
        wrong = f"Wrong: {wrong_count}"
        
        score = int(sum / self.data_size * 100)
        result = f"Score: {score}%"
        
        mb.showinfo("Result", f"{result}\n{sum}\n{wrong}")

    def check_ans(self, q_no):
        user_choice[q_no] = self.opt_selected.get()
        if self.opt_selected.get() == answer[q_no]:
            return True

    def next_btn(self):

        if self.q_no == len(question)-2:
            self.next['text']='Submit'
        
        if self.check_ans(self.q_no):
            self.correct += 1
            result_ans[self.q_no]=1
        else:
            result_ans[self.q_no]=0
        self.q_no += 1
        if self.q_no==self.data_size:
            self.display_result()
            gui.destroy()
        else:
            self.display_question()
            self.display_image()
            self.display_options()


    def add_textbox(self,x,y,placeholder="text"):
        textbox = Entry(text=placeholder)
        textbox.place(x=x,y=y)
        return textbox


    def buttons(self,place_next=True):
        next_button = None
        if place_next:
            next_button = Button(gui, text='Next',command=self.next_btn,
            width=10,bg="blue",fg="white",font=("ariel",16,"bold"))

            next_button.place(x=350,y=580)
        

        quit_button = Button(gui, text="Quit", command=gui.destroy,
        width=5,bg="black", fg="white",font=("ariel",16," bold"))

        quit_button.place(x=700,y=50)
        return next_button, quit_button

    def back_button(self):
        back_btn = Button(gui, text='Back',command=self.go_back,
            width=10,bg="blue",fg="white",font=("ariel",16,"bold"))
        back_btn.place(x=150,y=580)

    def go_back(self):
        if self.q_no==0:
            return
        self.q_no-=1
        self.display_question()
        self.display_image()
        self.display_options()


    def entry_button(self):
        entry_button = Button(gui, text="Entry",command=self.evaluate,
            width=10,bg="blue",fg="white",font=("ariel",16,"bold"))
        entry_button.place(x=200,y=200)
        return entry_button

    def evaluate(self):
        n= self.name.get()
        a= self.age.get()
        try:
            a= int(a)
        except ValueError:
            self.show_msg('input age is not a number')
            gui.destroy()
            return
        if n.strip() == '':
            self.show_msg('please enter valid name')
        if a<13 or a>100:
            self.show_msg('your age is not suitable for this quiz')
            gui.destroy()
        else:
            self.start()


    def display_options(self):
        val=0
        

        self.opt_selected.set(0)
        for option in options[self.q_no]:
            self.opts[val]['text']=option
            val+=1
        for count in range(1,5):
            if user_choice[self.q_no] == count:
                self.opt_selected.set(count)



    def display_question(self):
        
        q_no = Label(gui, text=question[self.q_no], width=100,
        font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
        
        q_no.place(x=70, y=100)

    def display_image(self):
        url = imgs[self.q_no]

        u = r.get(url)
        raw_data = u._content
        u.close()

        im = Image.open(BytesIO(raw_data))
        size = (200,200)
        im = im.resize(size)
        image = ImageTk.PhotoImage(im)
        self.img = image
        img = Label(image=image,height=200,width=200)
        img.place(x=100,y=150)


    def display_title(self):
        
        # The title to be shown
        title = Label(gui, text="Photosensitive QUIZ",
        width=50, bg="green",fg="white", font=("ariel", 20, "bold"))
        
        # place of the title
        title.place(x=0, y=2)


    def radio_buttons(self):
        
        q_list = []
        
        # position of the first option
        y_pos = 350
        
        # adding the options to the list
        while len(q_list) < 4:
            radio_btn = Radiobutton(gui,text=" ",variable=self.opt_selected,
            value = len(q_list)+1,font = ("ariel",14))
            
            # adding the button to the list
            q_list.append(radio_btn)
            
            # placing the button
            radio_btn.place(x = 100, y = y_pos)
            
            # incrementing the y-axis position by 40
            y_pos += 40
        
        # return the radio buttons
        return q_list

gui = Tk()

gui.geometry("800x700")

gui.title("PhotoEvaluate Quiz")

# get the data from the json file
with open('questions.json') as f:
    data = json.load(f)

# set the question, options,imgs links and answer
question = (data['question'])
options = (data['options'])
answer = (data[ 'answer'])
imgs = (data['imgs'])
result_ans={}
user_choice = {item:0 for item in range(len(question))}

quiz = Quiz()

gui.mainloop()

