import streamlit as st
import pandas as pd
import datetime
import json
import random
from PIL import Image
import io
import base64
import time
import os
import sqlite3
import hashlib
from datetime import datetime, timedelta

# ======================================================================
# 📋 قوائم الخيارات
# ======================================================================

CHRONIC_DISEASES_LIST = [
    "السكري",
    "ارتفاع ضغط الدم",
    "أمراض القلب",
    "فشل القلب",
    "الربو",
    "مرض الانسداد الرئوي المزمن",
    "أمراض الكلى المزمنة",
    "الفشل الكلوي",
    "أمراض الكبد",
    "التهاب الكبد الوبائي",
    "الغدة الدرقية",
    "فقر الدم",
    "السرطان",
    "لا يوجد"
]

ALLERGIES_LIST = [
    "البنسلين",
    "الأسبرين",
    "الإيبوبروفين",
    "المضادات الحيوية",
    "اللاتكس",
    "الغبار",
    "حبوب اللقاح",
    "البيض",
    "الحليب",
    "المكسرات",
    "لا يوجد"
]

MEDICATIONS_LIST = [
    "الأنسولين",
    "الليسينوبريل",
    "الاملوديبين",
    "الميتفورمين",
    "الديجوكسين",
    "الفيوروسيمايد",
    "الستاتينات",
    "الأسبرين",
    "الباراسيتامول",
    "المورفين",
    "لا يوجد"
]

DIAGNOSIS_LIST = [
    "Sepsis",
    "Septic Shock",
    "Pneumonia",
    "ARDS",
    "AKI",
    "Heart Failure",
    "Hypertension",
    "Diabetes",
    "Asthma",
    "COPD",
    "Stroke",
    "Myocardial Infarction",
    "Liver Cirrhosis",
    "Cancer",
    "Thyroid Disorder",
    "Anemia"
]

# ======================================================================
# 💊 قاعدة بيانات الأدوية
# ======================================================================

MEDICATION_DATABASE = {
    "Meropenem": {
        "standard_dose": 20,
        "max_dose": 6000,
        "frequency": "كل 8 ساعات",
        "route": "IV",
        "renal_adjust": True,
        "monitoring": ["ضغط الدم", "وظائف الكلى", "تعداد الدم"]
    },
    "Vancomycin": {
        "standard_dose": 15,
        "max_dose": 4000,
        "frequency": "كل 12 ساعات",
        "route": "IV",
        "renal_adjust": True,
        "monitoring": ["ضغط الدم", "وظائف الكلى", "مستوى الدواء"]
    },
    "Piperacillin-Tazobactam": {
        "standard_dose": 112.5,
        "max_dose": 18000,
        "frequency": "كل 6 ساعات",
        "route": "IV",
        "renal_adjust": True,
        "monitoring": ["ضغط الدم", "وظائف الكلى"]
    },
    "Ceftriaxone": {
        "standard_dose": 50,
        "max_dose": 4000,
        "frequency": "كل 24 ساعة",
        "route": "IV/IM",
        "renal_adjust": False,
        "monitoring": ["ضغط الدم", "وظائف الكبد"]
    },
    "Norepinephrine": {
        "standard_dose": 0.5,
        "max_dose": 30,
        "frequency": "مستمر",
        "route": "IV",
        "renal_adjust": False,
        "monitoring": ["ضغط الدم", "معدل النبض", "CVP"]
    },
    "Dobutamine": {
        "standard_dose": 5,
        "max_dose": 40,
        "frequency": "مستمر",
        "route": "IV",
        "renal_adjust": False,
        "monitoring": ["ضغط الدم", "معدل النبض", "ECG"]
    },
    "Furosemide": {
        "standard_dose": 20,
        "max_dose": 400,
        "frequency": "كل 12 ساعات",
        "route": "IV/PO",
        "renal_adjust": True,
        "monitoring": ["ضغط الدم", "وظائف الكلى", "البوتاسيوم"]
    },
    "Heparin": {
        "standard_dose": 18,
        "max_dose": 100,
        "frequency": "مستمر",
        "route": "IV",
        "renal_adjust": False,
        "monitoring": ["aPTT", "تعداد الصفائح"]
    },
    "Insulin": {
        "standard_dose": 0.1,
        "max_dose": 10,
        "frequency": "مستمر",
        "route": "IV",
        "renal_adjust": False,
        "monitoring": ["سكر الدم", "البوتاسيوم"]
    },
    "Midazolam": {
        "standard_dose": 0.05,
        "max_dose": 10,
        "frequency": "كل 4 ساعات",
        "route": "IV",
        "renal_adjust": True,
        "monitoring": ["ضغط الدم", "معدل التنفس", "الوعي"]
    }
}

