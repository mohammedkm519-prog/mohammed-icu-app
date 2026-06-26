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
# 🌐 إعدادات اللغات (4 لغات)
# ======================================================================

LANGUAGES = {
    "العربية": {
        "app_title": "🏥 محمد ICU",
        "app_subtitle": "نظام العناية المركزة الذكي المتقدم",
        "choose_role": "اختر دورك للدخول إلى النظام",
        "doctor": "👨‍⚕️ طبيب",
        "nurse": "👩‍⚕️ ممرض",
        "admin": "👑 مدير",
        "login": "🔐 تسجيل الدخول",
        "username": "👤 اسم المستخدم",
        "password": "🔑 كلمة المرور",
        "login_btn": "🚪 تسجيل الدخول",
        "logout": "🚪 خروج",
        "select_patient": "🩺 اختر المريض",
        "vitals": "📊 العلامات الحيوية",
        "lab": "🧪 المختبر",
        "assessment": "🧠 التقييم السريري",
        "ai": "🤖 الذكاء الاصطناعي",
        "alerts": "🔔 التنبيهات",
        "radiology": "🩻 الأشعة",
        "voice_record": "🎤 تسجيل صوتي",
        "statistics": "📊 الإحصائيات",
        "medical_orders": "📋 الأوامر الطبية",
        "admin_panel": "👑 لوحة المدير",
        "daily_report": "📋 تقرير يومي",
        "bed_report": "🛏️ تقرير السرير",
        "visitor_log": "📝 سجل الزوار",
        "morning": "☀️ صباحاً",
        "evening": "🌙 مساءً",
        "add_patient": "➕ إضافة مريض جديد",
        "quick_add": "⚡ إضافة سريعة",
        "full_add": "📋 إضافة كاملة",
        "full_name": "👤 الاسم الكامل",
        "age": "🧬 العمر",
        "gender": "⚤ الجنس",
        "weight": "⚖️ الوزن (كجم)",
        "height": "📏 الطول (سم)",
        "chronic_diseases": "💊 الأمراض المزمنة",
        "allergies": "⚠️ الحساسية",
        "current_medications": "💊 الأدوية الحالية",
        "select_disease": "اختر الأمراض المزمنة",
        "select_allergy": "اختر الحساسية",
        "select_medication": "اختر الأدوية",
        "select_diagnosis": "اختر التشخيص"
    },
    "English": {
        "app_title": "🏥 Mohammed ICU",
        "app_subtitle": "Advanced AI-Powered Intensive Care Unit",
        "choose_role": "Choose your role to enter the system",
        "doctor": "👨‍⚕️ Doctor",
        "nurse": "👩‍⚕️ Nurse",
        "admin": "👑 Admin",
        "login": "🔐 Login",
        "username": "👤 Username",
        "password": "🔑 Password",
        "login_btn": "🚪 Login",
        "logout": "🚪 Logout",
        "select_patient": "🩺 Select Patient",
        "vitals": "📊 Vital Signs",
        "lab": "🧪 Laboratory",
        "assessment": "🧠 Assessment",
        "ai": "🤖 AI Analysis",
        "alerts": "🔔 Alerts",
        "radiology": "🩻 Radiology",
        "voice_record": "🎤 Voice Record",
        "statistics": "📊 Statistics",
        "medical_orders": "📋 Medical Orders",
        "admin_panel": "👑 Admin Panel",
        "daily_report": "📋 Daily Report",
        "bed_report": "🛏️ Bed Report",
        "visitor_log": "📝 Visitor Log",
        "morning": "☀️ Morning",
        "evening": "🌙 Evening",
        "add_patient": "➕ Add New Patient",
        "quick_add": "⚡ Quick Add",
        "full_add": "📋 Full Add",
        "full_name": "👤 Full Name",
        "age": "🧬 Age",
        "gender": "⚤ Gender",
        "weight": "⚖️ Weight (kg)",
        "height": "📏 Height (cm)",
        "chronic_diseases": "💊 Chronic Diseases",
        "allergies": "⚠️ Allergies",
        "current_medications": "💊 Current Medications",
        "select_disease": "Select Chronic Diseases",
        "select_allergy": "Select Allergies",
        "select_medication": "Select Medications",
        "select_diagnosis": "Select Diagnosis"
    },
    "Türkçe": {
        "app_title": "🏥 Muhammed ICU",
        "app_subtitle": "Gelişmiş Yapay Zeka Destekli Yoğun Bakım Ünitesi",
        "choose_role": "Sisteme girmek için rolünüzü seçin",
        "doctor": "👨‍⚕️ Doktor",
        "nurse": "👩‍⚕️ Hemşire",
        "admin": "👑 Yönetici",
        "login": "🔐 Giriş Yap",
        "username": "👤 Kullanıcı Adı",
        "password": "🔑 Şifre",
        "login_btn": "🚪 Giriş",
        "logout": "🚪 Çıkış",
        "select_patient": "🩺 Hasta Seç",
        "vitals": "📊 Vital Bulgular",
        "lab": "🧪 Laboratuvar",
        "assessment": "🧠 Değerlendirme",
        "ai": "🤖 Yapay Zeka",
        "alerts": "🔔 Uyarılar",
        "radiology": "🩻 Radyoloji",
        "voice_record": "🎤 Ses Kaydı",
        "statistics": "📊 İstatistikler",
        "medical_orders": "📋 Tıbbi Emirler",
        "admin_panel": "👑 Yönetici Paneli",
        "daily_report": "📋 Günlük Rapor",
        "bed_report": "🛏️ Yatak Raporu",
        "visitor_log": "📝 Ziyaretçi Kaydı",
        "morning": "☀️ Sabah",
        "evening": "🌙 Akşam",
        "add_patient": "➕ Yeni Hasta Ekle",
        "quick_add": "⚡ Hızlı Ekle",
        "full_add": "📋 Tam Ekle",
        "full_name": "👤 Tam Ad",
        "age": "🧬 Yaş",
        "gender": "⚤ Cinsiyet",
        "weight": "⚖️ Kilo (kg)",
        "height": "📏 Boy (cm)",
        "chronic_diseases": "💊 Kronik Hastalıklar",
        "allergies": "⚠️ Alerjiler",
        "current_medications": "💊 Mevcut İlaçlar",
        "select_disease": "Kronik Hastalıkları Seç",
        "select_allergy": "Alerjileri Seç",
        "select_medication": "İlaçları Seç",
        "select_diagnosis": "Teşhis Seç"
    },
    "فارسی": {
        "app_title": "🏥 محمد ICU",
        "app_subtitle": "سیستم پیشرفته مراقبت‌های ویژه مبتنی بر هوش مصنوعی",
        "choose_role": "نقش خود را برای ورود به سیستم انتخاب کنید",
        "doctor": "👨‍⚕️ پزشک",
        "nurse": "👩‍⚕️ پرستار",
        "admin": "👑 مدیر",
        "login": "🔐 ورود",
        "username": "👤 نام کاربری",
        "password": "🔑 رمز عبور",
        "login_btn": "🚪 ورود",
        "logout": "🚪 خروج",
        "select_patient": "🩺 انتخاب بیمار",
        "vitals": "📊 علائم حیاتی",
        "lab": "🧪 آزمایشگاه",
        "assessment": "🧠 ارزیابی",
        "ai": "🤖 هوش مصنوعی",
        "alerts": "🔔 هشدارها",
        "radiology": "🩻 رادیولوژی",
        "voice_record": "🎤 ضبط صدا",
        "statistics": "📊 آمار",
        "medical_orders": "📋 دستورات پزشکی",
        "admin_panel": "👑 پنل مدیر",
        "daily_report": "📋 گزارش روزانه",
        "bed_report": "🛏️ گزارش تخت",
        "visitor_log": "📝 گزارش بازدیدکنندگان",
        "morning": "☀️ صبح",
        "evening": "🌙 عصر",
        "add_patient": "➕ افزودن بیمار جدید",
        "quick_add": "⚡ افزودن سریع",
        "full_add": "📋 افزودن کامل",
        "full_name": "👤 نام کامل",
        "age": "🧬 سن",
        "gender": "⚤ جنسیت",
        "weight": "⚖️ وزن (کیلوگرم)",
        "height": "📏 قد (سانتی‌متر)",
        "chronic_diseases": "💊 بیماری‌های مزمن",
        "allergies": "⚠️ حساسیت‌ها",
        "current_medications": "💊 داروهای فعلی",
        "select_disease": "بیماری‌های مزمن را انتخاب کنید",
        "select_allergy": "حساسیت‌ها را انتخاب کنید",
        "select_medication": "داروها را انتخاب کنید",
        "select_diagnosis": "تشخیص را انتخاب کنید"
    }
}

