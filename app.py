# ============================================================
# CDSS - Clinical Decision Support System
# Streamlit Application  |  Infectious Disease Diagnostics
# Run: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

from disease_data import (
    SYMPTOM_CATEGORIES,
    RISK_FACTORS,
    URGENCY_LEVELS,
    DISCLAIMER,
)
from analysis_engine import (
    generate_report,
    confidence_label,
    URGENCY_ORDER,
)

# ─────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CDSS — Infectious Disease Diagnostics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Main background */
    .main { background-color: #f0f4f8; }

    /* Top banner */
    .cdss-banner {
        background: linear-gradient(135deg, #1a3c5e 0%, #2980b9 100%);
        border-radius: 12px;
        padding: 28px 36px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    .cdss-banner h1 { font-size: 2.2rem; margin: 0; }
    .cdss-banner p  { font-size: 1.0rem; opacity: 0.88; margin: 4px 0 0 0; }

    /* Section headers */
    .section-header {
        background: #1a3c5e;
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-size: 1.05rem;
        font-weight: 600;
        margin: 20px 0 12px 0;
    }

    /* Urgency boxes */
    .urgency-box {
        border-radius: 10px;
        padding: 18px 24px;
        color: white;
        font-size: 1.2rem;
        font-weight: 700;
        text-align: center;
        margin: 12px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }

    /* Disease card */
    .disease-card {
        background: white;
        border-radius: 10px;
        padding: 18px 22px;
        border-left: 5px solid #2980b9;
        margin: 10px 0;
        box-shadow: 0 1px 6px rgba(0,0,0,0.08);
    }

    /* Red flag box */
    .red-flag-box {
        background: #fff5f5;
        border: 2px solid #e74c3c;
        border-radius: 10px;
        padding: 16px 22px;
        margin: 10px 0;
    }

    /* Metric card */
    .metric-tile {
        background: white;
        border-radius: 10px;
        padding: 14px 18px;
        text-align: center;
        box-shadow: 0 1px 6px rgba(0,0,0,0.08);
    }

    /* Self-care card */
    .care-card {
        background: #f8fff8;
        border: 1px solid #27ae60;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 6px 0;
    }

    /* Pharmacy card */
    .pharmacy-card {
        background: #fffbf0;
        border: 1px solid #f39c12;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 6px 0;
    }

    /* Doctor card */
    .doctor-card {
        background: #f0f7ff;
        border: 1px solid #2980b9;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 6px 0;
    }

    /* Step badges */
    .step-badge {
        display: inline-block;
        background: #2980b9;
        color: white;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        line-height: 28px;
        text-align: center;
        font-weight: bold;
        margin-right: 8px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: #1a3c5e; }
    section[data-testid="stSidebar"] .stMarkdown p { color: #cde4f7; }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: white; }

    /* Disclaimer */
    .disclaimer-box {
        background: #fff8e1;
        border-left: 4px solid #f39c12;
        border-radius: 6px;
        padding: 12px 18px;
        font-size: 0.82rem;
        color: #555;
    }

    /* Progress bar override */
    .stProgress > div > div { background-color: #2980b9; }

    /* Tabs */
    .stTabs [data-baseweb="tab"] { font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Session state initialisation
# ─────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "intake"
if "report" not in st.session_state:
    st.session_state.report = None

# ─────────────────────────────────────────────
# Helper: render sidebar
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("## 🏥 CDSS Navigation")
        st.markdown("---")

        pages = {
            "📋 Patient Intake": "intake",
            "🔍 Symptom Selection": "symptoms",
            "📊 Diagnostic Results": "results",
        }
        for label, key in pages.items():
            active = "➤ " if st.session_state.page == key else "  "
            st.markdown(f"**{active}{label}**")

        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown(
            "This CDSS uses weighted symptom analysis — a statistical approach — "
            "to suggest probable infectious disease diagnoses. "
            "No machine learning is used."
        )
        st.markdown("---")
        st.markdown("### 🦠 Diseases Covered")
        from disease_data import DISEASES
        for name in DISEASES:
            st.markdown(f"• {name}")
        st.markdown("---")
        st.caption("Version 1.0  |  For educational use only")

# ─────────────────────────────────────────────
# PAGE 1: Patient Intake
# ─────────────────────────────────────────────
def page_intake():
    st.markdown(
        """
        <div class="cdss-banner">
            <h1>🏥 Clinical Decision Support System</h1>
            <p>Infectious Disease Diagnostics  •  Symptom-Based Analysis  •  Educational Tool</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="disclaimer-box">' + DISCLAIMER.replace("\n", " ") + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown('<div class="section-header">📋 Step 1 — Patient Biodata</div>', unsafe_allow_html=True)
    st.markdown("Please fill in the information below as accurately as possible.")

    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name *", placeholder="e.g. Kwame")
        dob        = st.date_input(
            "Date of Birth *",
            value=date(1990, 1, 1),
            min_value=date(1920, 1, 1),
            max_value=date.today(),
        )
        gender = st.selectbox(
            "Gender *",
            ["-- Select --", "Male", "Female", "Other / Prefer not to say"],
        )
        blood_group = st.selectbox(
            "Blood Group",
            ["Unknown", "A+", "A−", "B+", "B−", "AB+", "AB−", "O+", "O−"],
        )

    with col2:
        last_name = st.text_input("Last Name *", placeholder="e.g. Mensah")
        nationality = st.text_input("Nationality / Country of Residence *", placeholder="e.g. Ghana")
        occupation = st.text_input("Occupation", placeholder="e.g. Teacher")
        weight_kg = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5)

    col3, col4 = st.columns(2)
    with col3:
        height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
        contact   = st.text_input("Contact Number", placeholder="e.g. +233 XX XXX XXXX")

    with col4:
        address = st.text_area("Residential Address", placeholder="City, Region, Country", height=98)

    st.markdown('<div class="section-header">🩺 Medical History</div>', unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        allergies    = st.text_area("Known Allergies (drugs/food)", placeholder="e.g. Penicillin", height=80)
        chronic_cond = st.text_area("Existing Chronic Conditions", placeholder="e.g. Diabetes, Hypertension", height=80)
    with col6:
        current_meds = st.text_area("Current Medications", placeholder="e.g. Metformin 500 mg daily", height=80)
        vaccination  = st.text_area("Recent Vaccinations (last 1 year)", placeholder="e.g. COVID-19, Yellow Fever", height=80)

    st.markdown('<div class="section-header">⚠️ Risk Factors</div>', unsafe_allow_html=True)
    risk_factors = st.multiselect(
        "Select any applicable risk factors:",
        list(RISK_FACTORS.keys()),
        default=["No known risk factors"],
    )

    st.markdown("---")

    # Validate and proceed
    if st.button("➤ Proceed to Symptom Selection", type="primary", use_container_width=True):
        if not first_name or not last_name:
            st.error("❌ Please enter the patient's first and last name.")
        elif gender == "-- Select --":
            st.error("❌ Please select a gender.")
        elif not nationality:
            st.error("❌ Please enter nationality / country of residence.")
        else:
            # Calculate age
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            st.session_state.patient_info = {
                "name": f"{first_name} {last_name}",
                "dob": str(dob),
                "age": age,
                "gender": gender,
                "nationality": nationality,
                "occupation": occupation,
                "blood_group": blood_group,
                "weight_kg": weight_kg,
                "height_cm": height_cm,
                "bmi": round(weight_kg / ((height_cm / 100) ** 2), 1),
                "contact": contact,
                "address": address,
                "allergies": allergies,
                "chronic_conditions": chronic_cond,
                "current_medications": current_meds,
                "vaccinations": vaccination,
                "risk_factors": risk_factors,
            }
            st.session_state.page = "symptoms"
            st.rerun()


# ─────────────────────────────────────────────
# PAGE 2: Symptom Selection
# ─────────────────────────────────────────────
def page_symptoms():
    patient = st.session_state.get("patient_info", {})

    st.markdown(
        f"""
        <div class="cdss-banner">
            <h1>🔍 Symptom Assessment</h1>
            <p>Patient: <b>{patient.get('name', 'Unknown')}</b>  •  Age: {patient.get('age', '—')}  
            •  Gender: {patient.get('gender', '—')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-header">🕐 Symptom Context</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        duration = st.selectbox(
            "How long have you had these symptoms?",
            [
                "Less than 24 hours",
                "1–3 days",
                "4–7 days",
                "1–2 weeks",
                "More than 2 weeks",
                "More than 1 month",
            ],
        )
        onset = st.selectbox(
            "How did the symptoms begin?",
            ["Sudden onset (within hours)", "Gradual onset (over days)", "Very gradual (over weeks)"],
        )
    with col2:
        severity = st.select_slider(
            "How severe are your symptoms overall?",
            options=["Mild", "Moderate", "Severe", "Very Severe"],
            value="Moderate",
        )
        travel = st.text_input(
            "Recent travel? (list countries/regions visited in last 30 days)",
            placeholder="e.g. Visited Northern Ghana, Ivory Coast",
        )

    st.markdown('<div class="section-header">✅ Select Your Symptoms</div>', unsafe_allow_html=True)
    st.info(
        "Tick **all symptoms** you are currently experiencing. "
        "You can also type a custom symptom below. "
        "Be as accurate as possible — more information leads to better analysis."
    )

    selected_symptoms = []

    for category, symptoms in SYMPTOM_CATEGORIES.items():
        with st.expander(f"**{category}**", expanded=True):
            cols = st.columns(2)
            for i, symptom in enumerate(symptoms):
                with cols[i % 2]:
                    if st.checkbox(symptom, key=f"sym_{symptom}"):
                        selected_symptoms.append(symptom)

    # Custom symptom input
    st.markdown('<div class="section-header">➕ Additional / Custom Symptoms</div>', unsafe_allow_html=True)
    custom_input = st.text_area(
        "Type any additional symptoms not listed above (one per line):",
        placeholder="e.g.\nUnusual rash on chest\nHiccups\nBitter taste in mouth",
        height=90,
    )
    if custom_input.strip():
        custom_list = [s.strip() for s in custom_input.strip().split("\n") if s.strip()]
        selected_symptoms.extend(custom_list)

    # Summary of selected symptoms
    st.markdown("---")
    if selected_symptoms:
        st.success(f"**{len(selected_symptoms)} symptoms selected.** Click below to run analysis.")
        with st.expander("View selected symptoms"):
            for s in selected_symptoms:
                st.markdown(f"• {s}")
    else:
        st.warning("Please select at least 2 symptoms to proceed.")

    col_a, col_b = st.columns([1, 3])
    with col_a:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "intake"
            st.rerun()
    with col_b:
        if st.button("🔬 Run Diagnostic Analysis", type="primary", use_container_width=True):
            if len(selected_symptoms) < 2:
                st.error("❌ Please select at least 2 symptoms for meaningful analysis.")
            else:
                with st.spinner("Analysing symptoms using weighted statistical models…"):
                    report = generate_report(
                        patient_info=patient,
                        selected_symptoms=selected_symptoms,
                        selected_risk_factors=patient.get("risk_factors", []),
                        symptom_duration=duration,
                        symptom_severity=severity,
                    )
                    report["travel_history"] = travel
                    report["onset"] = onset
                    st.session_state.report = report
                st.session_state.page = "results"
                st.rerun()


# ─────────────────────────────────────────────
# PAGE 3: Diagnostic Results
# ─────────────────────────────────────────────
def page_results():
    report = st.session_state.get("report")
    if not report or "error" in report:
        st.error(report.get("error", "No report found. Please start again."))
        if st.button("← Start Again"):
            st.session_state.page = "intake"
            st.rerun()
        return

    patient       = report["patient_info"]
    primary_name  = report["primary_disease"]
    primary_score = report["primary_score"]
    urgency_key   = report["primary_urgency"]
    urgency_info  = URGENCY_LEVELS[urgency_key]
    primary_data  = report["primary_data"]
    candidates    = report["candidates"]
    red_flags     = report["red_flags_present"]
    conf_label, conf_color = confidence_label(primary_score)

    # ── Banner ────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="cdss-banner">
            <h1>📊 Diagnostic Results</h1>
            <p>Patient: <b>{patient['name']}</b>  •  Age: {patient['age']}  
            •  Gender: {patient['gender']}  •  Date: {date.today().strftime('%d %B %Y')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Red Flag Alert ────────────────────────────────────────────────────
    if red_flags:
        st.markdown(
            f"""
            <div class="red-flag-box">
                <b>🚨 DANGER — Critical Symptoms Detected</b><br>
                The following symptoms require <b>IMMEDIATE emergency medical attention</b>:<br>
                {'  •  '.join(['<span style="color:#e74c3c"><b>' + s + '</b></span>' for s in red_flags])}
                <br><br>
                <b>Go to the nearest emergency department NOW or call emergency services.</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Four Metric Tiles ─────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""<div class="metric-tile">
                <div style="font-size:0.75rem;color:#666;">PRIMARY DIAGNOSIS</div>
                <div style="font-size:1.2rem;font-weight:700;color:#1a3c5e;">{primary_name}</div>
                <div style="font-size:0.7rem;color:#888;">ICD-10: {primary_data.get('icd10','')}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""<div class="metric-tile">
                <div style="font-size:0.75rem;color:#666;">MATCH SCORE</div>
                <div style="font-size:1.8rem;font-weight:700;color:{conf_color};">{primary_score:.1f}%</div>
                <div style="font-size:0.7rem;color:{conf_color};">{conf_label}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""<div class="metric-tile">
                <div style="font-size:0.75rem;color:#666;">SEVERITY</div>
                <div style="font-size:1.4rem;font-weight:700;color:#1a3c5e;">{primary_data['severity'].upper()}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f"""<div class="metric-tile">
                <div style="font-size:0.75rem;color:#666;">SYMPTOMS ANALYSED</div>
                <div style="font-size:1.8rem;font-weight:700;color:#1a3c5e;">{len(report['selected_symptoms'])}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Urgency Level ─────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="urgency-box" style="background:{urgency_info['color']};">
            {urgency_info['label']}
        </div>
        <p style="text-align:center;font-size:0.95rem;color:#333;">
            {urgency_info['description']}
        </p>
        """,
        unsafe_allow_html=True,
    )

    # ─────────────────────────────────────────────────────────────────────
    # TABS
    # ─────────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🦠 Diagnosis", "📈 Analysis Charts", "💊 Treatment Plan", "🚩 Red Flags", "📄 Patient Summary"]
    )

    # ══════════════════════════════════════════════════════════
    # TAB 1 — Diagnosis
    # ══════════════════════════════════════════════════════════
    with tab1:
        st.markdown('<div class="section-header">🏆 Primary Probable Diagnosis</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="disease-card">
                <h3 style="color:#1a3c5e;margin:0;">🦠 {primary_name}</h3>
                <small style="color:#888;">ICD-10: {primary_data.get('icd10','')} &nbsp;|&nbsp; 
                Severity: {primary_data['severity'].upper()} &nbsp;|&nbsp; 
                Confidence: <span style="color:{conf_color};font-weight:700;">{conf_label} ({primary_score:.1f}%)</span></small>
                <hr style="margin:10px 0;">
                <p>{primary_data['description']}</p>
                <b>Incubation Period:</b> {primary_data['incubation']}<br>
                <b>Transmission:</b> {primary_data['transmission']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Matching symptoms breakdown
        st.markdown('<div class="section-header">✅ Matching Symptoms Found</div>', unsafe_allow_html=True)
        primary_row = candidates[candidates["Disease"] == primary_name].iloc[0]
        matching    = primary_row["Matching Symptoms"]
        if matching:
            cols = st.columns(2)
            for i, sym in enumerate(matching):
                weight = primary_data["symptoms"].get(sym, 0)
                bar = "█" * weight + "░" * (10 - weight)
                with cols[i % 2]:
                    st.markdown(f"**• {sym}**  \n`{bar}` Weight: {weight}/10")
        else:
            st.info("No direct symptom matches found.")

        # Differential diagnoses
        st.markdown('<div class="section-header">📋 Differential Diagnoses (Top Candidates)</div>', unsafe_allow_html=True)
        st.markdown("Other conditions the symptom profile is consistent with:")

        for _, row in candidates.iterrows():
            cl, cc = confidence_label(row["Composite Score"])
            severity_colors = {"low": "#27ae60", "moderate": "#f39c12", "high": "#e67e22", "critical": "#e74c3c"}
            sev_color = severity_colors.get(row["Severity"], "#888")

            with st.expander(
                f"**{row['Disease']}** — Score: {row['Composite Score']:.1f}% ({cl})"
            ):
                c1, c2 = st.columns(2)
                c1.metric("Composite Score", f"{row['Composite Score']:.1f}%")
                c2.metric("Coverage", f"{row['Coverage (%)']}%")
                c1.metric("Specificity", f"{row['Specificity (%)']}%")
                c2.metric("Severity", row["Severity"].upper())
                st.progress(min(int(row["Composite Score"]), 100))
                if row["Matching Symptoms"]:
                    st.markdown("**Matched symptoms:** " + ", ".join(row["Matching Symptoms"]))
                if row["Missing Required"]:
                    st.warning("**Missing required symptoms:** " + ", ".join(row["Missing Required"]))

    # ══════════════════════════════════════════════════════════
    # TAB 2 — Analysis Charts
    # ══════════════════════════════════════════════════════════
    with tab2:
        st.markdown('<div class="section-header">📊 Diagnostic Score Comparison</div>', unsafe_allow_html=True)

        plot_df = candidates.head(8).copy()
        plot_df["Color"] = [
            "#e30abb" if i == 0 else "#2980b9" if i < 3 else "#7fb3d3"
            for i in range(len(plot_df))
        ]

        fig_bar = go.Figure(
            go.Bar(
                x=plot_df["Composite Score"],
                y=plot_df["Disease"],
                orientation="h",
                marker_color=plot_df["Color"],
                text=[f"{s:.1f}%" for s in plot_df["Composite Score"]],
                textposition="outside",
            )
        )
        fig_bar.update_layout(
            title="Weighted Composite Diagnostic Scores",
            xaxis_title="Composite Score (%)",
            yaxis_title="Disease",
            height=380,
            plot_bgcolor="#f8f9fa",
            paper_bgcolor="#ffffff",
            xaxis=dict(range=[0, 110]),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Radar chart — symptom coverage vs specificity
        st.markdown('<div class="section-header">🕸️ Coverage vs Specificity Radar</div>', unsafe_allow_html=True)

        top3 = candidates.head(3)
        categories = ["Coverage (%)", "Specificity (%)", "Composite Score"]
        fig_radar = go.Figure()
        colors_r = ["#1a3c5e", "#2980b9", "#85c1e9"]
        for i, (_, row) in enumerate(top3.iterrows()):
            vals = [row["Coverage (%)"], row["Specificity (%)"], row["Composite Score"]]
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=vals + [vals[0]],
                    theta=categories + [categories[0]],
                    name=row["Disease"],
                    line_color=colors_r[i],
                    fill="toself",
                    fillcolor=colors_r[i],
                    opacity=0.25,
                )
            )
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            height=380,
            title="Top 3 Diagnoses — Multi-Dimensional Comparison",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Symptom frequency chart
        st.markdown('<div class="section-header">🔬 Symptom Specificity Analysis</div>', unsafe_allow_html=True)
        freq_df = report["freq_table"]
        if not freq_df.empty:
            color_map = {"High": "#e74c3c", "Moderate": "#f39c12", "Low": "#27ae60"}
            fig_freq = px.bar(
                freq_df,
                x="Diseases Associated",
                y="Symptom",
                orientation="h",
                color="Specificity",
                color_discrete_map=color_map,
                title="How Many Diseases Each Symptom is Associated With",
                labels={"Diseases Associated": "No. of Diseases", "Symptom": ""},
            )
            fig_freq.update_layout(height=max(300, len(freq_df) * 30), plot_bgcolor="#f8f9fa")
            st.plotly_chart(fig_freq, use_container_width=True)
            st.caption(
                "🔴 High = fewer diseases → more specific  •  "
                "🟡 Moderate  •  🟢 Low = many diseases → less specific"
            )

        # Heatmap
        matrix = report.get("matrix")
        if matrix is not None and not matrix.empty:
            st.markdown('<div class="section-header">🗺️ Symptom–Disease Weight Heatmap</div>', unsafe_allow_html=True)
            fig_heat = px.imshow(
                matrix,
                color_continuous_scale="Blues",
                title="Symptom Weight per Disease (0 = absent, 10 = strongly associated)",
                labels=dict(x="Disease", y="Symptom", color="Weight"),
                aspect="auto",
            )
            fig_heat.update_layout(height=max(350, len(matrix) * 30 + 100))
            st.plotly_chart(fig_heat, use_container_width=True)

        # Pie — severity distribution of candidates
        st.markdown('<div class="section-header">📐 Severity Distribution of Candidates</div>', unsafe_allow_html=True)
        sev_counts = candidates["Severity"].value_counts().reset_index()
        sev_counts.columns = ["Severity", "Count"]
        sev_colors = {"low": "#27ae60", "moderate": "#f39c12", "high": "#e67e22", "critical": "#e74c3c"}
        fig_pie = px.pie(
            sev_counts,
            names="Severity",
            values="Count",
            color="Severity",
            color_discrete_map=sev_colors,
            title="Severity Distribution of Differential Diagnoses",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ══════════════════════════════════════════════════════════
    # TAB 3 — Treatment Plan
    # ══════════════════════════════════════════════════════════
    with tab3:
        st.markdown(
            f'<div class="section-header">🩺 Recommended Action — {urgency_info["label"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="urgency-box" style="background:{urgency_info['color']}; font-size:1rem;">
                {urgency_info['description']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Self-care / Home Remedies
        st.markdown('<div class="section-header">🏠 Home Care & Self-Treatment</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="care-card"><b>These measures are safe to start immediately at home:</b><br>',
            unsafe_allow_html=True,
        )
        for i, item in enumerate(primary_data["self_care"], 1):
            st.markdown(f"**{i}.** {item}")
        st.markdown("</div>", unsafe_allow_html=True)

        # Pharmacy / OTC drugs
        st.markdown('<div class="section-header">💊 Pharmacy / Over-the-Counter Medications</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="pharmacy-card"><b>Available without prescription — consult your pharmacist:</b><br>',
            unsafe_allow_html=True,
        )
        for item in primary_data["pharmacy_drugs"]:
            st.markdown(f"• {item}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.warning(
            "⚠️ Always inform your pharmacist about allergies and current medications. "
            "Do not exceed recommended doses."
        )

        if patient.get("allergies"):
            st.error(
                f"🚫 **Documented Allergies:** {patient['allergies']} — "
                "Confirm with pharmacist before taking any medication."
            )

        # Doctor treatments
        st.markdown('<div class="section-header">🏥 Medical / Clinical Treatments</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="doctor-card"><b>Treatments typically provided by a healthcare professional:</b><br>',
            unsafe_allow_html=True,
        )
        for item in primary_data["doctor_treatment"]:
            st.markdown(f"• {item}")
        st.markdown("</div>", unsafe_allow_html=True)

        # Transmission / Prevention
        st.markdown('<div class="section-header">🛡️ Prevention & Infection Control</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Transmission:** {primary_data['transmission']}")
        with col2:
            st.info(f"**Incubation Period:** {primary_data['incubation']}")

    # ══════════════════════════════════════════════════════════
    # TAB 4 — Red Flags
    # ══════════════════════════════════════════════════════════
    with tab4:
        st.markdown('<div class="section-header">🚨 Red Flag Symptoms — Seek Emergency Care</div>', unsafe_allow_html=True)

        if red_flags:
            st.error(
                f"🔴 **{len(red_flags)} critical symptom(s) detected in your report.** "
                "Seek emergency care immediately."
            )
            for rf in red_flags:
                st.markdown(f"🔴 **{rf}**")
        else:
            st.success("✅ No globally critical symptoms detected in your current selection.")

        st.markdown("---")
        st.markdown("### ⚠️ Red Flag Symptoms for Probable Diagnosis")
        st.markdown(f"**If you develop any of the following symptoms with {primary_name}, go to the emergency room immediately:**")

        for flag in primary_data["red_flags"]:
            st.markdown(
                f"""
                <div class="red-flag-box">
                    🚩 {flag}
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Follow-up timeline
        st.markdown('<div class="section-header">📅 Follow-Up Timeline</div>', unsafe_allow_html=True)
        timeline = {
            "home_care": "Monitor at home for 5–7 days. Return if symptoms worsen.",
            "pharmacy": "If no improvement in 3–5 days after OTC treatment, visit a clinic.",
            "clinic": "See a doctor within 24–48 hours for examination and testing.",
            "emergency": "Go to the emergency department NOW — do not wait.",
        }
        st.info(f"**Recommended timeline:** {timeline[urgency_key]}")

    # ══════════════════════════════════════════════════════════
    # TAB 5 — Patient Summary
    # ══════════════════════════════════════════════════════════
    with tab5:
        st.markdown('<div class="section-header">📄 Patient Information Summary</div>', unsafe_allow_html=True)

        info_df = pd.DataFrame(
            {
                "Field": [
                    "Full Name", "Date of Birth", "Age", "Gender", "Nationality",
                    "Occupation", "Blood Group", "Weight (kg)", "Height (cm)",
                    "BMI", "Contact", "Address",
                ],
                "Value": [
                    patient.get("name", "—"),
                    patient.get("dob", "—"),
                    f"{patient.get('age', '—')} years",
                    patient.get("gender", "—"),
                    patient.get("nationality", "—"),
                    patient.get("occupation", "—") or "Not specified",
                    patient.get("blood_group", "—"),
                    patient.get("weight_kg", "—"),
                    patient.get("height_cm", "—"),
                    patient.get("bmi", "—"),
                    patient.get("contact", "—") or "Not provided",
                    patient.get("address", "—") or "Not provided",
                ],
            }
        )
        st.dataframe(info_df, use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Allergies:**")
            st.info(patient.get("allergies") or "None reported")
            st.markdown("**Current Medications:**")
            st.info(patient.get("current_medications") or "None reported")
        with col2:
            st.markdown("**Chronic Conditions:**")
            st.info(patient.get("chronic_conditions") or "None reported")
            st.markdown("**Vaccinations (last 12 months):**")
            st.info(patient.get("vaccinations") or "None reported")

        st.markdown("**Risk Factors:**")
        for rf in patient.get("risk_factors", []):
            st.markdown(f"• {rf}")

        st.markdown('<div class="section-header">🔬 Symptom Report</div>', unsafe_allow_html=True)
        st.markdown(f"**Duration:** {report['symptom_duration']}  &nbsp;|&nbsp;  **Severity:** {report['symptom_severity']}  &nbsp;|&nbsp;  **Onset:** {report.get('onset', '—')}")
        st.markdown(f"**Travel History:** {report.get('travel_history', 'None specified') or 'None specified'}")
        st.markdown("**Reported Symptoms:**")
        sym_col = st.columns(2)
        for i, s in enumerate(report["selected_symptoms"]):
            with sym_col[i % 2]:
                st.markdown(f"✔ {s}")

        st.markdown("---")
        st.markdown(
            '<div class="disclaimer-box">' + DISCLAIMER.replace("\n", " ") + "</div>",
            unsafe_allow_html=True,
        )

    # ── Navigation buttons ────────────────────────────────────────────────
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("← Edit Symptoms", use_container_width=True):
            st.session_state.page = "symptoms"
            st.rerun()
    with c2:
        if st.button("🔄 New Patient", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with c3:
        # Download report as CSV
        csv = report["scores_df"][
            ["Disease", "ICD-10", "Composite Score", "Coverage (%)", "Specificity (%)", "Severity", "Urgency"]
        ].to_csv(index=False)
        st.download_button(
            label="⬇ Download Scores (CSV)",
            data=csv,
            file_name=f"cdss_report_{patient.get('name','patient').replace(' ','_')}_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
        )


# ─────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────
def main():
    render_sidebar()

    page = st.session_state.get("page", "intake")
    if page == "intake":
        page_intake()
    elif page == "symptoms":
        page_symptoms()
    elif page == "results":
        page_results()


if __name__ == "__main__":
    main()
