# Written by Nikhil Gupta
# Lou's List Parser
# March 23 2015

import requests
import re
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def IsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
def ClassSection(trClassOdd, trClassEven, css):
    return css == trClassOdd or css == trClassEven
    
def get_section_list(string):
    string = string.upper()
    
    #CHANGE SEMESTER
    #semester = 1152 #SPRING 2015
    semester = 1158 #FALL 2015

    courses = string.split(",")
    
    courses = sorted(courses)
    
    prevEnding = ""
    
    course_sections = {}
    
    for course in courses:
        course = course.strip()
      
        splitBySpace = course.split(" ")
        mnemonic = ""
        number = 0
    
        if len(splitBySpace) == 1:
            mnemonic = course[:len(course) - 4] # ex. CS, PHYS, etc.
            number = course[len(course)-4 :] # 2110, 1425, etc.
        else:
            mnemonic = splitBySpace[0]
            number = splitBySpace[1]
        
        url = 'http://rabi.phys.virginia.edu/mySIS/CS2/page.php?Semester=' + str(semester) + '&Type=Course&Mnemonic=' + mnemonic.upper() + '&Number=' + number
        
        try:
            result = requests.get(url)
        except ConnectionError as e:
            return 'ConnectionError'
        
        c = result.content
        soup = BeautifulSoup(c, from_encoding="utf-8")
    
            #classes = soup.findAll("td", {"class":"CourseNum"})
        
 #       prevEnding = ending
        
    
        courseforum = ''
        courseTitle = ''
        
        span = soup.find('td', {'class':'CourseNum'})
        name = soup.find('td', {'class':'CourseName'})
        
        print(span)
        
        if span != None:
            span = span.find('span')
            if span != None:
                courseforum = span['onclick'].split("'")[1] # Gets the course number
        
                print(courseforum)
            #print(courseforum)
        if name != None:
            courseTitle = name.text
        
        section = {}
        section['id'] = 0
        section['section_num'] = ''
        section['type'] = 'None'
        section['credits'] = ''
        section['status'] = 'None'
        section['current_enrollment'] = 0
        section['max_enrollment'] = 0
        section['times'] = []
        section['locations'] = []
        section['instructors'] = []
        section['topic'] = ''
        section['courseforum'] = ''
        section['course_title'] = ''
    
        curId = 0
        curData = 1
    
        nameWithoutSpace = course.replace(' ', '')
        #print(individualName)
        trClassOdd = "SectionOdd S " + nameWithoutSpace
        trClassEven = "SectionEven S " + nameWithoutSpace
        
        course_sections[nameWithoutSpace] = []
        
        rows = []
        for item in soup.findAll(True, {"class": re.compile("^(SectionOdd|SectionEven|SectionTopicOdd|SectionTopicEven)$")}):
            if nameWithoutSpace in item.attrs['class'] or nameWithoutSpace in item.attrs['class']:
                rows.append(item)
                print(item['class'])
        
        #rows = soup.findAll("tr", {'class':[trClassOdd, trClassEven]})
        
        #if curData == 9:
            #print("%d %s %s %s %s %d/%d %s %s %s"%(id, section, type, credits, status, curEnrollment, maxEnrollment, instructor, times, location))
            #print("Reset at 8")
        
        #print(rows)
        
        curData = 1
        
        current_topic = ''
        for row in rows:
            if 'SectionTopicOdd' in row['class'] or 'SectionTopicEven' in row['class']:
                for topic_cell in row.find_all("td"):
                    if topic_cell.text.strip():
                        current_topic = topic_cell.text
                continue
                
            cells = row.find_all("td") # get the individual cells in a row
            
            for cell in cells:
                text = cell.text.replace('Syllabus', '').replace(u'\xa0', '').replace('Website', '')
                
                if not text.strip():
                    continue
                
                #print("%s - %d"%(text, curData))
                if(curData > 8 and (curData - 8)%3 == 1): # Beginning of a new row, either ID or instructor
                    if IsInt(text):
                        if section['type'] != 'None':
                            course_sections[nameWithoutSpace].append(section)
                            
                        curData = 1
                        #sections.append("%d %s %s %s %s %d/%d %s %s %s"%(id, section, type, credits, status, curEnrollment, maxEnrollment, instructor, times, location))
                        section = {}
                        section['id'] = int(text)
                        section['section_num'] = ''
                        section['type'] = 'None'
                        section['credits'] = ''
                        section['status'] = 'None'
                        section['current_enrollment'] = 0
                        section['max_enrollment'] = 0
                        section['times'] = []
                        section['locations'] = []
                        section['instructors'] = []
                        section['topic'] = current_topic
                        section['courseforum'] = courseforum
                        section['course_title'] = courseTitle
                        
                    else:
                        section['instructors'].append(str(text))
                elif(curData > 8 and (curData - 8)%3 == 2): # Time
                    section['times'].append(str(text))
                elif(curData > 8 and (curData - 8)%3 == 0): # Location
                    section['locations'].append(str(text))
                elif(curData == 1 and IsInt(text)):
                    section['id'] = int(text)
                    section['topic'] = current_topic
                    section['courseforum'] = courseforum
                    section['course_title'] = courseTitle
                elif(curData == 2):
                    section['section_num'] = text
                elif(curData == 3):
                    part = text.partition("(")
                    section['type'] = part[0].strip()
                    credits = part[2].replace('(', '').replace(')', '').replace('Units','')
                    print('Credits: ' + credits)
                    if '-' in credits:
                        minCredits = float(credits.partition('-')[0])
                        maxCredits = float(credits.partition('-')[2]) # partition returns separator as element at index 1
                    else:
                        minCredits = float(credits)
                        maxCredits = float(credits)
                    
                    section['credits'] = minCredits
                    
                elif(curData == 4):
                    section['status'] = text
                elif(curData == 5):
                    part = text.partition(" / ")
                    section['current_enrollment'] = int(part[0])
                    section['max_enrollment'] = int(part[2].split(' ')[0])
                elif(curData == 6):
                    section['instructors'].append(str(text.split('+')[0]).encode('utf-8'))
                elif(curData == 7):
                    section['times'].append(str(text).encode('utf-8'))
                elif(curData == 8):
                    section['locations'].append(str(text).encode('utf-8'))
                
                curData += 1
            
            if row == rows[len(rows) - 1]:
                if section['type'] != 'None':
                    course_sections[nameWithoutSpace].append(section)
                section = {}
                section['id'] = 0
                section['section_num'] = ''
                section['type'] = 'None'
                section['credits'] = ''
                section['status'] = 'None'
                section['current_enrollment'] = 0
                section['max_enrollment'] = 0
                section['times'] = []
                section['locations'] = []
                section['instructors'] = []
                section['topic'] = current_topic
                section['courseforum'] = courseforum
                section['course_title'] = courseTitle
                #sections.append("%d %s %s %s %s %d/%d %s %s %s"%(id, section, type, credits, status, curEnrollment, maxEnrollment, instructor, times, location))

    #print course_sections
    return course_sections