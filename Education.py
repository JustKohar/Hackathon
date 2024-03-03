# bot.py
import os

import discord
from dataclasses import dataclass
from discord.ext import commands
from dotenv import load_dotenv
from bakery_canvas import get_courses
from bakery_canvas import get_submissions
import matplotlib.pyplot as plt
from datetime import datetime
import asyncio
import requests


load_dotenv(override=True)
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv('GUILD')    

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="~", intents=intents)
intents.typing = False
intents.presences = False
user_token = os.getenv("user_token")


class DiscordBotInformation:
    def __init__(self, class_name, professors, professors_hours, location_of_professors, emails, ta_hours):
        self.class_name = class_name
        self.professors = professors
        self.professors_hours = professors_hours
        self.location_of_professors = location_of_professors
        self.emails = emails
        self.ta_hours = ta_hours

def generate_formatted_message(info: DiscordBotInformation) -> str:
    formatted_message = f"**{info.class_name}**\n\n" \
                        f"**Professors Names**:\n{info.professors}\n\n" \
                        f"**Professors Office Hours**:\n{info.professors_hours}\n\n" \
                        f"**Teachers Locations**:\n{info.location_of_professors}\n\n" \
                        f"**Teachers Emails**:\n{info.emails}\n\n" \
                        f"**TA Hours**:\n{info.ta_hours}"
    return formatted_message

CISC181 = DiscordBotInformation(
    class_name="CISC181",
    professors="The Professors Names are Dr/Professor Bart and Professor Silber!",
    professors_hours="Dr/Professor Bart has Office Hours on Tuesday From 2:30pm-3:30pm\n"
                     "Professor Silber Has Office Hours on Friday from 11:30am-12:30pm",
    location_of_professors="Dr/Professor Bart is Located in Smith411 and Professor Silber is Located in Smith 413",
    emails="Dr/Professor Barts Email: acbart+cisc181@udel.edu\n"
           "Professor Silbers Email: silber@udel.edu",
    ta_hours="On Monday: 9-11am, 11:30am-1:30pm, 1:45pm-2:45pm, 3-5:30pm\n"
             "Tuesday: 10-2pm, 2:10-3:10pm, 4-5pm\n"
             "Wednesday: 9-12pm, 12:30-5pm\n"
             "Thursday: 11-3:15pm, 4-6pm\n"
             "Friday: 8-10am, 10:10-1:30pm, 1:45-2:45pm, 3-5pm, 5:30-7:30pm"
)
MUSC315 = DiscordBotInformation(
    class_name = "MUSC315",
    professors= "The Professor For This Course is Dr. Maria Anne Purciello",
    professors_hours= "Dr. Purciello Has Open Office Hours on Mondays and Wednesdays from 2-3pm",
    location_of_professors="317 Amy E. du Pont Music Building",
    emails="Dr. Purciello's Email Is: 'mpuriel@udel.edu",
    ta_hours= "N/A"
)
MUED337 = DiscordBotInformation(
    class_name = "MUED337",
    professors= "The Professor For This Course is Dr. Lauren Reynolds",
    professors_hours= "By Appointment",
    location_of_professors="AED 309",
    emails="Dr. Lauren Reynolds's Email Is: lhr@udel.edu",
    ta_hours= "N/A"
)
LING101 = DiscordBotInformation(
    class_name = "LING101",
    professors= "The Professor For This Course is Professor Nadya Pinus",
    professors_hours= "Professor Nadya Pinus Has Open Office Hours on Mondays from 3-4pm and Thursday from 10-11am and By Appoinement",
    location_of_professors="Linguistics & Cog. Sci Office Room 117",
    emails="Professor Nadya Pinus's Email Is: npincus@udel.edu",
    ta_hours="On Monday: 12-1pm\n"
             "Tuesday: 10-11am\n"
             "Wednesday: 11:30am-1pm\n"
             "Friday: 11:30am-12:30pm"
)

