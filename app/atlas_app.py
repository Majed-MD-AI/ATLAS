import streamlit as st
import pandas as pd
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="ATLAS v1.2", layout="centered")
file_path = "data/patient_log.csv"
os.makedirs("data", exist_ok=True)

trend_message = ""

# =========================
# CLINICAL ENGINE
# =========================
def calculate_risk(hr, sbp, spo2, rr):
    score = 0
    reasons = []
    red_flags = []
    suggested_labs = []
    plan_steps = []

    # Heart Rate
    if hr >= 130:
        score += 2
        reasons.append("Severe tachycardia (HR ≥ 130)")
        red_flags.append("Persistent severe tachycardia")
    elif hr >= 110:
        score += 1
        reasons.append("Elevated heart rate (HR ≥ 110)")

    # Blood Pressure
    if sbp < 90:
        score += 2
        reasons.append("Hypotension (SBP < 90)")
        red_flags.append("Hypotension requiring urgent review")
    elif sbp < 100:
        score += 1
        reasons.append("Borderline low blood pressure (SBP < 100)")

    # Oxygen Saturation
    if spo2 < 90:
        score += 2
        reasons.append("Severe hypoxia (SpO2 < 90)")
        red_flags.append("Severe oxygen desaturation")
    elif spo2 < 94:
        score += 1
        reasons.append("Mild hypoxia (SpO2 < 94)")
        suggested_labs.append("Consider arterial/venous blood gas if clinically indicated")

    # Respiratory Rate
    if rr >= 30:
        score += 2
        reasons.append("Severe tachypnea (RR ≥ 30)")
        red_flags.append("Marked respiratory distress risk")
    elif rr >= 22:
        score += 1
        reasons.append("Elevated respiratory rate (RR ≥ 22)")

    # Shock Index
    shock_index = hr / sbp if sbp > 0 else 0
    if shock_index >= 1.0:
        score += 2
        reasons.append("High shock index (≥ 1.0)")
        red_flags.append("Possible hemodynamic instability")
    elif shock_index >= 0.7:
        score += 1
        reasons.append("Borderline shock index (≥ 0.7)")

    # Risk Level
    if score <= 2:
        risk = "LOW RISK"
        message = "Patient currently appears stable."
        action = "Routine monitoring. Reassess in 4-6 hours."
        plan_steps = [
            "Continue routine observation.",
            "Repeat vital signs in 4-6 hours.",
            "Escalate if new symptoms develop or vitals worsen."
        ]
    elif score <= 6:
        risk = "MODERATE RISK"
        message = "Patient may be at early risk of deterioration."
        action = "Increase monitoring frequency and request clinical review."
        plan_steps = [
    "Maintain continuous monitoring of vital signs.",
    "Perform focused clinical reassessment within 2 hours.",
    "Assess volume status, infection signs, and respiratory function.",
    "Arrange clinical review if no improvement or if deterioration occurs."
        ]
        suggested_labs.extend([
            "CBC",
            "Electrolytes / renal profile",
            "Lactate if concern for hypoperfusion or sepsis"
        ])
    else:
        risk = "HIGH RISK"
        message = "High risk of deterioration detected."
        action = "Urgent clinical review. Consider higher level of care / ICU escalation."
        plan_steps = [
    "Urgent bedside clinical assessment.",
    "Maintain continuous monitoring of vital signs.",
    "Escalate to senior clinician / rapid response team immediately.",
    "Stabilize airway, breathing, and circulation based on clinical context."
        ]
        
        suggested_labs.extend([
            "CBC",
            "Electrolytes / renal profile",
            "Lactate",
            "Blood gas",
            "Infection workup if indicated"
        ])

    if not reasons:
        reasons.append("All entered vital signs are within reassuring range")

    if not red_flags:
        red_flags.append("No immediate red flag detected from current entered vitals")

    # Remove duplicate labs while preserving order
    seen = set()
    deduped_labs = []
    for lab in suggested_labs:
        if lab not in seen:
            deduped_labs.append(lab)
            seen.add(lab)
    suggested_labs = deduped_labs

    interpretation = (
        f"Patient classified as {risk} with risk score {score}. "
        f"Key drivers: {', '.join(reasons)}."
    )

    return {
        "score": score,
        "shock_index": round(shock_index, 2),
        "risk": risk,
        "message": message,
        "action": action,
        "reasons": reasons,
        "red_flags": red_flags,
        "suggested_labs": suggested_labs,
        "plan_steps": plan_steps,
        "interpretation": interpretation,
    }


# =========================
# UI
# =========================
st.title("🧠 ATLAS v1.2")
st.caption("Early Clinical Deterioration Detection System")

st.header("Enter Patient Vital Signs")

hr = st.number_input("Heart Rate (HR)", min_value=0, value=95)
sbp = st.number_input("Systolic Blood Pressure (SBP)", min_value=1, value=120)
spo2 = st.number_input("Oxygen Saturation (SpO2)", min_value=0, max_value=100, value=98)
rr = st.number_input("Respiratory Rate (RR)", min_value=0, value=18)

