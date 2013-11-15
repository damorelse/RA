from abc import ABCMeta, abstractmethod
import Tkinter as tkinter
from Tkinter import *
from math import floor

class Input(object):
    __metaclass__ = ABCMeta
        
    @abstractmethod
    def getMode(self):
        pass
    @abstractmethod
    def checkForInput(self):
        pass
        
    @staticmethod
    def code(type):
        curr = Code(self.project.video.getTime(), type)
        self.project.seq.insert(curr)
        
    @staticmethod
    def idea(curr):
        self.project.seq.ideaExpression(curr, self.project.video.getTime())
        
    @staticmethod
    def topic(curr):
        self.project.seq.newTopic(curr, self.project.video.getTime())
        
    @staticmethod
    def speaker(curr, id):
        self.project.seq.setSpeaker(curr, self.project.video.getTime(), id)
        
    @staticmethod
    def undo():
        self.project.seq.undo()
        
    @staticmethod
    def delete(curr):
        self.project.seq.delete(curr, self.project.video.getTime())
        
    @staticmethod
    def vidPlayPause():
        self.project.video.vidPlayPause()
        
    @staticmethod
    def vidSpeedUp(change):
        self.project.video.vidSpeed(change)
        
    @staticmethod
    def vidSpeedDown(change):
        self.project.video.vidSpeed(-1*change)
        
    @staticmethod
    def vidCaption():
        self.project.video.vidCaption()
        
    @staticmethod
    def showScreenKeys():
        pass #TODO
        
    @staticmethod
    def newProject():
        pass #TODO
        
    @staticmethod
    def saveProject():
        self.project.saveProject()
        
    @staticmethod
    def outputCode():
        self.project.outputCode()
    
class MouseInput(Input):
    def __init__(self, frame, project):
        self.project = project
        self.frame = frame
        frame.bind("<ButtonRelease-1>", self.callback)
        
    def getMode(self):
        return "mouse click"
    def checkForInput(self):
        ev = self.event
        #TODO get button origins
    def callback(self, event):
        print "clicked at", event.x, event.y
        self.event = event
        self.checkForInput()
        
class KeyboardInput(Input):
    def __init__(self, frame, project):
        self.project = project
        self.frame = frame
        frame.bind("<Key>", self.key)
        self.codemap = { #TODO
            'u':'support',
            'i':'interruption',
            'o':'yesand',
            'p':'deviation',
            'j':'move',
            'k':'question',
            'l':'block',
            ';':'overcomeblock',
            'n':'humor',
            'm':'hesitation',
            ',':'acceptblock',
            '.':''
        }
        self.vidSpeedChange = 1
            
    def getMode():
        return "keyboard"
    def checkForInput(self):
        ev = self.event
        echar = ev.char;
        esym = ev.keysym;
        if echar != '':
            if echar in self.codemap: #code
                super(KeyboardInput,  self).code(None, self.codemap[echar])
            elif echar == '\r': #enter
                super(KeyboardInput, self).idea(None)
            elif ord(echar)-ord('0') >= 0 and ord(echar)-ord('0')< 10: #number
                super(KeyboardInput, self).speaker(None, ord(echar)-ord('0'))
            elif echar == '\x1a': #Ctrl-Z
                super(KeyboardInput, self).undo()
            elif echar == '\x08': #backspace
                super(KeyboardInput, self).delete(None)
            elif echar == ' ': #spacebar
                super(KeyboardInput, self).vidPlayPause()
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
                super(KeyboardInput, self).topic()
    def key(self, event):
        print "pressed", repr(event.char), repr(event.keysym)
        self.event = event
        self.checkForInput()
   
class Timestamp:
    def __init__(self, seconds):
        self.time = seconds

class Code:
    def __init__(self, time, symbol):
        Code(self, time, symbol, -1, False, False, '', '')
    def __init__(self, time, symbol, speaker, idea, topic, topicname, sidenotes):
        self.time = time
        self.symbol = symbol
        self.speaker = speaker
        self.idea = idea
        self.topic = topic
        self.tname = topicname
        self.sidenotes = sidenotes
        
