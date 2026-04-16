ATLAS v1.2 — Clinical AI for Early Patient Deterioration

Overview

ATLAS is a clinical AI prototype designed to predict early signs of patient deterioration in ICU settings.

This system is built from a clinician’s perspective, focusing on real-world applicability rather than theoretical performance.

---

Clinical Motivation

In ICU environments, early detection of deterioration is critical for improving patient outcomes.

ATLAS aims to:

- Identify high-risk patients early
- Support clinical decision-making
- Provide interpretable risk signals

---

Features Used

- Heart Rate (HR)
- Systolic Blood Pressure (SBP)
- Shock Index
- Oxygen Saturation (SpO₂)
- Derived clinical features

---

Models Implemented

- Logistic Regression (baseline, interpretable)
- Random Forest (non-linear model)

---

Key Learnings

- Avoided data leakage (critical in clinical AI)
- Focused on clinically meaningful features
- Built a structured pipeline from raw data to prediction

---

Project Structure

ATLAS/
├── app/
├── notebooks/
├── src/
├── requirements.txt
├── README.md

---

Version

Current version: v1.2 — Initial Clinical Risk System

---

Author

Majed Hamad
Medical Doctor transitioning into Clinical AI

---

Future Work

- Add time-series features (trend analysis)
- Improve model calibration
- Integrate real clinical workflows
- Expand to full MIMIC-IV dataset