PHYS227 = DiscordBotInformation(
    class_name = "PHYS227",
    professors= "The Professor For This Course is Dr. John D Shaw",
    professors_hours= "Dr. John D Shaw Has Open Office Hours on Mondays/Tuesday/Thursday from 1-2pm **BUT ARE SUBJECT TO CHANGE!**",
    location_of_professors="Sharp Lab 210",
    emails="Dr. John D Shaw's Email Is: jdshaw@udel.edu",
    ta_hours="TA Hours Vary Since there Are So Many Labs. However the Physics Help Center is Open from Monday/Tuesday/Wednesday/Thursday from 11am-7pm and Friday from 11am-3pm in Sharp Lab 101"
)

CHEM120 = DiscordBotInformation(
    class_name = "CHEM120",
    professors= "The Professor For This Course is Professor Thomas P Beebe Jr",
    professors_hours= "Professor Thomas P Beebe Jr Has Online Office Hours on Tuesday/Thursday from 11:10am-12:30pm, the Zoom Link is https://udel.zoom.us/j/92941838443",
    location_of_professors="Not Listed",
    emails="Professor Thomas P Beebe Jr Email Is: UDChem120@udel.edu",
    ta_hours="TA Hours Vary Since there Are So Many Chem Classes. However the Chemistry Resource Center is Open from Monday through Friday from 8am-8pm in BRL 208"
)

PHYS207 = DiscordBotInformation(
    class_name = "PHYS207",
    professors= "The Professor For This Course is Dr. Olga Narvos",
    professors_hours= "Dr. Olga Narvos Has Office Hours on Monday from 1:45-2:40pm, Tuesday and Friday from 10:30-11:30am",
    location_of_professors="Sharp Lab 208",
    emails="Dr. Olga Narvos Email Is: onarvos@udel.edu",
    ta_hours="TA Hours Vary Since there Are So Many Physic Classes. However the Physics Help Center is Open from Monday/Tuesday/Wednesday/Thursday from 11am-7pm and Friday from 11am-3pm in Sharp Lab 101"
)

EDUC400 = DiscordBotInformation(
    class_name = "EDUC400",
    professors= "There are Many Teachers for This Course but The Supervisors are, Dr. Mark Adams (Instrumental Music), Dr. Duane Cottrell (Choral Music), and Aimee Pearsall (General Music)",
    professors_hours= "There is No Office Hours Provided",
    location_of_professors="N/A",
    emails="Dr. Mark Adams Email Is: adamsm@udel.edu, Dr. Duane Cottrell Email Is: dco@udel.edu, and Aimee Pearsall Email Is: apearsall@udel.edu ",
    ta_hours="There are no TA Hours Listed but Julia Grossman is a Graduate TA. Her Email Is: jngross@udel.edu"
)

CIEG161 = DiscordBotInformation(
    class_name = "CIEG161",
    professors= "There are Many Teachers for This Course but The Instructors are, Dr. Allen Jayne (Structure), Dr. Tian-Jian (Tom) (Coastal and Ocean), and Dr. Jack Puleo (Coastal and Ocean)",
    professors_hours= "Dr. Allen Jayne Has Office Hours on Monday from 9:30-10:30am and on Thursday from 12:30-1:30pm",
    location_of_professors="Dr. Allen Jayne is Located in 307 DuPont Hall, Dr. Tian-Jian is Located in 205 Ocean Engineering Lab, and Dr. Jack Puleo is Located in 301 DuPont Hall",
    emails="Dr. Allen Jayne Email Is: ajayne@udel.edu, Dr. Tian-Jian Email Is: thsu@udel.edu, and Dr. Jack Puleo Email Is: jpuleo@udel.edu",
    ta_hours="There are no TA's/TA Hours Listed"
)

HIST104 = DiscordBotInformation(
    class_name = "HIST104",
    professors= "The Professor For This Course is Professor Benjamin Tomak ",
    professors_hours= "Professor Benjamin Tomak Has Office Hours on Tuesday/Thursday from 12:45-2:05pm",
    location_of_professors="Professor Benjamin Tomak is Located in Gore 304",
    emails="Professor Benjamin Tomak's Email Is: btomak@udel.edu",
    ta_hours="There are no TA's/TA Hours Listed"
)

