from Tkinter import *
from random import randint, choice
import tkMessageBox
import tkFont
import ttk

class thoughtgenerator(object):
      
    def __init__(self, title, *args):
        self.title = (title,)       
        if args:  #when an instance passes coordenades as an argument they are used to create the oval(because it comes from a saved file)
            (coordenades,) = args
            self.oval_RT = float(coordenades[0])
            self.oval_TT = float(coordenades[1])
            self.oval_LT = float(coordenades[2])
            self.oval_BT = float(coordenades[3])
            self.coordenades_transcript = coordenades[0]+","+coordenades[1]+","+coordenades[2]+","+coordenades[3]+"\n"
          
        else: #when an instance's just created by the user coordenades of an object are generated randomly                          
            self.oval_RT = randint(1,(canvas_width-80))
            self.oval_LT = int(self.oval_RT+(90*(Size_factor+0.1)))
            self.oval_TT = randint(1,(canvas_height-50))
            self.oval_BT = int(self.oval_TT+(56*(Size_factor+0.1)))
            self.coordenades_transcript = str(self.oval_RT)+","+str(self.oval_TT)+","+str(self.oval_LT)+","+str(self.oval_BT)+"\n"                
        self.textX = (self.oval_RT+self.oval_LT)/2
        self.textY = (self.oval_TT +self.oval_BT)/2
        self.move_options = [1,-1]
        self.moveX = choice(self.move_options)
        self.moveY = choice(self.move_options)
        self.track_X = self.oval_RT
        self.track_Y = self.oval_TT  
        #an oval is ploted inside the canvas
        self.ovaled_thought = main_canvas.create_oval(self.oval_RT,self.oval_TT,self.oval_LT,self.oval_BT,
                                                        fill ="white", activefill = "pink",
                                                        width =1,activedash = 5, outline = "black",
                                                        activeoutline = "pink", tag = self.title )                                                                                                          
        self.tag1 = self.getting_key_tag()
        #Coordenades of the just generated oval/thought are saved in dict "coordenades"
        thought_content.save_coordenades(self.coordenades_transcript,self.tag1)
        #A text bos is created. it contains the tag of the thought and is placed at the center of the oval
        self.thought_text = main_canvas.create_text(self.textX,self.textY, text = title, font =  times13b)
        #input options bound to different functions 
        main_canvas.tag_bind(self.ovaled_thought, '<Button-1>', self.clicked_oval_ID)
        main_canvas.tag_bind(self.ovaled_thought, '<Double-Button-1>', Plus_button)
        main_canvas.tag_bind(self.ovaled_thought, '<Button-3>', self.clicked_oval_ID)
        main_canvas.tag_bind(self.ovaled_thought, '<Double-Button-3>', Minus_button)
        main_canvas.tag_bind(self.thought_text, '<Button-1>', self.clicked_oval_ID)
        main_canvas.tag_bind(self.thought_text, '<Double-Button-1>', Plus_button)
        main_canvas.tag_bind(self.thought_text, '<Button-3>', self.clicked_oval_ID)
        main_canvas.tag_bind(self.thought_text, '<Double-Button-3>', Minus_button)
        self.movement()
         
    def movement(self):      
        self.track = main_canvas.coords(self.ovaled_thought)
        self.track_X = self.track[0]
        self.track_Y = self.track[1]
        self.track_X2 = self.track[2]
        self.track_Y2 = self.track[3]
        
        self.track_X += self.moveX
        self.track_Y += self.moveY
        self.track_X2 += self.moveX
        self.track_Y2 += self.moveY    
        
        #checks the oval position and changes its trayectory if it touches one of the four sides of the canvas        
        if self.track_X == 1 or self.track_X < 1:
            self.moveX = 1
        elif self.track_X2 == (canvas_width) or self.track_X2 > (canvas_width):
            self.moveX = -1
            
        if self.track_Y == 1 or self.track_Y < 1:
            self.moveY = 1
        elif self.track_Y2 == (canvas_height) or self.track_Y2 > (canvas_height):
            self.moveY = -1 
            
        #moves the oval in the given direction       
        main_canvas.move(self.ovaled_thought,self.moveX,self.moveY)
        main_canvas.move(self.thought_text,self.moveX,self.moveY)
        window_1.after(25, self.movement)  
        
    def getting_key_tag(self):
        #returns the tag of a specific oval and returns the first value in a tuple if there is more than one tag 
        self.tag_1 = main_canvas.gettags(self.ovaled_thought)
        if len(self.tag_1) ==1:
            (self.tag1,) = self.tag_1
        else:
            (self.tag1, self.tag2) =  self.tag_1                      
                        
        return self.tag1
            
    def getting_key_tag_clicked_button(self):
        # returns the tag of the oval that was last clicked and returns the first element in a tuple if there is more than one tag 
        self.tag_1 = main_canvas.gettags(id_figure_clicked)
        if len(self.tag_1) ==1:
            (self.tag1,) = self.tag_1
        else:
            (self.tag1, self.tag2) =  self.tag_1                      
                        
        return self.tag1

    def clicked_oval_ID(self,event):
        #initializes the control board with the information of the thought clicked
        button_edit.place( in_ = Big_frame, anchor = NW, relx = 0.1, rely = 0.69, relwidth = 0.043)                    
        global id_figure_clicked
        id_figure_clicked = self.ovaled_thought
        self.tag1 = self.getting_key_tag_clicked_button()
        text_label.configure(state = NORMAL)
        text_thought.configure(state = NORMAL)
        text_label.delete(1.0, END)
        text_thought.delete(1.0, END)
        text_label.insert(END, self.tag1)

        self.cont = thought_content.concept(self.tag1)
        text_thought.insert(END, self.cont)
        button_accept.place_forget()
        button_cancel.place_forget()
        text_label.configure(state = DISABLED)
        text_thought.configure(state = DISABLED)
           