if st.button("🔍 Predict Clinical Risk"):
    result = calculate_risk(hr, sbp, spo2, rr)

    score = result["score"]
    shock_index = result["shock_index"]
    risk = result["risk"]
    message = result["message"]
    action = result["action"]
    reasons = result["reasons"]
    red_flags = result["red_flags"]
    suggested_labs = result["suggested_labs"]
    plan_steps = result["plan_steps"]
    interpretation = result["interpretation"]

    # Main Output
    st.subheader("🩺 ATLAS Clinical Output")
    st.write(f"❤️ HR: {hr}")
    st.write(f"🩸 SBP: {sbp}")
    st.write(f"🫁 SpO2: {spo2}")
    st.write(f"🌬️ RR: {rr}")
    st.write(f"📉 Shock Index: {shock_index}")
    st.write(f"🧮 Risk Score: {score}")

    if risk == "LOW RISK":
        st.success("✅ LOW RISK")
    elif risk == "MODERATE RISK":
        st.warning("⚠️ MODERATE RISK")
    else:
        st.error("🚨 HIGH RISK")

    st.info(message)
    st.write(f"👉 Immediate Action: {action}")

    # Clinical Interpretation
    st.subheader("🧠 Clinical Interpretation")
    st.write(interpretation)

        # Explanation
    st.subheader("📌 Why this result?")
    for r in reasons:
        st.write(f"- {r}")

    # Suggested Plan
    st.subheader("📋 Suggested Clinical Plan")
    for step in plan_steps:
        st.write(f"- {step}")

    # Suggested Labs
    st.subheader("🧪 Suggested Labs / Workup")
    if suggested_labs:
        for lab in suggested_labs:
            st.write(f"- {lab}")
    else:
        st.write("- No urgent lab suggestion from current entered vitals alone.")

    # Red Flags
    st.subheader("🚨 Red Flags")
    for flag in red_flags:
        st.write(f"- {flag}")

    # Copy-ready summary
    st.subheader("🧾 Copy-Ready Clinical Summary")
    summary_text = (
        f"ATLAS classified this patient as {risk} "
        f"(score {score}, shock index {shock_index}). "
        f"Key drivers: {', '.join(reasons)}. "
        f"Recommended immediate action: {action}"
    )
    st.code(summary_text, language="text")

    # Save row
    new_row = pd.DataFrame([{
        "HR": hr,
        "SBP": sbp,
        "SpO2": spo2,
        "RR": rr,
        "Shock_Index": shock_index,
        "Score": score,
        "Risk": risk,
        "Message": message,
        "Action": action,
        "Interpretation": interpretation
    }])

    if os.path.exists(file_path):
        log_df = pd.read_csv(file_path)
        if not log_df.empty:
            last_row = log_df.tail(1)
            same_values = last_row[["HR", "SBP", "SpO2", "RR"]].reset_index(drop=True).equals(
                new_row[["HR", "SBP", "SpO2", "RR"]].reset_index(drop=True)
            )
            if not same_values:
                log_df = pd.concat([log_df, new_row], ignore_index=True)
        else:
            log_df = new_row
    else:
        log_df = new_row

    log_df.to_csv(file_path, index=False)


# =========================
# LOG SECTION
# =========================
st.divider()
st.subheader("📁 Patient Log")

if os.path.exists(file_path):
    log_df = pd.read_csv(file_path)

# ===== TREND ANALYSIS =====
trend_message = ""
trend_score = 0

if len(log_df) >= 2:
    last = log_df.iloc[-1]
    prev = log_df.iloc[-2]

    # Heart Rate
    if last["HR"] > prev["HR"]:
        trend_score += 1
    elif last["HR"] < prev["HR"]:
        trend_score -= 1

    # Blood Pressure
    if last["SBP"] < prev["SBP"]:
        trend_score += 1
    elif last["SBP"] > prev["SBP"]:
        trend_score -= 1

    # Oxygen
    if last["SpO2"] < prev["SpO2"]:
        trend_score += 1
    elif last["SpO2"] > prev["SpO2"]:
        trend_score -= 1

    # Respiratory Rate
    if last["RR"] > prev["RR"]:
        trend_score += 1
    elif last["RR"] < prev["RR"]:
        trend_score -= 1

    # Final interpretation
    if trend_score >= 2:
        trend_message = "⚠️ Patient is clinically deteriorating compared to previous assessment."
    elif trend_score == 1:
        trend_message = "⚠️ Possible early deterioration trend."
    elif trend_score == 0:
        trend_message = "➖ No significant change compared to previous assessment."
    else:
        trend_message = "✅ Patient shows signs of clinical improvement."

    if st.button("🗑 Clear Patient Log"):
        os.remove(file_path)
        st.success("Patient log cleared.")
        st.stop()

    if not log_df.empty:
        st.subheader("🧾 Last Patient Result")
        st.write(log_df.tail(1))

    if trend_message:
        st.subheader("📈 Trend Analysis")
        st.write(trend_message)

        st.subheader("📊 Dashboard Summary")
        total_cases = len(log_df)
        low_count = len(log_df[log_df["Risk"] == "LOW RISK"])
        moderate_count = len(log_df[log_df["Risk"] == "MODERATE RISK"])
        high_count = len(log_df[log_df["Risk"] == "HIGH RISK"])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Cases", total_cases)
        col2.metric("Low Risk", low_count)
        col3.metric("Moderate Risk", moderate_count)
        col4.metric("High Risk", high_count)

        st.bar_chart(log_df["Risk"].value_counts())

        st.write("### Saved Cases")
        st.dataframe(log_df, use_container_width=True)
    else:
        st.write("No patient records yet.")
else:
    st.write("No patient records yet.")