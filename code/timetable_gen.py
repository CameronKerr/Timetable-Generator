import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from random import randint
    
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

class Timetable:
    '''Timetable class represents all courses the student is taking'''
    
    def __init__(self, courses=list()):
        '''Create new timetable'''
        self.courses = courses
    def return_table(self):
        for course in self.courses:
            course.return_course()

class Course:
    '''Course class represents a course and stores its timetable information'''
    
    def __init__(self, code, semester, lecture, tutorial, practical):
        '''Create new course'''
        self.code = code
        self.semester = semester
        self.lecture = lecture
        self.tutorial = tutorial
        self.practical = practical
    def return_course(self):
        print(self.code + " " + self.semester)
        for lec in self.lecture:
            lec.return_slot()
        if isinstance(self.tutorial, str):
            print(self.tutorial)
        else: 
            self.tutorial.return_slot()
        if isinstance(self.practical, str):
            print(self.practical)
        else:
            self.practical.return_slot()
        
class Timeslot:
    '''Timeslot class represents the information of a certain activity at a certain time'''
    
    def __init__(self, code, semester, activity, day, start, end):
        '''Create new timeslot'''
        self.code = code
        self.semester = semester
        self.activity = activity
        self.day = day
        self.start = start
        self.end = end
    def return_slot(self):
        print(self.activity + " " + self.day + ": " + self.start + " - " + self.end)      

def get_timetable(file):
    timetable = Timetable()
    
    f = open(file, "r")
    html_str = f.read() 
    
    raw_courses = html_str.split("class=\"coursePlan courseBox\"")[1:]
    for raw_course in raw_courses:
        name = raw_course[5:13]
        semester = raw_course.split("\"enrolment-code\">" + name)[1][1]
        raw_times = raw_course.split("class=\"time\"")
        
        if "Online Asynchronous" in raw_times[1]:
            day = "Online Asynchronous"
            lec = Timeslot(name, semester, "Online Asynchronous", NA, NA)
        else:
            lec_by_div = raw_times[1].split("</div>")
            lectures = list()
            for div in lec_by_div:
                for day in DAYS:
                    if day in div:
                        course_day = day
                        day_split = div.split(day)[1].split("\t\t\t")
                        start = day_split[1][0:(day_split[1].index("M")+1)]
                        end = day_split[2][0:(day_split[2].index("M")+1)]
                        lec = Timeslot(name, semester, "LEC", course_day, start, end)
                        lectures.append(lec)
        if "TUT" in raw_course:
            tut_by_line = raw_times[2].split("\n")
            day = tut_by_line[2][3:]
            start = tut_by_line[3][3:(len(tut_by_line[3])-2)]
            end = tut_by_line[4][3:]
            tut = Timeslot(name, semester, "TUT", day, start, end) 
        else:
            tut = "NA"
        if "PRA" in raw_course:
            pra_by_line = raw_times[2].split("\n")
            day = pra_by_line[2][3:]
            start = pra_by_line[3][3:(len(pra_by_line[3])-2)]
            end = pra_by_line[4][3:]
            pra = Timeslot(name, semester, "PRA", day, start, end)
        else:
            pra = "NA"
        course = Course(name, semester, lectures, tut, pra)
        timetable.courses.append(course)
    return timetable
    
def twelve_to_twentyfour(time):
    '''
    Converts time from twelve to twenty four hour
    '''
    is_pm = time[-2] == "P" and time[0:2] != "12"
    is_single = len(time) < 7
    
    if is_pm:
        twentyfour = int(time.split(":")[0]) + 12
    else:
        if is_single:
            twentyfour = int(time[0:1])
        else:
            twentyfour = int(time[0:2])
    if time == "12:00AM":
        twentyfour = 24
    return twentyfour
        