class gamesaved(object):
        
    def __init__ (self):
        self.saved_game = 0 # this variable indicates whether any change of the program has been saved or not
           
                
class thoughtvault(object):

    thought_vault = {} # this dictionary contains the tag (keys) and content (values) of each thought
    coordenades = {} # this dictionary contains the tag (keys) and coordenades (values) of each thought

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.increase_catalogue(title, content)
            
            
    def increase_catalogue(self, title, content):
        # populates thought_vault 
        self.thought_vault[title]= (content)          
                
    def concept(self, thetag):
        # gets the tag of a thought and returns its linked content inside thought_vault
        thetag = thetag.decode('utf-8')
        linked_content = self.thought_vault.get(thetag)
        return linked_content
                
    def shrinkdict(self, title):
        #deletes one item inside dict though_vault
        del self.thought_vault[title]
        
    def save_coordenades(self, coordenades,key_dict):   
        #populates coordenades    
        self.coordenades[key_dict] = coordenades
            
    def clear_coordenades(self):
        #deletes one item inside dict coordenades
        self.tag1 = one_thought.getting_key_tag_clicked_button()                                               
        del self.coordenades[self.tag1]
        
    def change_coordenades(self, coordenades):
        #modifies one item inside dict coordenades
        self.key_tag = one_thought.getting_key_tag_clicked_button()
        self.coordenades[self.key_tag] = coordenades
            
    def clear_all(self):
        #removes all the items inside canvas after obtaining confirmation of the player
        self.clear_question = tkMessageBox.askyesno("Thoughts Box", "Are you sure you want to remove all of the thoughts inside the Box")            
        if self.clear_question == 1:
            text_label.configure(state =  NORMAL)
            text_thought.configure(state =  NORMAL)
            main_canvas.delete(ALL)
            #dicts are cleared
            self.thought_vault.clear()
            self.coordenades.clear()
            #Sets control board to default appearance
            button_edit.place_forget()
            button_accept.place_forget()
            button_cancel.place_forget()
            text_label.delete(1.0, END)
            text_thought.delete(1.0, END)
            text_label.configure(state =  DISABLED)
            text_thought.configure(state =  DISABLED)
            gamesaved.saved_game = 1
                 
                        
    def save_thought(self): 
        #this three variables contain tags, content and coordenades of all thoughts    
        self.key_list =  list(self.thought_vault.keys())
        self.val_list =  list(self.thought_vault.values()) 
        self.coord_list =  list(self.coordenades.values())         
           
        self.Thoughts_pantry_file = open("saved_files/Pantry.txt", "w") 
        self.Thoughts_larder_file = open("saved_files/Larder.txt", "w")
        self.Thoughts_coordenades_file = open("saved_files/Coordenades.txt", "w")
        
        #tags are saved in Pantr.txt 
        for thought_label in self.key_list:
            thought_label = thought_label+"\n"
            self.Thoughts_pantry_file.write(thought_label.encode('utf-8')) 
            
        #content is saved in Larder.txt        
        for thought_cont in self.val_list:              
            thought_cont = thought_cont+"\n"
            self.Thoughts_larder_file.write(thought_cont.encode('utf-8'))
            
        #coordenades are saved in Coordenades.txt         
        for coordenades in self.coord_list:
            self.Thoughts_coordenades_file.write(coordenades)
                                                                             
        self.Thoughts_pantry_file.close()
        self.Thoughts_larder_file.close()  
        self.Thoughts_coordenades_file.close
        
        #A label that confirms changes were saved succesfully is defined and placed on a frame        
        self.saved_label = Label(Big_frame, text = "Changes saved successfully!", bg = "Slategray1", fg ="gray1")
        self.saved_label.place(in_ = Big_frame, anchor = NW, relx = 0.07, rely = 0.92)             
        self.fade_out(1) 
        saved_light.saved_game = 0            
        
        # Makes a label fade out and eventually dissapear        
    def fade_out(self, i):                               
        if  i < 60:
            self.i = i
            self.new_color = "gray" + str(self.i)                   
            self.saved_label.configure(fg = self.new_color) 
            self.i +=2                   
            window_1.after(40, lambda: self.fade_out(self.i))
        else:                   
            self.saved_label.destroy()                         
            
            
