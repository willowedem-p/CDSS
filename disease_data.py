# ============================================================
# CDSS - Clinical Decision Support System
# Disease Knowledge Base & Symptom Data
# ============================================================

# All symptoms available for selection, grouped by category
SYMPTOM_CATEGORIES = {
    "Fever & Temperature": [
        "High fever (>38.5°C / 101.3°F)",
        "Low-grade fever (37.5–38.5°C)",
        "Chills and rigors",
        "Night sweats",
        "Sweating episodes",
    ],
    "Respiratory": [
        "Dry cough",
        "Productive cough (with mucus)",
        "Shortness of breath",
        "Chest pain / tightness",
        "Wheezing",
        "Sore throat",
        "Runny nose",
        "Nasal congestion",
        "Loss of smell or taste",
        "Difficulty swallowing",
    ],
    "Gastrointestinal": [
        "Nausea",
        "Vomiting",
        "Diarrhea",
        "Abdominal pain / cramping",
        "Bloating",
        "Loss of appetite",
        "Blood in stool",
        "Jaundice (yellowing of skin/eyes)",
    ],
    "Neurological": [
        "Headache",
        "Severe headache / migraine",
        "Stiff neck",
        "Confusion / disorientation",
        "Seizures",
        "Sensitivity to light (photophobia)",
        "Sensitivity to sound (phonophobia)",
        "Dizziness",
    ],
    "Skin & Musculoskeletal": [
        "Skin rash",
        "Itchy skin",
        "Red spots / petechiae",
        "Joint pain",
        "Muscle aches and pains",
        "Body weakness / fatigue",
        "Swollen lymph nodes",
        "Eye redness / conjunctivitis",
    ],
    "Urinary & Reproductive": [
        "Painful urination",
        "Frequent urination",
        "Blood in urine",
        "Genital sores / discharge",
        "Lower back / flank pain",
    ],
    "General / Other": [
        "Extreme fatigue / malaise",
        "Weight loss (unintentional)",
        "Dehydration signs",
        "Ear pain",
        "Swollen face / parotid gland",
        "Bleeding gums / nose",
        "Dark urine",
        "Pale-coloured stools",
    ],
}

# Flat list of all symptoms
ALL_SYMPTOMS = [s for group in SYMPTOM_CATEGORIES.values() for s in group]

# ============================================================
# DISEASE DATABASE
# Each disease has:
#   - symptoms: dict of {symptom: weight (0-10)}
#   - required: list of symptoms that MUST be present for consideration
#   - exclusions: list of symptoms that strongly argue AGAINST this disease
#   - description: plain-language description
#   - severity: "low" | "moderate" | "high" | "critical"
#   - urgency: "home_care" | "pharmacy" | "clinic" | "emergency"
#   - incubation: incubation period string
#   - transmission: how it spreads
#   - self_care: list of home remedy / OTC recommendations
#   - pharmacy_drugs: list of OTC medications
#   - doctor_treatment: standard medical treatments
#   - red_flags: symptoms that should trigger immediate emergency care
#   - icd10: ICD-10 code
# ============================================================