class Sequence:
    timestep = 10.0
    bound = 2.5
    INSERT = 'insert'
    DELETE = 'delete'
    UPDATE = 'update'
    
    def __init__(self):
        self.seqIndex = [[]] #list of lists of Code
        self.changeType = '' #updated every time a function is called
        self.changeCode = '' #updated every time a function is called
        
    def getClosestCode(self, time):
        index = floor(time.time/Sequence.timestep)
        subindex = 0
        while (subindex < len(self.seqIndex[index])) and (self.seqIndex[index][subindex].time < time):
            ++subindex
        if len(self.seqIndex[index]) == 0: #if bucket empty
            if index != 0 and len(self.seqIndex[index-1])>0: #check prev bucket
                if time - self.seqIndex[index-1][len(self.seqIndex[index-1])-1].time < bound:
                    return self.seqIndex[index-1][len(self.seqIndex[index-1])-1]
            if index != len(self.seqIndex)-1 and len(self.seqIndex[index+1])>0: #check next bucket
                if self.seqIndex[index+1][0].time - time < bound:
                    return self.seqIndex[index+1][0]
            return None     
        elif subindex == 0: #if first in bucket
            if index != 0 and len(self.seqIndex[index-1])>0:
                if time - self.seqIndex[index-1][len(self.seqIndex[index-1])-1].time < self.seqIndex[index][subindex].time - time:
                    if time - self.seqIndex[index-1][len(self.seqIndex[index-1])-1].time < bound:
                        return self.seqIndex[index-1][len(self.seqIndex[index-1])-1]
            if self.seqIndex[index][subindex].time - time < bound:
                return self.seqIndex[index][subindex]
            return None     
        elif subindex == len(self.seqIndex[index]): #if last in bucket
            if index != len(self.seqIndex[index])-1 and len(self.seqIndex[index+1])>0:
                if self.seqIndex[index+1][0]-time < time - self.seqIndex[index][subindex-1]:
                    if self.seqIndex[index+1][0]-time < bound:
                        return self.seqIndex[index+1][0]
            if time - self.seqIndex [index][subindex-1].time < bound:
                return self.seqIndex [index][subindex-1];
            return None
        elif time - self.seqIndex[index][subindex-1].time < self.seqIndex[index][subindex].time - time: #in bucket, if prev closer than next
            if time - self.seqIndex[index][subindex-1].time < bound:
                return self.seqIndex[index][subindex-1]
        else: #in bucket, if next closer than prev
            if self.seqIndex[index][subindex].time - time < bound:
                return self.seqIndex[index][subindex]
        return None
        
    def insert(self, newcode):
        self.changeType = INSERT
        self.changeCode = newcode
        index = floor(time.time/Sequence.timestep)
        if index > len(self.seqIndex):
            for i in range(len(self.seqIndex) - index):
                self.seqIndex.append([])
        subtime = time.time - floor(time.time/Sequence.timestep)
        subindex = 0
        while (subindex < len(self.seqIndex[index])) and (self.seqIndex[index][subindex].time < subtime):
            ++subindex
        self.seqIndex[index].insert(subindex, newcode)
        
    def delete(self, curr, time):
        self.changeType = DELETE
        self.changeCode = curr
        if curr is None:
            curr = getClosestCode(time)
        index = floor(curr.time/Sequence.timestep)
        seqIndex[index].remove(curr)
        
    def undo(self):
        if self.changeType == DELETE:
            self.insert(self.changeCode)
            self.changeType = INSERT
        elif self.changeType == INSERT:
            self.delete(self.changeCode)
            self.changeType = DELETE
        elif self.changeType == UPDATE:
            index = floor(time.time/Sequence.timestep)
            subindex = seqIndex[index].index(self.changeCode)
            tmp = self.changeCode
            self.changeCode = seqIndex[index][subindex]
            seqIndex[index][subindex] = tmp

    def ideaExpression(self, curr, time):
        changeType = UPDATE
        changeCode = curr
        if curr is None:
            curr = getClosestCode(time)
        curr.idea = True
        
    def newTopic(self, curr, time, tname):
        changeType = UPDATE
        changeCode = curr
        if curr is None:
            curr = getClosestCode(time)
        curr.topic = True
        curr.tname = tname
        
    def setSpeaker(self, curr, time, speaker):
        changeType = UPDATE
        changeCode = curr
        if curr is None:
            curr = getClosestCode(time)
        curr.speaker = speaker
        
    def editTime(self, curr, time):
        changeType = UPDATE
        changeCode = curr
        if curr is None:
            curr = getClosestCode(time)
        curr.time = time
        self.delete(curr, -1)
        self.insert(curr)
            
class Project:
    def __init__(self, name, vidpath, logpath, numSpeakers):
        self.projectName = name
        self.videoPath = vidpath
        self.logFilePath = logpath
        self.numSpeaker = numSpeakers
        self.speakerID = {1:''}
        self.seq = Sequence()
        self.video = Video(vidpath)

    def saveProject(self):
        pass #TODO
    def outputCode(self):
        pass #TODO

class Video:
    def __init__(self, vidpath):
        self.speed = 1.0
        self.captionOn = True
        self.play = False
        self.currTime = 0.0
    
    def updateTime(self, time):
        selfTime = time
        #TODO
    def vidPlayPause(self):
        self.play = not self.play
        #TODO
    def vidSpeed(self, change):
        self.speed += change
        #TODO
    def vidCaption(self):
        self.captionOn = not self.captionOn
        #TODO
    def getTime(self):
        return self.currTime #TODO
        
class DisplayBar:
    def synchVideo(self):
        pass #TODO
        
def main():  
    root = Tk()
    root.geometry("350x300+300+300")
    p = Project('test', 'blah', '', 2)
    KeyboardInput(root, p)
    MouseInput(root, p)
    root.mainloop()  

if __name__ == '__main__':
    main()