class storing_thoughts(object):

    def __init__(self):
        #open, stores and organize information saved in txt files 
        self.Thoughts_pantry_file = open("saved_files/Pantry.txt", "r") #Pantry stores thoughts' tags          
        self.Thoughts_pantry = map(str.strip, self.Thoughts_pantry_file.readlines())
        self.Thoughts_pantry_file.close()
                
        self.Thoughts_larder_file = open("saved_files/Larder.txt", "r") #Pantry stores thoughts' content 
        self.Thoughts_larder = map(str.strip, self.Thoughts_larder_file.readlines())
        self.Thoughts_larder_file.close() 
            
        self.Thoughts_coordenades_file = open("saved_files/Coordenades.txt", "r") #Pantry stores thoughts' coordenades 
        self.Thoughts_coordenades = map(str.strip, self.Thoughts_coordenades_file.readlines())            
        self.Thoughts_coordenades_file.close() 
        self.list2 = []
        
        for i in self.Thoughts_coordenades:
            self.list1 = i.split(",")
            self.list2.append(self.list1)

        if len(self.Thoughts_pantry) >0: # only if there was anything stored in Pantry.txt
            for title, content, coordenades in zip(self.Thoughts_pantry, self.Thoughts_larder, self.list2):  
                global thought_content
                #Decodes info stored in the text files from utf-8 to ascci 
                title = title.decode('utf-8') 
                content = content.decode('utf-8')
                
                #transfer tag and content information in the txt files to dict in thought_content.
                thought_content = thoughtvault(title, content)                     
                global one_thought
                #creates new items in the canvas using the information stores in the txt files.
                one_thought =  thoughtgenerator(title, coordenades)

       
