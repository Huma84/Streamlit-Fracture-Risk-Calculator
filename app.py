# Streamlit Fracture Risk Calculator — Files

Below are the two files you requested. Save each code block into its respective filename in the same folder.

---

## File: `app.py`

```python
"""
Streamlit Fracture Risk Calculator (screening tool)

Notes:
- This application computes an approximate fracture risk *score* (relative risk / screening index)
  based on commonly used clinical risk factors. It does NOT compute an official FRAX 10-year
  probability. For formal 10-year fracture probability calculations, please use the FRAX tool
  provided by the University of Sheffield.

- The internal scoring algorithm here is a configurable screening model intended for
  educational and pilot-use only; it is NOT validated for clinical decision making.

Author: Generated for user
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

st.set_page_config(page_title="Fracture Risk Calculator", layout="centered")

st.title("Fracture Risk Calculator — Screening Tool")
st.markdown(
    "This app provides an **approximate screening score** for fracture risk based on common clinical risk factors. "
    "It is not a substitute for validated calculators such as FRAX (University of Sheffield)."
)

with st.expander("About / Disclaimer", expanded=False):
    st.markdown(
        "- The score produced is a heuristic screening index and **not** a validated 10-year probability.\n"
        "- For treatment decisions and formal 10-year fracture probabilities, use established tools such as FRAX.\n"
        "- You may adapt the internal weights in the source code for local validation studies."
    )

# --- Input form ---
with st.form("risk_form"):
    st.header("Patient information")

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age (years)", min_value=40, max_value=100, value=65)
        sex = st.selectbox("Sex", options=["Female", "Male"])
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
    with col2:
        height_cm = st.number_input("Height (cm)", min_value=120.0, max_value=220.0, value=160.0)
        bmi = round(weight / ((height_cm/100)**2), 1)
        st.metric("Body Mass Index (BMI)", f"{bmi}")
        femoral_neck_bmd = st.number_input("Femoral neck BMD (g/cm²) — optional", min_value=0.4, max_value=1.6, value=0.0, step=0.01, format="%.2f")
    with col3:
        prior_fracture = st.checkbox("Prior fragility fracture")
        parent_hip = st.checkbox("Parental hip fracture")
        current_smoker = st.checkbox("Current smoker")

    st.markdown("---")

    col4, col5 = st.columns(2)
    with col4:
        glucocorticoids = st.checkbox("Long-term systemic glucocorticoids")
        rheumatoid = st.checkbox("Rheumatoid arthritis")
        secondary_osteoporosis = st.checkbox("Secondary causes of osteoporosis")
    with col5:
        alcohol_3_more = st.checkbox("Alcohol >= 3 units/day")
        fall_in_last_year = st.checkbox("One or more falls in last year")
        immobility = st.checkbox("Prolonged immobility / wheelchair-bound")

    submitted = st.form_submit_button("Calculate screening score")

# --- Scoring algorithm (heuristic) ---
# The weights below are configurable. They create a relative screening index and are not
# claimed to reproduce FRAX probabilities.
AGE_WEIGHT = 0.12
SEX_MALE_WEIGHT = -0.10  # men typically have differing baseline risk patterns (heuristic)
BMI_WEIGHT = -0.05  # higher BMI is often protective to some extent
PRIOR_FRACTURE_WEIGHT = 1.2
PARENT_HIP_WEIGHT = 0.7
SMOKER_WEIGHT = 0.6
GLUCOCORTICOSTEROID_WEIGHT = 0.9
RHEUMATOID_WEIGHT = 0.8
SECONDARY_OSTEOPOROSIS_WEIGHT = 0.9
ALCOHOL_WEIGHT = 0.5
FALL_WEIGHT = 0.8
IMMOBILITY_WEIGHT = 1.0
BMD_WEIGHT = -2.5  # negative because higher BMD reduces risk (only used if BMD provided)
BASELINE = -6.0

if submitted:
    # Compute a simple linear predictor
    score = BASELINE
    score += AGE_WEIGHT * (age - 40)
    if sex == "Male":
        score += SEX_MALE_WEIGHT
    score += BMI_WEIGHT * (bmi - 25)
    score += PRIOR_FRACTURE_WEIGHT * int(prior_fracture)
    score += PARENT_HIP_WEIGHT * int(parent_hip)
    score += SMOKER_WEIGHT * int(current_smoker)
    score += GLUCOCORTICOSTEROID_WEIGHT * int(glucocorticoids)
    score += RHEUMATOID_WEIGHT * int(rheumatoid)
    score += SECONDARY_OSTEOPOROSIS_WEIGHT * int(secondary_osteoporosis)
    score += ALCOHOL_WEIGHT * int(alcohol_3_more)
    score += FALL_WEIGHT * int(fall_in_last_year)
    score += IMMOBILITY_WEIGHT * int(immobility)
    if femoral_neck_bmd and femoral_neck_bmd > 0.0:
        score += BMD_WEIGHT * (femoral_neck_bmd - 0.7)

    # Convert linear predictor to a 0-100 screening index via logistic transform
    prob_like = 1 / (1 + np.exp(-score))
    screening_index = round(prob_like * 100, 1)

    st.subheader("Results")
    st.write(f"**Screening index (approximate):** {screening_index} / 100")

    # Provide interpretation bands (heuristic)
    if screening_index < 10:
        interpretation = "Low (screening only)."
    elif screening_index < 20:
        interpretation = "Mild (consider bone densitometry if other concerns)."
    elif screening_index < 35:
        interpretation = "Moderate (consider referral for further assessment / DXA)."
    else:
        interpretation = "High (refer for DXA and specialist assessment)."

    st.info(interpretation)

    st.markdown("**Note:** This index is indicative and intended for screening only. For a validated 10-year fracture probability use FRAX or local validated tools.")

    # Create a downloadable CSV record
    user_data = {
        "date": [date.today().isoformat()],
        "age": [age],
        "sex": [sex],
        "weight_kg": [weight],
        "height_cm": [height_cm],
        "bmi": [bmi],
        "femoral_neck_bmd": [femoral_neck_bmd],
        "screening_index": [screening_index],
        "interpretation": [interpretation]
    }
    df = pd.DataFrame(user_data)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download result as CSV", data=csv, file_name="fracture_screening_result.csv", mime='text/csv')

    # Show the raw dataframe
    with st.expander("Show data row"):
        st.dataframe(df)

    st.markdown("---")
    st.markdown("References and notes:")
    st.markdown("- This app is a screening demonstration only and not for clinical diagnosis.\n- For validated 10-year fracture probability calculators see FRAX (University of Sheffield).")
```

---

## File: `requirements.txt`

```
streamlit>=1.24.0
pandas
numpy
```

---

## Instructions

1. Save the `app.py` and `requirements.txt` files in the same directory.
2. Create a virtual environment (recommended) and install requirements:

```bash
python -m venv venv
source venv/bin/activate   # On windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

---

If you would like a version that calculates actual FRAX probabilities (by integrating region-specific FRAX models or an offline FRAX library), I can prepare a version that:

* Accepts country selection and femoral neck T-score/BMD and
* Uses published FRAX equations or a wrapper to compute 10-year probabilities (note: FRAX algorithm specifics are maintained by its authors and University of Sheffield — I will supply appropriate references).

Save your files and tell me if you would like the FRAX-integrated version or adjustments to the internal scoring weights.
