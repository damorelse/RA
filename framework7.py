from Tkinter import *
import tkSimpleDialog
import tkFileDialog
from ttk import Frame, Button, Label, Style
import os
import sys
import gobject
import gst
import Tkinter
import threading
import time
import tkMessageBox
from abc import ABCMeta, abstractmethod
from bisect import bisect_right
from background7 import *

class Input(object):
    __metaclass__ = ABCMeta
        
    @abstractmethod
    def getMode(self):
        pass
    @abstractmethod
    def checkForInput(self):
        pass
        
    @staticmethod
    def code(mytype, parent, speakers, idea):
        parent.update_symbols(mytype, None, speakers, idea)
        
    @staticmethod
    def idea(curr):
        pass
        
    @staticmethod
    def topic(parent):
        pass
        
    @staticmethod
    def speaker(curr, id):
        pass
        
    @staticmethod
    def undo():
        #self.project.seq.undo()
        pass
        
    @staticmethod
    def delete(curr):
        pass
        
    @staticmethod
    def vidPlayPause(parent):
        parent.play_video()
        
    @staticmethod
    def vidPlayback(parent):
        parent.play_back()
        
    @staticmethod
    def vidPlayforward(parent):
        parent.play_forward()
        
    @staticmethod
    def vidCaption():
        pass
        
    @staticmethod
    def showScreenKeys():
        pass
        
    @staticmethod
    def newProject():
        NewProjectDialog(self.parent)
        
    @staticmethod
    def saveProject():
        self.parent.project.saveProject()
        
    @staticmethod
    def outputCode():
        self.parent.project.outputCode()
         
class KeyboardInput(Input):
    def __init__(self, parent, frame):
        self.parent = parent
        self.frame = frame
        frame.bind("<Key>", self.key)
        frame.bind("<KeyRelease>", self.keyrel)
        
        self.codemap = {
            'a':'yesandquestion',
            's':'interrupt',
            'd':'block',
            'f':'overcoming',
            'q':'move',
            'w':'question',
            'e':'support',
            'r':'yesand',
            'z':'deflection',
            'x':'humour',
            'c':'block-support',
            'v':'hesitation',
        }
        self.pressed = set()
        self.vidSpeedChange = 1
            
    def getMode():
        return "keyboard"
    def checkForInput(self):
        ev = self.event
        echar = ev.char;
        esym = ev.keysym;
        #print ev.keysym+' '+echar
        if echar != '':
            if echar.lower() in self.codemap: #code
                speakers = []
                for p in self.pressed:
                    if ord(p)-ord('0') >= 0 and ord(p)-ord('0') <= len(self.parent.speakers):
                        speakers.append(ord(p)-ord('0'))
                self.parent.buttonmap[echar.lower()].configure(bg="gray", relief=SUNKEN)
                super(KeyboardInput,  self).code(self.codemap[echar.lower()], self.parent, speakers, '\r' in self.pressed)
            elif echar == '\r': #enter
                self.parent.buttonmap[echar].select()
                super(KeyboardInput, self).idea(None)
            elif ord(echar)-ord('0') >= 0 and ord(echar)-ord('0')< 10: #number
                super(KeyboardInput, self).speaker(None, ord(echar)-ord('0'))
            elif echar == '\x1a': #Ctrl-Z
                super(KeyboardInput, self).undo()
            elif echar == '\x08': #backspace
                super(KeyboardInput, self).delete(None)
            elif echar == ' ': #spacebar
                super(KeyboardInput, self).vidPlayPause(self.parent)
            elif echar == '=': #= button
                super(KeyboardInput, self).vidSpeedUp(self.vidSpeedChange)
            elif echar == '-': #- button
                super(KeyboardInput, self).vidSpeedDown(self.vidSpeedChange)
            elif echar == '\x0e': #Ctrl-N
                super(KeyboardInput, self).newProject()
            elif echar == '\x13': #Ctrl-S
                super(KeyboardInput, self).saveProject()
        else:
            if esym == 'Shift_L': #any shift
                super(KeyboardInput, self).topic(self.parent)
            elif esym == 'Left':
                super(KeyboardInput, self).vidPlayback(self.parent)
            elif esym == 'Right':
                super(KeyboardInput, self).vidPlayforward(self.parent)
    def key(self, event):
        evc = event.char
        if len(evc.lower()) != 0:
            evc = evc.lower()
        if len(evc) != 0:
            self.pressed.add(evc)
        self.event = event
        self.checkForInput()
    def keyrel(self, event):
        self.pressed.discard(event.char)
        if event.char.lower() in self.codemap:
            self.parent.buttonmap[event.char.lower()].configure(bg="white", relief=RAISED)
        if event.char == '\r': #enter
            self.parent.buttonmap[event.char].deselect()
        