def invoking_thoughts():
    title = entry_thought_code.get()
    #controls that there is always a tag for each thought entered in the box
    if len(title.strip(" ")) < 1:
        tkMessageBox.showwarning("Thoughts Box", "A tag is required to place a thought in the Box")
    else:
        content = entry_thought.get()
        entry_thought_code.delete(0, END)
        entry_thought.delete(0, END)
        #content and tag of the thought are saved in the dict within thought_content
        global thought_content 
        thought_content = thoughtvault(title, content)
        global one_thought
        #class that creates items inside the canvas is instantiated
        one_thought =  thoughtgenerator(title)
        saved_light.saved_game = 1             
           
def Plus_button(*args):
    #get coordenades of canvas' item clicked                 
    coordenades = main_canvas.coords(id_figure_clicked)
    coordenades_diff = coordenades[2] - coordenades[0]
    #increases size and changes color of canvas' item clicked
    if int(coordenades_diff) < int(500*Size_factor):
        main_canvas.itemconfigure(id_figure_clicked, fill="goldenrod1")
        main_canvas.coords(id_figure_clicked, coordenades[0]-8,coordenades[1]-5,coordenades[2]+8,coordenades[3]+5)
        main_canvas.coords(id_figure_clicked+1, (coordenades[0]+coordenades[2])/2, (coordenades[1]+coordenades[3])/2)
        #updates dict "coordenades"
        coordenades = main_canvas.coords(id_figure_clicked)
        coordenades_transcript = str(coordenades[0])+","+str(coordenades[1])+","+str(coordenades[2])+","+str(coordenades[3])+"\n" 
        thought_content.change_coordenades(coordenades_transcript)
        saved_light.saved_game = 1

def Minus_button(*args):
    #get coordenades of canvas' item clicked  
    coordenades = main_canvas.coords(id_figure_clicked)
    coordenades_diff = coordenades[2] - coordenades[0]
    #increases size and changes color of canvas' item clicked
    if int(coordenades_diff) > int(110*Size_factor):
        main_canvas.itemconfigure(id_figure_clicked, fill="goldenrod1")
        coordenades = main_canvas.coords(id_figure_clicked)
        main_canvas.coords(id_figure_clicked, coordenades[0]+8,coordenades[1]+5,coordenades[2]-8,coordenades[3]-5)
        main_canvas.coords(id_figure_clicked+1, (coordenades[0]+coordenades[2])/2, (coordenades[1]+coordenades[3])/2)
        #updates dict "coordenades" 
        coordenades = main_canvas.coords(id_figure_clicked)
        coordenades_transcript = str(coordenades[0])+","+str(coordenades[1])+","+str(coordenades[2])+","+str(coordenades[3])+"\n"
        thought_content.change_coordenades(coordenades_transcript)
        saved_light.saved_game = 1  
            
def Remove_action():  
    text_label.configure(state =  NORMAL)
    text_thought.configure(state =  NORMAL)
    #updates dict "coordenades" 
    thought_content.clear_coordenades()
    #Takes out the selected thought in the canvas  
    main_canvas.delete(id_figure_clicked)
    main_canvas.delete(id_figure_clicked+1)  
    #updates dict in "thought_content    
    thought_title1 = text_label.get(1.0, END)   
    title = thought_title1.rstrip()
    thought_content.shrinkdict(title)
    #Set Control panel to default appearance 
    text_label.delete(1.0, END)
    text_thought.delete(1.0, END) 
    button_edit.place_forget()
    button_accept.place_forget()
    button_cancel.place_forget()
    text_label.configure(state =  DISABLED)
    text_thought.configure(state =  DISABLED)
    saved_light.saved_game = 1
                        
def Empty_box():
    thought_content.clear_all()
                            
