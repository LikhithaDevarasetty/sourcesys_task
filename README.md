# Internship Repository

This repository contains basic tasks and practice work completed as part of my internship at SourceSys Technology.

## About Me
Hello! My name is Likhitha Devarasetty.  
I am currently pursuing a B.Tech in Artificial Intelligence at Amrita Vishwa Vidyapeetham.  
I am interested in Data Science, Machine Learning, and Web Development.

##  Technologies Used
- Python
- SQL
- Power BI
- Git & GitHub

# Sourcesys Internship Tasks

## Task 1: Repository Setup
* Created a GitHub repository named **sourcesys**
* Initialized Git in the local system
* Created a sample Python file
* Pushed the file to GitHub repository
* Learned basic Git commands (add, commit, push)

## Task 2: Branching and Merging
* Created a new Python file
* Created a **feature branch**
* Made changes in the feature branch
* Merged the feature branch into the **main branch**
* Understood Git branching and merging workflow

## Task 3: Python Modules and Exception Handling
* Created multiple Python files using built-in modules
* Used modules like **math, datetime, random, file handling**
* Implemented **try-except blocks** for error handling
* Handled different exceptions (ValueError, FileNotFoundError, etc.)
* Used **else and finally blocks** for better control flow

## Task 4: Object-Oriented Programming Concepts
* Created Python programs using **classes and objects**
* Implemented **encapsulation** using private variables
* Used **abstraction** with abstract classes and methods
* Defined multiple functions inside classes
* Demonstrated real-world OOP concepts

## Task 5: Inheritance and Polymorphism
* Implemented **Inheritance** using parent and child classes
* Demonstrated code reusability through class hierarchy
* Used **method overriding** in derived classes
* Implemented **Polymorphism** using same method with different behaviors

## Task 6: Advanced Python Concepts
* **Iterators**
  * Implemented a custom iterator (Countdown system)
  * Used `__iter__()` and `__next__()` methods
  * Demonstrates manual control over iteration
* **Generators**
  * Created a generator function to read file data line by line
  * Used `yield` keyword for memory-efficient processing
  * Suitable for handling large data
* **Decorators**
  * Implemented a login authentication system
  * Used decorators to modify function behavior
  * Improved code reusability
* **Closure**
  * Developed a discount calculator using closures
  * Demonstrates how inner functions retain outer function variables
* **Regular Expressions**
  * Implemented email validation using `re` module
  * Used pattern matching for data validation

## Task7: NumPy Basics and Virtual Environment Setup
* **Virtual Environment Setup**
  * Created a virtual environment using Python
  * Activated the virtual environment
  * Installed required libraries inside the environment
* **Commands Used:**
  * python -m venv venv
  * venv\Scripts\activate
  * pip install numpy
* **Implemented basic operations using NumPy:**
  * Created arrays using np.array()
  * Generated arrays using np.zeros() and np.ones()
  * Performed arithmetic operations (addition, multiplication)
  * Used functions like mean(), sum(), and reshape()

## Task: NumPy Broadcasting
* **Description**
This project demonstrates **NumPy broadcasting**, which allows operations on arrays of different shapes without reshaping them.
* **Examples Covered**
  *Scalar broadcasting  
  *Same shape operations  
  *Row-wise and column-wise broadcasting  
  *Higher dimensional broadcasting  
  *Invalid case handling  
