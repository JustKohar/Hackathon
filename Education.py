# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from bakery_canvas import get_courses
from bakery_canvas import get_submissions
import matplotlib.pyplot as plt
from datetime import datetime



load_dotenv()
TOKEN = os.getenv("MTIxMzUzNzI3MzgxMTgzMjg0Mg.GSpTc2.LXNRPADODbVG91NWnL1SjsFf-oQePCcUbFLqFU")
GUILD = os.getenv('1213537641597894748')    

client = discord.Client()

bot = commands.Bot(command_prefix="/")

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
        
@bot.slash_command(name="main", description="Interact with a console to run execute function based on input")
async def main(ctx, user_token: str):
    """
    This function allows the user to interact with a console that will run the execute function
    based upon their input.
    It will run a while loop allowing user input until the user chooses to exit and that will stop the loop.
    """
    new = []
    courses = get_courses(user_token)  
    for course in courses:
        new.append(course.id)
    course_total = count_courses(user_token)  
    if not course_total:
        await ctx.send("No courses available")
        return
    b = find_cs1(user_token)  
    if b == 0:
        b = new[0]
    while b > 0:
        await ctx.send("Enter Your Command Here. For a list of commands, type help")
client.run(TOKEN)