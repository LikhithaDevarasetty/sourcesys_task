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