* **Folder Structure**
```
Task7/
│
├── venv/                # Virtual Environment
├── main.py              # Broadcasting implementation
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
├── .gitignore           # Ignored files
├── README.md            # Documentation
```
* **Setup & Run**
```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Task: HR Analytics Mini Project
Generates a synthetic employee dataset using Python's `random` module and prints analytics reports — **no external dependencies**.
* **Files**
| File | Purpose |
|---|---|
| `data_generator.py` | Constants + dataset generation |
| `analysis.py` | All 9 reporting functions |
| `main.py` | Entry point |

* **Run**
```bash
python main.py
```
* **Config**
Edit these in `main.py`:
```python
NUM_RECORDS = 200   # employees to generate
TOP_N       = 5     # top earners to show
SAMPLE_ROWS = 8     # sample rows to print
```
* **Libraries Used**
`random` · `statistics` · `collections`

## Task: NumPy 1D Array – Complete Operations

* **Description**
This project demonstrates **all major concepts and operations of NumPy using 1D arrays**. It provides a comprehensive understanding of how NumPy works with array creation, manipulation, mathematical operations, and data analysis.

* **Concepts Covered**

    - Array creation (array, zeros, ones, arange, linspace, random)
    - Array attributes (shape, size, dtype, ndim)
    - Indexing and slicing (basic, fancy, boolean)
    - Array modification and assignment
    - Arithmetic operations and broadcasting
    - Mathematical functions (sqrt, log, trigonometry, etc.)
    - Statistical operations (mean, median, std, sum, etc.)
    - Sorting and searching
    - Reshaping and array manipulation
    - Concatenation and splitting
    - Set operations
    - Logical and comparison operations
    - Bitwise operations
    - Linear algebra operations (dot, norm, etc.)
    - Type casting
    - Copy vs View
    - Handling NaN and infinite values
    - String operations using NumPy
    - Saving and loading arrays
    - Utility functions


## NUMPY — Advanced Topics Deep Dive

This project covers advanced NumPy concepts for efficient computation, memory optimization, and high-performance array operations.

---

## Topics Covered

### 1. Indexing (9 Types)
- **Scalar:** `a[0], a[-1]` → View  
- **Slicing:** `a[2:7:2], a[::-1]` → View  
- **Fancy Indexing:** `a[[0,3,6]]` → Copy  
- **Boolean Mask:** `a[a>5]` → Copy  
- **2D Indexing:** `mat[1,3], mat[:,2]` → View  
- **Cross Indexing:** `mat[np.ix_([0,2],[1,3])]` → Copy  
- **Ellipsis:** `arr3d[0,...]` → View  
- **New Axis:** `a[:, np.newaxis]` → View  
- **Selection Ops:** `take / choose / compress` → Copy  

---

### 2. Stacking (Key Functions)
- `np.stack()` → adds new axis  
- `vstack`, `hstack`, `dstack` → vertical/horizontal/depth  
- `column_stack()` → 1D → columns  
- `concatenate()` → flexible axis join  
- `block()` → block matrix assembly  

---

### 3. Memory Optimization
- `float32` → 50% less memory than `float64`  
- `float16` → 75% savings (ML use)  
- `uint8` (images), `int8` (labels)  
- Use `np.can_cast()` before downcasting  

---

### 4. Avoiding Copies
- Slices → **View (✓)** | Fancy indexing → **Copy (✗)**  
- Use in-place ops: `+=`, `*=`  
- `np.add(a, b, out=...)` → no temp arrays  
- `broadcast_to()` → zero-copy expansion  

---

### 5. Strides
- Defines memory step size (bytes)  
- Slicing changes strides, not data  
- `as_strided()` → advanced zero-copy views  
- Transpose swaps strides (no copy)  

---

### 6. Contiguous Arrays
- **C-contiguous** (row-major, default)  
- **F-contiguous** via `asfortranarray()`  
- Transpose/slices break contiguity  
- Fix using `ascontiguousarray()`  

---

### 7. Iteration Techniques
- `nditer` → efficient iteration  
- `ndenumerate` → (index, value)  
- `apply_along_axis()` → row/col ops  
- `vectorize()` → convenience wrapper  
- `flat` → flat iterator  
- Vectorization → ~60x faster than loops  

---

## Task: Student Marks Analysis — Linear Algebra with NumPy

A Python script demonstrating core linear algebra and data analysis concepts using a simulated student marks dataset (10 students × 5 subjects).



### Dataset

- **Students:** Aarav, Bhavya, Charan, Divya, Esha, Farhan, Geetha, Harish, Isha, Jayanth  
- **Subjects:** Maths, Physics, Chemistry, English, CS  
- **Marks range:** 40.0 – 98.0 (seed = 7)



### Sections

| # | Topic | What it covers |
|---|-------|----------------|
| 1 | Dataset Generation | Random marks → NumPy matrix (10×5) |
| 2 | Matrix Representation | Shape, transpose, dtype, memory |
| 3 | Vector Operations | Addition, dot product, norm, unit vector, projection |
| 4 | Matrix Operations | Multiplication, Hadamard product, transpose |
| 5 | Det · Trace · Rank · Inverse | Key matrix properties + invertibility check |
| 6 | Linear System Ax = b | `np.linalg.solve` and `lstsq` |
| 7 | Eigenvalues & Eigenvectors | Applied on student similarity matrix |
| 8 | Cosine Similarity | Angular distance between student score vectors |
| 9 | SVD | Low-rank approximation, energy per singular value |
| 10 | Covariance Matrix | Mean-centring, variance, verified vs `np.cov` |
| 11 | PCA | Manual PCA, explained variance, 2D projection |
| 12 | Weighted Scores & Grades | Final scores via matrix multiplication + ranking |
| 13 | Correlation Matrix | Subject-pair Pearson correlations |


## Student Data Analysis System

### Overview
This project performs **data analysis on a student dataset** using Python (Pandas & NumPy).

It includes:
- Data cleaning (handling missing values)
- Data operations (sorting, grouping, statistics)
- Data filtering (conditions & queries)
- Data analysis (insights & correlations)
- Exporting cleaned dataset


### Dataset
The dataset file used: STUDENT.csv


## Student Data Cleaning

This project focuses on **data cleaning** of a student dataset using Python (Pandas & NumPy).

### Dataset
`STUDENT.csv`



### Steps Performed
- Handled missing values  
  - Numerical → mean/median  
  - Categorical → default values  
- Removed duplicates  
- Converted data types to integers  
- Applied proper rounding  
- Standardized categorical values  


### Output
Cleaned dataset saved as:  
`cleaned_student_data.csv`

---

## Student Data Grouping & Analysis

### Overview
This project performs **grouping and analysis** on a student dataset using Python (Pandas).

### Operations Performed

- Grouping by:
  - Tuition
  - Health
  - Stress  

- Multiple grouping:
  - Tuition + Health  

- Aggregation:
  - Mean, Max, Min, Count  

- Pivot Table creation  

- Count analysis:
  - Health distribution  
  - Stress distribution  

- Correlation analysis between numerical features  

---

## Matplotlib Complete Practice

### Overview

This project is a **complete hands-on practice of Matplotlib**, covering all major visualization concepts from basic plots to advanced graphs.

### Technologies Used

* Python
* NumPy
* Matplotlib

---

### Concepts Covered

This project covers around **30 important Matplotlib concepts**:

1. Basic Line Plot
2. Styled Line Plot
3. Scatter Plot
4. Bar Chart
5. Horizontal Bar Chart
6. Grouped Bar Chart
7. Stacked Bar Chart
8. Pie Chart
9. Histogram
10. Box Plot
11. Area Plot
12. Subplots
13. Twin Axis Plot
14. Annotations
15. Step Plot
16. Stem Plot
17. Heatmap
18. Contour Plot
19. Filled Contour Plot
20. 3D Surface Plot
21. Polar Plot
22. Error Bar Plot
23. Violin Plot
24. Hexbin Plot
25. Logarithmic Scale Plot
26. Custom Figure Size
27. Multiple Legends
28. GridSpec Layout
29. Tick Customization
30. Shapes using Patches

---
# COVID-19 Data Visualization using Matplotlib

## Overview

This project focuses on visualizing COVID-19 data using **Matplotlib**.  

The dataset includes information such as:
- Confirmed cases  
- Recovered cases  
- Deaths  
- Critical cases  
- Country-wise data  

---

## Technologies Used

- Python  
- Pandas  
- NumPy  
- Matplotlib  

---

##  Graphs Used and Their Purpose

### 1. Basic Line Plot  
Shows trend of confirmed cases across countries  

### 2. Styled Line Plot  
Compares confirmed cases and deaths  

### 3. Scatter Plot  
Shows relationship between confirmed cases and deaths  

### 4. Bar Chart  
Compares confirmed cases across countries  

### 5. Horizontal Bar Chart  
Compares deaths across countries  

### 6. Grouped Bar Chart  
Compares confirmed vs recovered cases  

### 7. Stacked Bar Chart  
Shows total cases (confirmed + recovered)  

### 8. Pie Chart  
Shows percentage share of confirmed cases  

### 9. Histogram  
Shows distribution of confirmed cases  

### 10. Box Plot  
Shows spread and outliers in confirmed cases  

### 11. Area Plot  
Shows cumulative trend of confirmed cases  

### 12. Subplots  
Compares confirmed and deaths separately  

### 13. Twin Axis Plot  
Shows two variables with different scales  

### 14. Annotation Plot  
Highlights important point (maximum value)  

### 15. Step Plot  
Shows changes in discrete steps  

### 16. Stem Plot  
Shows discrete data distribution  

### 17. Heatmap  
Shows intensity of multiple variables  

### 18. Contour Plot  
Shows level curves (mathematical relationship)  

### 19. Filled Contour Plot  
Shows intensity using colors  

### 20. 3D Surface Plot  
Shows 3D relationship between variables  

### 21. Polar Plot  
Displays data in circular format  

### 22. Error Bar Plot  
Shows variation or uncertainty in data  

### 23. Violin Plot  
Shows distribution and density  

### 24. Hexbin Plot  
Shows density of data points  

### 25. Log Scale Plot  
Helps visualize large value ranges  

### 26. Custom Figure  
Demonstrates figure customization  

### 27. Multiple Legends  
Displays multiple labels clearly  

### 28. GridSpec Layout  
Arranges multiple plots in custom layout  

### 29. Tick Customization  
Improves axis readability  

### 30. Shapes Plot  
Adds geometric shapes to visualization  

---

# Weather Data Analysis & Visualization (Time Series)

##  Overview

This project performs **data analysis and visualization** on a weather time-series dataset using Python.

It explores different weather parameters such as:
- Temperature
- Humidity
- Wind Speed
- Pressure
- UV Index

Various types of graphs are used to understand trends, distributions, and relationships in the dataset.

---

##  Technologies Used

- Python  
- Pandas  
- NumPy  
- Matplotlib  

---

##  Graphs Used and Their Purpose

### 1. Line Chart  
Shows temperature changes over time  

### 2. Bar Chart  
Displays average temperature for each day  

### 3. Pie Chart  
Shows distribution of weather conditions  

### 4. Histogram  
Displays distribution of temperature values  

### 5. Scatter Plot  
Shows relationship between temperature and humidity  

### 6. Box Plot  
Shows temperature spread and outliers per day  

### 7. Area Chart  
Shows humidity trend over time  

### 8. Donut Chart  
Displays wind speed categories  

### 9. Heatmap  
Shows average temperature by hour and day  

### 10. Violin Plot  
Shows humidity distribution per day  

### 11. Horizontal Bar Chart  
Shows average values of weather parameters  

### 12. Step Chart  
Shows average UV index by hour  

### 13. Dual Axis Plot  
Compares temperature and pressure over time  

### 14. Pie Chart  
Shows ratio of daytime vs nighttime data  

### 15. Line Chart  
Compares wind speed and wind gust  

### 16. Histogram  
Shows wind speed distribution  

---

# Regression

## House Price Prediction using Linear Regression

This project uses Linear Regression to predict house prices using machine learning.

### Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

### Dataset
The dataset contains house details like:
- bedrooms
- bathrooms
- floors
- square footage
- city
- price

Target column:
price

### Features
- Data preprocessing
- Label encoding
- Train-test split
- Linear Regression model
- Price prediction
- Performance evaluation
- Graph visualization

### Evaluation Metrics
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R2 Score

### Graphs
- Actual vs Predicted Graph
- Residual Plot
- Feature Coefficients Graph
---
## Heart Disease Prediction using Logistic Regression

This project uses Logistic Regression to predict whether a person has heart disease or not.

### Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

### Dataset
The dataset contains medical details like:
- age
- cholesterol
- chest pain
- blood pressure
- heart rate

Target column:
target

0 = No Disease
1 = Disease

### Features
- Data preprocessing
- Train-test split
- Feature scaling
- Logistic Regression model
- Disease prediction
- Performance evaluation

### Evaluation Metrics
- Accuracy Score
- Confusion Matrix
- Classification Report
---

## Heart Disease Prediction – ML Classification

A machine learning project that predicts heart disease using **KNN**, **Random Forest**, and **Multinomial Naive Bayes** classifiers. Models are trained, evaluated, and tuned using **GridSearchCV**.

---

### Dataset

**File:** `heart.csv`
**Rows:** 303 | **Columns:** 14

**Target Column:**

* `1` → Heart Disease
* `0` → No Disease

---

### Files Overview

#### `preprocessing.py`

* Loads dataset
* Splits train/test data
* Applies:

  * `StandardScaler` for KNN
  * `MinMaxScaler` for Multinomial NB

---

#### `knn_model.py`

* Finds best K value
* Trains KNN model
* Applies GridSearchCV
* Evaluates using accuracy and confusion matrix

---

#### `random_forest_model.py`

* Trains Random Forest model
* Shows feature importance
* Applies GridSearchCV
* Evaluates model performance

---

#### `naive_bayes_model.py`

* Uses Multinomial Naive Bayes
* Uses MinMax scaled data
* Tunes `alpha` using GridSearchCV

---

#### `model_comparison.py`

* Compares all models
* Displays accuracy comparison
* Generates ROC curves and plots

---

### Models Used

| Model          | Purpose                            |
| -------------- | ---------------------------------- |
| KNN            | Distance-based classification      |
| Random Forest  | Ensemble tree-based classification |
| Multinomial NB | Probabilistic classification       |

---

### Methodology

* Train-Test Split: 80/20
* Cross Validation: 5-Fold
* Hyperparameter Tuning: GridSearchCV
* Evaluation Metrics:

  * Accuracy
  * Precision
  * Recall
  * F1-Score
  * ROC-AUC
  * Confusion Matrix

---

## BMI & Health Calculator

A clean, interactive **Body Mass Index calculator** built with [Streamlit](https://streamlit.io/). Enter your weight, height, age, and gender to instantly get your BMI score, category, ideal weight range, and a personalised health tip.

---

###  Features

-  **Unit toggle** — switch between Metric (kg / cm) and Imperial (lbs / in)
-  **Dropdown selectors** for weight and height (no typing needed)
-  **Age slider** and **gender selector**
-  **Result card** showing:
  - BMI score
  - Category badge (Underweight / Normal / Overweight / Obese)
  - Ideal weight range for your height
  - Height & weight used in the calculation
  - Personalised health tip
-  **Visual BMI scale** with your current position highlighted
-  Custom CSS styling with Google Fonts

---

### How BMI is Calculated

```
BMI = weight (kg) / height (m)²
```

| BMI Range     | Category     |
|---------------|--------------|
| Below 18.5    | Underweight  |
| 18.5 – 24.9   | Normal weight|
| 25.0 – 29.9   | Overweight   |
| 30.0 and above| Obese        |

> ⚠️ BMI is a general screening tool and does not account for muscle mass, bone density, or fat distribution. Always consult a healthcare professional for personalised advice.

---

### Built With

- [Streamlit](https://streamlit.io/) — frontend framework
- [Google Fonts](https://fonts.google.com/) — DM Sans + Playfair Display
- Pure Python — no extra data science libraries needed

---
## Data Visualization Dashboard

A Streamlit-based interactive dashboard that lets you upload your own Excel or CSV file and instantly generate different types of charts — no sample data, no hardcoded datasets. Everything is driven by your file.

---


### Supported File Formats

| Format | Extension |
|--------|-----------|
| Excel  | `.xlsx`, `.xls` |
| CSV    | `.csv` |

Multi-sheet Excel files are supported — a sheet selector will appear automatically in the sidebar.

---

###  Available Chart Types

| Chart | Best Used For |
|-------|--------------|
| **Bar Chart** | Comparing totals across categories |
| **Line Chart** | Trends over time or ordered values |
| **Scatter Plot** | Relationship between two numeric variables |
| **Pie / Donut Chart** | Part-to-whole proportions |
| **Histogram** | Distribution of a numeric column |
| **Box Plot** | Spread and outliers in numeric data |
| **Area Chart** | Cumulative or stacked trends over time |
| **Heatmap (Correlation)** | Correlation between all numeric columns |

---


###  Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web app framework |
| `pandas` | Data loading and manipulation |
| `plotly` | Interactive charts |
| `openpyxl` | Reading `.xlsx` Excel files |

Install all at once:

```bash
pip install -r requirements.txt
```

---

###  Streamlit_css-AI Analytics Dashboard

An interactive sales analytics dashboard built with **Streamlit** and **Plotly**, featuring a dark futuristic UI with your custom branding assets.

---


###  User Controls (Sidebar)

| Control | Description |
|---|---|
| **Year(s)** | Filter data by one or more order years (2015–2018) |
| **Region(s)** | Filter by geographic region (East, West, Central, South) |
| **Segment(s)** | Filter by customer segment (Consumer, Corporate, Home Office) |
| **Category(s)** | Filter by product category (Furniture, Office Supplies, Technology) |
| **X-Axis** | Choose what dimension drives the main chart |
| **Color By** | Choose the grouping variable for color encoding |
| **Chart Type** | Switch between Bar, Line, Area, Scatter, or Pie |

All filters apply globally across every chart on the page.

---

###  Charts Included

| Chart | Description |
|---|---|
| **Dynamic Main Chart** | Fully user-controlled via sidebar axis and chart type selectors |
| **Monthly Sales Trend** | Line chart comparing month-by-month sales across selected years |
| **Sales by Region** | Bar chart showing regional revenue breakdown |
| **Category Share** | Donut chart showing each category's revenue proportion |
| **Sub-Category Bar** | Horizontal bar ranked by sub-category sales |
| **Segment × Category** | Stacked bar showing how segments contribute per category |
| **Ship Mode Donut** | Shipping method distribution by revenue |
| **Quarterly Heatmap** | Year × Quarter grid showing seasonal patterns |
| **Top 10 States** | Bar chart of highest-revenue US states |

---

###  CSS Properties Used

All styling is injected via `st.markdown()` using a `<style>` block. Below is a breakdown of every CSS property used, grouped by the UI element it targets.

---

####  Global & Font

| Property | Value Used | Purpose |
|---|---|---|
| `@import` | Google Fonts — Inter | Loads the Inter typeface (weights 300–700) from Google's CDN |
| `font-family` | `'Inter', sans-serif` | Applied globally to all elements via `html, body, [class*="css"]` |

---

####  App Background (`.stApp`)

| Property | Value Used | Purpose |
|---|---|---|
| `background-image` | `url("data:image/png;base64,...")` | Embeds the `bg.png` background as a base64 inline image |
| `background-size` | `cover` | Scales the image to fill the entire viewport without gaps |
| `background-attachment` | `fixed` | Keeps the background pinned while content scrolls (parallax feel) |
| `background-position` | `center` | Centers the image in the viewport |

---

####  Dark Overlay (`.stApp::before`)

A pseudo-element placed over the background to darken it for readability.

| Property | Value Used | Purpose |
|---|---|---|
| `content` | `""` | Required to render a `::before` pseudo-element |
| `position` | `fixed` | Covers the full viewport regardless of scroll |
| `inset` | `0` | Shorthand for `top/right/bottom/left: 0` — fills the entire screen |
| `background` | `rgba(5, 8, 30, 0.72)` | Semi-transparent deep-navy layer dimming the background |
| `z-index` | `0` | Sits behind all UI content |
| `pointer-events` | `none` | Lets clicks pass through to elements underneath |

---

#### Sidebar (`section[data-testid="stSidebar"] > div:first-child`)

| Property | Value Used | Purpose |
|---|---|---|
| `background` | `rgba(10, 14, 50, 0.92)` | Deep navy with slight transparency |
| `border-right` | `1px solid rgba(100, 120, 255, 0.25)` | Subtle glowing right edge separating sidebar from content |
| `backdrop-filter` | `blur(18px)` | Blurs whatever is behind the sidebar panel (glassmorphism) |

---

####  Sidebar Labels (`.stSelectbox label`, `.stMultiSelect label`, `.stRadio label`)

| Property | Value Used | Purpose |
|---|---|---|
| `color` | `#a0b4ff` | Soft periwinkle blue for label text |
| `font-weight` | `500` | Medium weight for legibility |
| `font-size` | `0.82rem` | Slightly smaller than body text |
| `letter-spacing` | `0.05em` | Spreads characters for an uppercase label feel |
| `text-transform` | `uppercase` | Forces all label text to uppercase |

