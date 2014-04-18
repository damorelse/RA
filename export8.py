"""
This program contains the classes and functions required for converting a text-log file into pdf with appropriate display
Uses library reportlab (dependencies - freetype, imaging)
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT

filename = 'default.log'


"""
Class symbol represents an idn symbol

Members : 
    timestamp                 : timestamp of corresponding symbol
    code (eg: move, deflect)  : string
    speakers                  : list
    is_idea                   : boolean
    speaker_map               : dictionary from speaker number to speaker names 
 
Functions : 
    init                      : initialize members with given parameters
    get_image                 : returns the image for the idn symbol and speakers in the form accepted by the reportlab library
"""
class Symbol:
    def __init__(self, timestamp, code, speakers, idea):
        self.timestamp = timestamp
        self.code = code
        self.speakers = speakers
        self.idea = idea
        self.speaker_map = {'1':'A', '2':'B', '3':'C', '4': 'D', '5':'E', '6':'F', '7':'G', '8': 'H', '9':'I'}
        
    """
    Creates 2 styles    - idea     : yellow background
                        - not idea : without yellow background
    Return Value:
    ret_tab             - table with the image for idn symbol
    ret_speakers        - table with the speakers corresponding to the symbol
    """
    def get_image(self):
        im = Image('./output/'+self.code+'.gif')
        speakers = ""
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Style_no_idea', fontName ='Helvetica',fontSize=14, textColor=colors.black, alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Style_idea', fontName ='Helvetica',fontSize=14, textColor=colors.black, backColor=colors.yellow, alignment=TA_CENTER))
        t = []
        t.append(im)
        for s in self.speakers:
            if len(s)>0:
                speakers += self.speaker_map[s.strip()]
        res_speakers = []

        if self.idea == "True":
            res_speakers.append(Paragraph(speakers, styles["Style_idea"]))
        else:
            res_speakers.append(Paragraph(speakers, styles["Style_no_idea"]))
        
        image = [t]
        res_speakers = [res_speakers]
        if self.idea == "True":
            ret_tab = Table(image, style=[('BACKGROUND', (0,0), (0,0), colors.orange)])
        else:
            ret_tab = Table(image)
        ret_speakers = Table(res_speakers)
        return ret_tab, ret_speakers

"""
Input       : log file
Output      : Lists of idn symbols, speakers, timestamps

 - Parses the log file and builds the symbol objects for every idn code in the log file.
 - Converts "block followed by deflection" to a single "block-deflection" image
 - Maintain 3 lists : code, speakers, timestamps
 - Return the 3 lists
"""
def parse_file(filename):
    f = open(filename)
    data = f.readlines()
    num_speakers = int(data[2])
    start = 2 + num_speakers + 3

    result1 = []
    result2 = []
    timestamps = []
    topics = []
    flag = 0

    for i in range(start, len(data)):
        if len(data[i]) == 1:
            start = i+1
            break
        code_det = data[i].split('\t')
        if flag == 1:
            flag = 0
            continue
        
        speakers = code_det[2][1:-1].split(',')
        s = Symbol(code_det[0], code_det[1], speakers, code_det[3])
        if code_det[1]=="block" and i<len(data)-1:
            next_code = data[i+1].split('\t')
            if next_code[1] == "deflection":
                s = Symbol(code_det[0], "deviation", speakers, code_det[3])
                flag = 1

        code, speakers = s.get_image()
        #ts = Table([code_det[0]])

        timestamps.append(code_det[0])
        result1.append(code)
        result2.append(speakers)
        
    for i in range(start, len(data)):
        code_det = data[i].split('\t')
        topics.append([code_det[0], code_det[1]])
    #print timestamps
    return result1, result2, timestamps, topics

"""
Input       : Result of parsing the log file - code, speakers, timestamps and name of file to be created
Output      : Pdf output of the idn code with given filename

 - Arrange the symbols as 10 in a row
 - Speakers are displayed below the symbols
 - Timestamp is displayed at the start of every row
"""
def create_file(code, speakers, timestamps, topics, filename):
    doc = SimpleDocTemplate(filename+".pdf", pagesize=(1000,1000))
    story = []
    t = []
    s = []
    count = 10
    if len(timestamps) !=0:
        data = [[timestamps[0], "", "", "", "", "", ""]]
        story.append(Table(data, hAlign='LEFT'))

    for i in range(len(code)):
        if i%count == 0 and i!=0:
            if len(t)!=0:
                story.append(Table([t], hAlign='LEFT'))
                story.append(Table([s], hAlign='LEFT'))
                data = [[timestamps[i], "", "", "", "", "", ""]]
                story.append(Table(data, hAlign='LEFT'))
                t = []
                s = []
                t.append(code[i])
                s.append(speakers[i])
        else:
            t.append(code[i])
            s.append(speakers[i])
    if len(code)%count != 0:
        for i in range(count-len(code)%count):
            t.append("")
            s.append("")
    if len(t)!=0:
        story.append(Table([t]))
        story.append(Table([s]))

    doc.build(story)


"""
Input       : Result of parsing the log file - code, speakers, timestamps and name of file to be created
Output      : Pdf output of the idn code with given filename

 - Arrange the symbols of a topic in a row
 - Speakers are displayed below the symbols
 - Timestamp is displayed at the start of every row
"""
def create_topicfile(code, speakers, timestamps, topics, filename):
    line = 0
    i = 0
    prevend = 0
    mytopics = [[]]
    myspeakers = [[]]
    mytimestamps = []
    for start,end in topics:
        currtime = [timestamps[i],timestamps[i]]
        for curr in range(i, len(timestamps)):
            if timestamps[i] >= prevend and timestamps[i] < start:
                mytopics[line].append(code[i])
                myspeakers[line].append(speakers[i])
                currtime[1] = timestamps[i]
                i += 1
        mytimestamps.append(currtime)
        mytopics.append([])
        myspeakers.append([])
        line += 1
        mytimestamps.append([start, end])
        for curr in range(i, len(timestamps)):
            if timestamps[i] < end and timestamps[i] >= start:
                mytopics[line].append(code[i])
                myspeakers[line].append(speakers[i])
                i+= 1
        mytopics.append([])
        myspeakers.append([])
        line += 1
        prevend = end
    currtime = [timestamps[i],timestamps[i]]
    for curr in range(i, len(timestamps)):
        mytopics[line].append(code[i])
        myspeakers[line].append(speakers[i])
        currtime[1] = timestamps[i]
        i += 1
    mytimestamps.append(currtime)
    
    max = 0
    for tlist in mytopics:
        if len(tlist) > max:
            max = len(tlist)
            
    doc = SimpleDocTemplate(filename+".pdf", pagesize=(100*max,140*len(mytopics)))
    story = []
    i = 0

    for k in range(len(mytopics)):
        if len(mytopics[k]) == 0:
            continue
            
        #beginning timestamp
        data = [[mytimestamps[k][0]]]
        for i in range(max-1):
            data[0].append("")
        story.append(Table(data, hAlign='LEFT'))

        
        #topic code
        t = mytopics[k]
        s = myspeakers[k]
        for i in range(max-len(mytopics[k])):
            t.append("")
            s.append("")

        story.append(Table([t], hAlign='LEFT'))
        story.append(Table([s], hAlign='LEFT'))
        
        #ending timestamp
        data = [[mytimestamps[k][1]]]
        for i in range(max-1):
           data[0].append("")
        story.append(Table(data, hAlign='LEFT'))
         
    doc.build(story)