DISEASES = {
    "Malaria": {
        "icd10": "B54",
        "description": (
            "A life-threatening parasitic infection transmitted by Anopheles mosquitoes. "
            "Causes cyclical fever, chills, and flu-like symptoms. Common in tropical regions."
        ),
        "symptoms": {
            "High fever (>38.5°C / 101.3°F)": 10,
            "Chills and rigors": 9,
            "Sweating episodes": 8,
            "Headache": 7,
            "Muscle aches and pains": 6,
            "Nausea": 5,
            "Vomiting": 5,
            "Extreme fatigue / malaise": 6,
            "Jaundice (yellowing of skin/eyes)": 5,
            "Diarrhea": 3,
            "Abdominal pain / cramping": 4,
            "Confusion / disorientation": 4,
            "Loss of appetite": 4,
            "Dark urine": 5,
        },
        "required": ["High fever (>38.5°C / 101.3°F)", "Chills and rigors"],
        "exclusions": ["Skin rash", "Stiff neck", "Runny nose"],
        "severity": "high",
        "urgency": "clinic",
        "incubation": "7–30 days (varies by Plasmodium species)",
        "transmission": "Bite of infected female Anopheles mosquito",
        "self_care": [
            "Rest in a cool, well-ventilated room",
            "Stay hydrated — drink water, ORS (Oral Rehydration Salts), or coconut water",
            "Use a wet cloth on the forehead to bring down fever",
            "Sleep under insecticide-treated mosquito nets",
            "Wear long-sleeved clothing to prevent further bites",
            "Do NOT take chloroquine or artemisinin without a confirmed diagnosis",
        ],
        "pharmacy_drugs": [
            "Paracetamol (500–1000 mg every 6–8 hrs) for fever relief",
            "ORS sachets for rehydration if vomiting or diarrhea present",
        ],
        "doctor_treatment": [
            "Rapid Diagnostic Test (RDT) or blood smear microscopy for confirmation",
            "Artemisinin-based Combination Therapy (ACT) — e.g., Artemether-Lumefantrine",
            "IV Artesunate for severe/cerebral malaria",
            "Primaquine for P. vivax/ovale (radical cure)",
        ],
        "red_flags": [
            "Seizures or loss of consciousness",
            "Severe confusion / inability to walk",
            "Very dark or cola-coloured urine (blackwater fever)",
            "Breathing difficulty",
            "Unable to keep fluids down",
        ],
    },

    "Typhoid Fever": {
        "icd10": "A01.0",
        "description": (
            "A systemic bacterial infection caused by Salmonella typhi. "
            "Spread through contaminated food and water. Characterised by prolonged fever "
            "and gastrointestinal symptoms."
        ),
        "symptoms": {
            "High fever (>38.5°C / 101.3°F)": 9,
            "Headache": 7,
            "Abdominal pain / cramping": 8,
            "Loss of appetite": 7,
            "Nausea": 6,
            "Diarrhea": 5,
            "Extreme fatigue / malaise": 7,
            "Skin rash": 4,
            "Chills and rigors": 4,
            "Vomiting": 4,
            "Bloating": 5,
            "Blood in stool": 3,
            "Sweating episodes": 4,
            "Confusion / disorientation": 3,
        },
        "required": ["High fever (>38.5°C / 101.3°F)"],
        "exclusions": ["Runny nose", "Dry cough", "Stiff neck"],
        "severity": "high",
        "urgency": "clinic",
        "incubation": "6–30 days (usually 8–14 days)",
        "transmission": "Contaminated food or water; faecal-oral route",
        "self_care": [
            "Drink only boiled or bottled water",
            "Eat soft, easily digestible foods (rice porridge, bananas, boiled potatoes)",
            "Rest completely — avoid strenuous activity",
            "Maintain strict hand hygiene before eating and after toilet use",
            "Avoid raw vegetables and street food during illness",
            "Use ORS if experiencing diarrhea or vomiting",
        ],
        "pharmacy_drugs": [
            "Paracetamol for fever and headache management",
            "ORS sachets to maintain hydration",
            "Avoid ibuprofen/aspirin (risk of gastrointestinal bleeding)",
        ],
        "doctor_treatment": [
            "Blood culture or Widal test for diagnosis",
            "Ciprofloxacin or Azithromycin (first-line antibiotics)",
            "Ceftriaxone IV for severe cases or resistant strains",
            "Hospitalisation if complications suspected",
        ],
        "red_flags": [
            "Intestinal perforation (sudden severe abdominal pain)",
            "Bright red blood in stool",
            "Persistent high fever beyond 7 days despite treatment",
            "Severe confusion or altered consciousness",
            "Inability to take oral fluids",
        ],
    },

    "COVID-19": {
        "icd10": "U07.1",
        "description": (
            "A respiratory illness caused by the SARS-CoV-2 coronavirus. "
            "Ranges from mild cold-like symptoms to severe pneumonia. "
            "Highly contagious via respiratory droplets."
        ),
        "symptoms": {
            "High fever (>38.5°C / 101.3°F)": 7,
            "Low-grade fever (37.5–38.5°C)": 6,
            "Dry cough": 9,
            "Shortness of breath": 8,
            "Loss of smell or taste": 10,
            "Extreme fatigue / malaise": 8,
            "Headache": 6,
            "Muscle aches and pains": 6,
            "Sore throat": 5,
            "Nasal congestion": 4,
            "Diarrhea": 4,
            "Chest pain / tightness": 7,
            "Chills and rigors": 4,
            "Nausea": 3,
            "Confusion / disorientation": 3,
        },
        "required": [],
        "exclusions": ["Jaundice (yellowing of skin/eyes)", "Stiff neck", "Blood in stool"],
        "severity": "moderate",
        "urgency": "clinic",
        "incubation": "2–14 days (average 5–6 days)",
        "transmission": "Respiratory droplets, aerosols, contact with contaminated surfaces",
        "self_care": [
            "Isolate at home immediately — avoid contact with others",
            "Rest and sleep as much as possible",
            "Stay well-hydrated (water, warm soups, herbal teas with honey)",
            "Gargle with warm salt water for sore throat",
            "Steam inhalation to relieve nasal congestion",
            "Monitor oxygen saturation with a pulse oximeter if available",
            "Ventilate your room — open windows for fresh air",
        ],
        "pharmacy_drugs": [
            "Paracetamol (500–1000 mg every 6 hrs) for fever and pain",
            "Vitamin C (500–1000 mg daily) and Zinc supplements",
            "Nasal saline spray for congestion",
            "Antihistamines for runny nose if needed",
            "Avoid aspirin and strong NSAIDs",
        ],
        "doctor_treatment": [
            "PCR or Rapid Antigen Test for confirmation",
            "Antivirals: Nirmatrelvir/Ritonavir (Paxlovid) for high-risk patients",
            "Dexamethasone for hospitalised patients needing oxygen",
            "Supplemental oxygen / mechanical ventilation for severe cases",
            "Remdesivir IV for hospitalised patients",
        ],
        "red_flags": [
            "Oxygen saturation below 94% (SpO2 <94%)",
            "Persistent chest pain or pressure",
            "Inability to complete a sentence without breathlessness",
            "Blue lips or fingertips (cyanosis)",
            "Confusion or inability to stay awake",
        ],
    },

    "Influenza (Flu)": {
        "icd10": "J11.1",
        "description": (
            "A contagious respiratory illness caused by influenza viruses A or B. "
            "Typically seasonal, with sudden onset of fever, body aches, and respiratory symptoms."
        ),
        "symptoms": {
            "High fever (>38.5°C / 101.3°F)": 8,
            "Muscle aches and pains": 9,
            "Headache": 8,
            "Extreme fatigue / malaise": 8,
            "Dry cough": 7,
            "Chills and rigors": 7,
            "Sore throat": 6,
            "Nasal congestion": 5,
            "Runny nose": 5,
            "Loss of appetite": 5,
            "Nausea": 4,
            "Vomiting": 3,
            "Shortness of breath": 3,
        },
        "required": ["High fever (>38.5°C / 101.3°F)", "Muscle aches and pains"],
        "exclusions": ["Loss of smell or taste", "Jaundice (yellowing of skin/eyes)", "Diarrhea"],
        "severity": "moderate",
        "urgency": "pharmacy",
        "incubation": "1–4 days",
        "transmission": "Respiratory droplets when coughing, sneezing, or talking",
        "self_care": [
            "Rest at home and avoid going to work or school",
            "Drink plenty of warm fluids (water, broth, herbal teas)",
            "Honey and ginger tea to soothe throat and reduce cough",
            "Use a humidifier or steam inhalation for congestion",
            "Gargle with warm salt water",
            "Apply warm compress for muscle/joint aches",
            "Ensure warm room temperature and comfortable clothing",
        ],
        "pharmacy_drugs": [
            "Paracetamol or Ibuprofen for fever and body aches",
            "Decongestants (pseudoephedrine) for nasal congestion",
            "Cough suppressants (dextromethorphan) for dry cough",
            "Expectorants (guaifenesin) if producing mucus",
            "Multivitamins with Vitamin C and Zinc",
        ],
        "doctor_treatment": [
            "Rapid influenza diagnostic test (RIDT) for confirmation",
            "Oseltamivir (Tamiflu) — most effective within 48 hrs of symptom onset",
            "Zanamivir (Relenza) as alternative antiviral",
            "Antiviral prophylaxis for high-risk contacts",
        ],
        "red_flags": [
            "Difficulty breathing or rapid breathing",
            "Persistent chest pain",
            "Confusion or altered mental state",
            "Severe vomiting leading to dehydration",
            "Symptoms improve then return with high fever and worse cough",
        ],
    },

    "Tuberculosis (TB)": {
        "icd10": "A15.9",
        "description": (
            "A chronic bacterial infection caused by Mycobacterium tuberculosis. "
            "Primarily affects the lungs but can spread to other organs. "
            "Major public health concern in Sub-Saharan Africa."
        ),
        "symptoms": {
            "Productive cough (with mucus)": 9,
            "Night sweats": 9,
            "Weight loss (unintentional)": 9,
            "Extreme fatigue / malaise": 8,
            "Low-grade fever (37.5–38.5°C)": 7,
            "High fever (>38.5°C / 101.3°F)": 5,
            "Chest pain / tightness": 6,
            "Blood in stool": 2,
            "Loss of appetite": 7,
            "Shortness of breath": 5,
            "Swollen lymph nodes": 5,
            "Chills and rigors": 4,
        },
        "required": ["Productive cough (with mucus)", "Night sweats"],
        "exclusions": ["Runny nose", "Nasal congestion", "Loss of smell or taste", "Diarrhea"],
        "severity": "high",
        "urgency": "clinic",
        "incubation": "2–12 weeks (primary infection); reactivation can occur years later",
        "transmission": "Airborne droplets from coughing or sneezing by an infected person",
        "self_care": [
            "Cover mouth and nose with tissue or elbow when coughing",
            "Ensure good ventilation in living areas — open windows",
            "Eat nutritious, high-protein meals to support immunity",
            "Avoid alcohol and smoking completely",
            "Rest adequately — avoid strenuous activity",
            "Adhere strictly to prescribed medication (DO NOT self-medicate TB)",
        ],
        "pharmacy_drugs": [
            "No OTC drugs treat TB — antibiotics require prescription",
            "Paracetamol for fever management while awaiting diagnosis",
            "Nutritional supplements (Vitamin B6 / Pyridoxine) alongside TB drugs",
        ],
        "doctor_treatment": [
            "Sputum smear microscopy and GeneXpert test",
            "Chest X-ray",
            "6-month DOTS therapy: Isoniazid, Rifampicin, Pyrazinamide, Ethambutol",
            "Directly Observed Therapy Short-course (DOTS) programme",
            "Drug Susceptibility Testing for MDR-TB",
        ],
        "red_flags": [
            "Coughing up blood (haemoptysis)",
            "Severe difficulty breathing",
            "Sudden chest pain",
            "Rapid weight loss with night sweats lasting over 3 weeks",
            "Confusion or altered consciousness",
        ],
    },

    "Dengue Fever": {
        "icd10": "A90",
        "description": (
            "A mosquito-borne viral infection caused by the dengue virus. "
            "Transmitted by Aedes mosquitoes. Common in tropical and subtropical regions. "
            "Characterised by high fever, severe body pains, and rash."
        ),
        "symptoms": {
            "High fever (>38.5°C / 101.3°F)": 10,
            "Severe headache / migraine": 8,
            "Joint pain": 9,
            "Muscle aches and pains": 9,
            "Eye redness / conjunctivitis": 7,
            "Skin rash": 8,
            "Nausea": 6,
            "Vomiting": 6,
            "Extreme fatigue / malaise": 7,
            "Bleeding gums / nose": 7,
            "Red spots / petechiae": 8,
            "Abdominal pain / cramping": 5,
            "Chills and rigors": 4,
        },
        "required": ["High fever (>38.5°C / 101.3°F)", "Joint pain"],
        "exclusions": ["Runny nose", "Stiff neck", "Loss of smell or taste"],
        "severity": "high",
        "urgency": "clinic",
        "incubation": "4–10 days after mosquito bite",
        "transmission": "Bite of Aedes aegypti or Aedes albopictus mosquito",
        "self_care": [
            "Rest completely — dengue causes extreme fatigue",
            "Drink plenty of fluids: water, coconut water, ORS, papaya leaf juice",
            "Take cool sponge baths to manage high fever",
            "Apply insect repellent and sleep under mosquito nets",
            "Monitor platelet levels if test available",
            "Eat light, easily digestible foods",
        ],
        "pharmacy_drugs": [
            "Paracetamol ONLY for fever — NEVER take Aspirin or Ibuprofen (risk of bleeding)",
            "ORS sachets for rehydration",
            "Papaya leaf extract tablets (may help support platelet count)",
        ],
        "doctor_treatment": [
            "NS1 antigen test or IgM/IgG antibody test for confirmation",
            "Full blood count to monitor platelet count",
            "IV fluid resuscitation for dengue haemorrhagic fever",
            "Platelet transfusion if count drops critically",
            "Hospitalisation for severe dengue (dengue shock syndrome)",
        ],
        "red_flags": [
            "Bleeding from gums, nose, or blood in urine/stool",
            "Severe abdominal pain",
            "Rapid breathing or difficulty breathing",
            "Cold, clammy skin with low blood pressure",
            "Persistent vomiting",
            "Very low platelet count (<20,000/µL)",
        ],
    },

    "Cholera": {
        "icd10": "A00.9",
        "description": (
            "An acute diarrhoeal infection caused by ingestion of Vibrio cholerae. "
            "Can cause profuse, watery diarrhoea leading to severe dehydration and death "
            "within hours if untreated. Spread through contaminated water and food."
        ),
        "symptoms": {
            "Diarrhea": 10,
            "Vomiting": 9,
            "Dehydration signs": 10,
            "Abdominal pain / cramping": 7,
            "Muscle aches and pains": 5,
            "Nausea": 6,
            "Extreme fatigue / malaise": 7,
            "Low-grade fever (37.5–38.5°C)": 3,
        },
        "required": ["Diarrhea", "Dehydration signs"],
        "exclusions": ["Skin rash", "Headache", "Stiff neck", "Chest pain / tightness"],
        "severity": "critical",
        "urgency": "emergency",
        "incubation": "2 hours to 5 days",
        "transmission": "Contaminated food or water; faecal-oral route",
        "self_care": [
            "Begin ORS (Oral Rehydration Salts) IMMEDIATELY — this is life-saving",
            "If ORS not available: 1 litre of boiled water + 6 teaspoons sugar + 0.5 teaspoon salt",
            "Continue drinking even if vomiting — small sips frequently",
            "Maintain strict hand hygiene with soap and clean water",
            "Boil all drinking water",
            "Seek medical attention urgently — this is a medical emergency",
        ],
        "pharmacy_drugs": [
            "ORS sachets — most critical intervention",
            "Zinc supplements (20 mg/day for adults) to reduce diarrhoea duration",
        ],
        "doctor_treatment": [
            "Stool culture for V. cholerae confirmation",
            "IV Ringer's lactate for severe dehydration",
            "Doxycycline or Azithromycin (antibiotics to reduce duration)",
            "Tetracycline as alternative antibiotic",
            "Hospitalisation and isolation",
        ],
        "red_flags": [
            "Watery diarrhoea more than 10 times per hour",
            "Signs of severe dehydration: sunken eyes, dry mouth, no urination",
            "Loss of consciousness",
            "Muscle cramps throughout the body",
            "Patient is too weak to stand",
        ],
    },

    "Meningitis": {
        "icd10": "G03.9",
        "description": (
            "Inflammation of the membranes (meninges) surrounding the brain and spinal cord. "
            "Can be caused by bacteria (most serious), viruses, or fungi. "
            "A medical emergency requiring immediate treatment."
        ),
        "symptoms": {
            "Severe headache / migraine": 10,
            "Stiff neck": 10,
            "High fever (>38.5°C / 101.3°F)": 9,
            "Sensitivity to light (photophobia)": 9,
            "Sensitivity to sound (phonophobia)": 7,
            "Nausea": 6,
            "Vomiting": 6,
            "Confusion / disorientation": 8,
            "Seizures": 6,
            "Red spots / petechiae": 7,
            "Skin rash": 5,
            "Extreme fatigue / malaise": 6,
        },
        "required": ["Severe headache / migraine", "Stiff neck"],
        "exclusions": ["Runny nose", "Productive cough (with mucus)", "Diarrhea"],
        "severity": "critical",
        "urgency": "emergency",
        "incubation": "1–10 days (bacterial); 2–14 days (viral)",
        "transmission": "Respiratory droplets; direct contact with infected person",
        "self_care": [
            "THIS IS A MEDICAL EMERGENCY — Go to the nearest hospital immediately",
            "Do not attempt home treatment for suspected meningitis",
            "Keep patient calm and in a dark, quiet room while awaiting transport",
            "Do not give aspirin to children",
        ],
        "pharmacy_drugs": [
            "No self-medication — seek emergency care immediately",
            "Paracetamol only for mild headache while travelling to hospital",
        ],
        "doctor_treatment": [
            "Lumbar puncture (spinal tap) for CSF analysis",
            "IV Ceftriaxone or Penicillin (bacterial meningitis)",
            "IV Dexamethasone to reduce inflammation",
            "Aciclovir for viral (HSV) meningitis",
            "ICU care for severe cases",
            "Contact tracing and prophylaxis for close contacts",
        ],
        "red_flags": [
            "ALL symptoms of meningitis are red flags — seek emergency care NOW",
            "Petechial rash (non-blanching spots under skin)",
            "Seizures",
            "Loss of consciousness",
            "Rapidly worsening symptoms over hours",
        ],
    },

    "Urinary Tract Infection (UTI)": {
        "icd10": "N39.0",
        "description": (
            "A bacterial infection affecting the urinary tract, commonly the bladder (cystitis) "
            "or urethra. More common in women. Caused mainly by E. coli. "
            "Upper UTI involving kidneys (pyelonephritis) is more serious."
        ),
        "symptoms": {
            "Painful urination": 10,
            "Frequent urination": 9,
            "Blood in urine": 7,
            "Lower back / flank pain": 7,
            "Abdominal pain / cramping": 6,
            "High fever (>38.5°C / 101.3°F)": 5,
            "Nausea": 4,
            "Extreme fatigue / malaise": 4,
            "Dark urine": 5,
            "Chills and rigors": 4,
        },
        "required": ["Painful urination", "Frequent urination"],
        "exclusions": ["Skin rash", "Stiff neck", "Dry cough", "Joint pain"],
        "severity": "moderate",
        "urgency": "pharmacy",
        "incubation": "1–3 days after bacterial entry",
        "transmission": "Not contagious; caused by bacteria entering the urethra",
        "self_care": [
            "Drink at least 2–3 litres of water daily to flush bacteria",
            "Drink unsweetened cranberry juice (may help prevent bacteria from adhering)",
            "Urinate frequently — do not hold urine",
            "Use a warm heating pad on the lower abdomen for pain relief",
            "Wipe front to back after using the toilet",
            "Avoid caffeine, alcohol, and spicy foods",
            "Wear loose, breathable cotton underwear",
        ],
        "pharmacy_drugs": [
            "Phenazopyridine (urinary pain reliever) for burning sensation",
            "Paracetamol or Ibuprofen for pain and fever",
            "OTC UTI test strips to confirm if available",
            "Note: Antibiotics are required for cure — see a doctor",
        ],
        "doctor_treatment": [
            "Urine dipstick and midstream urine culture",
            "Trimethoprim-Sulfamethoxazole (Bactrim) 3–7 days",
            "Nitrofurantoin for uncomplicated lower UTI",
            "Ciprofloxacin for complicated UTI or pyelonephritis",
            "IV antibiotics if hospitalisation required",
        ],
        "red_flags": [
            "High fever with flank/back pain (suggests kidney infection)",
            "Blood in urine",
            "Symptoms lasting more than 3 days without improvement",
            "UTI in pregnant women — seek care urgently",
            "Chills and vomiting alongside UTI symptoms",
        ],
    },

    "Common Cold (Rhinovirus)": {
        "icd10": "J00",
        "description": (
            "A mild viral infection of the upper respiratory tract, mainly caused by rhinoviruses. "
            "Very common, self-limiting, and rarely serious in healthy adults."
        ),
        "symptoms": {
            "Runny nose": 10,
            "Nasal congestion": 9,
            "Sore throat": 8,
            "Dry cough": 7,
            "Productive cough (with mucus)": 6,
            "Low-grade fever (37.5–38.5°C)": 5,
            "Headache": 5,
            "Sneezing": 8,
            "Extreme fatigue / malaise": 4,
            "Muscle aches and pains": 3,
            "Ear pain": 3,
        },
        "required": ["Runny nose"],
        "exclusions": [
            "High fever (>38.5°C / 101.3°F)",
            "Muscle aches and pains",
            "Extreme fatigue / malaise",
            "Loss of smell or taste",
            "Chills and rigors",
        ],
        "severity": "low",
        "urgency": "home_care",
        "incubation": "1–3 days",
        "transmission": "Respiratory droplets; touching contaminated surfaces",
        "self_care": [
            "Rest at home for 2–7 days — the cold resolves on its own",
            "Drink warm fluids: warm water, honey-lemon tea, ginger tea",
            "Gargle warm salt water (1/4 tsp salt in 250 ml water) for sore throat",
            "Steam inhalation with menthol or eucalyptus oil for congestion",
            "Use saline nasal drops or sprays",
            "Eat light nutritious meals with plenty of fruit and vegetables",
            "Ensure adequate sleep (7–9 hours)",
            "Honey (1–2 tsp) to soothe throat and suppress cough",
        ],
        "pharmacy_drugs": [
            "Paracetamol or Ibuprofen for headache and mild fever",
            "Decongestant nasal spray (oxymetazoline) — max 3 days",
            "Antihistamines (loratadine or cetirizine) for runny nose",
            "Cough syrups containing dextromethorphan or guaifenesin",
            "Lozenges with benzocaine or menthol for sore throat",
            "Vitamin C and Zinc supplements to shorten duration",
        ],
        "doctor_treatment": [
            "Usually no specific treatment needed",
            "Antibiotics NOT effective (viral cause)",
            "Seek care if symptoms last more than 10 days or worsen",
        ],
        "red_flags": [
            "High fever (>39°C) persisting more than 3 days",
            "Ear pain or severe headache (may indicate secondary infection)",
            "Difficulty breathing",
            "Symptoms worse after 7 days",
            "Green/yellow thick nasal discharge lasting over 10 days",
        ],
    },

    "Hepatitis A": {
        "icd10": "B15.9",
        "description": (
            "A viral liver infection caused by the Hepatitis A virus. "
            "Spread through contaminated food and water. Usually self-limiting "
            "but can cause significant illness. Common in areas with poor sanitation."
        ),
        "symptoms": {
            "Jaundice (yellowing of skin/eyes)": 10,
            "Dark urine": 9,
            "Pale-coloured stools": 9,
            "Extreme fatigue / malaise": 8,
            "Loss of appetite": 8,
            "Nausea": 7,
            "Vomiting": 6,
            "Abdominal pain / cramping": 7,
            "Low-grade fever (37.5–38.5°C)": 6,
            "Muscle aches and pains": 4,
            "Itchy skin": 5,
            "Joint pain": 3,
        },
        "required": ["Jaundice (yellowing of skin/eyes)", "Dark urine"],
        "exclusions": ["Stiff neck", "Skin rash", "Dry cough", "Runny nose"],
        "severity": "moderate",
        "urgency": "clinic",
        "incubation": "15–50 days (average 28 days)",
        "transmission": "Contaminated food/water; faecal-oral route",
        "self_care": [
            "Rest completely — the liver needs time to heal",
            "Eat small, frequent, low-fat meals",
            "Avoid alcohol completely — it stresses the liver",
            "Avoid fatty, greasy, or spicy foods",
            "Drink plenty of clean boiled water",
            "Wash hands thoroughly before eating and after toilet use",
            "Avoid paracetamol and all liver-metabolised drugs",
        ],
        "pharmacy_drugs": [
            "Avoid paracetamol, ibuprofen, and any drugs processed by the liver",
            "ORS for hydration if vomiting",
            "Antihistamines for itchy skin (loratadine — ask pharmacist)",
        ],
        "doctor_treatment": [
            "Blood tests: Liver Function Tests (LFTs), Anti-HAV IgM antibody",
            "Supportive care — no specific antiviral treatment",
            "Vitamin K injection if blood clotting affected",
            "Hospitalisation for severe cases or acute liver failure",
        ],
        "red_flags": [
            "Confusion or unusual drowsiness (hepatic encephalopathy)",
            "Severe abdominal pain",
            "Uncontrolled vomiting",
            "Prolonged jaundice (>4 weeks) or worsening",
            "Bleeding or bruising easily",
        ],
    },

    "Chickenpox (Varicella)": {
        "icd10": "B01.9",
        "description": (
            "A highly contagious viral infection caused by the Varicella-Zoster virus. "
            "Characterised by itchy, blister-like rash. Common in children "
            "but can be severe in adults, pregnant women, and immunocompromised individuals."
        ),
        "symptoms": {
            "Skin rash": 10,
            "Itchy skin": 10,
            "Low-grade fever (37.5–38.5°C)": 7,
            "High fever (>38.5°C / 101.3°F)": 5,
            "Extreme fatigue / malaise": 6,
            "Headache": 5,
            "Loss of appetite": 5,
            "Muscle aches and pains": 4,
            "Sore throat": 3,
        },
        "required": ["Skin rash", "Itchy skin"],
        "exclusions": ["Stiff neck", "Productive cough (with mucus)", "Diarrhea", "Jaundice (yellowing of skin/eyes)"],
        "severity": "low",
        "urgency": "pharmacy",
        "incubation": "10–21 days",
        "transmission": "Airborne droplets; direct contact with blisters",
        "self_care": [
            "Isolate until all blisters have crusted over (usually 5–7 days)",
            "Apply calamine lotion to relieve itching",
            "Cool oatmeal baths to soothe skin",
            "Keep fingernails short and clean to prevent scratching and infection",
            "Wear loose, soft cotton clothing",
            "Apply cool, damp cloths to itchy areas",
            "Avoid scratching — this causes scarring and secondary infection",
        ],
        "pharmacy_drugs": [
            "Calamine lotion for topical itch relief",
            "Cetirizine or Chlorphenamine (antihistamines) for itching",
            "Paracetamol for fever — NEVER give aspirin (risk of Reye's syndrome)",
            "Antiseptic cream if blisters become infected",
        ],
        "doctor_treatment": [
            "Clinical diagnosis (visual); rarely lab confirmation needed",
            "Aciclovir (antiviral) — for adults, immunocompromised, or severe cases",
            "Varicella-Zoster Immune Globulin (VZIG) for high-risk contacts",
            "Antibiotics only if secondary bacterial skin infection occurs",
        ],
        "red_flags": [
            "Rash spreading to eyes",
            "Blisters becoming very red, warm, or draining pus (bacterial infection)",
            "High fever lasting more than 4 days",
            "Severe headache and stiff neck",
            "Difficulty walking or confusion",
            "Breathing difficulties",
        ],
    },
}