# ======================================================================
# 📋 القوائم
# ======================================================================

CHRONIC_DISEASES_LIST = [
    "السكري", "ارتفاع ضغط الدم", "أمراض القلب", "فشل القلب",
    "الربو", "مرض الانسداد الرئوي المزمن", "أمراض الكلى المزمنة",
    "الفشل الكلوي", "أمراض الكبد", "التهاب الكبد الوبائي",
    "الغدة الدرقية", "فقر الدم", "السرطان", "لا يوجد"
]

ALLERGIES_LIST = [
    "البنسلين", "الأسبرين", "الإيبوبروفين", "المضادات الحيوية",
    "اللاتكس", "الغبار", "حبوب اللقاح", "البيض",
    "الحليب", "المكسرات", "لا يوجد"
]

MEDICATIONS_LIST = [
    "الأنسولين", "الليسينوبريل", "الاملوديبين", "الميتفورمين",
    "الديجوكسين", "الفيوروسيمايد", "الستاتينات", "الأسبرين",
    "الباراسيتامول", "المورفين", "لا يوجد"
]

DIAGNOSIS_LIST = [
    "Sepsis", "Septic Shock", "Pneumonia", "ARDS",
    "AKI", "Heart Failure", "Hypertension", "Diabetes",
    "Asthma", "COPD", "Stroke", "Myocardial Infarction",
    "Liver Cirrhosis", "Cancer", "Thyroid Disorder", "Anemia"
]

# ======================================================================
# 💊 قاعدة بيانات الأدوية
# ======================================================================

