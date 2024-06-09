#!/usr/bin/python

# A script for compiling markdown like files containig a week
# schedule to pdf, by writing a latex file. Two steps: parse the
# file and create and compile the latex file.

#########################
#       Parameters
#########################

# Colors
colors = {  # Tag:      color
            "Register": "A37C40",
            "Ceremony": "98473E",
            "Plenary":  "DB7F67",
            "Coffee":   "E3D081",
            "Parallel": "91C7B1",
            "Lunch":    "E3D081",
            "Workshop": "947BD3",
            "Posters":  "B33951"
         }

color_text_slot     = "000000"      # The color of the text of each time slot

color_grid          = "62aeab"      # The color of the grid

color_bg_top_bar    = "1d8c84"      # The color of the background of the top bar
color_text_top_bar  = "FFFFFF"      # The color of the text of the top bar

color_bg_left_bar   = "FFFFFF"      # The color of the background of the left bar
color_text_left_bar = "000000"      # The color of the text of the left bar

# Sizes
scale = 1
slot_height = 0.8
slot_width  = 4

# Draw auxiliar elements
draw_grid        = True
draw_left_bar    = True
draw_hour_inline = True

# Optional to import in the preamble (for example, for setting the font)
optional_packages = r"\usepackage{mathptmx}"


#########################
#     Parse the file
#########################

def hour_to_mins(hour):
    return int(hour.split(":")[0])*60 + int(hour.split(":")[1])

def mins_to_hour(mins):
    return str(int((mins)/60)).zfill(2) + ":" + str(mins % 60).zfill(2)

schedule_file = "schedule.md"

# A list containing each day. Each day is a list containing
# each event. Each event is a tuple of the form:
# (start_hour, end_hour, tag, name). Tag is for indicating
# the latex format when compiling (color, font or other
# stuff).
schedule       = []
start_schedule = "24:00"
end_schedule   = "0:00"

# Parse each day
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
        event_hour = event[1:].split(")")[0].split("-")
        start      = event_hour[0].strip(" ")
        end        = event_hour[1].strip(" ")

        start = start.zfill(5) # For parsing 9:00 instead of 09:00
        end = end.zfill(5)

        if start_schedule > start:
            start_schedule = start

        if end_schedule < end:
            end_schedule = end

        event_strip_list = event.split(")")[1:] # TODO: this thing parses hour. It is trash
        event_strip = event_strip_list[0]
        for i in event_strip_list[1:]:
            event_strip += ")" + i

        # Parse tag
        tag = event_strip.split(":")[0]

        # Parse name TODO: this is trash
        name_list = event_strip.split(":")[1:]
        name = name_list[0]
        for i in range(1,len(name_list)):
            name += ":" + name_list[i]

        schedule[-1][1].append((start, end, tag, name))


# For debugging
#print("Schedule from " + start_schedule + " to " + end_schedule + "\n")
#for day in schedule:
    #print(day[0])
    #for event in day[1]:
        #print(event)


#########################
#  Create the tex file
#########################

import os, math

start_schedule_mins = hour_to_mins(start_schedule)
end_schedule_mins   = hour_to_mins(end_schedule)
total_schedule_mins = end_schedule_mins - start_schedule_mins
num_slots           = math.ceil(total_schedule_mins / 30)

# Add preamble
tex_str = r"\documentclass[a4paper, landscape]{article}"
tex_str += optional_packages
tex_str += r"\pagestyle{empty}" + "\n"
tex_str += r"\usepackage{xcolor}" + "\n"
tex_str += r"\usepackage{geometry}" + "\n"
tex_str += r"\geometry{" + "\n"
tex_str += r"top=60," + "\n"
tex_str += r"right=0," + "\n"
tex_str += r"bottom=0," + "\n"
tex_str += r"left=0" + "\n"
tex_str += r"}" + "\n"
tex_str += r"\usepackage{tikz}" + "\n"