MATH243 = DiscordBotInformation(
    class_name = "MATH243",
    professors= "The Professor For This Course is Dr. Cristina Bacuta ",
    professors_hours= "Dr. Cristina Bacuta Has Office Hours on Monday from 3-4:30pm and Wednesdays from 8:15-9:45am",
    location_of_professors="Dr. Cristina Bacuta is Located in Erwing 305",
    emails="Dr. Cristina Bacuta's Email Is: crbacuta@udel.edu",
    ta_hours="Since TA's Vary in Class Schedules, Ask TA for Hours"
)

COMM212 = DiscordBotInformation(
    class_name = "COMM212",
    professors= "The Professor For This Course is Dr. Alan Fox",
    professors_hours= "Dr. Alan Fox Has Office Hours on Tuesday/Thursday from 1-2pm",
    location_of_professors="Not Provided",
    emails="Dr. Alan Fox's Email Is: afox@udel.edu",
    ta_hours="Dr. Alan Fox has 'Writing Fellows'. Brandon Cangialosi and His Email Is: bcangial@udel.edu and Isabella Haigney Who's Email Is: ihaigney@udel.edu"
)

MATH351 = DiscordBotInformation(
    class_name = "MATH351",
    professors= "The Professor For This Course is Professor Shuya Yu",
    professors_hours= "Professor Shuya Yu Has Office Hours on Monday//Wednesday/Friday from 12-1pm",
    location_of_professors="Professor Shuya Yu is Located in Erwing 108",
    emails="Professor Shuya Yu's Email Is: shuyayu@udel.edu",
    ta_hours="No TA's Listed, Ask in Discussion"
)

CIEG315 = DiscordBotInformation(
    class_name = "CIEG315",
    professors= "The Professor For This Course is Dr. Mark Nejad",
    professors_hours= "Dr. Mark Nejad Has Office Hours on Tuesday/Thursday from 11am-12pm",
    location_of_professors="Dr. Mark Nejad is Located in 352-B DuPont Hall",
    emails="Dr. Mark Nejad's Email Is: shuyayu@udel.edu",
    ta_hours="Farshad Hesamfar, His Email Is: farshaad@udel.edu and His Office Hours are Monday/Wednesday from 4-6pm in 306K DuPont Hall"
)

CISC210 = DiscordBotInformation(
    class_name = "CISC210",
    professors= "The Professor For This Course is Professor Roosen",
    professors_hours= "Professor Roosen Has Office Hours on Monday from 10:30am-12pm and Thursday from 1:30-3pm",
    location_of_professors="Professor Roosen is Located in Smith 407",
    emails="Professor Roosen's Email Is: roosen@udel.edu",
    ta_hours="On Monday: 11:30am-12:30pm, 12:45pm-4:30pm\n"
             "Tuesday: 8:30-10:55am, 11:10am-2pm, 3:30-5:30pm\n"
             "Wednesday: 9:10-11:30am, 12:40-4pm, 4:15-5:15pm\n"
             "Thursday: 9:35-10:55am, 11:10-3pm, 3:55-6pm\n"
             "Friday: 9-10am, 10:15am-2:30pm, 5-7pm"
)

CPEG202 = DiscordBotInformation(
    class_name = "CPEG202",
    professors= "The Professor For This Course is Professor Nathan Lazarus",
    professors_hours= "Professor Nathan Lazarus Has Office Hours on Thursday from 2:40-3:40pm",
    location_of_professors="Professor Nathan Lazarus is Located in EVN201H",
    emails="Professor Nathan Lazarus's Email Is: nlazarus@udel.edu",
    ta_hours="There Are Only TA Hours on Monday from 11am-7pm"
)

ENGL110SeminarInComposition = DiscordBotInformation(
    class_name = "Seminar In Composition",
    professors= "The Professor For This Course is Professor Amelia Chaney",
    professors_hours= "Professor Amelia Chaney Has Office Hours Wednesday from 9-11am and 1-2pm on Zoom https://udel.zoom.us/j/96538994287",
    location_of_professors="Professor Amelia Chaney is Located in 047 Memorial Hall (available in person by appointment)",
    emails="Professor Amelia Chaney's Email Is: achaney@udel.edu",
    ta_hours="There are No TA's Provided"
)

