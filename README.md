
# Schedule generator

A script for generating a week timetable from a markdown like file. The file schedule.md contains the information of the events of the week using the following format:

```markdown
# Saturday
(9:00 - 09:30) clean: Clean the room
(9:40 - 10:00) homework: Homework

# Sunday
(10:00 - 10:30) tv: Watch tv
(10:30 - 10:50) clean: Clean the room
```

By running the script, the file tex/main.tex is generated. This contains a tikz picture of the timetable. Then, it is compiled to schedule.pdf using pdflatex. Each of the events is showed as a rectangle, whose color is indicated by its tag (clean, homework and tv in the above example).

Colors, sizes and additional features are configured in the first lines of gen_schedule.py.
