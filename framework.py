from Tkinter import Tk, Text, BOTH, W, N, E, S
from ttk import Frame, Button, Label, Style
import os
import sys
import gobject
import gst
import Tkinter as tkinter

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def on_sync_message(self, bus, message, window_id):
        if not message.structure is None:
            if message.structure.get_name() == 'prepare-xwindow-id':
                image_sink = message.src
                image_sink.set_property('force-aspect-ratio', True)
                image_sink.set_xwindow_id(window_id)

    def initUI(self):
      
        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(7, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(7, pad=7)
        
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
        video.grid(row=0, column=0, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)
        window_id = video.winfo_id()
 
        player = gst.element_factory_make('playbin2', 'player')
        player.set_property('video-sink', None)
        player.set_property('uri', 'file://%s' % (os.path.abspath(sys.argv[1])))
        

        def pause_video():
            player.set_state(gst.STATE_READY)
            player.set_state(gst.STATE_PAUSED)

        def play_video():
            player.set_state(gst.STATE_PLAYING)

        pause = Button(self, text="Pause", command=pause_video)
        pause.grid(row=5,column=0)

        play = Button(self, text="Play", command=play_video)
        play.grid(row=5,column=1)


        #player.set_state(gst.STATE_PLAYING)

        bus = player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('sync-message::element', self.on_sync_message, window_id)
        #Video embedding done---------------------------------------------------

        #Display of symbols
        disp = tkinter.StringVar()
        display = Label(self, textvariable=disp)
        display.grid(row=6, column=0, rowspan=2, columnspan=3, sticky=E+W)
        #Display done

        
        #Buttons for symbols----------------------------------------------------
        
        buttongrid = Frame(self)
        buttongrid.grid(row=0, column=3, rowspan=5, columnspan=4)
        
        def update_symbols(text):
            disp.set(disp.get()+text)

        idea = Button(buttongrid, text="Idea")
        idea.grid(row=0, column=3, columnspan=2)

        topic = Button(buttongrid, text="Topic")
        topic.grid(row=0, column=5, columnspan=2)

        b1 = Button(buttongrid, text="Move", command=lambda: update_symbols("Move "))
        b1.grid(row=1, column=3)

        b2 = Button(buttongrid, text="Block", command=lambda: update_symbols("Block "))
        b2.grid(row=1, column=4)

        b3 = Button(buttongrid, text="Deflect", command=lambda: update_symbols("Deflect "))
        b3.grid(row=1, column=5)

        b4 = Button(buttongrid, text="Interrupt", command=lambda: update_symbols("Interrupt "))
        b4.grid(row=1, column=6)

        b5 = Button(buttongrid, text="Humour", command=lambda: update_symbols("Humour "))
        b5.grid(row=2, column=3)

        b6 = Button(buttongrid, text="Question", command=lambda: update_symbols("Question "))
        b6.grid(row=2, column=4)

        b7 = Button(buttongrid, text="Hesistation", command=lambda: update_symbols("Hesitation "))
        b7.grid(row=2, column=5)

        b8 = Button(buttongrid, text="Support", command=lambda: update_symbols("Support "))
        b8.grid(row=2, column=6)

        b9 = Button(buttongrid, text="Overcoming", command=lambda: update_symbols("Overcoming "))
        b9.grid(row=3, column=3)

        b10 = Button(buttongrid, text="Yes and", command=lambda: update_symbols("Yes and "))
        b10.grid(row=3, column=4)

        b11 = Button(buttongrid, text="Deviation", command=lambda: update_symbols("Deviation "))
        b11.grid(row=3, column=5)

        b12 = Button(buttongrid, text="", command=lambda: update_symbols(""))
        b12.grid(row=3, column=6)
        #Buttons done---------------------------------------------------------

def main():
  
    root = Tk()
    root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()  

if __name__ == '__main__':
    main()

