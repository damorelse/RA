import Tkinter as tkinter
from Tkinter import *
from math import floor
from export8 import *
  
class Code:
    """ Represents one code symbol

    Attributes:
        time : A float of the video timestamp in seconds.
        symbol: A string indicating the symbol type (e.g. question, support, yesand etc).
        speaker: A list of positive integers indicating speakers.
        idea: A boolean indicating if symbol expresses an idea.
        topic: A boolean indicating if symbol expresses a topic change.
        topicname : A string (deprecated). 
        sidenotes : A string (deprecated). 

    """
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
    """ Represents a coded sequence of symbols

    Attributes:
        timestep : A float representing the time indexing step in seconds. Index = floor(timestamp / timestep)
        INSERT : A string representing change type insert.
        DELETE : A string representing change type delete.
        UPDATE : A string representing change type update.
        seqIndex : A map of index to Code representing the coded sequence.
        changeType : A string representing type of last change (INSERT, DELETE, or UPDATE). (deprecated)
        self.changeCode : A copy of the last changed Code before the change. (deprecated)
    """
    timestep = 0.2
    INSERT = 'insert'
    DELETE = 'delete'
    UPDATE = 'update'
    
    def __init__(self, inSeq = None):
        self.seqIndex = {} #map of Code
        if inSeq != None:
            self.seqIndex = inSeq
            self.changeType = '' #updated every time a function is called
            self.changeCode = '' #updated every time a function is called

    def getClosestCode(self, time):
        """ Given timestamp in seconds, returns Code object at index if it exists.
        """
        for code in self.seqIndex[int(floor(time/Sequence.timestep))]:
            if code.time == time:
                return code

    def insert(self, newcode):
        """ Given Code object, inserts into sequence.
        """
        self.changeType = self.INSERT
        self.changeCode = newcode
        index = int(floor(newcode.time/Sequence.timestep))
        if index not in self.seqIndex.keys():
            self.seqIndex[index] = [newcode]
            return
        self.seqIndex[index].append(newcode)
        self.seqIndex[index] = sorted(self.seqIndex[index], key=lambda x: x.time)

    def delete(self, curr, time):
        """ Given Code object or timestamp, will delete object at index.
        """
        self.changeType = self.DELETE
        self.changeCode = curr
        if curr is None:
            curr = self.getClosestCode(time)
        index = int(floor(curr.time/Sequence.timestep))
        self.seqIndex[index].remove(curr)
        
    def undo(self):
        """ Undo last Code object change.
        """
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
        """ Change Code object to express an idea.
        """
        changeType = self.UPDATE
        changeCode = curr
        if curr is None:
            curr = self.getClosestCode(time)
        curr.idea = True
        
    def newTopic(self, curr, time, tname):
        """ Change Code object to express a change in topic. 
        """
        changeType = self.UPDATE
        changeCode = curr
        if curr is None:
            curr = self.getClosestCode(time)
        curr.topic = True
        curr.tname = tname
        
    def setSpeaker(self, curr, time, speaker):
        """ Change Code object's speakers.
        """
        changeType = self.UPDATE
        changeCode = curr
        if curr is None:
            curr = self.getClosestCode(time)
        curr.speaker = speaker
        
    def editTime(self, curr, time):
        """ Change Code object's time.
        """
        changeType = self.UPDATE
        changeCode = curr
        if curr is None:
            curr = self.getClosestCode(time)
        curr.time = time
        self.delete(curr, -1)
        self.insert(curr)
            
class Project:
    """ Represent a project with one coding sequence.

    Attributes:
        projectName : A string representing the project specific name and saved session file (<name>.log).
        videoPath : A string representing the absolute path to the video file.
        logFilePath : A string representing the absolute path to the directory containing the log file (do not end in '/').
        numSpeakers : An integer indicating the number of speakers.
        speakerID : A map of integers to strings, mapping speaker number (1-based) to speaker notes.
        seq : A Sequence object representing the coded symbols.
    """
    def __init__(self, name, vidpath, logpath, numSpeakers, sID = None, inseq = None, intop = None):
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
        self.topics = {}
        if intop != None:
            self.topics = intop

    def saveProject(self):
        self.outputCode()
    def saveAsProject(self, newName):
        temp = self.projectName
        self.projectName = newName[newName.rfind('/')+1:-4]
        self.outputCode(newName)
        self.projectName = temp
    def saveAndExportImage(self):
        """ Outputs sequence to file then outputs visual code sequence.
        """
        self.outputCode()
        code, speakers, timestamps, topics = parse_file(self.logFilePath+'/'+self.projectName+'.log')
        create_topicfile(code, speakers, timestamps, topics, self.projectName)
    def outputCode(self, newFile = None):
        """ Helper function, outputs sequence to file.
        """
        if newFile == None:
            log = open(self.logFilePath+'/'+self.projectName+'.log', 'w+')
        else:
            log = open(newFile, 'w+')
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
        
        log.write("\n")
        for start in sorted(self.topics.keys()):
            log.write(str(start)+"\t"+str(self.topics[start])+"\n")
             