def Clear_action():
#Clears entry field
    entry_thought_code.delete(0, END)
    entry_thought.delete(0, END)   
   
def Edit_action():
#allows user to edit textboxes and places buttons accept and cancel on their frame
    button_accept.place( in_ = Big_frame, anchor = NW,  relx = 0.1, rely = 0.69, relwidth = 0.043)
    button_cancel.place( in_ = Big_frame, anchor = NW,  relx = 0.15, rely = 0.69, relwidth = 0.043)
    text_label.configure(state = NORMAL)
    text_thought.configure(state = NORMAL)
#saves premodification thought content and tag   
    global current_title, current_content
    current_title = text_label.get(1.0, END).strip()
    current_content = text_thought.get(1.0, END).strip()  
    
# when user edits a thoughts and cancels any modification:                                
def Cancel_action(): 
#Control panel goes back to default appearance      
    text_label.delete(1.0, END)
    text_thought.delete(1.0, END)
    text_label.insert(END, current_title)
    text_thought.insert(END, current_content)
    text_label.configure(state = DISABLED)
    text_thought.configure(state = DISABLED)
    button_accept.place_forget()
    button_cancel.place_forget()

# when user edits a thoughts and accepts the modification:                       
def Accept_action():    
    #new tag and content for the thoughts are obtained
    new_title = text_label.get(1.0, END)
    new_content = text_thought.get(1.0, END)
    new_title = new_title.rstrip() 
    new_content = new_content.rstrip()    
    #thought_content all thought content and tag are deleted and the new ones are stored
    thought_content.shrinkdict(current_title)
    thought_content.increase_catalogue(new_title, new_content)
    thought_content.clear_coordenades()
    #ovaled thought caption and tag are modified
    main_canvas.itemconfigure(id_figure_clicked, tag = (new_title,))
    main_canvas.itemconfigure(id_figure_clicked+1, text = new_title)
    #updates the dict "coordenades by linking new items tag with current coordendades
    thisistag = main_canvas.gettags(id_figure_clicked)
    coordenades = main_canvas.coords(id_figure_clicked)
    coordenades_transcript = str(coordenades[0])+","+str(coordenades[1])+","+str(coordenades[2])+","+str(coordenades[3])+"\n"
    thought_content.change_coordenades(coordenades_transcript)
    #Control panel goes to back to default appearance
    text_label.delete(1.0, END)
    text_thought.delete(1.0, END)                 
    text_label.configure(state = DISABLED)
    text_thought.configure(state = DISABLED)
    button_accept.place_forget()
    button_cancel.place_forget()
    saved_light.saved_game = 1
        
def Save_action():
    thought_content.save_thought()                        


def num_characters(event):
#regulates that no more than 10 characters are entered in the entry field "entry_thought_code"
    if len(Cont_entry_field.get()) > 10:
      Cont_entry_field.set(Cont_entry_field.get()[:10]) 


def ask_saving():
#message box pops out asking user to save changes, application's killed no be the game saved or not
    if saved_light.saved_game == 1:
        answer_saving = tkMessageBox.askyesnocancel("Thoughts Box", "Do you want to save any changes?")
        if answer_saving == True:
            Save_action()
            window_1.destroy()
         
        elif answer_saving == False:       
            window_1.destroy()
    else:
        window_1.destroy() 


def load_inst(): 
# returns instructions written in InstEn.txt
    inst_file = open("saved_files/InstEn.txt", "r").read()
    return inst_file
    
  
def invoking_inst():
#places instruction and button back on screen on top of other frames      
    instructions = load_inst()     
    inst_frame.place(in_ = window_1, relx = 0.04, rely = 0.15, relheight = 0.80, relwidth =0.50 )   
    button_back.place(in_ = inst_frame, relx = 0.11, rely = 0.857) 
        
    label_inst.configure(text = instructions)        
    label_inst.place(in_ = inst_frame, relx = 0.07, rely = 0.05)       
    inst_frame.lift()
    button_back.lift()
    label_inst.lift()

  