MEDICATION_DATABASE = {
    "Meropenem": {"standard_dose": 20, "max_dose": 6000, "frequency": "كل 8 ساعات", "route": "IV", "renal_adjust": True, "monitoring": ["ضغط الدم", "وظائف الكلى"]},
    "Vancomycin": {"standard_dose": 15, "max_dose": 4000, "frequency": "كل 12 ساعات", "route": "IV", "renal_adjust": True, "monitoring": ["ضغط الدم", "وظائف الكلى"]},
    "Piperacillin-Tazobactam": {"standard_dose": 112.5, "max_dose": 18000, "frequency": "كل 6 ساعات", "route": "IV", "renal_adjust": True, "monitoring": ["ضغط الدم"]},
    "Ceftriaxone": {"standard_dose": 50, "max_dose": 4000, "frequency": "كل 24 ساعة", "route": "IV/IM", "renal_adjust": False, "monitoring": ["ضغط الدم"]},
    "Norepinephrine": {"standard_dose": 0.5, "max_dose": 30, "frequency": "مستمر", "route": "IV", "renal_adjust": False, "monitoring": ["ضغط الدم", "النبض"]},
    "Dobutamine": {"standard_dose": 5, "max_dose": 40, "frequency": "مستمر", "route": "IV", "renal_adjust": False, "monitoring": ["ضغط الدم", "النبض", "ECG"]},
    "Furosemide": {"standard_dose": 20, "max_dose": 400, "frequency": "كل 12 ساعات", "route": "IV/PO", "renal_adjust": True, "monitoring": ["ضغط الدم", "البوتاسيوم"]},
    "Heparin": {"standard_dose": 18, "max_dose": 100, "frequency": "مستمر", "route": "IV", "renal_adjust": False, "monitoring": ["aPTT"]},
    "Insulin": {"standard_dose": 0.1, "max_dose": 10, "frequency": "مستمر", "route": "IV", "renal_adjust": False, "monitoring": ["سكر الدم", "البوتاسيوم"]},
    "Midazolam": {"standard_dose": 0.05, "max_dose": 10, "frequency": "كل 4 ساعات", "route": "IV", "renal_adjust": True, "monitoring": ["ضغط الدم", "التنفس"]}
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
    "mohammed": {"password": hash_password("07702574105"), "role": "admin", "name": "محمد - المدير", "approved": True, "permissions": ["all"]},
    "admin": {"password": hash_password("admin123"), "role": "admin", "name": "المدير", "approved": True, "permissions": ["all"]},
    "dr_ahmed": {"password": hash_password("doctor123"), "role": "doctor", "name": "د. أحمد", "approved": True, "permissions": ["all"]},
    "dr_sara": {"password": hash_password("sara123"), "role": "doctor", "name": "د. سارة", "approved": True, "permissions": ["all"]},
    "nurse_fatima": {"password": hash_password("nurse123"), "role": "nurse", "name": "فاطمة", "approved": True, "permissions": ["all"]},
    "nurse_ali": {"password": hash_password("ali123"), "role": "nurse", "name": "علي", "approved": True, "permissions": ["all"]}
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
    return True

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
    if gender in ["ذكر", "Male"]:
        return ((140 - age) * weight) / (72 * creatinine)
    else:
        return ((140 - age) * weight * 0.85) / (72 * creatinine)

def calculate_oxygenation_index(pao2, fio2=0.21):
    return pao2 / fio2

def calculate_caloric_needs(weight, age, gender, height, stress_factor=1.2):
    if gender in ["ذكر", "Male"]:
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr * stress_factor

def calculate_fluid_needs(weight, stress_factor=1.5):
    return weight * 30 * stress_factor

def calculate_protein_needs(weight, stress_factor=1.5):
    return weight * stress_factor

def calculate_dose(medication, weight, age, creatinine=1.0):
    med_info = MEDICATION_DATABASE.get(medication)
    if not med_info:
        return None, None, "دواء غير معروف"
    base_dose = med_info["standard_dose"] * weight
    if med_info["renal_adjust"] and creatinine > 1.5:
        base_dose = base_dose * 0.7
    if base_dose > med_info["max_dose"]:
        return med_info["max_dose"], med_info["frequency"], "تم تخفيض الجرعة للحد الأقصى"
    return base_dose, med_info["frequency"], "الجرعة ضمن الحد الآمن"

def check_contraindications(patient, medication):
    warnings = []
    for allergy in patient.get('allergies', []):
        if "البنسلين" in allergy and medication in ["Meropenem", "Piperacillin-Tazobactam"]:
            warnings.append("تحذير: حساسية للبنسلين!")
    if medication in ["Norepinephrine", "Dobutamine"] and patient['vitals']['systolic_bp'] > 180:
        warnings.append("تحذير: ضغط الدم مرتفع جداً!")
    if patient['labs']['creatinine'] > 2.5 and medication in ["Vancomycin", "Meropenem"]:
        warnings.append("تحذير: وظائف الكلى متدهورة!")
    return warnings

# ======================================================================
# 🤖 الذكاء الاصطناعي المتقدم
# ======================================================================

def generate_advanced_diagnosis(patient, lang):
    """توليد تشخيص متقدم مفصل مع نسب ثقة وأدلة"""
    
    bp = patient['vitals']['systolic_bp']
    hr = patient['vitals']['heart_rate']
    temp = patient['vitals']['temperature']
    spo2 = patient['vitals']['spo2']
    rr = patient['vitals']['respiratory_rate']
    
    lactate = patient['labs']['lactate']
    creatinine = patient['labs']['creatinine']
    potassium = patient['labs']['k']
    wbc = patient['labs']['wbc']
    ph = patient['labs']['ph']
    pao2 = patient['labs']['pao2']
    
    bmi = calculate_bmi(patient['weight'], patient['height'])
    creatinine_clearance = calculate_creatinine_clearance(
        patient['age'], patient['weight'], creatinine, patient['gender']
    )
    pf_ratio = calculate_oxygenation_index(pao2)
    caloric_needs = calculate_caloric_needs(
        patient['weight'], patient['age'], patient['gender'], patient['height']
    )
    fluid_needs = calculate_fluid_needs(patient['weight'])
    protein_needs = calculate_protein_needs(patient['weight'])
    
    report = f"""
### 📋 التقرير السريري المتقدم

---

#### 🧬 معلومات المريض
- **الاسم:** {patient['name']}
- **العمر:** {patient['age']} سنة
- **الجنس:** {patient['gender']}
- **الوزن:** {patient['weight']} كجم
- **الطول:** {patient['height']} سم
- **BMI:** {bmi:.1f} ({'طبيعي' if bmi < 25 else 'مرتفع' if bmi < 30 else 'سمنة'})

---

#### 📊 تحليل العلامات الحيوية

| المؤشر | القيمة | الطبيعي | التقييم |
|--------|--------|---------|---------|
| ضغط الدم الانقباضي | {bp} | 90-120 | {'⚠️ منخفض' if bp < 90 else '✅ طبيعي' if bp < 140 else '⚠️ مرتفع'} |
| ضغط الدم الانبساطي | {patient['vitals']['diastolic_bp']} | 60-80 | {'⚠️ منخفض' if patient['vitals']['diastolic_bp'] < 60 else '✅ طبيعي' if patient['vitals']['diastolic_bp'] < 90 else '⚠️ مرتفع'} |
| معدل النبض | {hr} | 60-100 | {'⚠️ تسرع قلبي' if hr > 100 else '⚠️ بطء قلبي' if hr < 60 else '✅ طبيعي'} |
| درجة الحرارة | {temp} | 36.5-37.5 | {'⚠️ حمى' if temp > 37.5 else '⚠️ انخفاض' if temp < 36.5 else '✅ طبيعي'} |
| SpO2 | {spo2} | 95-100 | {'🚨 نقص أكسجة شديد' if spo2 < 90 else '⚠️ نقص أكسجة' if spo2 < 95 else '✅ طبيعي'} |
| معدل التنفس | {rr} | 12-20 | {'⚠️ تسرع تنفس' if rr > 20 else '⚠️ بطء تنفس' if rr < 12 else '✅ طبيعي'} |

---

#### 🧪 تحليل المختبر

| المؤشر | القيمة | الطبيعي | التقييم |
|--------|--------|---------|---------|
| WBC | {wbc} | 4-11 | {'🚨 ارتفاع شديد' if wbc > 15 else '⚠️ ارتفاع' if wbc > 11 else '✅ طبيعي'} |
| Lactate | {lactate} | 0.5-2.2 | {'🚨 ارتفاع شديد' if lactate > 4 else '⚠️ ارتفاع' if lactate > 2.2 else '✅ طبيعي'} |
| Creatinine | {creatinine} | 0.6-1.2 | {'🚨 ارتفاع شديد' if creatinine > 2 else '⚠️ ارتفاع' if creatinine > 1.2 else '✅ طبيعي'} |
| Potassium | {potassium} | 3.5-5.0 | {'🚨 ارتفاع شديد' if potassium > 5.5 else '⚠️ ارتفاع' if potassium > 5.0 else '✅ طبيعي'} |
| pH | {ph} | 7.35-7.45 | {'🚨 حماض' if ph < 7.35 else '⚠️ قلاء' if ph > 7.45 else '✅ طبيعي'} |
| PaO2 | {pao2} | 80-100 | {'🚨 نقص أكسجة شديد' if pao2 < 60 else '⚠️ نقص أكسجة' if pao2 < 80 else '✅ طبيعي'} |

---

#### 📈 المؤشرات المحسوبة
- **تصفية الكرياتينين:** {creatinine_clearance:.1f} mL/min ({'✅ طبيعي' if creatinine_clearance > 90 else '⚠️ ضعف كلوي' if creatinine_clearance > 60 else '🚨 فشل كلوي'})
- **P/F Ratio:** {pf_ratio:.1f} ({'✅ طبيعي' if pf_ratio > 300 else '⚠️ ضعف أكسجة' if pf_ratio > 200 else '🚨 فشل تنفسي'})
- **الاحتياجات السعرية:** {caloric_needs:.0f} سعرة/يوم
- **الاحتياجات السائلة:** {fluid_needs:.0f} مل/يوم
- **الاحتياجات البروتينية:** {protein_needs:.1f} جرام/يوم

---

#### 🎯 التشخيص التفريقي مع نسب الثقة

"""
    diagnoses = []
    if lactate > 4 and bp < 90:
        diagnoses.append(("🩺 **Sepsis مع Septic Shock**", 92, ["Lactate > 4", "ضغط منخفض", "تسرع قلبي", "حمى"]))
    elif lactate > 4:
        diagnoses.append(("🩺 **Sepsis (إنتان)**", 78, ["Lactate > 4", "تسرع قلبي", "حمى"]))
    elif creatinine > 2:
        diagnoses.append(("🩺 **AKI (فشل كلوي حاد)**", 75, ["Creatinine > 2", "BUN مرتفع"]))
    
    if spo2 < 90 and rr > 20:
        diagnoses.append(("🩺 **ARDS (متلازمة الضائقة التنفسية)**", 65, ["SpO2 < 90", "تسرع تنفس", "PaO2 منخفض"]))
    
    if potassium > 5.5:
        diagnoses.append(("⚠️ **ارتفاع البوتاسيوم الحاد**", 80, ["K > 5.5", "خطر توقف القلب"]))
    
    if ph < 7.35:
        diagnoses.append(("⚠️ **حماض استقلابي**", 70, ["pH < 7.35", "HCO3 منخفض"]))
    
    if wbc > 15 and temp > 38:
        diagnoses.append(("⚠️ **عدوى بكتيرية محتملة**", 60, ["WBC مرتفع", "حمى"]))
    
    if not diagnoses:
        diagnoses.append(("🩺 **حالة مستقرة - يحتاج إلى مراقبة**", 60, ["جميع المؤشرات ضمن الحدود المقبولة"]))

    for i, (diag, conf, evidence) in enumerate(diagnoses, 1):
        report += f"\n{i}. **{diag}** - نسبة الثقة: {conf}%\n"
        report += f"   الأدلة: {', '.join(evidence)}\n"

    report += f"""

---

#### 💊 خطة العلاج المقترحة

| الأولوية | الإجراء | التفاصيل | السبب |
|----------|---------|----------|-------|
| 1 | 💉 السوائل الوريدية | Normal Saline 30ml/kg = {patient['weight'] * 30:.0f}ml | تحسين التروية وضغط الدم |
| 2 | 💊 المضادات الحيوية | Meropenem 1g IV كل 8 ساعات | تغطية الجراثيم في الإنتان |
| 3 | 🫁 دعم التنفس | أكسجين عالي التدفق 60-100% | تحسين الأكسجة |
| 4 | 💉 فازوبريشر | Norepinephrine عند الحاجة | دعم ضغط الدم |
| 5 | 🧪 مراقبة المختبر | Lactate, Creatinine, K كل 4-6 ساعات | متابعة الاستجابة |

---

#### 🔔 تنبيهات وتوصيات عاجلة

"""
    if bp < 90:
        report += "🚨 **عاجل:** ضغط الدم منخفض! ابدأ بالسوائل الوريدية فوراً.\n"
    if spo2 < 90:
        report += "🚨 **عاجل:** نقص أكسجة حاد! أعطِ أكسجين عالي التدفق.\n"
    if lactate > 4:
        report += "🚨 **عاجل:** ارتفاع اللاكتات! أعد تقييم الإنتان.\n"
    if potassium > 5.5:
        report += "🚨 **عاجل:** ارتفاع البوتاسيوم! أعطِ كالسيوم جلوكونات.\n"
    
    report += f"""
    - 📊 إعادة فحص Lactate خلال 2-4 ساعات
    - 🩸 مراقبة ضغط الدم كل ساعة
    - 🧪 إعادة تحليل الكرياتينين بعد 24 ساعة
    - 📋 إعادة تقييم الحالة خلال 24-48 ساعة

---

🤖 *تم إنشاء هذا التقرير بواسطة الذكاء الاصطناعي المتقدم*
⚠️ *هذا التقرير استرشادي ويجب مراجعته من قبل الطبيب المختص*
"""
    return report

def get_ai_diagnosis(patient, lang):
    if GEMINI_AVAILABLE:
        try:
            context = f"""
            Patient: {patient['name']}, Age: {patient['age']}, Gender: {patient['gender']}
            Weight: {patient['weight']}kg, Height: {patient['height']}cm
            BMI: {calculate_bmi(patient['weight'], patient['height']):.1f}
            
            Vitals: BP {patient['vitals']['systolic_bp']}/{patient['vitals']['diastolic_bp']}, HR {patient['vitals']['heart_rate']}, Temp {patient['vitals']['temperature']}°C, SpO2 {patient['vitals']['spo2']}%
            
            Labs: WBC {patient['labs']['wbc']}, HB {patient['labs']['hb']}, PLT {patient['labs']['plt']}, pH {patient['labs']['ph']}, PaCO2 {patient['labs']['paco2']}, PaO2 {patient['labs']['pao2']}, HCO3 {patient['labs']['hco3']}, Na {patient['labs']['na']}, K {patient['labs']['k']}, Ca {patient['labs']['ca']}, Creatinine {patient['labs']['creatinine']}, BUN {patient['labs']['bun']}, ALT {patient['labs']['alt']}, AST {patient['labs']['ast']}, Bilirubin {patient['labs']['bilirubin']}, INR {patient['labs']['inr']}, Troponin {patient['labs']['troponin']}, Lactate {patient['labs']['lactate']}
            
            SOFA: {patient['sofa_score']}, NEWS2: {patient['news2_score']}, GCS: {patient['gcs_score']}
            
            Provide comprehensive diagnosis and treatment plan in {lang}.
            """
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(context)
            return {"success": True, "diagnosis": response.text, "source": "Gemini AI"}
        except:
            pass
    
    return {"success": True, "diagnosis": generate_advanced_diagnosis(patient, lang), "source": "AI Simulator"}

# ======================================================================
# 🔔 التنبيهات
# ======================================================================

def check_alerts(patient):
    alerts = []
    if patient['vitals']['systolic_bp'] < 90:
        alerts.append({"type": "critical", "title": "انخفاض الضغط", "message": f"الضغط: {patient['vitals']['systolic_bp']} mmHg", "action": "ابدأ بالسوائل الوريدية"})
    if patient['vitals']['spo2'] < 90:
        alerts.append({"type": "critical", "title": "نقص أكسجة", "message": f"SpO2: {patient['vitals']['spo2']}%", "action": "أعطِ أكسجين"})
    if patient['vitals']['heart_rate'] > 120:
        alerts.append({"type": "critical", "title": "تسرع قلبي", "message": f"النبض: {patient['vitals']['heart_rate']} نبضة/دقيقة", "action": "تحقق من حالة السوائل"})
    if patient['vitals']['temperature'] > 39.0:
        alerts.append({"type": "critical", "title": "حمى شديدة", "message": f"الحرارة: {patient['vitals']['temperature']}°C", "action": "خذ عينات للزراعة"})
    if patient['labs']['lactate'] > 4:
        alerts.append({"type": "critical", "title": "ارتفاع اللاكتات", "message": f"Lactate: {patient['labs']['lactate']} mmol/L", "action": "أعد تقييم الإنتان"})
    if patient['labs']['k'] > 5.5:
        alerts.append({"type": "critical", "title": "ارتفاع البوتاسيوم", "message": f"K: {patient['labs']['k']} mEq/L", "action": "أعطِ كالسيوم جلوكونات"})
    if patient['labs']['wbc'] > 15:
        alerts.append({"type": "high", "title": "ارتفاع كريات الدم البيضاء", "message": f"WBC: {patient['labs']['wbc']}", "action": "ابحث عن مصدر العدوى"})
    if patient['sofa_score'] >= 4:
        alerts.append({"type": "critical", "title": "خلل عضوي", "message": f"SOFA: {patient['sofa_score']}", "action": "تقييم عاجل"})
    return alerts

# ======================================================================
# 📱 إعدادات الصفحة
# ======================================================================

st.set_page_config(page_title="Mohammed ICU", page_icon="🏥", layout="wide")

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
                "systolic_bp": 85, "diastolic_bp": 55, "heart_rate": 115,
                "temperature": 38.5, "respiratory_rate": 24, "spo2": 88,
                "cvp": 12, "icp": 18, "ecg": "تسرع قلبي"
            },
            "labs": {
                "wbc": 18.5, "hb": 10.2, "plt": 85, "ph": 7.28,
                "paco2": 45, "pao2": 60, "hco3": 18, "na": 135,
                "k": 5.8, "ca": 8.2, "creatinine": 2.5, "bun": 45,
                "alt": 120, "ast": 150, "bilirubin": 3.2,
                "pt": 18.5, "inr": 1.8, "troponin": 0.15, "lactate": 5.2
            },
            "sofa_score": 6, "news2_score": 8, "gcs_score": 12,
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
                "systolic_bp": 110, "diastolic_bp": 70, "heart_rate": 85,
                "temperature": 37.8, "respiratory_rate": 18, "spo2": 95,
                "cvp": 8, "icp": 12, "ecg": "طبيعي"
            },
            "labs": {
                "wbc": 12.5, "hb": 12.5, "plt": 250, "ph": 7.38,
                "paco2": 38, "pao2": 75, "hco3": 22, "na": 140,
                "k": 4.2, "ca": 9.0, "creatinine": 0.8, "bun": 18,
                "alt": 45, "ast": 55, "bilirubin": 0.8,
                "pt": 12.5, "inr": 1.0, "troponin": 0.02, "lactate": 1.8
            },
            "sofa_score": 2, "news2_score": 3, "gcs_score": 15,
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
    lang = st.session_state.lang
    L = LANGUAGES[lang]
    
    # اختيار اللغة في الأعلى
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        selected_lang = st.selectbox("🌐", list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index(lang))
        if selected_lang != lang:
            st.session_state.lang = selected_lang
            st.rerun()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0c2340, #1a5276); padding: 35px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 48px; margin: 0;">{L['app_title']}</h1>
        <p style="font-size: 20px; opacity: 0.9;">{L['app_subtitle']}</p>
        <p style="font-size: 14px; opacity: 0.7;">🌐 {lang}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='text-align: center;'>{L['choose_role']}</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button(L['doctor'], use_container_width=True):
                st.session_state.role = "doctor"
                st.session_state.page = "login_form"
                st.rerun()
        with col_b:
            if st.button(L['nurse'], use_container_width=True):
                st.session_state.role = "nurse"
                st.session_state.page = "login_form"
                st.rerun()
        with col_c:
            if st.button(L['admin'], use_container_width=True):
                st.session_state.role = "admin"
                st.session_state.page = "login_form"
                st.rerun()

