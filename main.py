#!/usr/bin/python

# A script for compiling markdown like files containig a week
# schedule to pdf, by writing a latex file. Two steps: parse the
# file and create and compile the latex file.

#########################
#       Parameters
#########################

# Colors for each tag
colors = {
            "Plenary":  "#232323",
            "Coffee":   "#FFFFFF",
        }


#########################
#     Parse the file
#########################

schedule_file = "schedule.md"

# A list containing each day. Each day is a list containing
# each event. Each event is a tuple of the form:
# (start_hour, end_hour, tag, name). Tag is for indicating
# the latex format when compiling (color, font or other
# stuff).
schedule = []

#232323 Parse each day
with open(schedule_file, 'r') as file:
    days_list = file.read().split("#")[1:]

for day in days_list:
    curr_day_list = [line for line in day.split("\n") if line.strip()]           # https://stackoverflow.com/questions/3711856/how-to-remove-empty-lines-with-or-without-whitespace
    curr_day_name = curr_day_list[0][1:]
    curr_day_list = curr_day_list[1:]
    schedule.append((curr_day_name, []))

    # Parse each event
    for event in curr_day_list:
        # Parse start hour and end hour
        event_hour  = event[1:].split(")")[0].split("-")
        start = event_hour[0].strip(" ")
        end   = event_hour[1].strip(" ")

        event_strip = event.split(")")[1][1:]

        # Parse tag
        tag = event_strip.split(":")[0]

        # Parse name
        name = event_strip.split(":")[1][1:] # TODO: use strip instead of [1:]

        schedule[-1][1].append((start, end, tag, name))

#for day in schedule:
    #print(day[0])
    #for event in day[1]:
        #print(event)


#########################
#  Create the tex file
#########################

import os

# Add preamble
preamble_file = "tex/preamble.tex"
with open(preamble_file, 'r') as file:
    tex_str = file.read()

tex_str += r"\begin{document}" + "\n"
#...
tex_str += r"hello" + "\n"
tex_str += r"\end{document}"

# Write to file
with open("tex/main.tex", 'w') as file:
    file.write(tex_str)

#os.system("pdflatex -interaction=nonstopmode -no-shell-escape tex/main.tex")
#os.system("cd tex; pdflatex -interaction=nonstopmode main.tex; cp -f tex/main.pdf main.pdf")
os.system("pdflatex -output-directory=tex tex/main.tex")    # Compile file
os.system("cp tex/main.pdf main.pdf")                       # Place pdf in current directory