HIST137 = DiscordBotInformation(
    class_name = "HIST137",
    professors= "The Professor For This Course is Dr. Dotno D. Pount",
    professors_hours= "Dr. Dotno D. Pount Has Office Hours Wednesday from 9-10am on Zoom https://upenn.zoom.us/j/4102686688",
    location_of_professors="This Class is Asynchronous",
    emails="Dr. Dotno D. Pount's Email Is: dpount@udel.edu",
    ta_hours="There are No TA's Provided"
)

MATH242 = DiscordBotInformation(
    class_name = "MATH242",
    professors= "The Professor For This Course is Dr. Kim Daewa",
    professors_hours= "Dr. Kim Daewa Has Office Hours on Monday/Wednesday/Friday From 11am-12pm",
    location_of_professors="Dr. Kim Daewa is Located in Erwing 306",
    emails="Dr. Kim Daewa's Email Is: daewakim@udel.edu",
    ta_hours="Emmanuel Adebayo Is The TA and His Email Is: adebayo@udel.edu and His Office Hours are Monday/Wednesday/Friday from 10-11am Located in Erwing 212"
)

MUSC462 = DiscordBotInformation(
    class_name = "MUSC462",
    professors= "The Professor For This Course is Dr. Aimee Persall",
    professors_hours= "Dr. Aimee Pearsall Does Not Hold Office Hours For This Class",
    location_of_professors="Dr. Aimee Persall is Located Amy E. Dupont Music Building, Room 313",
    emails="Dr. Aimee Persall's Email Is: apearsall@udel.edu",
    ta_hours="The TA for This Course is Katelyn Viszoki, Who Can be Reached At: kmviszok@udel.edu in Erwing 212"
)

CISC181 = generate_formatted_message(CISC181)
MUSC315 = generate_formatted_message(MUSC315)
MUED337 = generate_formatted_message(MUED337)
LING101 = generate_formatted_message(LING101)
PHYS227 = generate_formatted_message(PHYS227)
CHEM120 = generate_formatted_message(CHEM120)
PHYS207 = generate_formatted_message(PHYS207)
EDUC400 = generate_formatted_message(EDUC400)
CIEG161 = generate_formatted_message(CIEG161)
HIST104 = generate_formatted_message(HIST104)
MATH243 = generate_formatted_message(MATH243)
COMM212 = generate_formatted_message(COMM212)
MATH351 = generate_formatted_message(MATH351)
CIEG315 = generate_formatted_message(CIEG315)
CISC210 = generate_formatted_message(CISC210)
CPEG202 = generate_formatted_message(CPEG202)
ENGL110SeminarInComposition = generate_formatted_message(ENGL110SeminarInComposition)
HIST137 = generate_formatted_message(HIST137)
MATH242 = generate_formatted_message(MATH242)
MUSC462 = generate_formatted_message(MUSC462)


async def predict_grades(ctx, user_token: str, course_id: int): 
    """
    consumes a user_token (a string) and a course_id (an integer) 
    and returns nothing but creates a graph with three running sums
    """
    total_weighted = 0
    submissions = get_submissions(user_token, course_id)
    max_score = []
    min_score = []
    max_points = []
    score = 0 
    score1 = 0 
    score2 = 0 
    for submission in submissions: 
        total_weighted += (submission.assignment.points_possible*submission.assignment.group.weight)/100
    for submission in submissions: 
        if submission.score == 0:
            max_points.append((score + (submission.assignment.points_possible * submission.assignment.group.weight)/total_weighted))
            min_score.append((score1 + (submission.score * submission.assignment.group.weight)/total_weighted))
            max_score.append((score2 + (submission.assignment.points_possible * submission.assignment.group.weight)/total_weighted))
            score += ((submission.assignment.points_possible * submission.assignment.group.weight)/total_weighted)
            score1 += ((submission.score * submission.assignment.group.weight)/total_weighted)
            score2 += ((submission.assignment.points_possible * submission.assignment.group.weight)/total_weighted)
        else: 
            max_points.append((score + (submission.assignment.points_possible * submission.assignment.group.weight)/total_weighted))
            min_score.append((score1 + (submission.score * submission.assignment.group.weight)/total_weighted))
            max_score.append((score2 + (submission.score * submission.assignment.group.weight)/total_weighted))
            score += ((submission.assignment.points_possible * submission.assignment.group.weight)/total_weighted)
            score1 += ((submission.score * submission.assignment.group.weight)/total_weighted)
            score2 += ((submission.score * submission.assignment.group.weight)/total_weighted)
            
    plt.plot(max_points)
    plt.plot(max_score)
    plt.plot(min_score)
    plt.grid()
    plt.ylabel("Scores")
    plt.xlabel("Assignment")
    plt.title("Min, Max, and Possible Score Graph")
    plt.show()
    plt.savefig("grades_graph.png")
    plt.close()    

