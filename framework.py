from Tkinter import Tk, Text, BOTH, W, N, E, S
from ttk import Frame, Button, Label, Style
import os
import sys
import gobject
import gst
import Tkinter as tkinter
import threading

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.lock = threading.Lock() 
        self.parent = parent
        self.NUM_SPEAKERS = 5       
        self.initUI()
        self.num_inserted = []

    def on_sync_message(self, bus, message, window_id):
        print "sync message"
        if not message.structure is None:
            if message.structure.get_name() == 'prepare-xwindow-id':
                image_sink = message.src
                image_sink.set_property('force-aspect-ratio', True)
                self.lock.acquire()
                image_sink.set_xwindow_id(window_id)
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

    def initUI(self):
      
        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(15, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(9, pad=7)
        
        def hello():
            print "hello!"

        #Menubar--------------------------------------------------------------
        menubar = tkinter.Menu(self)
        
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=hello)
        filemenu.add_command(label="Open", command=hello)
        filemenu.add_command(label="Save", command=hello)
        filemenu.add_command(label="Save As", command=hello)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.parent.quit)
        menubar.add_cascade(label="File", menu=filemenu)
       
        editmenu = tkinter.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Copy", command=hello)
        editmenu.add_command(label="Paste", command=hello)
        editmenu.add_command(label="SelectAll", command=hello)
        editmenu.add_command(label="Undo", command=hello)
        editmenu.add_command(label="Redo", command=hello)
        menubar.add_cascade(label="Edit", menu=editmenu)
        
        #Create analysis window here
        def do_popup_analysis():
            new_frame = Tk()
            
        menubar.add_command(label="Analysis", command=do_popup_analysis)

        def do_popup_plot():
            new_frame = Tk()
            
        menubar.add_command(label="Plot", command=do_popup_plot)
        menubar.add_command(label="Help", command=hello)

        self.parent.config(menu=menubar)
        #Menubar done----------------------------------------------------------

        #Video embedding part--------------------------------------------------
        gobject.threads_init()
        video = Frame(self)
        video.grid(row=0, column=0, columnspan=8, rowspan=4, 
            padx=2, sticky=E+W+S+N)
        window_id = video.winfo_id()
 
        
        self.buf = gst.Buffer()


        self.bin = gst.Bin("my-bin")
        timeoverlay = gst.element_factory_make("timeoverlay", "overlay")
        self.bin.add(timeoverlay)
        pad = timeoverlay.get_pad("video_sink")
        ghostpad = gst.GhostPad("sink", pad)
        self.bin.add_pad(ghostpad)
        videosink = gst.element_factory_make("autovideosink")
        self.bin.add(videosink)
        gst.element_link_many(timeoverlay, videosink)
        
        self.player = gst.element_factory_make('playbin2', 'player')
        self.player.set_property('video-sink', self.bin)
        self.player.set_property('uri', 'file://%s' % (os.path.abspath(sys.argv[1])))
       
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message, window_id)
        bus.connect('sync-message::element', self.on_sync_message, window_id)


        def play_video():
            if self.play["text"] == "Play":
                self.player.set_state(gst.STATE_PLAYING)
                self.play["text"] = "Pause"
            else:
                self.player.set_state(gst.STATE_PAUSED)
                self.play["text"] = "Play"

        
        self.play = Button(self, text="Play", command=play_video, width=50)
        self.play.grid(row=5,column=0)

        self.entry = tkinter.Entry(self, width=50)
        self.entry.grid(row=5, column=1)

        def play_back():
            pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
            text = self.entry.get()
            diff = 0
            if text=="":
                diff = pos_int - (3*(10**9))
            else:
                val = float(self.entry.get())
                diff = pos_int - (val*(10**9))
            
            if diff>0:
                self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, diff)
            else:
                self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 0)
 

        self.back = Button(self, text="Playback", command=play_back, width=50)
        self.back.grid(row=5, column=2)

        #Video embedding done---------------------------------------------------

        #Display of symbols
        self.display = Text(self, height=2, wrap=tkinter.NONE)
        self.display.grid(row=6, column=0, rowspan=3, columnspan=3, sticky=E+W)

        scrollbar = tkinter.Scrollbar(self, orient=tkinter.HORIZONTAL, command=self.display.xview)
        scrollbar.grid(row=9,column=0, columnspan=3, sticky=N+S+E+W)
        self.display['xscrollcommand'] = scrollbar.set
        #Display done
       
        
        #Buttons for symbols----------------------------------------------------
        buttongrid = Frame(self)
        buttongrid.grid(row=0, column=8, rowspan=7, columnspan=4)

        #Speakers
        alpha = ['A','B','C','D','E','F','G','H','I','J']
        s = []
        self.checkvars = []
        for i in range(self.NUM_SPEAKERS):
            s.append(alpha[i])
            self.checkvars.append(tkinter.IntVar())
        
        i=0
        self.speakers = []
        colors = ["blue", "green", "yellow", "orange", "pink"]
        for text in s:
            if i<3:
                b = tkinter.Checkbutton(buttongrid, text=text, variable=self.checkvars[i], onvalue = 1, offvalue = 0)
                self.speakers.append((b, colors[i]))
                b.grid(row=0, column=(i%3)+3)
            else:
                b = tkinter.Checkbutton(buttongrid, text=text, variable=self.checkvars[i], onvalue = 1, offvalue = 0)
                self.speakers.append((b, colors[i]))
                b.grid(row=1, column=(i%3)+3)
            i += 1
        #Done with speakers



        deflect_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/deflection.gif", height=30, width=50)
        question_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/question.gif", height=30, width=50)
        hesitation_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/hesitation.gif", height=30, width=50)
        interrupt_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/interrupt.gif", height=30, width=50)
        overcoming_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/overcoming.gif", height=30, width=50)
        support_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/support.gif", height=30, width=50)
        yesand_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/yesand.gif", height=30, width=50)
        humour_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/humour.gif", height=30, width=50)
        move_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/move.gif", height=30, width=50)
        block_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/block.gif", height=30, width=50)
        deviation_image = tkinter.PhotoImage(file="/home/aparna/RA/Framework/symbols/deviation.gif", height=30, width=50)

        self.idea_var = tkinter.IntVar()

        def update_symbols(text):
            
            
            #self.display.edit_separator()
            #Stores timestamp
            timestamp = self.player.query_position(gst.FORMAT_TIME, None)[0]
            print timestamp

            #Stores current speakers
            current_speakers = []
            for i in range(len(self.speakers)):
                if self.checkvars[i].get() == 1:
                    current_speakers.append((self.speakers[i][0]['text'], self.speakers[i][1]))

            if text=="deflection":
                self.display.image_create(tkinter.END, image= deflect_image)
            elif text=="question":
                self.display.image_create(tkinter.END, image= question_image)
            elif text=="hesitation":
                self.display.image_create(tkinter.END, image= hesitation_image)
            elif text=="interrupt":
                self.display.image_create(tkinter.END, image= interrupt_image)
            elif text=="overcoming":
                self.display.image_create(tkinter.END, image= overcoming_image)
            elif text=="support":
                self.display.image_create(tkinter.END, image= support_image)
            elif text=="yesand":
                self.display.image_create(tkinter.END, image= yesand_image)
            elif text=="humour":
                self.display.image_create(tkinter.END, image= humour_image)
            elif text=="move":
                self.display.image_create(tkinter.END, image= move_image)
            elif text=="block":
                self.display.image_create(tkinter.END, image= block_image)
            elif text=="deviation":
                self.display.image_create(tkinter.END, image= deviation_image)

            ct= 1
            for sp in current_speakers:
                ct+= 1
                self.display.tag_config(sp[0], foreground=sp[1])
                if self.idea_var.get()==1:
                    self.display.tag_config("is_idea", background="yellow")
                    self.display.insert(tkinter.END, sp[0], (sp[0], "is_idea"))
                else:
                    self.display.tag_config("not_idea", background="white")
                    self.display.insert(tkinter.END, sp[0], (sp[0], "not_idea"))
            self.num_inserted.append(ct)
            self.display.see(tkinter.END)

       
        idea = tkinter.Checkbutton(buttongrid, text="Idea", variable=self.idea_var, onvalue = 1, offvalue = 0, indicatoron=0, width=15, height=1)
        #idea = Button(buttongrid, text="Idea", width=14, command=idea)
        idea.grid(row=2, column=3, columnspan=2)

        topic = tkinter.Button(buttongrid, text="Topic", width=13, height=1)
        topic.grid(row=2, column=5, columnspan=2)

        b1 = Button(buttongrid, image=move_image, command=lambda: update_symbols("move"))
        b1.image = move_image
        b1.grid(row=3, column=3)

        b2 = Button(buttongrid, image=block_image, command=lambda: update_symbols("block"))
        b2.image = block_image
        b2.grid(row=3, column=4)

        b3 = Button(buttongrid, image=deflect_image, command=lambda: update_symbols("deflection"))
        b3.image = deflect_image
        b3.grid(row=3, column=5)

        b4 = Button(buttongrid, image=interrupt_image, command=lambda: update_symbols("interrupt"))
        b4.image = interrupt_image
        b4.grid(row=3, column=6)

        b5 = Button(buttongrid, image=humour_image, command=lambda: update_symbols("humour"))
        b5.image = humour_image
        b5.grid(row=4, column=3)

        b6 = Button(buttongrid, image=question_image, command=lambda: update_symbols("question"))
        b6.image = question_image
        b6.grid(row=4, column=4)

        b7 = Button(buttongrid, image=hesitation_image, command=lambda: update_symbols("hesitation"))
        b7.image = hesitation_image
        b7.grid(row=4, column=5)

        b8 = Button(buttongrid, image=support_image, command=lambda: update_symbols("support"))
        b8.image = support_image
        b8.grid(row=4, column=6)

        b9 = Button(buttongrid, image=overcoming_image, command=lambda: update_symbols("overcoming"))
        b9.image = overcoming_image
        b9.grid(row=5, column=3)

        b10 = Button(buttongrid, image=yesand_image, command=lambda: update_symbols("yesand"))
        b10.image = yesand_image
        b10.grid(row=5, column=4)

        b11 = Button(buttongrid, image=deviation_image, command=lambda: update_symbols("deviation"))
        b11.image = deviation_image
        b11.grid(row=5, column=5)

        def undo():
            val = self.num_inserted[-1]
            for i in range(val):
                self.display.delete("end-2c")
            self.display.see(tkinter.END)
            del self.num_inserted[-1]
        
        undo = tkinter.Button(buttongrid, text="Undo", command=undo, width=5)
        undo.grid(row=5, column=6)
        #Buttons done---------------------------------------------------------

def main():
  
    root = Tk()
    root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()  

if __name__ == '__main__':
    main()

