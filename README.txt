|=============================================|
| Submission Date (College): 6 December 2025  |
| Repository Upload: 3rd January 2026         |
| Project Status: Completed                   |
|=============================================|

Project: Delhi Metro Route and Schedule Simulator
Name: Shessaanand Siva Sivamurugan
Roll Number: 2025623

Data Sources: DMRC Official Website

=====================
FEATURES
=====================
- Next-train arrival calculation (peak & off-peak logic)
- Route planning with interchanges
- Minimum-interchange-first routing strategy
- Dynamic fare calculation (weekday vs Sunday/holiday)
- Supports multiple metro lines (Blue, Magenta, Yellow, Red, etc.)

=====================
DATA STRUCTURE
=====================
The program reads 'metro_data.txt'. The data is stored in a List of Lists in Python.

=====================
ASSUMPTIONS MADE AND 
HOW IT WORKS
=====================
1. Operational Hours: 06:00 AM to 11:00 PM.
2. Schedule Frequency:
   - Peak Hours (08:00-10:00 & 17:00-19:00): Every 4 minutes.
   - Off-Peak: Every 8 minutes.
3. Start Time: All trains start running from all stations at 06:00 AM.
4. Input Data: The input file 'metro_data.txt' is assumed to be error-free.
5. I have taken the interchange point in the text file, metro_data.txt 
   but have not used it in the metro_simulator.py 
   and is just used for my reference.

=====================
HOW TO RUN
=====================
```bash
python metro_simulator.py

|==================================================|
| PROJECT DEMO VIDEO: https://youtu.be/Nl6W_-kkkGY |
|==================================================|