# ======================================================================
# 🔑 Gemini API
# ======================================================================

GEMINI_API_KEY = "AQ.Ab8RN6I9tQyt3v3bUCQO67ozRjCYPNpdi4Ars-B5rFpz_fVaSg"

try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

# ======================================================================
# 💾 قاعدة البيانات
# ======================================================================

DB_NAME = "mohammed_icu.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        name TEXT NOT NULL,
        approved INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        weight REAL,
        height REAL,
        chronic_diseases TEXT,
        allergies TEXT,
        surgeries TEXT,
        current_medications TEXT,
        diagnosis TEXT,
        status TEXT,
        risk_level TEXT,
        vitals TEXT,
        labs TEXT,
        sofa_score INTEGER,
        news2_score INTEGER,
        gcs_score INTEGER,
        bed_number TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        role TEXT NOT NULL,
        login_time TIMESTAMP,
        logout_time TIMESTAMP,
        session_duration TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medical_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        medication TEXT,
        dose REAL,
        unit TEXT,
        frequency TEXT,
        route TEXT,
        notes TEXT,
        prescribed_by TEXT,
        prescribed_time TIMESTAMP,
        received_by_nurse TEXT,
        received_time TIMESTAMP,
        executed_by_nurse TEXT,
        executed_time TIMESTAMP,
        status TEXT DEFAULT 'pending'
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        bed_number TEXT,
        nurse_name TEXT,
        shift TEXT,
        report_date DATE,
        report_time TIME,
        notes TEXT,
        vitals_summary TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

init_database()

# ======================================================================
# 🔐 المستخدمون
# ======================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

AUTHORIZED_USERS = {
    "mohammed": {
        "password": hash_password("07702574105"),
        "role": "admin",
        "name": "محمد - المدير",
        "approved": True,
        "permissions": ["all"]
    },
    "admin": {
        "password": hash_password("admin123"),
        "role": "admin",
        "name": "المدير",
        "approved": True,
        "permissions": ["all"]
    },
    "dr_ahmed": {
        "password": hash_password("doctor123"),
        "role": "doctor",
        "name": "د. أحمد",
        "approved": True,
        "permissions": ["view_patients", "ai_analysis", "radiology", "voice", "alerts", "prescribe"]
    },
    "dr_sara": {
        "password": hash_password("sara123"),
        "role": "doctor",
        "name": "د. سارة",
        "approved": True,
        "permissions": ["view_patients", "ai_analysis", "radiology", "voice", "alerts", "prescribe"]
    },
    "nurse_fatima": {
        "password": hash_password("nurse123"),
        "role": "nurse",
        "name": "فاطمة",
        "approved": True,
        "permissions": ["view_patients", "add_vitals", "voice", "alerts", "receive_orders", "execute_orders"]
    },
    "nurse_ali": {
        "password": hash_password("ali123"),
        "role": "nurse",
        "name": "علي",
        "approved": True,
        "permissions": ["view_patients", "add_vitals", "voice", "alerts", "receive_orders", "execute_orders"]
    }
}

# ======================================================================
# 🔐 دوال تسجيل الدخول
# ======================================================================

def check_login(username, password):
    if username in AUTHORIZED_USERS:
        user = AUTHORIZED_USERS[username]
        if user["password"] == hash_password(password) and user.get("approved", False):
            return user
    return None

def has_permission(user, permission):
    if not user:
        return False
    if user.get("role") == "admin":
        return True
    return True if "all" in user.get("permissions", []) else permission in user.get("permissions", [])

