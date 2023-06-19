# Timetable-Generator

# Description
Due to the large number of students at UofT, adding courses to your enrolment cart is vital. Courses can have many lecture cohorts, tutorials, and practicals with limited space. Although finding a set of course times with no conflicts can be difficult, UofT doesn't allow you to visualize your timetable pre-enrolment. This repository takes the raw HTML file of the course selection page on ACORN and outputs your fall and winter timetable.

---
# Organization

## Tree
```bash
code
   |-- timetable_gen.py
results
   |-- fall_timetable_sample.png
   |-- sample_data.html
   |-- winter_timetable_sample.png
```
# Running the project

To run the project, download the repository, enter the main project directory, and run:
```
python3 code/timetable_gen.py
```
You will then be prompted to enter the path and file of the raw course selection HTML. Winter and fall timetables will be stored as 'fall_timetable.png' and 'winter_timetable.png' in the results directory.

---
# Results
Output from sample_data.html, note the scheduling conflict on Tuesday morning in the winter timetable.

Fall                   |  Winter                  |
:-------------------------:|:-------------------------:|
![](https://github.com/CameronKerr/Timetable-Generator/blob/main/results/fall_timetable_sample.png)  |  ![](https://github.com/CameronKerr/Timetable-Generator/blob/main/results/winter_timetable_sample.png) | 