def going_back():
# removes frame inst_frame from screen and therefore the instructions   
    inst_frame.place_forget()
            
#defining main window and its features
window_1 = Tk()
window_1.title("Thought Box")
window_1.configure(bg ="snow")
window_1.state("zoomed")

#Variables that contain size of the screen
x = window_1.winfo_screenwidth()
y = window_1.winfo_screenheight()

#Size_factor accounts for the size of the skin and its used to resize the canvas and objects within it
Size_factor = abs(1+((y-1080.0)/1080.0))

#defining several fonts
helv36 = tkFont.Font(family='Courier', size=int(30*Size_factor)) #weight = tkFont.BOLD)
times14 = tkFont.Font(family='Times', size=int(14*(Size_factor+0.15)))
helv20 = tkFont.Font(family='Helvetica', size=int(20*Size_factor))
times13 = tkFont.Font(family='Times', size=int(13*(Size_factor+0.15)))
times13b = tkFont.Font(family='Times', size=int(13*(Size_factor+0.15)))
times14underline = tkFont.Font(family='Times', size=int(13*(Size_factor+0.15)), underline = 1, slant = "italic")
times11 = tkFont.Font(family='Times', size=int(11*(Size_factor+0.15)))

#defining frames
Big_frame = Frame(window_1, bg = "Slategray1", bd = 3)
Long_frame = Frame(window_1, bg = "light slate gray",bd = 3)
Control_frame = Frame(window_1, bg = "Slategray1", bd=2, relief = GROOVE)
inst_frame = Frame(window_1, bg = "Slategray1", bd=2)


#laying down frames on the main window
Big_frame.place(anchor = NW, relx = 0.02, rely = 0.02, relheight = 0.96, relwidth =0.96 )
Long_frame.place(anchor = NW, relx = 0.015, rely = 0.03, relheight = 0.075, relwidth =0.98)
Control_frame.place(anchor = NW, relx = 0.09, rely = 0.46, relheight = 0.30, relwidth =0.35)


#defining labels
label_welcome = Label(window_1, text = "INSIDE THE BOX", bg = "light slate gray", fg ="white", font = helv36)
label_onethought_code = Label(window_1, text = "Tag your thought", bg = "Slategray1", font = times14,fg = "gray10")
label_onethought = Label(window_1, text = "Write the content of your thought", bg = "Slategray1", font = times14,fg = "gray10")
label_panel = Label(window_1, text = "Select a thought to show its content", bg="Slategray1", font = times13, fg = "gray10")
label_panel_title = Label(window_1, text = "Control Panel", bg="Slategray1", fg = "gray54", font = times11)
label_inst = Label(window_1, text = "", bg = "Slategray1", font = times13, justify = LEFT, fg = "gray10")


#laying down labels on the main window
label_welcome.place(in_ = Long_frame, anchor = NW, relx = 0.10, rely = 0.25)
label_onethought_code.place(in_ = Big_frame, anchor = NW, relx = 0.1, rely = 0.16)
label_onethought.place(in_ = Big_frame, anchor = NW, relx = 0.1, rely = 0.24)
label_panel_title.place(in_ = Big_frame, anchor = NW, relx = 0.09, rely = 0.445)
label_panel.place(in_ = Big_frame, anchor = NW, relx = 0.1, rely = 0.49)

#Defining entry fields
Cont_entry_field = StringVar()
entry_thought_code = Entry(window_1, textvariable = Cont_entry_field, font = times13, bg  ="white")
entry_thought_code.bind("<Key>", num_characters)
entry_thought = Entry(window_1, font = times13, bg  ="white")

#Placing entry fields
entry_thought_code.place(in_ = Big_frame, anchor = NW, relx = 0.1, rely = 0.20, relwidth = 0.18)
entry_thought.place(in_ = Big_frame, anchor = NW, relx = 0.1, rely = 0.28, relwidth = 0.28)