def vis_f_timetable(timetable):
    '''
    Plots fall timetable
    '''    
    color = []
    n = len(timetable.courses)
    for i in range(n):
        color.append('#%06X' % randint(0, 0xFFFFFF))    
    
    fig=plt.figure(figsize=(10,5.89))
    for course_index in range(len(timetable.courses)):
        course = timetable.courses[course_index]
        if course.semester == "F" or course.semester == "Y":
            for lecture in range(len(course.lecture)):
                lec = course.lecture[lecture]
                day_index = DAYS.index(lec.day)
                start = twelve_to_twentyfour(lec.start)
                end = twelve_to_twentyfour(lec.end)
                
                plt.fill_between([day_index, day_index+0.96], [start, start], [end,end], edgecolor='k', color=color[course_index], linewidth=0.5)
                plt.text(day_index+0.48, (start+end)*0.5, course.code + " " + lec.activity, ha='center', va='center', fontsize=11)
                
            if course.tutorial != "NA":
                tut = course.tutorial
                day_index = DAYS.index(tut.day)
                start = twelve_to_twentyfour(tut.start)
                end = twelve_to_twentyfour(tut.end) 
                
                plt.fill_between([day_index, day_index+0.96], [start, start], [end,end], edgecolor='k', color=color[course_index], linewidth=0.5)
                plt.text(day_index+0.48, (start+end)*0.5, course.code + " " + tut.activity, ha='center', va='center', fontsize=11)  
            if course.practical != "NA":
                pra = course.practical
                day_index = DAYS.index(pra.day)
                start = twelve_to_twentyfour(pra.start)
                end = twelve_to_twentyfour(pra.end) 
                
                plt.fill_between([day_index, day_index+0.96], [start, start], [end,end], edgecolor='k', color=color[course_index], linewidth=0.5)
                plt.text(day_index+0.48, (start+end)*0.5, course.code + " " + pra.activity, ha='center', va='center', fontsize=11)                  
            
    ax = fig.gca()
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.savefig('results/fall_timetable.png', dpi=200)

def vis_w_timetable(timetable):
    '''
    Plots winter timetable
    '''    
    color = []
    n = len(timetable.courses)
    for i in range(n):
        color.append('#%06X' % randint(0, 0xFFFFFF))    
    
    fig=plt.figure(figsize=(10,5.89))
    for course_index in range(len(timetable.courses)):
        course = timetable.courses[course_index]
        if course.semester == "S" or course.semester == "Y":
            for lecture in range(len(course.lecture)):
                lec = course.lecture[lecture]
                day_index = DAYS.index(lec.day)
                start = twelve_to_twentyfour(lec.start)
                end = twelve_to_twentyfour(lec.end)
                
                plt.fill_between([day_index, day_index+0.96], [start, start], [end,end], edgecolor='k', color=color[course_index], linewidth=0.5)
                plt.text(day_index+0.48, (start+end)*0.5, course.code + " " + lec.activity, ha='center', va='center', fontsize=11)
                
            if course.tutorial != "NA":
                tut = course.tutorial
                day_index = DAYS.index(tut.day)
                start = twelve_to_twentyfour(tut.start)
                end = twelve_to_twentyfour(tut.end) 
                
                plt.fill_between([day_index, day_index+0.96], [start, start], [end,end], edgecolor='k', color=color[course_index], linewidth=0.5)
                plt.text(day_index+0.48, (start+end)*0.5, course.code + " " + tut.activity, ha='center', va='center', fontsize=11)  
            if course.practical != "NA":
                pra = course.practical
                day_index = DAYS.index(pra.day)
                start = twelve_to_twentyfour(pra.start)
                end = twelve_to_twentyfour(pra.end) 
                
                plt.fill_between([day_index, day_index+0.96], [start, start], [end,end], edgecolor='k', color=color[course_index], linewidth=0.5)
                plt.text(day_index+0.48, (start+end)*0.5, course.code + " " + pra.activity, ha='center', va='center', fontsize=11)                  
            
    ax = fig.gca()
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.savefig('results/winter_timetable.png', dpi=200)

def generate_plot(file_path):
    table = get_timetable(file_path)
    vis_f_timetable(table)
    vis_w_timetable(table)
    
if __name__ == '__main__':
    val = input("Enter the name and path of course file: ")
    generate_plot(val)