def plot_points(user_token: str, course_id: int): 
    """
     consumes a user_token (a string) and a course_id (an integer) and returns nothing,
     but creates a graph comparing the points possible for each assignment with the weighted points possible for that assignment.
     """
    x_data = []
    y_data = []   
    submissions = get_submissions(user_token, course_id)
    total_weighted = 0
    for submission in submissions: 
         total_weighted += ((submission.assignment.points_possible * submission.assignment.group.weight)/100)   
    for submission in submissions: 
        x_data.append(submission.assignment.points_possible)
    for submisison in submissions:
        if total_weighted == 0:
            return 
    for submission in submissions:
        weighted = (submission.assignment.points_possible * submission.assignment.group.weight)/total_weighted
        y_data.append(weighted)
    plt.scatter(x_data, y_data) 
    plt.xlabel("Points Possible")
    plt.ylabel("Weighted Points Possible")
    plt.title("Points Possible V. Weighted Points Possible")
    plt.show()

def days_apart(first_date: str, second_date: str) -> int:
    """
    Determines the days between `first` and `second` date.
    Do not modify this function!
    """
    first_date = datetime.strptime(first_date, "%Y-%m-%dT%H:%M:%S%z")
    second_date = datetime.strptime(second_date, "%Y-%m-%dT%H:%M:%S%z")
    difference = second_date - first_date
    return difference.days

def plot_earliness(user_token: str, course_id: int):
    """
    consumes a user_token (a string) and a course_id (an integer) and returns nothing,
    but creates a graph representing the distribution of the lateness of each submission.
    """
    graph_data = []
    submissions = get_submissions(user_token, course_id)
    for submission in submissions: 
        if submission.submitted_at:
            if submission.assignment.due_at:
                graph_data.append(days_apart(submission.submitted_at, submission.assignment.due_at))
    plt.hist(graph_data)
    plt.xlabel("days late")
    plt.ylabel("frequency")
    plt.title("Fraction Grade Distribution")
    plt.show()

def plot_scores(user_token: str, course_id: int):
    """
    consumes a user_token (a string) and a course_id (an integer) 
    and returns nothing but creates a graph representing the distribution of the fractional scores in the course
    """
    graph_data = []
    submissions = get_submissions(user_token, course_id)
    for submission in submissions:
        if submission.status == "graded":
            if submission.assignment.group.weight >= 0:
                 graph_data.append((submission.score/submission.assignment.points_possible)*100)
    plt.hist(graph_data)
    plt.xlabel("fractional grade")
    plt.ylabel("frequency")
    plt.title("Fraction Grade Distribution")
    plt.show()

def render_all(user_token: str, course_id: int) -> str:
    """
    consumes a user_token (a string) and a course_id (an integer), 
    and produces a single string that describes all of the submissions in the course.
    """
    submission_descriptions = ""
    submissions = get_submissions(user_token, course_id) 
    for submission in submissions:
        if submission.status == "graded":
            submission_descriptions += str(submission.assignment.id) + ":" + " " + submission.assignment.name + " " + "(graded)" + "\n"
        else: 
            submission_descriptions += str(submission.assignment.id) + ":" + " " + submission.assignment.name + " " + "(ungraded)" + "\n"
    return submission_descriptions    

