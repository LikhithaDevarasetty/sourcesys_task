#  Student Data Analysis System

##  Overview
This project performs **data analysis on a student dataset** using Python (Pandas & NumPy).

## Dataset
The dataset file used: STUDENT.csv

### Features in Dataset
- Name
- Age
- Attendance
- Exam Scores
- Video Games Time
- Tuition
- Health
- Stress
- Daily Work
- Self Study

---

### Functionalities

### 1. Data Cleaning
- Handles missing values
- Converts numeric values to integers
- Fills categorical missing values

### 2. Operations
- Dataset inspection (`shape`, `columns`, `describe`)
- Sorting students by scores
- Mathematical operations (mean, max, min)
- Grouping and aggregation

### 3. Filters
- High scorers
- Low attendance students
- Tuition-based filtering
- Multi-condition filtering
- Query-based filtering

### 4. Data Analysis
- Tuition vs Performance
- Health vs Performance
- Stress vs Performance
- Correlation matrix
- Pivot table

### 5. Feature Engineering
- Adds:
  - `PERFORMANCE` (Excellent / Average / Poor)
  - `STATUS` (Pass / Fail)

### 6. Output
- Saves cleaned dataset to:final_output.csv