# Define colors
colors["grid"] = color_grid
colors["bg_top_bar"] = color_bg_top_bar
colors["bg_left_bar"] = color_bg_left_bar
colors["text_slot"] = color_text_slot
colors["text_top_bar"] = color_text_top_bar
colors["text_left_bar"] = color_text_left_bar

for tag in colors:
    tex_str += r"\definecolor{" + tag + "}{HTML}{" + colors[tag] + "}\n"

tex_str += r"\begin{document}" + "\n"
tex_str += r"\centering"
tex_str += r"\begin{tikzpicture}[scale=" + str(scale) + ", every node/.style={scale=" + str(scale) + "}]" + "\n"

# Draw grid
if draw_grid:
    for row in range(num_slots):
        tex_str += r"   \draw [draw=grid] (" + str(slot_width) + "," + str(slot_height*row) + ") -- (" + str(slot_width*(len(schedule)+1)) + ", " + str(slot_height*row) + ");" +  "\n"

    for col in range(len(schedule)+1):
        tex_str += r"   \draw [draw=grid] (" + str((col+1)*slot_width) + ", 0) -- (" + str((col+1)*slot_width) + ", " + str(slot_height*num_slots) + ");" +  "\n"

# Draw each day
for i in range(0,len(schedule)):
    curr_day_text = r"{\bf " + schedule[i][0] + "}"
    pos_x         = slot_width*(i+1)
    pos_y         = num_slots*slot_height
    tex_str += r"   \filldraw [fill=bg_top_bar,draw=grid] (" + str(pos_x) + ", " + str(pos_y) + ") rectangle (" + str(pos_x + slot_width) + ", " + str(pos_y + slot_height) + ") node[color=text_top_bar,pos=.5] {" + curr_day_text + " };" + "\n"

    # Draw events
    for event in schedule[i][1]:
        pos_y_start = num_slots*slot_height - (hour_to_mins(event[0]) - start_schedule_mins) / total_schedule_mins * slot_height * num_slots
        pos_y_end   = num_slots*slot_height - (hour_to_mins(event[1]) - start_schedule_mins) / total_schedule_mins * slot_height * num_slots
        curr_color  = event[2]
        curr_text   = event[3]
        if draw_hour_inline:
            curr_text = r"\tiny " + event[0] + " - " + event[1] + r"\\" + curr_text

        # Draw
        tex_str += r"   \filldraw [fill=" + curr_color + ",draw=grid] (" + str(pos_x) + ", " + str(pos_y_start) + ") rectangle (" + str(pos_x + slot_width) + ", " + str(pos_y_end) + ") node[align=center,color=text_slot,pos=.5,scale=0.8] {" + curr_text + " };" + "\n"

# Draw left bar indicating hours
if draw_left_bar:
    curr_end_min  = start_schedule_mins + 30
    curr_end_time = start_schedule
    for i in range(1,num_slots+1):
        curr_start_time = curr_end_time
        curr_end_time   = mins_to_hour(curr_end_min)

        pos_y = (num_slots - i)*slot_height
        hour_text = curr_start_time + " - " + curr_end_time
        tex_str += r"   \filldraw [fill=bg_left_bar,draw=grid] (0," + str(pos_y) + ") rectangle (" + str(slot_width) + ", " + str(pos_y + slot_height) + ") node[color=text_left_bar,pos=.5] {" + hour_text + " };" + "\n"

        curr_end_min += 30

tex_str += r"\end{tikzpicture}" + "\n"
tex_str += r"\end{document}"

# Write to file
with open("tex/main.tex", 'w') as file:
    file.write(tex_str)

#os.system("pdflatex -interaction=nonstopmode -no-shell-escape tex/main.tex")
#os.system("cd tex; pdflatex -interaction=nonstopmode main.tex; cp -f tex/main.pdf main.pdf")
os.system("pdflatex -interaction=nonstopmode -output-directory=tex tex/main.tex &> /dev/null")    # Compile file
os.system("cp tex/main.pdf schedule.pdf")                       # Place pdf in current directory
