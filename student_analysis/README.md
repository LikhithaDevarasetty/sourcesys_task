# Student Data Analysis Dashboard

## Project Overview

This project is an interactive **Student Data Analysis System** built using **Python, Pandas, NumPy, and Streamlit**.

It allows users to explore, analyze, and extract insights from a student dataset through a simple and user-friendly interface.

The system performs complete **data analysis (EDA)** and provides multiple options for users to perform their own customized analysis.

---

## Objectives

* To analyze student performance data
* To understand factors affecting exam scores
* To provide an interactive dashboard for data exploration
* To implement real-world data analysis concepts using Python

---

## Technologies Used

* **Python**
* **Pandas** – Data manipulation
* **NumPy** – Numerical computations
* **Streamlit** – Interactive web application

---

## Project Structure

```
project/
│── app.py                     # Streamlit frontend
│── analysis.py               # Backend data analysis (Pandas + NumPy)
│── STUDENT.csv               # Original dataset
│── cleaned_student_data.csv  # Processed dataset
│── README.md                 # Project documentation
```

---

## Features

### Data Analysis (Backend)

* Dataset loading and inspection
* Handling missing values
* Statistical analysis (mean, median, std, etc.)
* Group-by analysis
* Correlation analysis
* Feature engineering
* Custom insights generation

---

### Streamlit Dashboard (Frontend)

* View complete dataset
* Perform data cleaning
* Column-wise operations (unique, value counts)
* Dynamic filtering based on user input
* Group analysis with different aggregations
* Statistical calculations for selected columns
* Correlation matrix visualization
* Custom calculations (add, subtract, multiply, divide)
* Automatic insights generation
* Download processed dataset

---


### Dataset Description

The dataset contains information about students such as:

* Age
* Attendance
* Exam Score
* Self Study Hours
* Video Game Hours
* Tuition (Yes/No)
* Health Condition
* Stress Level
* Daily Work Performance

---

