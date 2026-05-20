# ============================================================
# CDSS - Analysis Engine
# Pure data-analysis-based diagnostic reasoning (no ML)
# ============================================================

import pandas as pd
import numpy as np
from disease_data import DISEASES, RISK_FACTORS, URGENCY_LEVELS


# ─────────────────────────────────────────────
# 1.  Core scoring function
# ─────────────────────────────────────────────

def compute_disease_scores(selected_symptoms: list[str]) -> pd.DataFrame:
    """
    For every disease in the knowledge-base, compute a weighted match score
    based on the symptoms the user reported.

    Scoring logic (pure statistics / rule-based):
      • Base score  = sum of weights for matching symptoms
      • Coverage    = proportion of the disease's symptoms that were reported
      • Match ratio = proportion of reported symptoms that belong to this disease
      • Penalty     = applied when a required symptom is absent
      • Bonus       = applied when highly-specific symptoms are present
      • Exclusion   = large negative weight when an exclusion symptom is present

    The final composite score is normalised to 0–100.
    """
    if not selected_symptoms:
        return pd.DataFrame()

    records = []
    selected_set = set(selected_symptoms)

    for disease_name, disease in DISEASES.items():
        symptom_weights: dict = disease["symptoms"]
        required: list       = disease.get("required", [])
        exclusions: list     = disease.get("exclusions", [])

        # ── Exclusion check ──────────────────────────────────────────────
        exclusion_hits = [s for s in exclusions if s in selected_set]
        exclusion_penalty = len(exclusion_hits) * 15  # heavy penalty per exclusion

        # ── Required symptom check ───────────────────────────────────────
        missing_required = [s for s in required if s not in selected_set]
        required_penalty = len(missing_required) * 12  # penalty per missing required symptom

        # ── Base weighted score ──────────────────────────────────────────
        matching_symptoms = {s: w for s, w in symptom_weights.items() if s in selected_set}
        base_score = sum(matching_symptoms.values())
        max_possible = sum(symptom_weights.values())

        # ── Coverage ratio (how many of the disease's symptoms were reported) ──
        coverage = len(matching_symptoms) / len(symptom_weights) if symptom_weights else 0

        # ── Match specificity (how many reported symptoms belong to this disease) ─
        match_specificity = len(matching_symptoms) / len(selected_symptoms) if selected_symptoms else 0

        # ── Normalised base score ────────────────────────────────────────
        normalised = (base_score / max_possible * 100) if max_possible > 0 else 0

        # ── Composite score formula ──────────────────────────────────────
        composite = (
            normalised * 0.50
            + coverage * 100 * 0.25
            + match_specificity * 100 * 0.25
            - exclusion_penalty
            - required_penalty
        )
        composite = max(0.0, composite)  # floor at 0

        # ── High-weight symptom bonus ─────────────────────────────────────
        high_weight_matches = [s for s, w in matching_symptoms.items() if w >= 8]
        bonus = len(high_weight_matches) * 3
        composite = min(100.0, composite + bonus)

        records.append(
            {
                "Disease": disease_name,
                "ICD-10": disease.get("icd10", ""),
                "Raw Score": base_score,
                "Max Score": max_possible,
                "Composite Score": round(composite, 2),
                "Coverage (%)": round(coverage * 100, 1),
                "Specificity (%)": round(match_specificity * 100, 1),
                "Matching Symptoms": list(matching_symptoms.keys()),
                "Matching Count": len(matching_symptoms),
                "Missing Required": missing_required,
                "Exclusion Hits": exclusion_hits,
                "Severity": disease["severity"],
                "Urgency": disease["urgency"],
                "Description": disease["description"],
                "Incubation": disease["incubation"],
                "Transmission": disease["transmission"],
                "Self Care": disease["self_care"],
                "Pharmacy Drugs": disease["pharmacy_drugs"],
                "Doctor Treatment": disease["doctor_treatment"],
                "Red Flags": disease["red_flags"],
            }
        )

    df = pd.DataFrame(records)
    df = df.sort_values("Composite Score", ascending=False).reset_index(drop=True)
    return df


# ─────────────────────────────────────────────
# 2.  Urgency adjuster (risk factors)
# ─────────────────────────────────────────────

URGENCY_ORDER = ["home_care", "pharmacy", "clinic", "emergency"]


def escalate_urgency(base_urgency: str, risk_factors: list[str]) -> str:
    """Escalate urgency level if the patient has high-risk factors."""
    high_risk = [rf for rf in risk_factors if RISK_FACTORS.get(rf) == "high"]
    moderate_risk = [rf for rf in risk_factors if RISK_FACTORS.get(rf) == "moderate"]

    idx = URGENCY_ORDER.index(base_urgency)

    if high_risk and idx < len(URGENCY_ORDER) - 1:
        idx = min(idx + 1, len(URGENCY_ORDER) - 1)
    elif moderate_risk and base_urgency == "home_care":
        idx = min(idx + 1, len(URGENCY_ORDER) - 1)

    return URGENCY_ORDER[idx]