---

####  Sidebar Dropdowns (`div[data-baseweb="select"] > div`)

| Property | Value Used | Purpose |
|---|---|---|
| `background` | `rgba(30, 40, 100, 0.7)` | Dark translucent blue input background |
| `border` | `1px solid rgba(100, 130, 255, 0.4)` | Faint blue border around the dropdown |
| `border-radius` | `10px` | Rounded corners on the select box |
| `color` | `#e0e8ff` | Light text color inside the dropdown |
| `border-color` *(focus)* | `#6c7fff` | Brighter border when the dropdown is active |
| `box-shadow` *(focus)* | `0 0 0 2px rgba(108, 127, 255, 0.35)` | Glowing ring effect on focus |

---

####  Metric Cards (`.metric-card`)

| Property | Value Used | Purpose |
|---|---|---|
| `background` | `linear-gradient(135deg, rgba(20,28,90,0.85), rgba(40,20,100,0.75))` | Diagonal dark blue-to-purple gradient |
| `border` | `1px solid rgba(130, 100, 255, 0.35)` | Purple-tinted translucent border |
| `border-radius` | `16px` | Rounded card corners |
| `padding` | `22px 24px` | Inner spacing (vertical horizontal) |
| `backdrop-filter` | `blur(14px)` | Glassmorphism blur behind each card |
| `transition` | `transform 0.2s, box-shadow 0.2s` | Smooth animation on hover |
| `text-align` | `center` | Centers all card content |
| `transform` *(hover)* | `translateY(-4px)` | Card lifts upward on mouse hover |
| `box-shadow` *(hover)* | `0 12px 40px rgba(100, 80, 255, 0.3)` | Purple glow shadow on hover |

