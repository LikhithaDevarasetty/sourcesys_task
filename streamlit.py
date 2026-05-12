import streamlit as st

# --- page config ---
st.set_page_config(
    page_title="BMI Health Calculator",
    page_icon="🩺",
    layout="centered"
)

# --- custom styling ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@700&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
        }

        .main {
            background-color: #f7f9fc;
        }

        .result-card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-top: 20px;
            border-left: 6px solid #4f8ef7;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        }

        .bmi-value {
            font-size: 3rem;
            font-weight: 700;
            color: #4f8ef7;
            font-family: 'Playfair Display', serif;
        }

        .category-tag {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 6px;
        }

        .tip-box {
            background: #eef3ff;
            border-radius: 12px;
            padding: 16px 20px;
            margin-top: 16px;
            font-size: 0.92rem;
            color: #3a3a5c;
        }

        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# --- helpers ---
def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

def get_category(bmi):
    if bmi < 18.5:
        return "Underweight", "#f0a500", "⚠️"
    elif bmi < 25:
        return "Normal weight", "#27ae60", "✅"
    elif bmi < 30:
        return "Overweight", "#e67e22", "⚠️"
    else:
        return "Obese", "#e74c3c", "🚨"

def ideal_weight_range(height_cm):
    h = height_cm / 100
    low  = round(18.5 * h * h, 1)
    high = round(24.9 * h * h, 1)
    return low, high

def get_tip(category):
    tips = {
        "Underweight": "Consider eating nutrient-rich foods more frequently. Consult a dietitian for a personalised plan.",
        "Normal weight": "Great job! Keep up your balanced diet and regular physical activity to maintain this range.",
        "Overweight": "Small changes help — try 30 mins of walking daily and cut back on processed foods.",
        "Obese": "It's never too late to start. Speak with a healthcare provider for a safe and steady plan.",
    }
    return tips[category]


# --- header ---
st.markdown("## 🩺 BMI & Health Calculator")
st.markdown("Enter your details below to get your Body Mass Index and some quick health insights.")
st.divider()

# --- unit system toggle ---
col1, col2 = st.columns(2)
with col1:
    unit_system = st.radio("Unit system", ["Metric (kg / cm)", "Imperial (lbs / in)"], horizontal=True)

st.write("")

# --- weight & height dropdowns ---
if unit_system == "Metric (kg / cm)":
    # options in 0.5 increments
    weight_options = [round(x * 0.5, 1) for x in range(20, 601)]   # 10.0 – 300.0 kg
    height_options = [round(x * 0.5, 1) for x in range(100, 501)]  # 50.0 – 250.0 cm

    col_a, col_b = st.columns(2)
    with col_a:
        weight_kg = st.selectbox(
            "Weight (kg)",
            options=weight_options,
            index=weight_options.index(70.0)    # default 70 kg
        )
    with col_b:
        height_cm = st.selectbox(
            "Height (cm)",
            options=height_options,
            index=height_options.index(170.0)   # default 170 cm
        )

else:
    weight_options = list(range(22, 661))                           # 22 – 660 lbs
    height_options = [round(x * 0.5, 1) for x in range(40, 201)]   # 20.0 – 100.0 inches

    col_a, col_b = st.columns(2)
    with col_a:
        weight_lbs = st.selectbox(
            "Weight (lbs)",
            options=weight_options,
            index=weight_options.index(154)     # default 154 lbs
        )
    with col_b:
        height_in = st.selectbox(
            "Height (inches)",
            options=height_options,
            index=height_options.index(67.0)    # default 67 in ≈ 5'7"
        )
    weight_kg = round(weight_lbs * 0.453592, 2)
    height_cm = round(height_in * 2.54, 2)

# --- age & gender ---
col_c, col_d = st.columns(2)
with col_c:
    age = st.slider("Age", min_value=5, max_value=100, value=25)
with col_d:
    gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])

st.write("")
calculate = st.button("Calculate BMI →", use_container_width=True, type="primary")

# --- results ---
if calculate:
    bmi = calculate_bmi(weight_kg, height_cm)
    category, color, icon = get_category(bmi)
    low, high = ideal_weight_range(height_cm)
    tip = get_tip(category)

    st.markdown(f"""
        <div class="result-card">
            <div style="margin-bottom:4px; color:#888; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">Your BMI</div>
            <div class="bmi-value">{bmi}</div>
            <div class="category-tag" style="background:{color}22; color:{color};">{icon} {category}</div>
            <hr style="margin:16px 0; border:none; border-top:1px solid #eee;">
            <div style="display:flex; gap:32px; flex-wrap:wrap;">
                <div>
                    <div style="font-size:0.8rem; color:#999; text-transform:uppercase; letter-spacing:0.5px;">Ideal range for your height</div>
                    <div style="font-weight:700; font-size:1.05rem; color:#1a1a2e; margin-top:2px;">{low} – {high} kg</div>
                </div>
                <div>
                    <div style="font-size:0.8rem; color:#999; text-transform:uppercase; letter-spacing:0.5px;">Height used</div>
                    <div style="font-weight:700; font-size:1.05rem; color:#1a1a2e; margin-top:2px;">{height_cm} cm</div>
                </div>
                <div>
                    <div style="font-size:0.8rem; color:#999; text-transform:uppercase; letter-spacing:0.5px;">Weight used</div>
                    <div style="font-weight:700; font-size:1.05rem; color:#1a1a2e; margin-top:2px;">{weight_kg} kg</div>
                </div>
            </div>
            <div class="tip-box">💡 <strong>Tip:</strong> {tip}</div>
        </div>
    """, unsafe_allow_html=True)

    # BMI scale visual
    st.write("")
    st.markdown("#### BMI Scale")
    scale_cols = st.columns(4)
    zones = [
        ("< 18.5",      "Underweight", "#f0a500"),
        ("18.5 – 24.9", "Normal",      "#27ae60"),
        ("25 – 29.9",   "Overweight",  "#e67e22"),
        ("≥ 30",        "Obese",       "#e74c3c"),
    ]
    for col, (rng, label, clr) in zip(scale_cols, zones):
        is_current = label.lower().startswith(category.split()[0].lower())
        border = "3px solid #333" if is_current else "1px solid #eee"
        you_tag = "<div style='font-size:0.7rem; font-weight:600; color:#333; margin-top:4px;'>◀ You</div>" if is_current else ""
        col.markdown(f"""
            <div style="background:{clr}22; border:{border}; border-radius:10px; padding:10px; text-align:center;">
                <div style="font-weight:700; color:{clr}; font-size:0.85rem;">{label}</div>
                <div style="font-size:0.78rem; color:#666;">{rng}</div>
                {you_tag}
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.caption("ℹ️ BMI is a general screening tool and doesn't account for muscle mass, bone density, or fat distribution. Always consult a healthcare professional for personalised advice.")