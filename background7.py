import Tkinter as tkinter
from Tkinter import *
from math import floor
from export6 import *
  
class Code:
    def __init__(self, time, symbol, speaker=None, idea=None, topic=None, topicname=None, sidenotes=None):
        self.time = time
        self.symbol = symbol
        self.speaker = speaker
        if speaker is None:
            self.speaker = []
        self.idea = idea
        if idea is None:
            self.idea = False
        self.topic = topic
        if topic is None:
            self.topic = False
        self.tname = topicname
        if topicname is None:
            self.tname = ''
        self.sidenotes = sidenotes
        if sidenotes is None:
            self.sidenotes = ''
class Sequence:
    timestep = 0.2
    bound = 2
    INSERT = 'insert'
    DELETE = 'delete'
    UPDATE = 'update'
    
    def __init__(self, inSeq = None):
        self.seqIndex = {} #list of lists of Code
        if inSeq != None:
            self.seqIndex = inSeq
            self.changeType = '' #updated every time a function is called
            self.changeCode = '' #updated every time a function is called

    def getClosestCode(self, time):
        for code in self.seqIndex[int(floor(time/Sequence.timestep))]:
            if code.time == time:
                return code

    def insert(self, newcode):
        self.changeType = self.INSERT
        self.changeCode = newcode
        index = int(floor(newcode.time/Sequence.timestep))
        if index not in self.seqIndex.keys():
            self.seqIndex[index] = [newcode]
            return
        self.seqIndex[index].append(newcode)
        self.seqIndex[index] = sorted(self.seqIndex[index], key=lambda x: x.time)
    def delete(self, curr, time):
        self.changeType = self.DELETE
        self.changeCode = curr
        if curr is None:
            curr = self.getClosestCode(time)
        index = int(floor(curr.time/Sequence.timestep))
        self.seqIndex[index].remove(curr)
        
    def undo(self):
        if self.changeType == self.DELETE:
            self.insert(self.changeCode)
            self.changeType = INSERT
        elif self.changeType == INSERT:
            self.delete(self.changeCode)
            self.changeType = self.DELETE
        elif self.changeType == UPDATE:
            index = floor(time/Sequence.timestep)
            subindex = seqIndex[index].index(self.changeCode)
            tmp = self.changeCode
            self.changeCode = self.seqIndex[index][subindex]
            self.seqIndex[index][subindex] = tmp

    def ideaExpression(self, curr, time):
        changeType = self.UPDATE
        changeCode = curr
        if curr is None:
            curr = self.getClosestCode(time)
        curr.idea = True
        
    def newTopic(self, curr, time, tname):
        changeType = self.UPDATE
        changeCode = curr
        if curr is None:
            curr = self.getClosestCode(time)
        curr.topic = True
        curr.tname = tname
        
    def setSpeaker(self, curr, time, speaker):
        changeType = self.UPDATE
        changeCode = curr
        if curr is None:
            curr = self.getClosestCode(time)
        curr.speaker = speaker
        
    def editTime(self, curr, time):
        changeType = self.UPDATE
        changeCode = curr
        if curr is None:
            curr = self.getClosestCode(time)
        curr.time = time
        self.delete(curr, -1)
        self.insert(curr)
            
class Project:
    def __init__(self, name, vidpath, logpath, numSpeakers, sID = None, inseq = None):
        self.projectName = name
        self.videoPath = vidpath
        self.logFilePath = logpath
        self.numSpeaker = numSpeakers
        self.speakerID = {}
        for i in range(numSpeakers):
            self.speakerID[i+1] = str(i+1)
        if sID != None:
            self.speakerID = sID.copy()
        self.seq = Sequence()
        if inseq != None:
             self.seq = inseq

    def saveProject(self):
        self.outputCode()
    def saveAsProject(self, newName):
        temp = self.projectName
        self.projectName = newName
        self.outputCode()
        self.projectName = temp
    def saveAndExportImage(self):
        self.outputCode()
        code, speakers, timestamps = parse_file(self.projectName+'.log')
        create_file(code, speakers, timestamps, self.projectName)
    def outputCode(self, newFile = None):
        log = open(self.logFilePath+'/'+self.projectName+'.log', 'w')
        log.write(self.projectName+"\n")
        log.write(self.videoPath+"\n")
        log.write(str(self.numSpeaker)+"\n")
        for key,value in self.speakerID.iteritems():
            log.write(str(key)+"\t"+value+"\n")
        log.write(str(self.seq.timestep)+"\n")
        log.write("\n")
        for bucket in sorted(self.seq.seqIndex.keys()):
            for code in self.seq.seqIndex[bucket]:
                log.write(str(code.time)+"\t"+code.symbol+"\t"+str(code.speaker)+"\t"+str(code.idea)+"\t"+str(code.topic)+"\t"+code.tname+"\t"+code.sidenotes+"\n")
                


def main():  
    root = Tk()
    root.geometry("350x300+300+300")
    p = Project('test', 'blah', '', 2)
    KeyboardInput(root, p)
    MouseInput(root, p)
    root.mainloop()  

if __name__ == '__main__':
    main()
