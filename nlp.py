exec(open('chilkatmain.py').read())
import operator
import sys
import chilkat
import re
# This example requires the Chilkat API to have been previously unlocked.
# See Global Unlock Sample for sample code.
# The mailman object is used for sending and receiving email.

# Set the SMTP server (obviously, use your SMTP server, not chilkatsoft.com)
try:
    import Tkinter as tk
    from Tkinter import *
except ImportError:
    import tkinter as tk
    from tkinter import *

class Placeholder_State(object):
     __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'with_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")
    
    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.with_placeholder=True

    def on_focusin(event, entry=entry, state=state):
        if state.with_placeholder:
            entry.delete(0, "end")
            entry.config(fg = state.normal_color, font=state.normal_font)
        
            state.with_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)
            
            state.with_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg = color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")
    
    entry.placeholder_state = state

    return state

class TrieNode(object):
    
    def __init__(self, char):
        
        self.char = char
        self.children = []
        self.wordFinished = False;
         

        
class Application(object):
        
        
        def getStringArrayFromCorpus(self, fileName):
            
            corpus = self.getCorpus(fileName)
            corpusArray = corpus.split(' ')
            
            return corpusArray
        
        
        def getCorpus(self, fileName):
            
            with open(fileName, 'r') as myfile:
                data = myfile.read().replace('\n', ' ')
            
            return data
        
        
        def makeUnigramMap(self):
            
            for string in self.corpusArray:
                self.unigramMap[string] = self.unigramMap.get(string, 0) + 1
                
                
        
        def makeBigramMap(self):
            
            size = len(self.corpusArray)
            
            for i in range(size - 1):
                string = self.corpusArray[i] + ' ' + self.corpusArray[i + 1]
                self.bigramMap[string] = self.bigramMap.get(string, 0) + 1
            
       
        def makeTrigramMap(self):
            
            size = len(self.corpusArray)
            
            for i in range(size - 2):
                string = self.corpusArray[i] + ' ' + self.corpusArray[i + 1] + ' ' + self.corpusArray[i + 2]
                self.trigramMap[string] = self.trigramMap.get(string, 0) + 1
            
            
        
        def makeNgramMap(self):
            
            size = len(self.corpusArray)
            
            for i in range(size - 3):
                string = self.corpusArray[i] + ' ' + self.corpusArray[i + 1] + ' ' + self.corpusArray[i + 2] + ' ' + self.corpusArray[i + 3]
                self.ngramMap[string] = self.ngramMap.get(string, 0) + 1
            
            
        
        def makeNextWordsListMap(self):
            
            for string in self.corpusArray:
                self.nextWordsListMap[string] = set()
                
            size = len(self.corpusArray)
            
            for i in range(size - 1):
                self.nextWordsListMap[self.corpusArray[i]].add(self.corpusArray[i + 1])
        
            
        
        def getNextWordsPrediction(self, screenText,textBox1):
            
            screenTextArray = screenText.split()
            size = len(screenTextArray)
            
            probabilityMap = dict()
            
            # Unigram Case
            if(size == 0):
                
                for key, value in self.unigramMap.items():
                    probabilityMap[str(key)] = float(value)
            
            # Bigram Case
            elif(size == 1):
                denString = screenTextArray[size - 1]
                lastWord = screenTextArray[size - 1]
                den = float(self.unigramMap.get(denString))
                
                for numString in self.nextWordsListMap[lastWord]:
                    search = denString + ' ' + numString
                    
                    if(self.bigramMap.get(search) == None):
                        num = 0
                    else:
                        num = float(self.bigramMap.get(search))
                    
                    value = self.calculateProbability(num, den)
                    
                    probabilityMap[numString] = value
            
            # Trigram Case
            elif(size == 2):
                denString = screenTextArray[size - 2] + ' ' + screenTextArray[size - 1]
                lastWord = screenTextArray[size - 1]
                den = float(self.bigramMap.get(denString))
                
                for numString in self.nextWordsListMap[lastWord]:
                    search = denString + ' ' + numString
                    
                    if(self.trigramMap.get(search) == None):
                        num = 0
                    else:
                        num = float(self.trigramMap.get(search))
                    
                    value = self.calculateProbability(num, den)
                    probabilityMap[numString] = value
            
            # Ngram Case
            else:
                denString = screenTextArray[size - 3] + ' ' + screenTextArray[size - 2] + ' ' + screenTextArray[size - 1]
                lastWord = screenTextArray[size - 1]
                den = float(self.trigramMap.get(denString))
                
                for numString in self.nextWordsListMap[lastWord]:
                    search = denString + ' ' + numString
                    
                    if(self.ngramMap.get(search) == None):
                        num = 0
                    else:
                        num = float(self.ngramMap.get(search))
                    
                    value = self.calculateProbability(num, den)
                    probabilityMap[numString] = value
            
            # get max of 3 words only to show on screen
            size = min(3, len(probabilityMap))
            
            # get top 3 words
            sortedProbabilityMap = dict(sorted(probabilityMap.items(), key = operator.itemgetter(1), reverse = True)[:size])
            
            # print these words
            for key in sortedProbabilityMap.keys():
                print(key, end='     ')
                textBox1.insert(INSERT, key+"     ")
                
            print()
            print('-------------------------------------------------------------------')
            textBox1.insert(INSERT, '\n-------------------------------------------------------------------')
            textBox1.config(state=DISABLED)
        
        def calculateProbability(self, num, den):
            return float(float(num) / float(den))
        
        
        def addWordsToTrie(self):
            
            size = len(self.corpusArray)
            
            for i in range(size):
                
                word = str(self.corpusArray[i])
                node = self.root
            
                for char in word:
                    
                    charFound = False
                    
                    for child in node.children:
                        
                        if char == child.char:
                            node = child
                            charFound = True
                            break
                        
                    if not charFound:
                        newNode = TrieNode(char)
                        node.children.append(newNode)
                        node = newNode
                    
                node.wordFinished = True
            
        
        def getLastWordFromSentence(self, screenText):
            
            screenTextArray = screenText.split()
            size = len(screenTextArray)
            
            return screenTextArray[size - 1]
        
        
        def getAllWordsAfterPrefix(self, node, prefix):
        
            self.getLargestCommonPrefix(node, prefix)
        
        
        def getLargestCommonPrefix(self, root, word):
            
            node = root
            prefix = ""
            
            for char in word:
                
                charFound = False
                
                for child in node.children:
                    
                    if char == child.char:
                        node = child
                        charFound = True
                        prefix = prefix + child.char
                        break
                    
                if not charFound:
                    return self.DFSOnTrie(node, prefix)
                
            return self.DFSOnTrie(node, prefix)
        
        
        def DFSOnTrie(self, node, prefixNow):
            
            if node.wordFinished:
                self.wordList.append(prefixNow)
            
            for child in node.children:
                self.DFSOnTrie(child, prefixNow + child.char)
            
            
        
        def getTopFrequentWords(self,textBox1):
            
            frequencyMap = dict()
            
            for word in self.wordList:
                
                frequencyMap[word] = self.unigramMap.get(word)
                
            size = min(3, len(frequencyMap))
            
            sortedFrequencyMap = dict(sorted(frequencyMap.items(), key = operator.itemgetter(1), reverse = True)[:size])
            
            for key in sortedFrequencyMap.keys():
                print(key, end='     ')
                textBox1.insert(INSERT, key+"     ")
            
            print()
            print('-------------------------------------------------------------------')
            textBox1.insert(INSERT, '\n-------------------------------------------------------------------')
            textBox1.config(state=DISABLED)
        
        
        def clearWordList(self):
            
            self.wordList = []
        
      
        def __init__(self):
            
            self.unigramMap = dict()
            self.bigramMap = dict()
            self.trigramMap = dict()
            self.ngramMap = dict()
            self.nextWordsListMap = dict()
            
            self.root = TrieNode('*')
            self.corpusArray = self.getStringArrayFromCorpus('Big.txt')
            
            self.makeUnigramMap()
            self.makeBigramMap()
            self.makeTrigramMap()
            self.makeNgramMap()
            self.makeNextWordsListMap()
            self.addWordsToTrie()
            
            # To store results everytime a button is pressed.
            self.wordList = []