# ============================================================
# RISK FACTORS that modify urgency
# ============================================================
RISK_FACTORS = {
    "Age under 5 years": "high",
    "Age over 60 years": "high",
    "Pregnancy": "high",
    "HIV/AIDS or immunocompromised": "high",
    "Diabetes mellitus": "moderate",
    "Chronic lung disease (asthma, COPD)": "moderate",
    "Chronic kidney disease": "moderate",
    "Chronic liver disease": "moderate",
    "Sickle cell disease": "high",
    "Malnutrition": "moderate",
    "No known risk factors": "none",
}

# ============================================================
# URGENCY LEVEL DEFINITIONS
# ============================================================
URGENCY_LEVELS = {
    "home_care": {
        "label": "🏠 Home Care",
        "color": "#27ae60",
        "description": "Your symptoms suggest a mild condition manageable at home. Follow the self-care guidelines and monitor your symptoms. Seek medical attention if symptoms worsen or do not improve within 7 days.",
    },
    "pharmacy": {
        "label": "💊 Pharmacy / OTC Treatment",
        "color": "#f39c12",
        "description": "Your condition may benefit from over-the-counter medications available at a pharmacy. Speak with a pharmacist for guidance. Visit a clinic if symptoms worsen or last more than 5–7 days.",
    },
    "clinic": {
        "label": "🏥 Visit a Clinic or Hospital",
        "color": "#e67e22",
        "description": "Your symptoms suggest a condition that requires professional medical evaluation. Please visit a clinic or hospital as soon as possible — ideally within 24 hours.",
    },
    "emergency": {
        "label": "🚨 SEEK EMERGENCY CARE IMMEDIATELY",
        "color": "#e74c3c",
        "description": "Your symptoms indicate a potentially life-threatening condition. Go to the nearest emergency department or call emergency services NOW. Do not delay.",
    },
}

# ============================================================
# DISCLAIMER
# ============================================================
DISCLAIMER = """
⚠️ Medical Disclaimer: This Clinical Decision Support System (CDSS) is intended 
for informational and educational purposes only. It does NOT replace professional 
medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional 
for proper evaluation and management of your symptoms. In case of a medical emergency, 
call your local emergency number or go to the nearest hospital immediately.

This system uses statistical symptom weighting — not machine learning — to suggest 
probable diagnoses. Results should be interpreted by a healthcare professional.
"""