def log_login(username, role):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO login_logs (username, role, login_time)
    VALUES (?, ?, ?)
    ''', (username, role, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def log_logout(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, login_time FROM login_logs 
    WHERE username = ? AND logout_time IS NULL 
    ORDER BY id DESC LIMIT 1
    ''', (username,))
    record = cursor.fetchone()
    if record:
        login_time = datetime.strptime(record[1], "%Y-%m-%d %H:%M:%S")
        logout_time = datetime.now()
        duration = str(logout_time - login_time)
        cursor.execute('''
        UPDATE login_logs 
        SET logout_time = ?, session_duration = ?
        WHERE id = ?
        ''', (logout_time.strftime("%Y-%m-%d %H:%M:%S"), duration, record[0]))
    conn.commit()
    conn.close()

# ======================================================================
# 🧮 دوال الحسابات
# ======================================================================

def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m * height_m)

def calculate_ideal_weight(height):
    return 50 + 2.3 * (height - 152.4) / 2.54

def calculate_creatinine_clearance(age, weight, creatinine, gender):
    is_male = gender in ["ذكر", "Male", "Erkek", "مرد"]
    if is_male:
        return ((140 - age) * weight) / (72 * creatinine)
    else:
        return ((140 - age) * weight * 0.85) / (72 * creatinine)

def calculate_dose(medication, weight, age, creatinine=1.0):
    med_info = MEDICATION_DATABASE.get(medication)
    if not med_info:
        return None, None, "دواء غير معروف"
    
    base_dose = med_info["standard_dose"] * weight
    
    if med_info["renal_adjust"] and creatinine > 1.5:
        adjustment = 0.7
        base_dose = base_dose * adjustment
    
    if base_dose > med_info["max_dose"]:
        final_dose = med_info["max_dose"]
        warning = "تم تخفيض الجرعة إلى الحد الأقصى"
    else:
        final_dose = base_dose
        warning = "الجرعة ضمن الحد الآمن"
    
    return final_dose, med_info["frequency"], warning

# ======================================================================
# 🤖 الذكاء الاصطناعي
# ======================================================================

def get_ai_diagnosis(patient, lang):
    bmi = calculate_bmi(patient['weight'], patient['height'])
    ideal_weight = calculate_ideal_weight(patient['height'])
    creatinine_clearance = calculate_creatinine_clearance(
        patient['age'], patient['weight'], 
        patient['labs']['creatinine'], patient['gender']
    )
    
    if GEMINI_AVAILABLE:
        try:
            context = f"""
            Patient: {patient['name']}, Age: {patient['age']}, Gender: {patient['gender']}
            Weight: {patient['weight']}kg, Height: {patient['height']}cm
            BMI: {bmi:.1f}
            
            Vitals:
            - BP: {patient['vitals']['systolic_bp']}/{patient['vitals']['diastolic_bp']} mmHg
            - HR: {patient['vitals']['heart_rate']} bpm
            - Temp: {patient['vitals']['temperature']}°C
            - SpO2: {patient['vitals']['spo2']}%
            
            Labs:
            - WBC: {patient['labs']['wbc']}
            - HB: {patient['labs']['hb']}
            - PLT: {patient['labs']['plt']}
            - pH: {patient['labs']['ph']}
            - PaCO2: {patient['labs']['paco2']}
            - PaO2: {patient['labs']['pao2']}
            - HCO3: {patient['labs']['hco3']}
            - Na: {patient['labs']['na']}
            - K: {patient['labs']['k']}
            - Ca: {patient['labs']['ca']}
            - Creatinine: {patient['labs']['creatinine']}
            - BUN: {patient['labs']['bun']}
            - ALT: {patient['labs']['alt']}
            - AST: {patient['labs']['ast']}
            - Bilirubin: {patient['labs']['bilirubin']}
            - INR: {patient['labs']['inr']}
            - Troponin: {patient['labs']['troponin']}
            - Lactate: {patient['labs']['lactate']}
            
            Provide a detailed diagnosis and treatment plan.
            Respond in {lang} language.
            """
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(context)
            
            return {
                "success": True,
                "diagnosis": response.text,
                "bmi": bmi,
                "ideal_weight": ideal_weight,
                "creatinine_clearance": creatinine_clearance,
                "source": "Gemini AI"
            }
        except:
            pass
    
    return {
        "success": True,
        "diagnosis": "تشخيص غير متاح حالياً. يرجى المحاولة مرة أخرى.",
        "bmi": bmi,
        "ideal_weight": ideal_weight,
        "creatinine_clearance": creatinine_clearance,
        "source": "AI Simulator"
    }