class ErrorDialog(tkSimpleDialog.Dialog):
    def __init__(self, parent, msg, title=None):
        self.msg = msg
        if title==None:
            title = 'Error'
        tkSimpleDialog.Dialog.__init__(self, parent, title)
    def body(self, parent):
        Label(parent, text=self.msg).pack()
    def buttonbox(self):
        box = Frame(self)
        btn = Button(box, text="OK", width=10, command=self.destroy)
        btn.pack(side=LEFT, padx=5, pady=5)
        box.pack()
        
class helpDialog(tkSimpleDialog.Dialog):
    def __init__(self, parent):
        self.keymap = [
            ['Enter', 'Idea'],
            ['Shift', 'Topic'],
            ['1,2,3' , 'Speakers A,B,C'],
            ['Right-click', 'Delete symbol/topic'],
            ['Left-click', 'Edit symbol/topic'],
            ['Spacebar', 'Video play/pause'],
            ['Left arrow', 'Video playback'],
            ['Right arrow', 'Video playforward'],       
        ]
        tkSimpleDialog.Dialog.__init__(self, parent, 'Keyboard Coding')
        
    def body(self, parent):
        for i, key in enumerate(self.keymap):
            Label(parent, text=key[0]).grid(row=i, column=0, sticky='W')
            Label(parent, text='     ').grid(row=i, column=1, sticky='W')
            Label(parent, text=key[1]).grid(row=i, column=2, sticky='W')
    def buttonbox(self):
        box = Frame(self)
        btn = Button(box, text="OK", width=10, command=self.destroy)
        btn.pack(side=LEFT, padx=5, pady=5)
        box.pack()
        
class SaveAsDialog:  
    def __init__(self, parent, project):
        self.project = project
        #tkSimpleDialog.Dialog.__init__(self, parent, 'Save As') 
        ftypes = [('Log files', '*.log')]
        filename = tkFileDialog.asksaveasfile(title='Save As', filetypes = ftypes)
        if filename and len(filename.name) != 0:
            self.project.saveAsProject(filename.name)
        
