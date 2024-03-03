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

load_dotenv(override=True)
TOKEN = os.getenv("TOKEN")
GUILD = os.getenv('GUILD')    

intents = discord.Intents.all()
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="~", intents=intents)

# Define your Discord bot information class
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
    emails="Dr. Purciello's Email Is: lhr@udel.edu",
    ta_hours= "N/A"
)
CISC181 = generate_formatted_message(CISC181)
MUSC315 = generate_formatted_message(MUSC315)
MUED337 = generate_formatted_message(MUED337)

#MUSC315 = DiscordBotInformation("MUSC315\n", "The Professor for this course is Dr. Maria Anne Purciello\n","Dr. Purciello has open office hours on Thursday from 12:30-1:30\n",
#"Dr. Purciello can be found on the third floor of the Amy E. DuPont Music building, room 317\n", "Dr. Purciello's email is: 'mpuriel@udel.edu'")

#MUED337 = DiscordBotInformation("MUED337\n", "The Professor for this course is Dr. Lauren Reynolds", "Dr Reynolds holds office holds office hours by appointment.\n", 
#                                "Dr. Reynolds office is located in the Amy E. Dupont music building, room 309\n", "Dr. Reynold's email address is: lhr@udel.edu")

#MUSC462 = DiscordBotInformation("MUSC462\n", "The Professor for this course is Dr. Aimee Persall.\n", "Dr. Pearsall does not hold office hours for this class.\n", 
#                                "Dr. Pearsall can be found in the Amy E. Dupont Music building, room 313.\n", "Dr. Pearsall's email is: apearsall.udel.edu\n", 
#                                "The TA for this course is Katelyn Viszoki, who can be reached at: kmviszok@udel.edu")

#HIST137 = DiscordBotInformation ("HIST137\n", "The Professor for this course is Dr. Donto D. Pount\n", "Dr. Pount holds office hours Wednesdays from 9-10am\n", 
 #                                "Dr. Pount's class is virtual, her zoom ID is '410 268 6688'\n", "Dr. Pount's email is dpount@udel.edu")
#
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

@bot.command(name="execute")
async def execute(ctx, command: str, user_token: str, course_id: int):
    if command == "course":
        await ctx.send(render_courses(user_token))
        a = await ctx.send("Please enter the new course ID:")
        try:
            response = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=30)
            a = int(response.content)
            await ctx.send(find_course(user_token, a))
            return a
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Please try again.")
            return course_id
    elif command == "exit":
        await ctx.send("Exiting the application.")
        return 0
    elif command == "points":
        await ctx.send(total_points(user_token, course_id))
    elif command == "comments":
        await ctx.send(count_comments(user_token, course_id))
    # Add other commands here...
    else:
        await ctx.send("Invalid command. Please try again.")
        return course_id

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

@bot.event
async def on_ready():
    print(f'{bot.user} is now running')

bot.run(TOKEN)