# ======================================================================
# 🔔 التنبيهات
# ======================================================================

def check_alerts(patient):
    alerts = []
    
    if patient['vitals']['systolic_bp'] < 90:
        alerts.append({
            "type": "critical",
            "title": "انخفاض الضغط",
            "message": f"الضغط: {patient['vitals']['systolic_bp']} mmHg",
            "action": "ابدأ بالسوائل الوريدية"
        })
    
    if patient['vitals']['spo2'] < 90:
        alerts.append({
            "type": "critical",
            "title": "نقص أكسجة",
            "message": f"SpO2: {patient['vitals']['spo2']}%",
            "action": "أعطِ أكسجين"
        })
    
    if patient['labs']['lactate'] > 4:
        alerts.append({
            "type": "critical",
            "title": "ارتفاع اللاكتات",
            "message": f"Lactate: {patient['labs']['lactate']} mmol/L",
            "action": "أعد تقييم الإنتان"
        })
    
    if patient['labs']['k'] > 5.5:
        alerts.append({
            "type": "critical",
            "title": "ارتفاع البوتاسيوم",
            "message": f"K: {patient['labs']['k']} mEq/L",
            "action": "أعطِ كالسيوم جلوكونات"
        })
    
    if patient['sofa_score'] >= 4:
        alerts.append({
            "type": "critical",
            "title": "خلل عضوي",
            "message": f"SOFA: {patient['sofa_score']}",
            "action": "تقييم عاجل"
        })
    
    return alerts

# ======================================================================
# 📱 إعدادات الصفحة
# ======================================================================

st.set_page_config(
    page_title="Mohammed ICU",
    page_icon="🏥",
    layout="wide"
)

# ======================================================================
# 🌐 حالة الجلسة
# ======================================================================

if 'lang' not in st.session_state:
    st.session_state.lang = "العربية"

if 'patients' not in st.session_state:
    st.session_state.patients = [
        {
            "id": 1,
            "name": "أحمد محمد",
            "age": 65,
            "gender": "ذكر",
            "weight": 78,
            "height": 175,
            "chronic_diseases": ["السكري"],
            "allergies": ["البنسلين"],
            "surgeries": ["قسطرة قلبية 2020"],
            "current_medications": ["الأنسولين"],
            "diagnosis": "Sepsis",
            "status": "حرج",
            "bed_number": "سرير 1",
            "vitals": {
                "systolic_bp": 85,
                "diastolic_bp": 55,
                "heart_rate": 115,
                "temperature": 38.5,
                "respiratory_rate": 24,
                "spo2": 88,
                "cvp": 12,
                "icp": 18,
                "ecg": "تسرع قلبي"
            },
            "labs": {
                "wbc": 18.5,
                "hb": 10.2,
                "plt": 85,
                "ph": 7.28,
                "paco2": 45,
                "pao2": 60,
                "hco3": 18,
                "na": 135,
                "k": 5.8,
                "ca": 8.2,
                "creatinine": 2.5,
                "bun": 45,
                "alt": 120,
                "ast": 150,
                "bilirubin": 3.2,
                "pt": 18.5,
                "inr": 1.8,
                "troponin": 0.15,
                "lactate": 5.2
            },
            "sofa_score": 6,
            "news2_score": 8,
            "gcs_score": 12,
            "risk_level": "حرج"
        },
        {
            "id": 2,
            "name": "سارة خالد",
            "age": 45,
            "gender": "أنثى",
            "weight": 62,
            "height": 165,
            "chronic_diseases": ["الربو"],
            "allergies": ["لا يوجد"],
            "surgeries": ["لا يوجد"],
            "current_medications": ["لا يوجد"],
            "diagnosis": "Pneumonia",
            "status": "متوسط",
            "bed_number": "سرير 2",
            "vitals": {
                "systolic_bp": 110,
                "diastolic_bp": 70,
                "heart_rate": 85,
                "temperature": 37.8,
                "respiratory_rate": 18,
                "spo2": 95,
                "cvp": 8,
                "icp": 12,
                "ecg": "طبيعي"
            },
            "labs": {
                "wbc": 12.5,
                "hb": 12.5,
                "plt": 250,
                "ph": 7.38,
                "paco2": 38,
                "pao2": 75,
                "hco3": 22,
                "na": 140,
                "k": 4.2,
                "ca": 9.0,
                "creatinine": 0.8,
                "bun": 18,
                "alt": 45,
                "ast": 55,
                "bilirubin": 0.8,
                "pt": 12.5,
                "inr": 1.0,
                "troponin": 0.02,
                "lactate": 1.8
            },
            "sofa_score": 2,
            "news2_score": 3,
            "gcs_score": 15,
            "risk_level": "متوسط"
        }
    ]

