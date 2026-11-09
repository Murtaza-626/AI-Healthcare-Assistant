import streamlit as st
import random

# Configure the page layout to wide for the 3-column dashboard
st.set_page_config(layout="wide", page_title="Medical AI Intake & Dashboard")

# SIMULATED CLOUD / ONLINE STATUS 
# In a real app, this checks if your server or DB is reachable.
# We add a checkbox in the sidebar so you can test the "Offline Mode" notice instantly!
st.sidebar.title("Prototype Controls")
is_online = st.sidebar.checkbox("Cloud Services Online", value=True)

if not is_online:
    st.error("⚠️ Offline Mode Active: Cloud services are currently unreachable. Data will be saved locally.")

# APP TABS: PATIENT INTAKE & DOCTOR DASHBOARD
tab1, tab2 = st.tabs(["📋 Patient Intake Screen", "🩺 Doctor Dashboard"])


# TAB 1: PATIENT INTAKE SCREEN
with tab1:
    st.header("Patient Intake Portal")
    st.write("Please fill out the intake form below to submit symptoms to the triage system.")
    
    # 1. Symptom Checkboxes
    st.subheader("1. Select Symptoms")
    col_sym1, col_sym2 = st.columns(2)
    with col_sym1:
        fever = st.checkbox("Fever (بخار)")
        cough = st.checkbox("Cough (کھانسی)")
        fatigue = st.checkbox("Fatigue (تھکن)")
    with col_sym2:
        shortness_breath = st.checkbox("Shortness of Breath (سردی/سانس پھولنا)")
        body_ache = st.checkbox("Body Aches (جسم میں درد)")
        headache = st.checkbox("Headache (سر درد)")

    # 2. Record Audio Button
    st.subheader("2. Voice Memo / Audio Notes")
    audio_file = st.button("🎙️ Record Patient Audio (Urdu/English)")
    if audio_file:
        st.info("Recording simulated... (In production, this activates the microphone device via HTML5).")
        # Simulated transcription text
        st.session_state['urdu_text'] = "مریض کو تین دن سے شدید بخار ہے اور سانس لینے میں دشواری ہو رہی ہے۔"
    
    # 3. Lab Report Upload Button
    st.subheader("3. Medical Records")
    uploaded_file = st.file_uploader("Upload Lab Report PDF / Image", type=["pdf", "png", "jpg"])
    if uploaded_file:
        st.success(f"Successfully uploaded: {uploaded_file.name}")
        # Simulated extracted values
        st.session_state['lab_wbc'] = "11.5 x10^3/µL (High)"
        st.session_state['lab_crp'] = "45 mg/L (Elevated)"
        st.session_state['lab_hb'] = "13.2 g/dL (Normal)"

    # Submit Button
    if st.button("Submit to Dashboard", type="primary"):
        st.success("Intake successfully processed and forwarded to doctor dashboard!")

# -----------------------------------------------------------------------------
# TAB 2: DOCTOR DASHBOARD (THREE COLUMNS)
# -----------------------------------------------------------------------------
with tab2:
    st.header("Clinical Decision Support Dashboard")
    st.markdown("---")
    
    # Define the three columns requested in the layout
    doc_col1, doc_col2, doc_col3 = st.columns([1.5, 1.2, 1.3])
    
    # COLUMN 1: Patient Symptoms and Urdu Text
    with doc_col1:
        st.subheader("📋 Symptoms & Transcripts")
        
        # Display selected symptoms from Tab 1
        active_symptoms = []
        if fever: active_symptoms.append("Fever")
        if cough: active_symptoms.append("Cough")
        if fatigue: active_symptoms.append("Fatigue")
        if shortness_breath: active_symptoms.append("Shortness of Breath")
        if body_ache: active_symptoms.append("Body Aches")
        if headache: active_symptoms.append("Headache")
        
        if active_symptoms:
            st.write("**Reported Symptoms:**")
            for sym in active_symptoms:
                st.markdown(f"- {sym}")
        else:
            st.info("No checkbox symptoms selected in intake.")
            
        st.markdown("---")
        st.write("**Urdu Audio Transcript:**")
        # Pull from session state if recorded, otherwise provide default prototype text
        urdu_display = st.session_state.get('urdu_text', "مریض نے ابھی تک کوئی آڈیو ریکارڈ نہیں کروائی۔")
        st.info(urdu_display)

    # COLUMN 2: Lab Values
    with doc_col2:
        st.subheader("🧪 Extracted Lab Values")
        
        # Display extracted metrics or defaults
        wbc = st.session_state.get('lab_wbc', "Pending Upload")
        crp = st.session_state.get('lab_crp', "Pending Upload")
        hb = st.session_state.get('lab_hb', "Pending Upload")
        
        st.metric(label="White Blood Cell (WBC)", value=wbc)
        st.metric(label="C-Reactive Protein (CRP)", value=crp)
        st.metric(label="Hemoglobin (Hb)", value=hb)

    # COLUMN 3: Risk Percentage & Two-Sentence Explanation
    with doc_col3:
        st.subheader("🚨 ML Predictive Assessment")
        
        # Calculate dynamic placeholder risk based on selected items
        risk_pct = 15
        if fever or shortness_breath:
            risk_pct += 45
        if crp != "Pending Upload" and "High" in crp or "Elevated" in crp:
            risk_pct += 25
        risk_pct = min(risk_pct, 98) # cap at 98%
        
        # Display large percentage metric
        st.metric(label="Calculated Triage Risk Indicator", value=f"{risk_pct}%")
        
        # Two-sentence ML explanation block
        st.markdown("**Model Diagnostic Context:**")
        if risk_pct > 50:
            st.warning(
                "**Explanation:** The predictive model indicates an elevated risk due to acute respiratory symptoms combined with elevated systemic inflammatory markers from the lab panel. "
                "Immediate secondary clinical evaluation is recommended to rule out bacterial infection."
            )
        else:
            st.success(
                "**Explanation:** Patient presents with baseline vital parameters and low-severity systemic symptoms. "
                "The current risk score recommends standard outpatient observation without escalated clinical protocols."
            )