def render_assignment(user_token: str, course_id: int, assignment_id: int)-> str:
    """
    consumes a user_token (a string), a course_id (an integer), and an assignment_id (an integer). 
    The function produces a string representing the assignment and its submission details.
    If the assignment cannot be found in the user's submissions, 
    then return the string "Assignment missing: " followed by the assignment_id.
    """
    correct_submission = []
    submissions = get_submissions(user_token, course_id) 
    for submission in submissions: 
        if submission.assignment.id == assignment_id:
            correct_submission.append(submission)
    if not correct_submission:
        return "Assignment missing: " + str(assignment_id)
    for submission in correct_submission:
        line1 = str(assignment_id) + ":" + " " + submission.assignment.name
        line2 = "Group: " + submission.assignment.group.name
        line3 = "Module: " + submission.assignment.module
        line4 = "Grade: (missing)"
        if submission.status == "graded":
            line4 = "Grade: " + str(submission.score) + "/" + str(submission.assignment.points_possible) + " " + "(" + submission.grade + ")"
            return line1 + "\n" + line2 + "\n" + line3 + "\n" + line4
        return line1 + "\n" + line2 + "\n" + line3 + "\n" + line4


def average_group(user_token: str, course_id: int, group_name: str)-> float:
    """
    consumes a user_token (a string), a course_id (an integer), and a group_name (a string). 
    The function returns a float representing the average, 
    unweighted grade ratio for all the graded submissions with that group_name.
    """
    total_points = 0.0
    possible_points = 0.0
    submissions = get_submissions(user_token, course_id)
    for submission in submissions:
        if submission.status == 'graded':
            if submission.assignment.group.name.lower() == group_name.lower():
                total_points += submission.score
                possible_points += submission.assignment.points_possible
    if total_points == 0.0:
        if possible_points == 0.0:
            return 0.0
    return total_points/possible_points

def average_weighted(user_token: str, course_id: int) -> float:
    """
    consumes a user_token (a string) and a course_id (an integer), 
    and produces a float representing the average, weighted score of all the graded assignments in the course.
    """
    total_points = 0.0
    possible_points = 0.0
    submissions = get_submissions(user_token, course_id)
    for submission in submissions:
        if submission.status == 'graded':
            total_points += (submission.score * submission.assignment.group.weight)
            possible_points += (submission.assignment.points_possible * submission.assignment.group.weight)
    return total_points/possible_points

def average_score(user_token: str, course_id:int) -> float:
    """
    consumes a user_token (a string) and a course_id (an integer), 
    and produces a float representing the average, unweighted score of all the graded assignments in the course.
    """
    total_points = 0.0
    possible_points = 0.0
    submissions = get_submissions(user_token, course_id)
    for submission in submissions:
        if submission.status == 'graded':
            total_points += submission.score
            possible_points += submission.assignment.points_possible
    return total_points/possible_points

def ratio_graded(user_token: str, course_id: int) -> str:
    """
    consumes a user_token (a string) and a course_id (an integer), 
    and produces a string value representing the number of assignments that have been graded,
    compared to the number of total assignments in the course
    """
    graded = 0 
    total = 0 
    submissions = get_submissions(user_token, course_id)
    for submission in submissions:
        total += 1 
        if submission.status == "graded":
            graded += 1
    return str(graded) + "/" + str(total)

def count_comments(user_token: str, course_id: int) -> int:
    """
    consumes a user_token (a string) and a course_id (an integer), 
    and produces an integer representing the number of comments across all the submissions for that course.
    """
    count = 0
    submissions = get_submissions(user_token, course_id)
    for submission in submissions:
        for comment in submission.comments:
            count += 1
    return count

def total_points(user_token: str, course_id: int) -> int:
    """
    consumes a user_token (a string) and a course_id (an integer), 
    and produces an integer representing the total number of points possible in the course 
    """
    total = 0
    submissions = get_submissions(user_token, course_id)
    for submission in submissions:
        total += submission.assignment.points_possible
    return total