if 'medical_orders' not in st.session_state:
    st.session_state.medical_orders = {}

if 'daily_reports' not in st.session_state:
    st.session_state.daily_reports = []

if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = st.session_state.patients[0] if st.session_state.patients else None

if 'page' not in st.session_state:
    st.session_state.page = "login"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user' not in st.session_state:
    st.session_state.user = None

if 'role' not in st.session_state:
    st.session_state.role = None

if 'login_username' not in st.session_state:
    st.session_state.login_username = None

# ======================================================================
# 🔐 صفحة تسجيل الدخول
# ======================================================================

def login_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0c2340, #1a5276); padding: 35px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 48px; margin: 0;">🏥 Mohammed ICU</h1>
        <p style="font-size: 20px; opacity: 0.9;">نظام العناية المركزة الذكي المتقدم</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>اختر دورك للدخول إلى النظام</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("👨‍⚕️ طبيب", use_container_width=True):
                st.session_state.role = "doctor"
                st.session_state.page = "login_form"
                st.rerun()
        with col_b:
            if st.button("👩‍⚕️ ممرض", use_container_width=True):
                st.session_state.role = "nurse"
                st.session_state.page = "login_form"
                st.rerun()
        with col_c:
            if st.button("👑 مدير", use_container_width=True):
                st.session_state.role = "admin"
                st.session_state.page = "login_form"
                st.rerun()

def login_form():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0c2340, #1a5276); padding: 25px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 36px; margin: 0;">🏥 Mohammed ICU</h1>
        <p style="font-size: 16px; opacity: 0.8;">نظام العناية المركزة الذكي المتقدم</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("### 🔐 تسجيل الدخول")
            username = st.text_input("👤 اسم المستخدم")
            password = st.text_input("🔑 كلمة المرور", type="password")
            submitted = st.form_submit_button("🚪 تسجيل الدخول", use_container_width=True)
            
            if submitted:
                user = check_login(username, password)
                if user:
                    st.session_state.user = user
                    st.session_state.logged_in = True
                    st.session_state.login_username = username
                    log_login(username, user['role'])
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("❌ بيانات غير صحيحة")
            
            st.caption("📝 المدير: mohammed / 07702574105")

# ======================================================================
# 📊 لوحة التحكم
# ======================================================================

