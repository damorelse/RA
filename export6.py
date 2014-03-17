from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT

filename = 'default.log'

class Symbol:
    def __init__(self, timestamp, code, speakers, idea):
        self.timestamp = timestamp
        self.code = code
        self.speakers = speakers
        self.idea = idea
        self.speaker_map = {'1':'A', '2':'B', '3':'C', '4': 'D', '5':'E', '6':'F', '7':'G', '8': 'H', '9':'I'}

    def get_image(self):
        im = Image('./symbols/'+self.code+'.gif')
        speakers = ""
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Style_no_idea', fontName ='Helvetica',fontSize=14, textColor=colors.black, alignment=TA_LEFT))
        styles.add(ParagraphStyle(name='Style_idea', fontName ='Helvetica',fontSize=14, textColor=colors.black, backColor=colors.yellow, alignment=TA_LEFT))
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
            ret_tab = Table(image, style=[('BACKGROUND', (0,0), (0,0), colors.yellow)])
        else:
            ret_tab = Table(image)
        ret_speakers = Table(res_speakers)
        return ret_tab, ret_speakers

def parse_file(filename):
    f = open(filename)
    data = f.readlines()
    num_speakers = int(data[2])
    start = 2 + num_speakers + 3

    result1 = []
    result2 = []
    timestamps = []
    flag = 0

    for i in range(start, len(data)):
        code_det = data[i].split('\t')
        if flag == 1:
            flag = 0
            continue
        
        speakers = code_det[2][1:-1].split(',')
        s = Symbol(code_det[0], code_det[1], speakers, code_det[3])
        
        if code_det[1]=="block" and i<len(data)-1:
            next_code = data[i+1].split('\t')
            if next_code[1] == "deflection":
                s = Symbol(code_det[0], "block-deflection", speakers, code_det[3])
                flag = 1

        code, speakers = s.get_image()
        #ts = Table([code_det[0]])

        timestamps.append(code_det[0])
        result1.append(code)
        result2.append(speakers)
    #print timestamps
    return result1, result2, timestamps

def create_file(code, speakers, timestamps, filename):
    doc = SimpleDocTemplate(filename+".pdf")
    story = []
    t = []
    s = []
    if len(timestamps) !=0:
        data = [[timestamps[0], "", "", "", "", ""]]
        story.append(Table(data, hAlign='LEFT'))

    for i in range(len(code)):
        if i%6 == 0 and i!=0:
            if len(t)!=0:
                story.append(Table([t], hAlign='LEFT'))
                story.append(Table([s], hAlign='LEFT'))
                data = [[timestamps[i], "", "", "", "", ""]]
                story.append(Table(data, hAlign='LEFT'))
                print timestamps[i]
                t = []
                s = []
                t.append(code[i])
                s.append(speakers[i])
        else:
            t.append(code[i])
            s.append(speakers[i])
    if len(code)%6 != 0:
        for i in range(6-len(code)%6):
            t.append("")
            s.append("")
    if len(t)!=0:
        story.append(Table([t]))
        story.append(Table([s]))

    doc.build(story)