class Main:
    
    def eml(self,E1,E4,E2,E3,E6,textBox,main,frame):
        mailman = chilkat.CkMailMan()
        f = open("priority words.txt", "r")
        pri={}
        for x in f:
           l =x.split(":")
           aaa=l[1]
           aaa.strip()
           pri[l[0]]=int(aaa)
        f.close()
        
        zox=textBox.get("1.0", 'end-1c')
        # string or message goes hererr
    
        o=zox
        a=zox.lower()
        z=re.split('\s|\\s|\n|\t',a)
        #for i in range(0,n)
        ress=0
        count=0
        for i in z:
            for key in pri:
                if i in key:
                    ress =ress + pri[key]
                    count=count+1
        length=len(z)
        if count!=0:
            res  =ress/count
        else:
            res=0
        #res=ress/length
        print("Normalized Priority: ",res)
        
        l7 = Label(main, text="Normalized Priority (between -2 and 2) : ")
        l7.place(x=130,y=600)
        #textBox2 = tk.Text(frame)
        #textBox2.place(x = 350, y = 600, height = 20, width = 130)
        E7 = Entry(main,width=20,justify=CENTER)
        E7.place(x=350,y=600)
        E7.insert(0,res)
        #textBox2.insert(INSERT,res)
        E7.config(state=DISABLED,disabledbackground="white")
        l8 = Label(main, text="")
        if (res>=1.5):
            priorityx=1
            l8["text"]="(HIGH Priority)"
            l8["fg"]="red"
        elif (res<1.5 and res>0.5):
            priorityx=2
            l8["text"]="(HIGH Priority)"
            l8["fg"]="red"
        elif (res<=0.5 and res>=-0.5):
            priorityx=3
            l8["fg"]="blue"
            l8["text"]="(NORMAL Priority)"
        elif (res<-0.5 and res>=-1.5):
            priorityx=4
            l8["text"]="(LOW Priority)"
            l8["fg"]="green"
        else:
            priorityx=5
            l8["fg"]="green"
            l8["text"]="(LOW Priority)"
        
        l8.place(x=460,y=600)
        
        mailman = chilkat.CkMailMan()
        # Set the SMTP server (obviously, use your SMTP server, not chilkatsoft.com)
        mailman.put_SmtpHost("smtp.gmail.com")
        
        # Set the SMTP login/password (if required)
        
        mailman.put_SmtpUsername(E3.get())
        mailman.put_SmtpPassword(E6.get())
        
        # Create a new email object
        email = chilkat.CkEmail()
        powee =priorityx
        aaa= "This is a "+str(powee)+" priority gmail"
        #email.put_Subject(o[poweeind])
        email.put_Subject(E4.get())
        
        email.put_Body(textBox.get("1.0", 'end-1c'))
        email.put_From(E1.get()+" <"+E2.get()+">")
        success = email.AddTo(E1.get(),E2.get())
        email.AddHeaderField("X-Priority",str(powee))
        
        success = mailman.SendEmail(email)
        if (success != True):
            messagebox.showinfo("Error in sending mail","Mail has not been sent!!!\nSee console for error logs.")
            print(mailman.lastErrorText())
            sys.exit()
        else:
            messagebox.showinfo("Mail Sent", "Mail has been sent successfully!!!")
        success = mailman.CloseSmtpConnection()
        if (success != True):
            print("Connection to SMTP server not closed cleanly.")
        
    
    def nextFunction(self, textBox, nwp,textBox1):
        
        print('Top words predicted are: ')
        textBox1.config(state=NORMAL)
        textBox1.delete("1.0", 'end-1c')
        textBox1.insert(INSERT, "Top words predicted are: \n")
        nwp.getNextWordsPrediction(textBox.get("1.0", 'end-1c'),textBox1)

    def completionFunction(self, textBox, nwp,textBox1):
        
        print('Any of the following words you want: ')
        textBox1.config(state=NORMAL)
        textBox1.delete("1.0", 'end-1c')
        textBox1.insert(INSERT, "Any of the following words you want: \n")
        prefix = nwp.getLastWordFromSentence(textBox.get("1.0", 'end-1c'))
        nwp.getAllWordsAfterPrefix(nwp.root, prefix)
        nwp.getTopFrequentWords(textBox1)
        nwp.clearWordList()

    def correctionFunction(self, textBox, nwp,textBox1):
        
        print('Did you mean? ')
        textBox1.config(state=NORMAL)
        textBox1.delete("1.0", 'end-1c')
        textBox1.insert(INSERT, "Did you mean? \n")
        lastWord = nwp.getLastWordFromSentence(textBox.get("1.0", 'end-1c'))
        nwp.getAllWordsAfterPrefix(nwp.root, lastWord)
        nwp.getTopFrequentWords(textBox1)
        nwp.clearWordList()
        
    def movement1(self):
        
        maxwidth = 420
        minwidth = 350
        x0,y0,x1,y1=self.canvas.coords(self.rectangle1)
        if((x0+10)>maxwidth):
            self.x=-5
            self.canvas.move(self.rectangle1, self.x, self.y)
        elif((x1-10)<minwidth):
            self.x=5
            self.canvas.move(self.rectangle1, self.x, self.y)
        else:
            self.canvas.move(self.rectangle1, self.x, self.y)
        self.canvas.after(100, self.movement1) 
        
    def movements(self, max1, min1, sq):
        def movementsrec():
            x0,y0,x2,y2=self.canvas.coords(sq)
            if((y2+5)>max1):
                self.t1=-5
                self.canvas.move(sq, self.s1, self.t1)
            elif((y0-5)<min1):
                self.t1=5
                self.canvas.move(sq, self.s1, self.t1)
            else:
                self.canvas.move(sq, self.s1, self.t1)
            self.canvas.after(1000, movementsrec) 
        movementsrec()

    def __init__(self):
        
        def enter11(e):
            image2=tk.PhotoImage(file="button2.png")
            button11["image"]=image2
            button11.image=image2
        
        def leave11(e):
            image1=tk.PhotoImage(file="button1.png")
            button11["image"]=image1
            button11.image=image1
        
        def enter12(e):
            image2=tk.PhotoImage(file="button2.png")
            button12["image"]=image2
            button12.image=image2
        
        def leave12(e):
            image1=tk.PhotoImage(file="button1.png")
            button12["image"]=image1
            button12.image=image1
            
        def enter13(e):
            image2=tk.PhotoImage(file="button2.png")
            button13["image"]=image2
            button13.image=image2
        
        def leave13(e):
            image1=tk.PhotoImage(file="button1.png")
            button13["image"]=image1
            button13.image=image1
            
        def enter14(e):
            image3=tk.PhotoImage(file="send.png")
            button14["image"]=image3
            button14.image=image3
        
        def leave14(e):
            image1=tk.PhotoImage(file="button1.png")
            button14["image"]=image1
            button14.image=image1
            
        def change_color():
            current_color = emailbutton.cget("fg")
            next_color = "black" if current_color == "red" else "red"
            emailbutton.config(fg=next_color)
            main.after(1000, change_color)
            
            
        nwp = Application()
        
        main = tk.Tk()
        main.resizable(False, False)
        frame = tk.Frame(main, width = 780, height = 700)
        frame.pack()
        self.canvas = tk.Canvas(frame,width = 780, height = 700) 
        self.canvas.pack()
        main.title("NLP Application")
        
        l1 = Label(main, text="Name: ")
        l1.place(x=56,y=5)
        E1 = Entry(main,width=105)
        E1.place(x=105,y=5)
        add_placeholder_to(E1, 'Enter Name to be sent along with email...')
        
        l4 = Label(main, text="Subject: ")
        l4.place(x=50,y=35)
        E4 = Entry(main,width=105)
        E4.place(x=105,y=35)
        add_placeholder_to(E4, 'Enter subject for the email...')
        
        l2 = Label(main, text="To: ")
        l2.place(x=76,y=65)
        E2 = Entry(main,width=105)
        E2.place(x=105,y=65)
        add_placeholder_to(E2, 'Enter the Email to which message is to be sent...')
        
        l3 = Label(main, text="From: ")
        l3.place(x=61,y=95)
        E3 = Entry(main,width=105)
        E3.place(x=105,y=95)
        add_placeholder_to(E3, 'Enter the Email from which message is to be sent...')
        
        l6 = Label(main, text="Password: ")
        l6.place(x=40,y=125)
        E6 = Entry(main,width=105)
        E6.place(x=105,y=125)
        add_placeholder_to(E6, 'Enter the password of the Email from which message is to be sent...')
        
        l3 = Label(main, text="Enter the message here: \n",font = ('times new roman',12,'bold'))
        l3.place(x=40,y=160,height = 30)
        textBox = tk.Text(self.canvas)
        textBox.place(x = 40, y = 190, height = 120, width = 700)
        
        '''style = Style() 
        style.configure('TButton', font = ('calibri', 20, 'bold'), borderwidth = '4') 
        style.map('TButton', foreground = [('active', 'green')], background = [('active', 'black')])'''
        l5 = Label(main, text="Output Suggestions: \n",font = ('times new roman',12,'bold'))
        l5.place(x=40,y=430,height = 30)
        textBox1 = tk.Text(self.canvas)
        textBox1.place(x = 40, y = 460, height = 120, width = 700)
        textBox1.config(state=DISABLED)
        nextButton = tk.Button(main, text = 'Next',activeforeground='white',activebackground='black', command = lambda: self.nextFunction(textBox, nwp,textBox1))
        nextButton.place(x = 260, y = 330, height = 30, width = 120)
        
        completeButton = tk.Button(main, text = 'Complete',activeforeground='white',activebackground='black', command = lambda: self.completionFunction(textBox, nwp,textBox1))
        completeButton.place(x = 390, y = 330, height = 30, width = 120)
        
        correctButton = tk.Button(main, text = 'Correct',activeforeground='white',activebackground='black', command = lambda: self.correctionFunction(textBox, nwp,textBox1))
        correctButton.place(x = 325, y = 380, height = 30, width = 120)
        
        emailbutton = tk.Button(main, text = 'Send E-mail', font =('Arial', 9, 'bold'),fg="black",activeforeground='white',activebackground='black',command = lambda: self.eml(E1,E4,E2,E3,E6,textBox,main,frame))
        emailbutton.place(x = 325, y = 630, height = 30, width = 120)
        
        change_color()
        image1=tk.PhotoImage(file="button1.png")
        button11=tk.Button(main,borderwidth=0,command = lambda: self.nextFunction(textBox, nwp,textBox1))
        button11.image=image1
        button11.place(x = 350, y = 335, height = 20, width = 20)
        
        button11.bind("<Enter>",enter11)
        button11.bind("<Leave>",leave11)
        button11.bind("<Button-2>",enter11)
        
        nextButton.bind("<Enter>",enter11)
        nextButton.bind("<Leave>",leave11)
        nextButton.bind("<Button-2>",enter11)
        
        button12=tk.Button(main,borderwidth=0,command = lambda: self.completionFunction(textBox, nwp,textBox1))
        button12.image=image1
        button12.place(x = 480, y = 335, height = 20, width = 20)
        
        button12.bind("<Enter>",enter12)
        button12.bind("<Leave>",leave12)
        button12.bind("<Button-2>",enter12)
        
        completeButton.bind("<Enter>",enter12)
        completeButton.bind("<Leave>",leave12)
        completeButton.bind("<Button-2>",enter12)
        
        button13=tk.Button(main,borderwidth=0,command = lambda: self.correctionFunction(textBox, nwp,textBox1))
        button13.image=image1
        button13.place(x = 415, y = 385, height = 20, width = 20)
        
        button13.bind("<Enter>",enter13)
        button13.bind("<Leave>",leave13)
        button13.bind("<Button-2>",enter13)
        
        correctButton.bind("<Enter>",enter13)
        correctButton.bind("<Leave>",leave13)
        correctButton.bind("<Button-2>",enter13)
        
        button14=tk.Button(main,borderwidth=0,command = lambda: self.eml(E1,E4,E2,E3,E6,textBox,main,frame))
        button14.image=image1
        button14.place(x = 423, y = 635, height = 20, width = 20)
        
        button14.bind("<Enter>",enter14)
        button14.bind("<Leave>",leave14)
        button14.bind("<Button-2>",enter14)
        
        emailbutton.bind("<Enter>",enter14)
        emailbutton.bind("<Leave>",leave14)
        emailbutton.bind("<Button-2>",enter14)
        
        self.x=5
        self.y=0
        self.s1=0
        self.t1=5
        
        self.rectangle1 = self.canvas.create_rectangle(350, 312, 361, 323, fill = "black") 
        self.canvas.pack() 
        self.movement1()
        
        self.square1 = self.canvas.create_rectangle(770, 5, 775, 10, fill = "black") 
        self.square2 = self.canvas.create_rectangle(770, 15, 775, 20, fill = "black") 
        self.square3 = self.canvas.create_rectangle(770, 25, 775, 30, fill = "black") 
        self.square4 = self.canvas.create_rectangle(770, 35, 775, 40, fill = "black") 
        self.square5 = self.canvas.create_rectangle(770, 45, 775, 50, fill = "black") 
        self.square6 = self.canvas.create_rectangle(770, 55, 775, 60, fill = "black") 
        self.square7 = self.canvas.create_rectangle(770, 65, 775, 70, fill = "black") 
        self.square8 = self.canvas.create_rectangle(770, 75, 775, 80, fill = "black") 
        self.square9 = self.canvas.create_rectangle(770, 85, 775, 90, fill = "black") 
        self.square10 = self.canvas.create_rectangle(770, 95, 775, 100, fill = "black") 
        self.square11 = self.canvas.create_rectangle(770, 105, 775, 110, fill = "black") 
        self.square12 = self.canvas.create_rectangle(770, 115, 775, 120, fill = "black") 
        self.square13 = self.canvas.create_rectangle(770, 125, 775, 130, fill = "black") 
        self.square14 = self.canvas.create_rectangle(770, 135, 775, 140, fill = "black") 
        self.square15 = self.canvas.create_rectangle(770, 145, 775, 150, fill = "black") 
        self.square16 = self.canvas.create_rectangle(770, 155, 775, 160, fill = "black") 
        self.square17 = self.canvas.create_rectangle(770, 165, 775, 170, fill = "black") 
        self.square18 = self.canvas.create_rectangle(770, 175, 775, 180, fill = "black") 
        self.square19 = self.canvas.create_rectangle(770, 185, 775, 190, fill = "black") 
        self.square20 = self.canvas.create_rectangle(770, 195, 775, 200, fill = "black") 
        self.square21 = self.canvas.create_rectangle(770, 205, 775, 210, fill = "black")
        self.square22 = self.canvas.create_rectangle(770, 215, 775, 220, fill = "black")
        self.square23 = self.canvas.create_rectangle(770, 225, 775, 230, fill = "black")
        self.square24 = self.canvas.create_rectangle(770, 235, 775, 240, fill = "black")
        self.square25 = self.canvas.create_rectangle(770, 245, 775, 250, fill = "black")
        self.square26 = self.canvas.create_rectangle(770, 255, 775, 260, fill = "black")
        self.square27 = self.canvas.create_rectangle(770, 265, 775, 270, fill = "black")
        self.square28 = self.canvas.create_rectangle(770, 275, 775, 280, fill = "black")
        self.square29 = self.canvas.create_rectangle(770, 285, 775, 290, fill = "black")
        self.square30 = self.canvas.create_rectangle(770, 295, 775, 300, fill = "black")
        self.square31 = self.canvas.create_rectangle(770, 305, 775, 310, fill = "black")
        self.square32 = self.canvas.create_rectangle(770, 315, 775, 320, fill = "black")
        self.square33 = self.canvas.create_rectangle(770, 325, 775, 330, fill = "black")
        self.square34 = self.canvas.create_rectangle(770, 335, 775, 340, fill = "black")
        self.square35 = self.canvas.create_rectangle(770, 345, 775, 350, fill = "black")
        self.square36 = self.canvas.create_rectangle(770, 355, 775, 360, fill = "black")
        self.square37 = self.canvas.create_rectangle(770, 365, 775, 370, fill = "black")
        self.square38 = self.canvas.create_rectangle(770, 375, 775, 380, fill = "black")
        self.square39 = self.canvas.create_rectangle(770, 385, 775, 390, fill = "black")
        self.square40 = self.canvas.create_rectangle(770, 395, 775, 400, fill = "black")
        self.square41 = self.canvas.create_rectangle(770, 405, 775, 410, fill = "black")
        self.square42 = self.canvas.create_rectangle(770, 415, 775, 420, fill = "black")
        self.square43 = self.canvas.create_rectangle(770, 425, 775, 430, fill = "black")
        self.square44 = self.canvas.create_rectangle(770, 435, 775, 440, fill = "black")
        self.square45 = self.canvas.create_rectangle(770, 445, 775, 450, fill = "black")
        self.square46 = self.canvas.create_rectangle(770, 455, 775, 460, fill = "black")
        self.square47 = self.canvas.create_rectangle(770, 465, 775, 470, fill = "black")
        self.square48 = self.canvas.create_rectangle(770, 475, 775, 480, fill = "black")
        self.square49 = self.canvas.create_rectangle(770, 485, 775, 490, fill = "black")
        self.square50 = self.canvas.create_rectangle(770, 495, 775, 500, fill = "black")
        self.square51 = self.canvas.create_rectangle(770, 505, 775, 510, fill = "black")
        self.square52 = self.canvas.create_rectangle(770, 515, 775, 520, fill = "black")
        self.square53 = self.canvas.create_rectangle(770, 525, 775, 530, fill = "black")
        self.square54 = self.canvas.create_rectangle(770, 535, 775, 540, fill = "black")
        self.square55 = self.canvas.create_rectangle(770, 545, 775, 550, fill = "black")
        self.square56 = self.canvas.create_rectangle(770, 555, 775, 560, fill = "black")
        self.square57 = self.canvas.create_rectangle(770, 565, 775, 570, fill = "black")
        self.square58 = self.canvas.create_rectangle(770, 575, 775, 580, fill = "black")
        self.square59 = self.canvas.create_rectangle(770, 585, 775, 590, fill = "black")
        self.square60 = self.canvas.create_rectangle(770, 595, 775, 600, fill = "black")
        self.square61 = self.canvas.create_rectangle(770, 605, 775, 610, fill = "black")
        self.square62 = self.canvas.create_rectangle(770, 615, 775, 620, fill = "black")
        self.square63 = self.canvas.create_rectangle(770, 625, 775, 630, fill = "black")
        self.square64 = self.canvas.create_rectangle(770, 635, 775, 640, fill = "black")
        self.square65 = self.canvas.create_rectangle(770, 645, 775, 650, fill = "black")
        self.square66 = self.canvas.create_rectangle(770, 655, 775, 660, fill = "black")
        self.square67 = self.canvas.create_rectangle(770, 665, 775, 670, fill = "black")
        self.square68 = self.canvas.create_rectangle(770, 675, 775, 680, fill = "black")
        self.square69 = self.canvas.create_rectangle(770, 685, 775, 690, fill = "black")
        
        self.s1quare1 = self.canvas.create_rectangle(5, 5, 10, 10, fill = "black") 
        self.s1quare2 = self.canvas.create_rectangle(5, 15, 10, 20, fill = "black") 
        self.s1quare3 = self.canvas.create_rectangle(5, 25, 10, 30, fill = "black") 
        self.s1quare4 = self.canvas.create_rectangle(5, 35, 10, 40, fill = "black") 
        self.s1quare5 = self.canvas.create_rectangle(5, 45, 10, 50, fill = "black") 
        self.s1quare6 = self.canvas.create_rectangle(5, 55, 10, 60, fill = "black") 
        self.s1quare7 = self.canvas.create_rectangle(5, 65, 10, 70, fill = "black") 
        self.s1quare8 = self.canvas.create_rectangle(5, 75, 10, 80, fill = "black") 
        self.s1quare9 = self.canvas.create_rectangle(5, 85, 10, 90, fill = "black") 
        self.s1quare10 = self.canvas.create_rectangle(5, 95, 10, 100, fill = "black") 
        self.s1quare11 = self.canvas.create_rectangle(5, 105, 10, 110, fill = "black") 
        self.s1quare12 = self.canvas.create_rectangle(5, 115, 10, 120, fill = "black") 
        self.s1quare13 = self.canvas.create_rectangle(5, 125, 10, 130, fill = "black") 
        self.s1quare14 = self.canvas.create_rectangle(5, 135, 10, 140, fill = "black") 
        self.s1quare15 = self.canvas.create_rectangle(5, 145, 10, 150, fill = "black") 
        self.s1quare16 = self.canvas.create_rectangle(5, 155, 10, 160, fill = "black") 
        self.s1quare17 = self.canvas.create_rectangle(5, 165, 10, 170, fill = "black") 
        self.s1quare18 = self.canvas.create_rectangle(5, 175, 10, 180, fill = "black") 
        self.s1quare19 = self.canvas.create_rectangle(5, 185, 10, 190, fill = "black") 
        self.s1quare20 = self.canvas.create_rectangle(5, 195, 10, 200, fill = "black") 
        self.s1quare21 = self.canvas.create_rectangle(5, 205, 10, 210, fill = "black")
        self.s1quare22 = self.canvas.create_rectangle(5, 215, 10, 220, fill = "black")
        self.s1quare23 = self.canvas.create_rectangle(5, 225, 10, 230, fill = "black")
        self.s1quare24 = self.canvas.create_rectangle(5, 235, 10, 240, fill = "black")
        self.s1quare25 = self.canvas.create_rectangle(5, 245, 10, 250, fill = "black")
        self.s1quare26 = self.canvas.create_rectangle(5, 255, 10, 260, fill = "black")
        self.s1quare27 = self.canvas.create_rectangle(5, 265, 10, 270, fill = "black")
        self.s1quare28 = self.canvas.create_rectangle(5, 275, 10, 280, fill = "black")
        self.s1quare29 = self.canvas.create_rectangle(5, 285, 10, 290, fill = "black")
        self.s1quare30 = self.canvas.create_rectangle(5, 295, 10, 300, fill = "black")
        self.s1quare31 = self.canvas.create_rectangle(5, 305, 10, 310, fill = "black")
        self.s1quare32 = self.canvas.create_rectangle(5, 315, 10, 320, fill = "black")
        self.s1quare33 = self.canvas.create_rectangle(5, 325, 10, 330, fill = "black")
        self.s1quare34 = self.canvas.create_rectangle(5, 335, 10, 340, fill = "black")
        self.s1quare35 = self.canvas.create_rectangle(5, 345, 10, 350, fill = "black")
        self.s1quare36 = self.canvas.create_rectangle(5, 355, 10, 360, fill = "black")
        self.s1quare37 = self.canvas.create_rectangle(5, 365, 10, 370, fill = "black")
        self.s1quare38 = self.canvas.create_rectangle(5, 375, 10, 380, fill = "black")
        self.s1quare39 = self.canvas.create_rectangle(5, 385, 10, 390, fill = "black")
        self.s1quare40 = self.canvas.create_rectangle(5, 395, 10, 400, fill = "black")
        self.s1quare41 = self.canvas.create_rectangle(5, 405, 10, 410, fill = "black")
        self.s1quare42 = self.canvas.create_rectangle(5, 415, 10, 420, fill = "black")
        self.s1quare43 = self.canvas.create_rectangle(5, 425, 10, 430, fill = "black")
        self.s1quare44 = self.canvas.create_rectangle(5, 435, 10, 440, fill = "black")
        self.s1quare45 = self.canvas.create_rectangle(5, 445, 10, 450, fill = "black")
        self.s1quare46 = self.canvas.create_rectangle(5, 455, 10, 460, fill = "black")
        self.s1quare47 = self.canvas.create_rectangle(5, 465, 10, 470, fill = "black")
        self.s1quare48 = self.canvas.create_rectangle(5, 475, 10, 480, fill = "black")
        self.s1quare49 = self.canvas.create_rectangle(5, 485, 10, 490, fill = "black")
        self.s1quare50 = self.canvas.create_rectangle(5, 495, 10, 500, fill = "black")
        self.s1quare51 = self.canvas.create_rectangle(5, 505, 10, 510, fill = "black")
        self.s1quare52 = self.canvas.create_rectangle(5, 515, 10, 520, fill = "black")
        self.s1quare53 = self.canvas.create_rectangle(5, 525, 10, 530, fill = "black")
        self.s1quare54 = self.canvas.create_rectangle(5, 535, 10, 540, fill = "black")
        self.s1quare55 = self.canvas.create_rectangle(5, 545, 10, 550, fill = "black")
        self.s1quare56 = self.canvas.create_rectangle(5, 555, 10, 560, fill = "black")
        self.s1quare57 = self.canvas.create_rectangle(5, 565, 10, 570, fill = "black")
        self.s1quare58 = self.canvas.create_rectangle(5, 575, 10, 580, fill = "black")
        self.s1quare59 = self.canvas.create_rectangle(5, 585, 10, 590, fill = "black")
        self.s1quare60 = self.canvas.create_rectangle(5, 595, 10, 600, fill = "black")
        self.s1quare61 = self.canvas.create_rectangle(5, 605, 10, 610, fill = "black")
        self.s1quare62 = self.canvas.create_rectangle(5, 615, 10, 620, fill = "black")
        self.s1quare63 = self.canvas.create_rectangle(5, 625, 10, 630, fill = "black")
        self.s1quare64 = self.canvas.create_rectangle(5, 635, 10, 640, fill = "black")
        self.s1quare65 = self.canvas.create_rectangle(5, 645, 10, 650, fill = "black")
        self.s1quare66 = self.canvas.create_rectangle(5, 655, 10, 660, fill = "black")
        self.s1quare67 = self.canvas.create_rectangle(5, 665, 10, 670, fill = "black")
        self.s1quare68 = self.canvas.create_rectangle(5, 675, 10, 680, fill = "black")
        self.s1quare69 = self.canvas.create_rectangle(5, 685, 10, 690, fill = "black")
        
        u=15
        v=5
        for i in range(69):
            sq1 = "square"+str(i+1)
            xy1 = getattr(self, sq1)
            self.movements(u,v,xy1)
            
            sq2 = "s1quare"+str(i+1)
            xy2 = getattr(self, sq2)
            self.movements(u,v,xy2)
            u+=10
            v+=10
        
        main.mainloop()


class Driver:
    
    Main()