class OldProjectDialog(Frame):
    def __init__(self, parent):    
        self.parent = parent
        self._w = ''
        ftypes = [('Log files', '*.log')]
        dlg = tkFileDialog.Open(self.parent, filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            self.parent.display.config(state=NORMAL)
            self.parent.display.delete(1.0,END)
            self.parent.display.config(state=DISABLED) 
            self.parent.num_inserted=[]
            self.readFile(fl)
    def readFile(self, filename):
        try:
            f = open(filename, "r")
            content = f.readlines()
            name = content[0]
            vidPath = content[1]
            numSpeaker = int(content[2])
            speakerID = {}
            for i in range(numSpeaker):
                info = content[3+i].split()
                speakerID[int(info[0])] = info[1]
            codes = {}
            prevtime = 0
            for i in range(5+numSpeaker, len(content)):
                if len(content[i]) > 0:
                    info = content[i].split('\t')
                    for i in range(len(info), 7):
                        info.append('');
                    if info[3] == 'False':
                        info[3] = False
                    else:
                        info[3] = True
                    if info[4] == 'False':
                        info[4] = False
                    else:
                        info[4] = True
                    speakers = []
                    if len(info[2]) > 2:
                        speakers = [int(x) for x in info[2][1:-1].split(',')]
                    tmp = Code(float(info[0]), info[1], speakers, info[3], info[4], info[5], info[6].rstrip())
                    #for i in range(len(codes), int(floor(float(info[0])/Sequence.timestep))+1):
                    #    codes.append([])
                    #codes[int(floor(float(info[0])/Sequence.timestep))].append(tmp)
                    if int(floor(float(info[0])/Sequence.timestep)) in codes.keys():
                        codes[int(floor(float(info[0])/Sequence.timestep))].append(tmp)
                    else:
                        codes[int(floor(float(info[0])/Sequence.timestep))] = [tmp]
                    for i in range(int(floor(float(info[0])/.2)) - prevtime):
                        self.parent.display.image_create('1.end', image=self.parent.imagemap['blank'])
                    self.parent.update_symbols(info[1], float(info[0])*1000000000.0, speakers, info[3])
                    prevtime = int(floor(float(info[0])/.2))
            seq = Sequence(codes)
            self.parent.getProject(Project(name.rstrip(), vidPath.rstrip(), '/'.join(filename.rstrip().split('/')[0:-1]), numSpeaker, speakerID, seq))
        except Exception:
            ErrorDialog(self.parent, "Error while reading log file. Check file format.")
 
class NewProjectDialog(tkSimpleDialog.Dialog):
    def __init__(self, parent):
        tkSimpleDialog.Dialog.__init__(self, parent, 'New Project')
        self.parent = parent

    def buttonbox(self):
        box = Frame(self)
        btn = Button(box, text="Create", width=10, command=self.newP, default=ACTIVE)
        btn.pack(side=LEFT, padx=5, pady=5)
        box.pack()

    def body(self, master):
        self.form = Frame(self, width = 30, height=50)
        self.form.pack()
        Label(self.form, text='Project name').grid(row=0, column=0)
        self.e1 = Entry(self.form)
        self.e1.insert(0, "default")
        self.e1.grid(row=0, column=1)
        Label(self.form, text='Video file').grid(row=1, column=0)
        self.e2 = Entry(self.form)
        self.e2.grid(row=1, column=1)
        Label(self.form, text='Project directory').grid(row=3, column=0)
        self.e3 = Entry(self.form)
        self.e3.insert(0, os.getcwd())
        self.e3.grid(row=3, column=1)
        Button(self.form, text="Select Video", command=self.load_file, width=17).grid(row=2, column=1)
        Label(self.form, text='Number of Speakers').grid(row=4, column=0)
        self.e4 = Listbox(self.form, selectmode = BROWSE)
        for item in [1, 2, 3, 4, 5, 6, 7, 8]:
            self.e4.insert(END, item)
        self.e4.grid(row=4, column=1)      
    def load_file(self):
        ftypes = [('Mov files', '*.mov'), ('Mp4 files', '*.mp4'), ('Avi files', '*.avi'), ('All files', '*.*')]
        dlg = tkFileDialog.Open(self.parent, filetypes=ftypes)
        fl = dlg.show()
        if fl != '':
            self.e2.delete(0, END)
            self.e2.insert(0, fl)
    def newP(self):
        if len(self.e1.get())==0:
            ErrorDialog(self.parent, "Need a project name.")
        elif len(self.e2.get())==0:
            ErrorDialog(self.parent, "Need a video file.")
        elif not os.path.exists(self.e2.get()):
            ErrorDialog(self.parent, "Video file does not exist.")
        elif len(self.e3.get())==0:
            ErrorDialog(self.parent, "Need a project directory.")
        elif not os.path.isdir(self.e3.get()):
            ErrorDialog(self.parent, "Project directory does not exist.")
        elif len(self.e4.curselection())==0:
            ErrorDialog(self.parent, "Need to select number of speakers.")
        else:
            self.parent.getProject(Project(self.e1.get(), self.e2.get(), self.e3.get(), int(self.e4.curselection()[0])+1))
            self.parent.display.config(state=NORMAL)
            self.parent.display.delete(1.0,END)
            self.parent.display.config(state=DISABLED)
            self.parent.num_inserted=[]
            self.destroy()
            
class EditSymDialog(tkSimpleDialog.Dialog):
    def __init__(self, parent, event):
        self.parent = parent
        self.event = event
        self.img = str(self.event.widget)
        self.img = self.img[self.img.rfind(".")+1:]
        self.code = self.parent.project.seq.getClosestCode(self.parent.imgMap[int(self.img)])
        tkSimpleDialog.Dialog.__init__(self, parent, 'Edit Code')

    def buttonbox(self):
        box = Frame(self)
        btn = Button(box, text="OK", width=10, command=self.OK, default=ACTIVE)
        btn.pack(side=LEFT, padx=5, pady=5)
        box.pack()

    def body(self, master):
        self.form = Frame(self, width = 30, height=50)
        self.form.pack()
        
        Label(self.form, text='Code type').grid(row=0, column=0)
        self.typevar = StringVar(self.form)
        self.e1 = OptionMenu(self.form, self.typevar, 'move','block','deflection','interrupt','humour','question','hesitation','support','overcoming','yesand','yesandquestion')
        self.typevar.set(self.code.symbol)
        self.e1.grid(row=0, column=1)
        
        Label(self.form, text='Timestamp (sec)').grid(row=1, column=0)
        self.e2 = Entry(self.form)
        self.e2.insert(0, ""+str(self.code.time))
        self.e2.grid(row=1, column=1)
        
        Label(self.form, text='Speakers').grid(row=2, column=0)
        scrollbar = Scrollbar(self.form, orient=HORIZONTAL)
        self.e3 = Listbox(self.form, selectmode = MULTIPLE, height=len(self.parent.speakers))
        alpha = ['A','B','C','D','E','F','G','H','I']
        for num in range(len(self.parent.speakers)):
            self.e3.insert(END, alpha[num])
        for index in self.code.speaker:
            self.e3.selection_set(int(index)-1)
        self.e3.grid(row=2, column=1)
        
        Label(self.form, text='Idea').grid(row=3, column=0)
        self.ivar = BooleanVar()
        e4 = Checkbutton(self.form, variable=self.ivar)
        self.ivar.set(self.code.idea)
        e4.grid(row=3, column=1)
        
        self.tvar = BooleanVar()
        '''
        Label(self.form, text='Topic switch').grid(row=4, column=0)
        e5 = Checkbutton(self.form, variable=self.tvar)
        self.tvar.set(self.code.topic)
        e5.grid(row=4, column=1)
        '''
    def OK(self):
        if len(self.e2.get())>0:
            try:
                text = self.typevar.get()
                timestamp = float(self.e2.get()) * 1000000000.0
                inspeakers = []
                for i in range(len(self.e3.curselection())):
                    inspeakers.append(int(self.e3.curselection()[i])+ 1)
                inidea = self.ivar.get()
                intopic = self.tvar.get()
                if len(text)>0:
                    #deleteSymbol start     
                    self.parent.display.config(state=NORMAL)
                    self.parent.display.delete(CURRENT) 
                    self.parent.display.config(state=DISABLED) 
                    self.parent.display.image_create(CURRENT, image=self.parent.imagemap['blank'])
                    self.parent.project.seq.delete(None, self.parent.imgMap[int(self.img)])
                    #deleteSymbol end
                    del self.parent.imgMap[int(self.img)]
                    self.parent.update_symbols(text, timestamp, inspeakers, inidea)
                self.destroy() 
            except Exception:
                print "edit code error"
            
class Mainframe(Frame): 
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.lock = threading.Lock()
        self.parent = parent
        self.project = None
        self.speakers = None
        self.imgDir = "symbols/"
        self.alpha = ['A','B','C','D','E','F','G','H','I']
        self.colors = ["blue", "green", "yellow", "orange", "pink", "purple", "red", "brown", "black"]
        self.imagemap = {}
        h = 30
        w = 50
        self.imagemap['deflection'] = PhotoImage(file=self.imgDir+"deflection.gif", height=h, width=w)
        self.imagemap['question'] = PhotoImage(file=self.imgDir+"question.gif", height=h, width=w)
        self.imagemap['hesitation'] = PhotoImage(file=self.imgDir+"hesitation.gif", height=h, width=w)
        self.imagemap['interrupt'] = PhotoImage(file=self.imgDir+"interrupt.gif", height=h, width=w)
        self.imagemap['overcoming'] = PhotoImage(file=self.imgDir+"overcoming.gif", height=h, width=w)
        self.imagemap['support'] = PhotoImage(file=self.imgDir+"support.gif", height=h, width=w)
        self.imagemap['yesand'] = PhotoImage(file=self.imgDir+"yesand.gif", height=h, width=w)
        self.imagemap['humour'] = PhotoImage(file=self.imgDir+"humour.gif", height=h, width=w)
        self.imagemap['move'] = PhotoImage(file=self.imgDir+"move.gif", height=h, width=w)
        self.imagemap['block'] = PhotoImage(file=self.imgDir+"block.gif", height=h, width=w)
        self.imagemap['yesandquestion'] = PhotoImage(file=self.imgDir+"yesandquestion.gif", height=h, width=w)
        self.imagemap['blank'] = PhotoImage(file=self.imgDir+"blank.gif", height=h, width=w)
        self.imagemap['block-support'] = PhotoImage(file=self.imgDir+"block-support.gif", height=h, width=w)
        self.buttonmap={}
        
        self.player = gst.element_factory_make('playbin2', 'player')
        self.play = Button(self, text="Play", width=45)
        self.play.grid(row=5,column=0)
        self.entry = Entry(self, width=50)
        self.entry.grid(row=5, column=1)
        self.back = Button(self, text="Playback", width=45)
        self.back.grid(row=5, column=2)
        self.imgID = 0
        self.imgMap = {}
        #self.progress 
        self.var = DoubleVar()
        self.prev = 0
        self.flag_video_start = 0
        self.pause_changed = 0

        self.initUI()
    def getTime(self):
        pass
    def on_sync_message(self, bus, message, window_id):
        print "sync message"
        if not message.structure is None:
            if message.structure.get_name() == 'prepare-xwindow-id':
                image_sink = message.src
                image_sink.set_property('force-aspect-ratio', True)
                self.lock.acquire()
                #image_sink.set_xwindow_id(window_id)
                self.lock.release()

    def on_message(self, bus, message, window_id):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.play["Text"] = "Play"
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.play["Text"] = "Play"

    #Video embedding part--------------------------------------------------
    
    def sel_play(self):
        #print self.prev
        val2 = self.var.get()
        #print val2
        val = val2 + 1
        if val2 == 0 and self.flag_video_start == 0:
            print "starting"
            self.var.set(0)
            self.flag_video_start = 1
        else:
            self.var.set(val)
        #print self.prev - self.var.get()
        if self.pause_changed:
            print "paused flag"
            self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, (self.var.get()-1)*(10**9))
            self.prev = self.var.get()-1
            self.var.set(self.prev)
            self.pause_changed = 0

        if (self.prev-self.var.get()) != -1:
            #print self.var.get()-val
            self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, self.var.get()*(10**9))
            self.prev = self.var.get()
        else:
            self.prev = self.var.get()
        self.job = self.after(1000, self.sel_play)

    def play_video(self):
        if self.play["text"] == "Play":
            self.player.set_state(gst.STATE_PLAYING)
            self.play["text"] = "Pause"
            self.sel_play()

        else:
            self.pause_changed = 1
            self.player.set_state(gst.STATE_PAUSED)
            self.play["text"] = "Play"
            self.after_cancel(self.job)
         
        self.duration = self.player.query_duration(gst.FORMAT_TIME, None)[0]
        self.slider.configure(from_=0, to=self.duration/1000000000)
        
    def play_back(self):
        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
        text = self.entry.get()
        diff = 0
        if text=="":
            diff = pos_int - (3*(10**9))
        else:
            val = float(self.entry.get())
            diff = pos_int - (val*(10**9))
        #print pos_int
        #print diff/(10**9)
        if diff>0:
            self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, diff)
            print self.var.get() - (diff/10**9)
            self.var.set(diff/10**9)
        else:
            self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 0)
            self.var.set(0)
    def play_forward(self):
        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
        text = self.entry.get()
        diff = 0
        if text=="":
            diff = pos_int + (3*(10**9))
        else:
            val = float(self.entry.get())
            diff = pos_int + (val*(10**9))
        #print pos_int
        #print diff/(10**9)
        if diff>0:
            self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, diff)
            print self.var.get() - (diff/10**9)
            self.var.set(diff/10**9)
        else:
            self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 0)
            self.var.set(0)
    def startVid(self):
        gobject.threads_init()
        video = Frame(self, background='black')
        video.grid(row=0, column=0, columnspan=8, rowspan=4, padx=2, sticky=E+W+S+N)
        window_id = video.winfo_id()
     
        self.buf = gst.Buffer()

        self.bin = gst.Bin("my-bin")
        timeoverlay = gst.element_factory_make("timeoverlay", "overlay")
        self.bin.add(timeoverlay)
        pad = timeoverlay.get_pad("video_sink")
        ghostpad = gst.GhostPad("sink", pad)
        self.bin.add_pad(ghostpad)
        videosink = gst.element_factory_make("ximagesink")
        self.bin.add(videosink)
        gst.element_link_many(timeoverlay, videosink)
    
        self.player.set_property('video-sink', self.bin)
        self.player.set_property('uri', 'file://%s' % (os.path.abspath(self.project.videoPath)))

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()

        bus.connect("message", self.on_message, window_id)
        bus.connect('sync-message::element', self.on_sync_message, window_id)

        self.play.configure(command=lambda: self.play_video())

        self.back.configure(command=self.play_back)
        #self.back = Button(self, text="Playback", command=play_back, width=50)
        #self.back.grid(row=5, column=2)
    #Video embedding done---------------------------------------------------
    
    def startSpeakers(self):
        #Speakers

        s = []
        self.checkvars = []
        for i in range(self.NUM_SPEAKERS):
            s.append(self.alpha[i])
            self.checkvars.append(IntVar())
        if self.speakers != None:
            for pair in self.speakers:
                pair[0].grid_forget()
        i=0
        self.speakers = []
        sframe = Frame(height=2)
        for text in s:
            b = Checkbutton(self.buttongrid, text=text, variable=self.checkvars[i], onvalue = 1, offvalue = 0)
            self.speakers.append((b, self.colors[i]))
            #b.grid(row=i//4, column=(i%4))
            b.grid(row=i,column=0)
            def callback(sv, i):
                self.project.speakerID[i+1] = sv.get()
            sv = StringVar()
            sv.trace("w", lambda name, index, mode, sv=sv, i=i:callback(sv, i))
            c = Entry(self.buttongrid, textvariable=sv)
            c.insert(0, self.project.speakerID[i+1])
            c.grid(row=i, column=1, columnspan=3)
            i += 1

        #Done with speakers

    def getProject(self, inp):
        self.project = inp
        self.NUM_SPEAKERS = self.project.numSpeaker 
        self.parent.title("Project "+self.project.projectName)   
        self.startVid()
        self.startSpeakers()
        self.num_inserted = []
        self.var.set(0)    

    def deleteSymbol(self, event):
        print("delete")
        try:
            img = str(event.widget)
            img = img[img.rfind(".")+1:]
            self.display.config(state=NORMAL)
            self.display.delete(CURRENT) 
            self.display.config(state=DISABLED) 
            self.display.image_create(CURRENT, image=self.imagemap['blank'])
            self.project.seq.delete(None, self.imgMap[int(img)])
            del self.imgMap[int(img)] 
        except:
            print "error delete"
    
    def update_symbols(self, text, timestamp = None, inspeakers = None, inidea = None):
        #Stores timestamp
        if timestamp == None:
            timestamp = self.player.query_position(gst.FORMAT_TIME, None)[0]
        
        self.display.mark_set("mine", "1.%d" % floor(timestamp/1000000000.0/.2))
        if len(str(self.display.get("mine"))) == 0:
            self.display.config(state=NORMAL)
            self.display.delete("mine")
            self.display.config(state=DISABLED)

            
        #Stores current speakers
        current_speakers = []
        store_speakers = []
        if inspeakers == None:
            for i in range(len(self.speakers)):
                if self.checkvars[i].get() == 1:
                    current_speakers.append((self.alpha[i], self.colors[i]))
                    store_speakers.append(i+1)
        else:
            store_speakers = inspeakers
            current_speakers = [(self.alpha[i-1], self.colors[i-1]) for i in inspeakers]

        tempstr = ""
        for sp in current_speakers:
            tempstr += sp[0]
        if inidea or (inidea == None and self.idea_var.get()==1):
            tmplbl = Label(self.display, name="%u" %  self.imgID, image=self.imagemap[text], text=tempstr, compound="bottom", background="yellow")
        else:
            tmplbl = Label(self.display, name="%u" %  self.imgID, image=self.imagemap[text], text=tempstr, compound="bottom", background="white")
        tmpwin = self.display.window_create('mine', window=tmplbl)
        tmplbl.bind("<Button-3>", self.deleteSymbol) #right click
        tmplbl.bind("<Button-1>", lambda ev: EditSymDialog(self, ev)) #left click
        
        self.imgID += 1

        idea = False
        if inidea == True or (inidea == None and self.idea_var.get() == 1):
            idea = True
        if self.project != None:
            curr = Code(timestamp/1000000000.0, text, store_speakers, idea)
            self.project.seq.insert(curr)
        self.imgMap[self.imgID-1] = timestamp/1000000000.0
    
    def update_display(self):
            self.display.image_create('1.0', image=self.imagemap['blank'])
            while True:
                if self.play["text"] == "Pause":
                    try:
                        timestamp = self.player.query_position(gst.FORMAT_TIME, None)[0]
                        self.display.mark_set("mine2", "1.%d" % floor(timestamp/1000000000.0/.2))
                        self.display.see("1.%d" % (floor(timestamp/1000000000.0/.2)+8))
                        self.display.see("mine2")
                        self.display.config(state=NORMAL)
                        for i in range(int(floor(timestamp/1000000000.0/.2))+10 - int(self.display.index('1.end').split('.')[1])):
                            self.display.image_create('1.end', image=self.imagemap['blank'])
                        self.display.config(state=DISABLED)
                        time.sleep(.2)
                    except:
                        continue
                else:
                    time.sleep(.2)
                


    def initUI(self):
        self.parent.title("Main")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(15, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(10, pad=7)
        
        def hello():
            print "hello!"

        #Menubar--------------------------------------------------------------
        menubar = Tkinter.Menu(self)
        
        filemenu = Tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=lambda: NewProjectDialog(self))
        filemenu.add_command(label="Open", command=lambda: OldProjectDialog(self))
        filemenu.add_command(label="Save", command=lambda: self.project.saveProject())
        filemenu.add_command(label="Save As", command=lambda: SaveAsDialog(self, self.project))
        filemenu.add_command(label="Save and Export Image", command=lambda: self.project.saveAndExportImage())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.parent.quit)
        menubar.add_cascade(label="File", menu=filemenu)
       
        
        #Create analysis window here
        #def do_popup_analysis():
        #    new_frame = Tkinter.Tk()
            
        #menubar.add_command(label="Analysis", command=do_popup_analysis)

        #def do_popup_plot():
        #    new_frame = Tkinter.Tk()
            
        #menubar.add_command(label="Plot", command=do_popup_plot)
        
            
        menubar.add_command(label="Help", command=lambda: helpDialog(self))
        
        self.parent.config(menu=menubar)
        #Menubar done----------------------------------------------------------
    
    
        #Choose Project part---------------------------------------------------
        self.box = Frame(self)
        self.box.grid(row=0, column=0, columnspan=8, rowspan=4, padx=2)
        btn = Button(self.box, text="New Project", command=lambda: NewProjectDialog(self), default=ACTIVE)
        btn.grid(row=0, column=0, columnspan = 4, rowspan=4, padx=2)
        btn2 = Button(self.box, text="Open Project", command=lambda: OldProjectDialog(self), default=ACTIVE)
        btn2.grid(row=0, column=4, columnspan = 4, rowspan=4,padx=2)
        #Project done----------------------------------------------------------

        #Display of symbols
        self.display = Text(self, height=4, wrap=NONE)
        self.display.grid(row=7, column=0, rowspan=3, columnspan=3, sticky=E+W)
        
        
        #scrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.display.xview) #remove seekbar
        #scrollbar.grid(row=10,column=0, columnspan=3, sticky=N+S+E+W)
        #self.display['xscrollcommand'] = scrollbar.set
        
        #Adding time dependent display
        self.t = threading.Thread(target=self.update_display)
        self.t.daemon = True
        self.t.start()
        #Display done
       
        #Slider
        self.slider = Scale(self, orient=HORIZONTAL, variable = self.var)
        self.slider.grid(row=6, column=0, columnspan=3, sticky=N+S+E+W)
        #Done with slider

        #Buttons for symbols----------------------------------------------------
        buttongrid = Frame(self)
        self.buttongrid = buttongrid
        buttongrid.grid(row=0, column=8, rowspan=10, columnspan=5)


    #Topic implementation    
        self.idea_var = IntVar()
        self.topic_var = IntVar()
        idea = Checkbutton(buttongrid, text="Idea", variable=self.idea_var, onvalue = 1, offvalue = 0, indicatoron=0, height=2, width=16)
        idea.grid(row=11, column=0, columnspan=2)
        self.buttonmap['\r'] = idea
        
        def delTopic(event):
            line = self.topic_display.index(CURRENT).split(".")[0]
            self.topic_display.config(state=NORMAL)
            self.topic_display.delete(""+line+".0", ""+str(int(line)+1)+".0")
            self.topic_display.config(state=DISABLED)
        topic = Checkbutton(buttongrid, text="Topic", variable=self.topic_var, onvalue = 1, offvalue = 0, indicatoron=0, width=16, height=2)
        topic.grid(row=11, column=2, columnspan=2)
        topic_indicator = Label(buttongrid, width=33, height=2, bg="gray")
        topic_indicator.grid(row=10, column=0, columnspan=4)
        self.topic_change_var = 0
        self.topic_display = Text(buttongrid, wrap=NONE, state=DISABLED)
        self.topic_display.grid(row=15, column=0, columnspan=4, sticky=N+S+W)
        self.topic_display.configure(height=10, width=36)
        self.topic_display.bind("<Button-3>", delTopic)

        scrollbar2 = Scrollbar(buttongrid, orient=VERTICAL, command=self.topic_display.yview)
        scrollbar2.grid(row=15,column=3, sticky=N+S+E)
        self.display['yscrollcommand'] = scrollbar2.set
        
        self.topics = []
        def change_color():
            self.topic_change_var = self.topic_change_var %4
            col_map = {0 : "red", 1 : "blue", 2 : "green", 3 : "yellow"}
            if self.topic_var.get():
                #Get timestamp
                self.timest = pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
                topic_indicator.configure(bg=col_map[self.topic_change_var])
                self.topic_change_var += 1
            else:
                self.topic_display.config(state=NORMAL)
                topic_col = col_map[(self.topic_change_var-1)%4]
                self.topic_display.tag_config(str(self.topic_change_var), background=topic_col)
                insert = bisect_right(self.topics, self.timest/1000000000.0)
                self.topics.insert(insert, self.timest/1000000000.0)
                self.topic_display.insert("%d.0" % (insert+1), str(self.timest/1000000000.0)+"-"+str(self.player.query_position(gst.FORMAT_TIME, None)[0]/1000000000.0)+"\n", (str(self.timest/1000000000.0), str(self.topic_change_var)))
                self.topic_display.see("%d.0" % (insert+1))
                topic_indicator.configure(bg="gray")
                self.topic_display.config(state=DISABLED)
        
        topic.configure(command=change_color)
        #topic.bind("<Shift_L>", change_color())
        
        
        #def update_topInd(): #TODO: change colors on playback
        #    while True:
        #        if self.play["text"] == "Pause":
        #            try:
        #                timestamp = self.player.query_position(gst.FORMAT_TIME, None)[0]/1000000000.0
        #                insert = bisect_right(self.topics, timestamp)
        #                if insert > 0 and float(self.topic_display.get("%d.0" % (insert), "%d.end" % (insert)).split('-')[1]) >= timestamp:
        #                    #topic_indicator.configure(bg= #get color in self.topic_display at line insert
        #                    pass
        #                time.sleep(.1)
        #            except:
        #                continue
        #        else:
        #            time.sleep(.2)
        #self.tt = threading.Thread(target=update_topInd)
        #self.tt.daemon = True
        #self.tt.start()
        
    #Done with topic

        
        h = '44'
        w = '40'
        c = "top"
        codemap = {
            'a':'yesandquestion',
            's':'interrupt',
            'd':'block',
            'f':'overcoming',
            'q':'move',
            'w':'question',
            'e':'support',
            'r':'yesand',
            'z':'deflection',
            'x':'humour',
            'c':'block-support',
            'v':'hesitation',
        }
        firstrow = 12
        b1 = Button(buttongrid, image=self.imagemap[codemap['a']], command=lambda: self.update_symbols(codemap['a']), background="white", height=h, width=w, compound=c, text="A")
        b1.image = self.imagemap[codemap['a']]
        b1.grid(row=firstrow, column=0)
        self.buttonmap['a'] = b1
        
        b2 = Button(buttongrid, image=self.imagemap[codemap['s']], command=lambda: self.update_symbols(codemap['s']), background="white", height=h, width=w, compound=c, text="S")
        b2.image = self.imagemap[codemap['s']]
        b2.grid(row=firstrow, column=1)
        self.buttonmap['s'] = b2
        
        b3 = Button(buttongrid, image=self.imagemap[codemap['d']], command=lambda: self.update_symbols(codemap['d']), background="white", height=h, width=w, compound=c, text="D")
        b3.image = self.imagemap[codemap['d']]
        b3.grid(row=firstrow, column=2)
        self.buttonmap['d'] = b3
        
        b4 = Button(buttongrid, image=self.imagemap[codemap['f']], command=lambda: self.update_symbols(codemap['f']), background="white", height=h, width=w, compound=c, text="F")
        b4.image = self.imagemap[codemap['f']]
        b4.grid(row=firstrow, column=3)
        self.buttonmap['f'] = b4
        
        b5 = Button(buttongrid, image=self.imagemap[codemap['q']], command=lambda: self.update_symbols(codemap['q']), background="white", height=h, width=w, compound=c, text="Q")
        b5.image = self.imagemap[codemap['q']]
        b5.grid(row=firstrow+1, column=0)
        self.buttonmap['q'] = b5
        
        b6 = Button(buttongrid, image=self.imagemap[codemap['w']], command=lambda: self.update_symbols(codemap['w']), background="white", height=h, width=w, compound=c, text="W")
        b6.image = self.imagemap[codemap['w']]
        b6.grid(row=firstrow+1, column=1)
        self.buttonmap['w'] = b6
        
        b7 = Button(buttongrid, image=self.imagemap[codemap['e']], command=lambda: self.update_symbols(codemap['e']), background="white", height=h, width=w, compound=c, text="E")
        b7.image = self.imagemap[codemap['e']]
        b7.grid(row=firstrow+1, column=2)
        self.buttonmap['e'] = b7
        
        b8 = Button(buttongrid, image=self.imagemap[codemap['r']], command=lambda: self.update_symbols(codemap['r']), background="white", height=h, width=w, compound=c, text="R", font=100)
        b8.image = self.imagemap[codemap['r']]
        b8.grid(row=firstrow+1, column=3)
        self.buttonmap['r'] = b8
        
        b9 = Button(buttongrid, image=self.imagemap[codemap['z']], command=lambda: self.update_symbols(codemap['z']), background="white", height=h, width=w, compound=c, text="Z")
        b9.image = self.imagemap[codemap['z']]
        b9.grid(row=firstrow+2, column=0)
        self.buttonmap['z'] = b9
        
        b10 = Button(buttongrid, image=self.imagemap[codemap['x']], command=lambda: self.update_symbols(codemap['x']), background="white", height=h, width=w, compound=c, text="X", font=100)
        b10.image = self.imagemap[codemap['x']]
        b10.grid(row=firstrow+2, column=1)
        self.buttonmap['x'] = b10
        
        b11 = Button(buttongrid, image=self.imagemap[codemap['c']], command=lambda: self.update_symbols(codemap['c']), background="white", height=h, width=w, compound=c, text="C", font=100)
        b11.image = self.imagemap[codemap['c']]
        b11.grid(row=firstrow+2, column=2)
        self.buttonmap['c'] = b11
        
        b12 = Button(buttongrid, image=self.imagemap[codemap['v']], command=lambda: self.update_symbols(codemap['v']), background="white", height=h, width=w, compound=c, text="V", font=100)
        b12.image = self.imagemap[codemap['v']]
        b12.grid(row=firstrow+2, column=3)
        self.buttonmap['v'] = b12
        

        #def undo():
        #    val = self.num_inserted[-1]
        #    for i in range(val):
        #        self.display.delete("end-2c")
        #    self.display.see(END)
        #    del self.num_inserted[-1]
        #    self.project.seq.undo()
        
        #undo = Button(buttongrid, text="Undo", command=undo, background="white")
        #undo.grid(row=6, column=6)
        #Buttons done---------------------------------------------------------

def main():
  
    root = Tk()
    root.geometry("1110x600+0+100") 
    app = Mainframe(root)
    KeyboardInput(app, root)
    root.mainloop()  

if __name__ == '__main__':
    main()