#defining buttons
button_clear = Button(window_1, text = "Clear", command  = Clear_action, font = times13)
button_enter = Button(window_1, text = "Enter", command = invoking_thoughts, font = times13)
button_larger = Button(window_1, text = "+", command  = Plus_button, bg = "pale violet red", fg = "white", font = helv20)
button_smaller = Button(window_1, text = "-", command  = Minus_button, bg = "pale violet red", fg = "white", font = helv20)
button_remove = Button(window_1, text = "Remove", command  = Remove_action, bg = "maroon", fg = "white", font = times13)
button_edit = Button(window_1, text = "Edit", command  = Edit_action, font = times13)
button_accept = Button(window_1, text = "Accept", command  = Accept_action, font = times13)
button_cancel = Button(window_1, text = "Cancel", command  = Cancel_action, font = times13)
button_save = Button(window_1, text = "Save Box", command  = Save_action, font = times13)
button_empty_box = Button(window_1, text = "Empty Box", command  = Empty_box, font = times13)
button_inst = Button(window_1, text = "Instructions", font = times14underline, bd = 0, relief = FLAT, bg = "Slategray1", activebackground= "Slategray1", command = invoking_inst)
button_back = Button(window_1, text = "Back", font = times14underline, bd = 0, relief = FLAT, bg = "Slategray1", activebackground= "Slategray1", command = going_back)

#Placing buttons on the frames
button_enter.place(in_ = Big_frame, anchor = NW, relx = 0.1, rely = 0.32, relwidth = 0.043)
button_clear.place(in_ = Big_frame, anchor = NW, relx = 0.15, rely = 0.32, relwidth = 0.043)
button_larger.place(in_ = Big_frame, anchor = NW, relx = 0.9225, rely = 0.12, relheight =0.03 , relwidth = 0.019  )
button_smaller.place(in_ = Big_frame, anchor = NW, relx = 0.9225, rely = 0.18, relheight =0.03 , relwidth = 0.019 )
button_remove.place( in_ = Big_frame, anchor = NW, relx = 0.911, rely = 0.24, relwidth = 0.043)
button_save.place( in_ = Big_frame, anchor = NW, relx = 0.320, rely = 0.69, relwidth = 0.06)
button_empty_box.place( in_ = Big_frame, anchor = NW, relx = 0.260, rely = 0.69, relwidth = 0.06) 
button_inst.place(in_ = Big_frame, anchor = NW, relx = 0.07, rely = 0.85)

#calculating canvas height and width[toolbar(bottom) and title bar(Top) take up aprox 62 pixels in total, this is substracted from the final heights if the canvas]
canvas_height = int(((y*0.90)-62))
canvas_width = int(x*0.31)

#defining canvas
main_canvas = Canvas(window_1, height =canvas_height, width=canvas_width, bg = "snow", borderwidth =2, highlightthickness=1, highlightbackground = "light slate gray")

#Placing canvas on the frame
main_canvas.place(in_ = Big_frame, anchor = NW, relx = 0.57, rely = 0.038)

#defining textboxes
text_label = Text(window_1, height = 1, state = DISABLED, font = times13)
text_thought = Text(window_1, height = 5, state = DISABLED, font = times13)

#placing textboxes
text_label.place( in_ = Big_frame, anchor = NW, relx = 0.1, rely = 0.525, relwidth = 0.18 )
text_thought.place(in_ = Big_frame, anchor = NW, relx = 0.1, rely = 0.575,  relwidth = 0.28, relheight = 0.10 )

   
#loading previously saved items on canvas
saved_light = gamesaved()
initializing = storing_thoughts()     

#protocol to be followed when the user tryes to kill the programme
window_1.protocol("WM_DELETE_WINDOW", ask_saving) 

#infinite loop, keeps the application running 
window_1.mainloop()