def count_courses(user_token: str) -> int:
    """
    from a user token, this function counts the number of courses the user is taking
    """
    return len(get_courses(user_token))

def find_cs1(user_token: str)-> int:
    """
    this function consumes a user token and returns the course ID of a CISC1 course if found.
    if not found, the function returns 0
    """
    for courses in get_courses(user_token):
            if courses.code == "CISC1":
                return courses.id
    return 0


def find_course(user_token: str, course_id: int)-> str:
    """
    this course gets a list of courses from a user token, 
    then tries to find the course the user is taking that 
    matches the course_id input, and if found the function 
    returns the name of that course.
    else "no course" is returned
    """
    for courses in get_courses(user_token):
        if courses.id == course_id:
            return courses.name
    return "no course"
def render_courses(user_token: str)-> str:
    """
    this function consumes a user token and returns a string
    of all their courses and their course Ids with each being 
    its own seperate line
    """
    new = []
    for courses in get_courses(user_token):
        a = ""
        b = courses.code
        c = str(courses.id)
        a = c + ":" + " " + b + "\n"
        new.append(a)
    apple = ""
    for course in new:
        apple = apple + course
    return apple 

bot.command(name = "Run!")
async def execute(ctx):
    
    def execute(command: str, user_token: str, course_id: int)-> int:
        """
        this function does a variety of things based upon the command.
    
        if the command is course, the function will return the new course and course ID
    
        if the command is exit, the function closes
    
        if the command is points, the function prints the total points available for all assignments
    
        if the command is comments, the function runs count_comments on the current course_id and prints the result
    
        if the command is graded, the function prints the result of calling ratio_graded on the function
    
        if the command is score_unweighted, the function prints the result of calling average_score for the current course id 
    
        if the command is score, the fucntion prints the result of calling average_weighted for the current course_id 
    
        if the command is group, the fucntion prints the average of a group by:
        Prompting the user for a group name
        Calling the average_group function
        Printing the result
    
        if the command is assignment, the function prints out the assignment details by:
        Prompting the user for an assignment ID
        Converting the result to an integer
        Calling the render_assignment function
        Printing the result
    
        if the command is list,  the fucntion prints out the result of calling render_all on the current course ID, to list all the current assignments.
    
        if the command is scores, the function calls the plot_scores function to create a graph of the distribution of fractional scores of graded assignments.
    
        if the command is earliness, the function calls the plot_earliness function 
        to create a graph of the distribution of the earliness of submissions relative to their due date.
    
        if the command is compare, the function calls the plot_points function to create a graph of the relationship between assignments' 
        points possible and their weighted points possible, to analyze how different the values are.
    
        if the command is predict, the function calls the predict_grades function to create a graph with three running sums, 
        showing the possible grades that could be earned in the course (maximum ever possible, maximum still possible, minimum still possible).
    
        if the command is help, the function prints out a list of commands and a short description to go with each 
    
        otherwise the function returns the course_id value that was input at the beginning
        """
        command = input("enter your in[put here]")
        if command == "course":
            print(render_courses(user_token))
            a = input("new course ID")
            a = int(a)
            print(find_course(user_token, a))
            return a
        if command == "exit":
            return 0
        if command == "points":
            print(total_points(user_token, course_id))
        if command == "comments":
            print(count_comments(user_token, course_id))
        if command == "graded":
            print(ratio_graded(user_token, course_id))
        if command == "score_unweighted":
            print(average_score(user_token, course_id)) 
        if command == "score":
            print(average_weighted(user_token, course_id))
        if command == "group":
            group_name = input("What's the group name?")
            print(average_group(user_token, course_id, group_name))
        if command == "assignment":
            placeholder = input("what's the assignment id?")
            assignment_id = int(placeholder) 
            print(render_assignment(user_token, course_id, assignment_id))
        if command == "list":
            print(render_all(user_token, course_id))
        if command == "scores":
            plot_scores(user_token, course_id)
        if command == "earliness":
            plot_earliness(user_token, course_id) 
        if command == "compare":
            plot_points(user_token, course_id) 
        if command == "predict":
            predict_grades(user_token, course_id)
        if command == "help":
            print("""
exit > Exit the application
help > List all the commands
course > Change current course
points > Print total points in course
comments > Print how many comments in course
graded > Print ratio of ungraded/graded assignments
score_unweighted > Print average unweighted score
score > Print average weighted score
group > Print average of assignment group, by name
assignment > Print the details of a specific assignment, by ID
list > List all the assignments in the course
scores > Plot the distribution of grades in the course
earliness > Plot the distribution of the days assignments were submitted early
compare > Plot the relationship between assignments' points possible and their weighted points possible
predict > Plot the trends in grades over assignments, showing max ever possible, max still possible, and minimum still possible
""")
            return 0 
        else:
            return course_id

    def main(user_token: str):
        """
        this function allows the user to interact with a console that will run the execute function 
        based upon their input.
        it will run a while loop allowing user input until the user chooses to exit and that will stop the loop.
        """
        new = []
        courses = get_courses(user_token)
        for course in courses:
            new.append(course.id)
        course_total = count_courses(user_token)
        if not course_total:
            print("No courses available")
            return 
        b = find_cs1(user_token)
        if b == 0:
            b = new[0]
        while b > 0:
            command = input("Enter Your Command Here. For a list of commands, type help")
            b = execute(command, user_token, b)