def dashboard():
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user['name']}")
        role_names = {"doctor": "طبيب", "nurse": "ممرض", "admin": "مدير"}
        st.markdown(f"📋 {role_names.get(st.session_state.role, '')}")
        st.markdown(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
        st.markdown("---")
        
        if st.session_state.patients:
            patient_names = [p["name"] + " (" + p.get('bed_number', '') + ")" for p in st.session_state.patients]
            selected = st.selectbox("🩺 اختر المريض", patient_names)
            idx = patient_names.index(selected)
            st.session_state.selected_patient = st.session_state.patients[idx]
        
        st.markdown("---")
        
        critical = sum(1 for p in st.session_state.patients if p['risk_level'] == 'حرج')
        moderate = sum(1 for p in st.session_state.patients if p['risk_level'] == 'متوسط')
        low = sum(1 for p in st.session_state.patients if p['risk_level'] == 'منخفض')
        st.metric("حرج", critical)
        st.metric("متوسط", moderate)
        st.metric("منخفض", low)
        
        st.markdown("---")
        if st.button("🚪 خروج", use_container_width=True):
            log_logout(st.session_state.login_username)
            st.session_state.clear()
            st.rerun()
    
    patient = st.session_state.selected_patient
    
    if patient:
        risk_class = "status-critical" if patient['risk_level'] == "حرج" else "status-moderate" if patient['risk_level'] == "متوسط" else "status-low"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0c2340, #1a5276); padding: 25px; border-radius: 12px; color: white; margin-bottom: 25px;">
            <h2 style="margin: 0;">🩺 {patient['name']}</h2>
            <p>العمر: {patient['age']} سنة | {patient['gender']} | الوزن: {patient['weight']} كجم</p>
            <p>🛏️ {patient.get('bed_number', 'لا يوجد')}</p>
            <p>التشخيص: {patient['diagnosis']}</p>
            <span style="display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 14px; background: {'#e74c3c' if patient['risk_level'] == 'حرج' else '#f1c40f' if patient['risk_level'] == 'متوسط' else '#2ecc71'}; color: {'white' if patient['risk_level'] == 'حرج' else 'black' if patient['risk_level'] == 'متوسط' else 'white'};">{patient['risk_level']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        tabs = st.tabs(["العلامات الحيوية", "المختبر", "التقييم", "الذكاء الاصطناعي", "التنبيهات", "الأشعة", "تسجيل صوتي", "الأوامر الطبية"])
        
        # العلامات الحيوية
        with tabs[0]:
            vitals = patient['vitals']
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("ضغط الدم", f"{vitals['systolic_bp']}/{vitals['diastolic_bp']}")
            with col2:
                st.metric("معدل النبض", f"{vitals['heart_rate']}")
            with col3:
                st.metric("درجة الحرارة", f"{vitals['temperature']}°C")
            with col4:
                st.metric("SpO2", f"{vitals['spo2']}%")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("معدل التنفس", f"{vitals['respiratory_rate']}")
            with col2:
                st.metric("CVP", f"{vitals['cvp']}")
            with col3:
                st.metric("ICP", f"{vitals['icp']}")
        
        # المختبر
        with tabs[1]:
            labs = patient['labs']
            lab_data = {
                "الفحص": ["WBC", "HB", "PLT", "pH", "PaCO2", "PaO2", "HCO3", "Na", "K", "Ca", "Creatinine", "BUN", "ALT", "AST", "Bilirubin", "INR", "Troponin", "Lactate"],
                "النتيجة": [labs['wbc'], labs['hb'], labs['plt'], labs['ph'], labs['paco2'], labs['pao2'], labs['hco3'], labs['na'], labs['k'], labs['ca'], labs['creatinine'], labs['bun'], labs['alt'], labs['ast'], labs['bilirubin'], labs['inr'], labs['troponin'], labs['lactate']],
                "الوحدة": ["×10³/µL", "g/dL", "×10³/µL", "", "mmHg", "mmHg", "mEq/L", "mEq/L", "mEq/L", "mEq/L", "mg/dL", "mg/dL", "U/L", "U/L", "mg/dL", "", "ng/mL", "mmol/L"]
            }
            df = pd.DataFrame(lab_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # التقييم
        with tabs[2]:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("SOFA Score", patient['sofa_score'])
            with col2:
                st.metric("NEWS2", patient['news2_score'])
            with col3:
                st.metric("GCS", patient['gcs_score'])
                st.metric("مستوى الخطورة", patient['risk_level'])
        
        # الذكاء الاصطناعي
        with tabs[3]:
            if not has_permission(st.session_state.user, "ai_analysis"):
                st.warning("ليس لديك صلاحية")
            else:
                if st.button("تشغيل التحليل الذكي", use_container_width=True):
                    with st.spinner("جاري التحليل..."):
                        result = get_ai_diagnosis(patient, "العربية")
                        if result["success"]:
                            st.markdown("### المؤشرات المحسوبة")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("BMI", f"{result['bmi']:.1f}")
                            with col2:
                                st.metric("تصفية الكرياتينين", f"{result['creatinine_clearance']:.1f} mL/min")
                            with col3:
                                st.metric("المصدر", result['source'])
                            st.markdown("### التقرير السريري")
                            st.markdown(result["diagnosis"])
        
        # التنبيهات
        with tabs[4]:
            alerts = check_alerts(patient)
            if alerts:
                for alert in alerts:
                    st.warning(f"**{alert['title']}**\n\n{alert['message']}\n\n🛑 {alert['action']}")
            else:
                st.success("✅ لا يوجد تنبيهات")
        
        # الأشعة
        with tabs[5]:
            uploaded = st.file_uploader("رفع صورة الأشعة", type=["jpg", "jpeg", "png"])
            if uploaded:
                st.image(uploaded, caption="صورة الأشعة", use_container_width=True)
                st.success("تم رفع الصورة بنجاح")
        
        # تسجيل صوتي
        with tabs[6]:
            audio = st.file_uploader("رفع ملف صوتي", type=["wav", "mp3"])
            if audio:
                st.success("تم رفع الملف الصوتي")
        
        # الأوامر الطبية
        with tabs[7]:
            is_doctor = st.session_state.role == "doctor"
            is_admin = st.session_state.role == "admin"
            
            if patient['id'] in st.session_state.medical_orders:
                orders = st.session_state.medical_orders[patient['id']]
                for i, order in enumerate(orders):
                    status = order.get('status', 'معلق')
                    st.markdown(f"""
                    <div style="background: #eaf2f8; padding: 15px; border-radius: 10px; margin: 10px 0; border-right: 4px solid #2e86c1;">
                        <strong>💊 {order['medication']}</strong>
                        <br>الجرعة: {order['dose']:.1f} {order['unit']}
                        <br>التوقيت: {order['frequency']}
                        <br>الطريق: {order['route']}
                        <br>الحالة: {status}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.session_state.role == "nurse":
                        if order.get('status') == 'pending':
                            if st.button(f"استلام الأمر", key=f"receive_{i}"):
                                order['status'] = 'received'
                                order['received_by_nurse'] = st.session_state.user['name']
                                order['received_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                st.rerun()
                        if order.get('status') == 'received':
                            if st.button(f"تنفيذ الأمر", key=f"execute_{i}"):
                                order['status'] = 'executed'
                                order['executed_by_nurse'] = st.session_state.user['name']
                                order['executed_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                st.rerun()
            else:
                st.info("لا توجد أوامر طبية")
            
            if is_doctor or is_admin:
                st.markdown("---")
                with st.form("new_order"):
                    medication = st.selectbox("اختيار الدواء", list(MEDICATION_DATABASE.keys()))
                    dose, frequency, warning = calculate_dose(medication, patient['weight'], patient['age'], patient['labs']['creatinine'])
                    st.info(f"الجرعة المحسوبة: {dose:.1f} mg - {frequency}")
                    custom_dose = st.number_input("تعديل الجرعة", value=float(dose), step=100.0)
                    route = st.selectbox("طريق الإعطاء", ["IV", "IM", "PO", "SC"])
                    notes = st.text_area("ملاحظات")
                    
                    if st.form_submit_button("حفظ الأمر", use_container_width=True):
                        order = {
                            "medication": medication,
                            "dose": custom_dose,
                            "unit": "mg",
                            "frequency": frequency,
                            "route": route,
                            "notes": notes,
                            "prescribed_by": st.session_state.user['name'],
                            "prescribed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "pending",
                            "received_by_nurse": "",
                            "received_time": "",
                            "executed_by_nurse": "",
                            "executed_time": ""
                        }
                        if patient['id'] not in st.session_state.medical_orders:
                            st.session_state.medical_orders[patient['id']] = []
                        st.session_state.medical_orders[patient['id']].append(order)
                        st.success("تم إضافة الأمر الطبي")
                        st.rerun()

# ======================================================================
# 🚀 تشغيل التطبيق
# ======================================================================

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "login_form":
    login_form()
elif st.session_state.logged_in:
    dashboard()
else:
    st.session_state.page = "login"
    st.rerun()