def login_form():
    lang = st.session_state.lang
    L = LANGUAGES[lang]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        selected_lang = st.selectbox("🌐", list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index(lang))
        if selected_lang != lang:
            st.session_state.lang = selected_lang
            st.rerun()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0c2340, #1a5276); padding: 25px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 36px; margin: 0;">{L['app_title']}</h1>
        <p style="font-size: 16px; opacity: 0.8;">{L['app_subtitle']}</p>
        <p style="font-size: 14px; opacity: 0.6;">{L[st.session_state.role]} | 🌐 {lang}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown(f"### {L['login']}")
            username = st.text_input(L['username'])
            password = st.text_input(L['password'], type="password")
            submitted = st.form_submit_button(L['login_btn'], use_container_width=True)
            
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
                    st.error("❌ " + ("بيانات غير صحيحة" if lang == "العربية" else "Invalid credentials"))
            
            st.caption(f"📝 {L['admin']}: mohammed / 07702574105")

# ======================================================================
# 📊 لوحة التحكم
# ======================================================================

def dashboard():
    lang = st.session_state.lang
    L = LANGUAGES[lang]
    
    with st.sidebar:
        # اختيار اللغة
        selected_lang = st.selectbox("🌐", list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index(lang))
        if selected_lang != lang:
            st.session_state.lang = selected_lang
            st.rerun()
        
        st.markdown("---")
        
        st.markdown(f"### 👤 {st.session_state.user['name']}")
        role_names = {"doctor": L['doctor'], "nurse": L['nurse'], "admin": L['admin']}
        st.markdown(f"📋 {role_names.get(st.session_state.role, '')}")
        st.markdown(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
        st.markdown("---")
        
        if st.session_state.patients:
            patient_names = [p["name"] + " (" + p.get('bed_number', '') + ")" for p in st.session_state.patients]
            selected = st.selectbox(L['select_patient'], patient_names)
            idx = patient_names.index(selected)
            st.session_state.selected_patient = st.session_state.patients[idx]
        
        st.markdown("---")
        
        critical = sum(1 for p in st.session_state.patients if p['risk_level'] == 'حرج')
        moderate = sum(1 for p in st.session_state.patients if p['risk_level'] == 'متوسط')
        low = sum(1 for p in st.session_state.patients if p['risk_level'] == 'منخفض')
        st.metric("🔴 " + L['critical'], critical)
        st.metric("🟡 " + L['moderate'], moderate)
        st.metric("🟢 " + L['low'], low)
        
        st.markdown("---")
        if st.button(L['logout'], use_container_width=True):
            log_logout(st.session_state.login_username)
            st.session_state.clear()
            st.rerun()
    
    patient = st.session_state.selected_patient
    
    if patient:
        risk_class = "status-critical" if patient['risk_level'] == "حرج" else "status-moderate" if patient['risk_level'] == "متوسط" else "status-low"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0c2340, #1a5276); padding: 25px; border-radius: 12px; color: white; margin-bottom: 25px;">
            <h2 style="margin: 0;">🩺 {patient['name']}</h2>
            <p>🧬 {L['age']}: {patient['age']} {'سنة' if lang == 'العربية' else 'years'} | {patient['gender']} | ⚖️ {L['weight']}: {patient['weight']} {'كجم' if lang == 'العربية' else 'kg'}</p>
            <p>🛏️ {patient.get('bed_number', 'لا يوجد')}</p>
            <p>📋 {L['diagnosis']}: {patient['diagnosis']}</p>
            <span style="display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 14px; background: {'#e74c3c' if patient['risk_level'] == 'حرج' else '#f1c40f' if patient['risk_level'] == 'متوسط' else '#2ecc71'}; color: {'white' if patient['risk_level'] == 'حرج' else 'black' if patient['risk_level'] == 'متوسط' else 'white'};">{patient['risk_level']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        tabs = st.tabs([
            L['vitals'],
            L['lab'],
            L['assessment'],
            L['ai'],
            L['alerts'],
            L['radiology'],
            L['voice_record'],
            L['medical_orders']
        ])
        
        # ===== العلامات الحيوية =====
        with tabs[0]:
            vitals = patient['vitals']
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(L['blood_pressure'], f"{vitals['systolic_bp']}/{vitals['diastolic_bp']}")
            with col2:
                st.metric(L['heart_rate'], f"{vitals['heart_rate']}")
            with col3:
                st.metric(L['temperature'], f"{vitals['temperature']}°C")
            with col4:
                st.metric(L['spo2'], f"{vitals['spo2']}%")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(L['respiratory'], f"{vitals['respiratory_rate']}")
            with col2:
                st.metric("CVP", f"{vitals['cvp']}")
            with col3:
                st.metric("ICP", f"{vitals['icp']}")
        
        # ===== المختبر =====
        with tabs[1]:
            labs = patient['labs']
            lab_data = {
                "الفحص" if lang == "العربية" else "Test": ["WBC", "HB", "PLT", "pH", "PaCO2", "PaO2", "HCO3", "Na", "K", "Ca", "Creatinine", "BUN", "ALT", "AST", "Bilirubin", "INR", "Troponin", "Lactate"],
                "النتيجة" if lang == "العربية" else "Result": [labs['wbc'], labs['hb'], labs['plt'], labs['ph'], labs['paco2'], labs['pao2'], labs['hco3'], labs['na'], labs['k'], labs['ca'], labs['creatinine'], labs['bun'], labs['alt'], labs['ast'], labs['bilirubin'], labs['inr'], labs['troponin'], labs['lactate']],
                "الوحدة" if lang == "العربية" else "Unit": ["×10³/µL", "g/dL", "×10³/µL", "", "mmHg", "mmHg", "mEq/L", "mEq/L", "mEq/L", "mEq/L", "mg/dL", "mg/dL", "U/L", "U/L", "mg/dL", "", "ng/mL", "mmol/L"]
            }
            df = pd.DataFrame(lab_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # ===== التقييم السريري =====
        with tabs[2]:
            st.subheader("🧠 " + L['assessment'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("SOFA Score", patient['sofa_score'])
                st.metric("APACHE II", "18")
            with col2:
                st.metric("NEWS2", patient['news2_score'])
                st.metric("qSOFA", "2")
            with col3:
                st.metric("GCS", patient['gcs_score'])
                st.metric(L['risk_level'], patient['risk_level'])
            
            st.markdown("---")
            if patient['sofa_score'] >= 4:
                st.error(f"🚨 **SOFA Score = {patient['sofa_score']}** - خلل عضوي حاد")
            if patient['news2_score'] >= 7:
                st.error(f"🚨 **NEWS2 = {patient['news2_score']}** - حالة حرجة")
            if patient['gcs_score'] <= 8:
                st.error(f"🚨 **GCS = {patient['gcs_score']}** - غيبوبة عميقة")
        
        # ===== الذكاء الاصطناعي =====
        with tabs[3]:
            st.subheader("🤖 " + L['ai'])
            
            if not has_permission(st.session_state.user, "ai_analysis"):
                st.warning("⚠️ " + ("ليس لديك صلاحية" if lang == "العربية" else "No permission"))
            else:
                if st.button("🧠 " + ("تشغيل التحليل الذكي" if lang == "العربية" else "Run AI Analysis"), use_container_width=True, type="primary"):
                    with st.spinner("🧠 " + ("جاري التحليل..." if lang == "العربية" else "Analyzing...")):
                        result = get_ai_diagnosis(patient, lang)
                        if result["success"]:
                            st.markdown("### 📊 " + ("التقرير السريري المتقدم" if lang == "العربية" else "Advanced Clinical Report"))
                            st.markdown(result["diagnosis"])
                            st.info(f"📡 {L['source']}: {result['source']}")
                        else:
                            st.error(f"❌ {result.get('error', 'Unknown error')}")
        
        # ===== التنبيهات =====
        with tabs[4]:
            st.subheader("🔔 " + L['alerts'])
            alerts = check_alerts(patient)
            if alerts:
                for alert in alerts:
                    st.warning(f"**{alert['title']}**\n\n{alert['message']}\n\n🛑 {alert['action']}")
            else:
                st.success("✅ " + L['no_alerts'])
        
        # ===== الأشعة =====
        with tabs[5]:
            st.subheader("🩻 " + L['radiology'])
            uploaded = st.file_uploader("📤 " + ("رفع صورة الأشعة" if lang == "العربية" else "Upload Radiology Image"), type=["jpg", "jpeg", "png"])
            if uploaded:
                st.image(uploaded, caption="صورة الأشعة", use_column_width=True)
                st.success("✅ " + ("تم رفع الصورة بنجاح" if lang == "العربية" else "Image uploaded"))
        
        # ===== تسجيل صوتي =====
        with tabs[6]:
            st.subheader("🎤 " + L['voice_record'])
            audio = st.file_uploader("🎵 " + ("رفع ملف صوتي" if lang == "العربية" else "Upload Audio"), type=["wav", "mp3"])
            if audio:
                st.success("✅ " + ("تم رفع الملف الصوتي" if lang == "العربية" else "Audio uploaded"))
                notes = st.text_area("📝 " + ("ملاحظات إضافية" if lang == "العربية" else "Additional Notes"))
                if st.button("💾 " + ("حفظ" if lang == "العربية" else "Save")):
                    st.success("✅ " + ("تم حفظ التسجيل الصوتي" if lang == "العربية" else "Audio saved"))
        
        # ===== الأوامر الطبية =====
        with tabs[7]:
            st.subheader("📋 " + L['medical_orders'])
            
            is_doctor = st.session_state.role == "doctor"
            is_admin = st.session_state.role == "admin"
            
            if patient['id'] in st.session_state.medical_orders:
                orders = st.session_state.medical_orders[patient['id']]
                for i, order in enumerate(orders):
                    status = order.get('status', 'معلق')
                    status_color = "orange" if status == 'pending' else "blue" if status == 'received' else "green"
                    
                    # تحذيرات موانع الاستخدام
                    contraindications = check_contraindications(patient, order['medication'])
                    
                    st.markdown(f"""
                    <div style="background: #eaf2f8; padding: 15px; border-radius: 10px; margin: 10px 0; border-right: 4px solid #2e86c1;">
                        <strong>💊 {order['medication']}</strong>
                        <br>📊 الجرعة: {order['dose']:.1f} {order['unit']}
                        <br>⏰ التوقيت: {order['frequency']}
                        <br>💉 الطريق: {order['route']}
                        <br>📝 ملاحظات: {order.get('notes', 'لا يوجد')}
                        <br>🕐 وصف بواسطة: {order.get('prescribed_by', 'الطبيب')} في {order.get('prescribed_time', '')}
                        <br>📥 استلم بواسطة: {order.get('received_by_nurse', 'لم يستلم')}
                        <br>🔄 نفذ بواسطة: {order.get('executed_by_nurse', 'لم ينفذ')}
                        <br>⚠️ التحذيرات: {', '.join(contraindications) if contraindications else '✅ لا توجد موانع'}
                        <br>📋 تعليمات المراقبة: {', '.join(MEDICATION_DATABASE.get(order['medication'], {}).get('monitoring', []))}
                        <br><span style="color: {status_color};">الحالة: {status}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.session_state.role == "nurse":
                        col1, col2 = st.columns(2)
                        with col1:
                            if order.get('status') == 'pending':
                                if st.button(f"📥 استلام الأمر", key=f"receive_{i}"):
                                    order['status'] = 'received'
                                    order['received_by_nurse'] = st.session_state.user['name']
                                    order['received_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    st.rerun()
                        with col2:
                            if order.get('status') == 'received':
                                if st.button(f"🔄 تنفيذ الأمر", key=f"execute_{i}"):
                                    order['status'] = 'executed'
                                    order['executed_by_nurse'] = st.session_state.user['name']
                                    order['executed_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    st.rerun()
            else:
                st.info("📝 " + ("لا توجد أوامر طبية حالياً" if lang == "العربية" else "No medical orders"))
            
            if is_doctor or is_admin:
                st.markdown("---")
                st.markdown("### ➕ " + ("إضافة أمر طبي جديد" if lang == "العربية" else "Add New Medical Order"))
                
                with st.form("new_order"):
                    col1, col2 = st.columns(2)
                    with col1:
                        medication = st.selectbox("💊 " + ("اختيار الدواء" if lang == "العربية" else "Select Medication"), list(MEDICATION_DATABASE.keys()))
                        weight = patient['weight']
                        age = patient['age']
                        creatinine = patient['labs']['creatinine']
                        dose, frequency, warning = calculate_dose(medication, weight, age, creatinine)
                        
                        st.info(f"""
                        ⚖️ {L['weight']}: {weight} {'كجم' if lang == 'العربية' else 'kg'}
                        🧬 {L['age']}: {age} {'سنة' if lang == 'العربية' else 'years'}
                        🧪 Creatinine: {creatinine} mg/dL
                        """)
                        
                        st.markdown(f"""
                        <div style="background: #d5f5e3; padding: 15px; border-radius: 10px;">
                            <strong>💉 {L['weight']}:</strong> {dose:.1f} mg
                            <br><strong>⏰ {L['age']}:</strong> {frequency}
                            <br><strong>{warning}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        custom_dose = st.number_input("✏️ " + ("تعديل الجرعة" if lang == "العربية" else "Custom Dose"), value=float(dose), step=100.0)
                        route = st.selectbox("💉 " + ("طريق الإعطاء" if lang == "العربية" else "Route"), ["IV", "IM", "PO", "SC"])
                        notes = st.text_area("📝 " + ("ملاحظات إضافية" if lang == "العربية" else "Additional Notes"))
                    
                    if st.form_submit_button("💾 " + ("حفظ الأمر الطبي" if lang == "العربية" else "Save Order"), use_container_width=True, type="primary"):
                        order = {
                            "medication": medication,
                            "dose": custom_dose,
                            "unit": "mg" if medication != "Heparin" else "units",
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
                        st.success(f"✅ " + (f"تم إضافة الأمر الطبي لـ {medication} بنجاح!" if lang == "العربية" else f"Medical order for {medication} added successfully!"))
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