# ─────────────────────────────────────────────
# 3.  Confidence label helper
# ─────────────────────────────────────────────

def confidence_label(score: float) -> tuple[str, str]:
    """Return a human-readable confidence label and colour."""
    if score >= 70:
        return "High Confidence", "#27ae60"
    elif score >= 45:
        return "Moderate Confidence", "#f39c12"
    elif score >= 20:
        return "Low Confidence", "#e67e22"
    else:
        return "Very Low / Unlikely", "#e74c3c"


# ─────────────────────────────────────────────
# 4.  Red-flag detector
# ─────────────────────────────────────────────

GLOBAL_RED_FLAG_SYMPTOMS = {
    "Seizures",
    "Confusion / disorientation",
    "Shortness of breath",
    "Bleeding gums / nose",
    "Blood in stool",
    "Blood in urine",
    "Stiff neck",
    "Red spots / petechiae",
    "Chest pain / tightness",
}


def check_red_flags(selected_symptoms: list[str]) -> list[str]:
    """Return any globally dangerous symptoms the user has reported."""
    return [s for s in selected_symptoms if s in GLOBAL_RED_FLAG_SYMPTOMS]


# ─────────────────────────────────────────────
# 5.  Summary statistics for charts
# ─────────────────────────────────────────────

def symptom_frequency_table(selected_symptoms: list[str]) -> pd.DataFrame:
    """
    For each selected symptom, calculate how many diseases in the
    knowledge-base include it and the average weight.
    """
    rows = []
    for symptom in selected_symptoms:
        diseases_with = [
            (name, d["symptoms"][symptom])
            for name, d in DISEASES.items()
            if symptom in d["symptoms"]
        ]
        count = len(diseases_with)
        avg_weight = np.mean([w for _, w in diseases_with]) if diseases_with else 0
        rows.append(
            {
                "Symptom": symptom,
                "Diseases Associated": count,
                "Average Weight": round(avg_weight, 1),
                "Specificity": "High" if count <= 3 else ("Moderate" if count <= 6 else "Low"),
            }
        )
    return pd.DataFrame(rows).sort_values("Diseases Associated")


def build_symptom_disease_matrix(selected_symptoms: list[str]) -> pd.DataFrame:
    """
    Build a presence/absence matrix:
    Rows = selected symptoms, Columns = top diseases.
    Used for heatmap visualisation.
    """
    scores_df = compute_disease_scores(selected_symptoms)
    top_diseases = scores_df[scores_df["Composite Score"] > 10].head(8)["Disease"].tolist()

    matrix = {}
    for disease in top_diseases:
        disease_data = DISEASES[disease]
        col = []
        for symptom in selected_symptoms:
            weight = disease_data["symptoms"].get(symptom, 0)
            col.append(weight)
        matrix[disease] = col

    return pd.DataFrame(matrix, index=selected_symptoms)


# ─────────────────────────────────────────────
# 6.  Final diagnostic report generator
# ─────────────────────────────────────────────

def generate_report(
    patient_info: dict,
    selected_symptoms: list[str],
    selected_risk_factors: list[str],
    symptom_duration: str,
    symptom_severity: str,
) -> dict:
    """
    Master function that combines all analysis into a structured report dict.
    """
    scores_df = compute_disease_scores(selected_symptoms)

    if scores_df.empty or scores_df["Composite Score"].max() < 5:
        return {"error": "Insufficient symptoms to generate a diagnosis. Please select more symptoms."}

    # Top 5 candidate diseases with score > 5
    candidates = scores_df[scores_df["Composite Score"] > 5].head(5)

    # Primary diagnosis
    primary = candidates.iloc[0]
    primary_urgency = escalate_urgency(primary["Urgency"], selected_risk_factors)

    # Red flags
    red_flags_present = check_red_flags(selected_symptoms)
    if red_flags_present:
        primary_urgency = "emergency"

    # Severity modifier from duration
    if symptom_duration in ("More than 2 weeks", "More than 1 month"):
        primary_urgency = escalate_urgency(primary_urgency, ["Age over 60 years"])  # escalate once

    # Build symptom frequency table
    freq_table = symptom_frequency_table(selected_symptoms)

    # Heatmap matrix
    try:
        matrix = build_symptom_disease_matrix(selected_symptoms)
    except Exception:
        matrix = pd.DataFrame()

    return {
        "patient_info": patient_info,
        "selected_symptoms": selected_symptoms,
        "selected_risk_factors": selected_risk_factors,
        "symptom_duration": symptom_duration,
        "symptom_severity": symptom_severity,
        "scores_df": scores_df,
        "candidates": candidates,
        "primary_disease": primary["Disease"],
        "primary_score": primary["Composite Score"],
        "primary_urgency": primary_urgency,
        "primary_data": DISEASES[primary["Disease"]],
        "red_flags_present": red_flags_present,
        "freq_table": freq_table,
        "matrix": matrix,
    }
