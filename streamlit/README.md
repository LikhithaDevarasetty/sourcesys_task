#  BMI & Health Calculator

A clean, interactive **Body Mass Index calculator** built with [Streamlit](https://streamlit.io/). Enter your weight, height, age, and gender to instantly get your BMI score, category, ideal weight range, and a personalised health tip.

---

##  Features

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

##  Project Structure

```
bmi-calculator/
│
├── bmi_calculator.py   # Main Streamlit app
└── README.md           # Project documentation
```

---

##  Requirements

- Python 3.8+
- Streamlit

Install dependencies:

```bash
pip install streamlit
```

---

##  How to Run

```bash
streamlit run streamlit.py
```

Then open your browser at `http://localhost:8501`

---

##  How BMI is Calculated

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

##  Built With

- [Streamlit](https://streamlit.io/) — frontend framework
- [Google Fonts](https://fonts.google.com/) — DM Sans + Playfair Display
- Pure Python — no extra data science libraries needed

---