---

#### Metric Card Text

| Selector | Property | Value | Purpose |
|---|---|---|---|
| `.metric-label` | `color` | `#8899dd` | Muted blue-grey for the label line |
| `.metric-label` | `font-size` | `0.75rem` | Small uppercase caption |
| `.metric-label` | `font-weight` | `600` | Semi-bold |
| `.metric-label` | `letter-spacing` | `0.1em` | Spread letters for caps label style |
| `.metric-label` | `text-transform` | `uppercase` | All caps label |
| `.metric-label` | `margin-bottom` | `6px` | Space between label and value |
| `.metric-value` | `color` | `#ffffff` | Bright white for the main number |
| `.metric-value` | `font-size` | `1.9rem` | Large display number |
| `.metric-value` | `font-weight` | `700` | Bold |
| `.metric-value` | `line-height` | `1.1` | Tighter line height for large text |
| `.metric-delta` | `color` | `#66ffb2` | Mint green for the delta/subtitle line |
| `.metric-delta` | `font-size` | `0.78rem` | Smallest text in the card |
| `.metric-delta` | `margin-top` | `5px` | Space above delta text |

---

####  Chart Wrapper (`.chart-box`)

| Property | Value Used | Purpose |
|---|---|---|
| `background` | `rgba(10, 15, 55, 0.75)` | Semi-transparent dark navy panel |
| `border` | `1px solid rgba(90, 110, 255, 0.25)` | Subtle blue border around each chart |
| `border-radius` | `18px` | Rounded container edges |
| `padding` | `20px` | Inner breathing room around the chart |
| `backdrop-filter` | `blur(16px)` | Glassmorphism blur effect |
| `margin-bottom` | `20px` | Vertical gap between chart boxes |