@bot.command(name="say")
async def say_message(ctx, *, message: str):
    channel_id = 'GUILD'  # Replace with the actual channel ID
    channel = bot.get_channel(channel_id)
    await channel.send(message)

@bot.command(name="MUED337")
async def apples(ctx):
    await ctx.send(MUED337)
    
@bot.command(name="MUSC315")
async def mued337(ctx):
    await ctx.send(MUSC315)
    
@bot.command(name="CISC181")
async def cisc181(ctx):
    await ctx.send(CISC181)

@bot.command(name="LING101")
async def ling101(ctx):
    await ctx.send(LING101)
    
@bot.command(name="PHYS227")
async def phys227(ctx):
    await ctx.send(PHYS227)
    
@bot.command(name="CHEM120")
async def chem120(ctx):
    await ctx.send(CHEM120)
    
@bot.command(name="PHYS207")
async def phys207(ctx):
    await ctx.send(PHYS207)
    
@bot.command(name="EDUC400")
async def udac400(ctx):
    await ctx.send(EDUC400)
    
@bot.command(name="CIEG161")
async def cieg161(ctx):
    await ctx.send(CIEG161)

@bot.command(name="HIST104")
async def hist104(ctx):
    await ctx.send(HIST104)
    
@bot.command(name="MATH243")
async def math243(ctx):
    await ctx.send(MATH243)
    
@bot.command(name="COMM212")
async def comm212(ctx):
    await ctx.send(COMM212)
    
@bot.command(name="MATH351")
async def math351(ctx):
    await ctx.send(MATH351)
    
@bot.command(name="CIEG315")
async def cieg315(ctx):
    await ctx.send(CIEG315)

@bot.command(name="CISC210")
async def cisc210(ctx):
    await ctx.send(CISC210)
    
@bot.command(name="CPEG202")
async def cpeg202(ctx):
    await ctx.send(CPEG202)
    
@bot.command(name="HIST137")
async def hist137(ctx):
    await ctx.send(HIST137)
    
@bot.command(name="MATH242")
async def math242(ctx):
    await ctx.send(MATH242)

@bot.command(name="MUSC462")
async def musc462(ctx):
    await ctx.send(MUSC462)

@bot.command(name="ENGL110SeminarInComposition")
async def engl110seminarincomposition(ctx):
    await ctx.send(ENGL110SeminarInComposition)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
@bot.command(name= "Canvas")  
async def set_data(ctx):
    await ctx.send("Please Enter Your :")
    try:
        message = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
        data = message.content
        # Save the data for later use
        # Your code here
        print(execute(data))
        await ctx.send("Data saved successfully!")
    except asyncio.TimeoutError:
        await ctx.send("Timeout! Please try again.")

bot.run(TOKEN)