---

####  Chart Title (`.chart-title`)

| Property | Value Used | Purpose |
|---|---|---|
| `color` | `#c0caff` | Soft lavender-blue text |
| `font-size` | `0.9rem` | Slightly smaller than body text |
| `font-weight` | `600` | Semi-bold |
| `letter-spacing` | `0.08em` | Spaced for an uppercase label feel |
| `text-transform` | `uppercase` | All-caps section label |
| `margin-bottom` | `12px` | Space below the title |
| `padding-bottom` | `10px` | Space before the divider line |
| `border-bottom` | `1px solid rgba(100, 120, 255, 0.2)` | Thin separator line under the title |

---

####  Logo Bar (`.logo-bar`, `.logo-bar img`, `.logo-bar-text`)

| Property | Value Used | Purpose |
|---|---|---|
| `display` | `flex` | Enables flexbox layout for horizontal alignment |
| `align-items` | `center` | Vertically centers the logo and text |
| `gap` | `14px` | Space between logo image and text |
| `padding` | `10px 0 18px` | Top and bottom spacing |
| `width` *(img)* | `90px` | Fixed logo image width |
| `border-radius` *(img)* | `12px` | Rounded logo corners |
| `font-size` *(text)* | `1.05rem` | Brand name font size |
| `font-weight` *(text)* | `700` | Bold brand text |
| `color` *(text)* | `#a8baff` | Periwinkle brand color |
| `letter-spacing` *(text)* | `0.06em` | Slightly spaced for branding feel |
| `line-height` *(text)* | `1.35` | Controls spacing between the two text lines |

---

####  Sidebar Divider (`.sidebar-divider`)

| Property | Value Used | Purpose |
|---|---|---|
| `border` | `none` | Removes default `<hr>` border |
| `border-top` | `1px solid rgba(100, 130, 255, 0.2)` | Custom thin translucent blue line |
| `margin` | `14px 0` | Vertical spacing above and below the divider |

---

#### Streamlit UI Cleanup

| Selector | Property | Value | Purpose |
|---|---|---|---|
| `footer` | `visibility` | `hidden` | Hides Streamlit's default footer |
| `#MainMenu` | `visibility` | `hidden` | Hides the hamburger menu |
| `.stPlotlyChart` | `border-radius` | `14px` | Rounds the Plotly chart iframe corners |
| `div[data-testid="stHorizontalBlock"]` | `gap` | `16px` | Adds spacing between side-by-side columns |

---
