# ======================================================================
# 🏥 MOHAMMED ICU - نظام العناية المركزة الذكي المتكامل
# ======================================================================
# الإصدار النهائي المتكامل - مع نظام المدير والممرضين والأوامر
# ======================================================================

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
    "السكري (Diabetes Mellitus)",
    "ارتفاع ضغط الدم (Hypertension)",
    "أمراض القلب (Heart Disease)",
    "فشل القلب (Heart Failure)",
    "الربو (Asthma)",
    "مرض الانسداد الرئوي المزمن (COPD)",
    "أمراض الكلى المزمنة (CKD)",
    "الفشل الكلوي (Renal Failure)",
    "أمراض الكبد (Liver Disease)",
    "التهاب الكبد الوبائي (Hepatitis)",
    "الغدة الدرقية (Thyroid Disease)",
    "فقر الدم (Anemia)",
    "السرطان (Cancer)",
    "لا يوجد"
]

ALLERGIES_LIST = [
    "البنسلين (Penicillin)",
    "الأسبرين (Aspirin)",
    "الإيبوبروفين (Ibuprofen)",
    "المضادات الحيوية (Antibiotics)",
    "اللاتكس (Latex)",
    "الغبار (Dust)",
    "حبوب اللقاح (Pollen)",
    "البيض (Eggs)",
    "الحليب (Milk)",
    "المكسرات (Nuts)",
    "لا يوجد"
]

MEDICATIONS_LIST = [
    "الأنسولين (Insulin)",
    "الليسينوبريل (Lisinopril)",
    "الاملوديبين (Amlodipine)",
    "الميتفورمين (Metformin)",
    "الديجوكسين (Digoxin)",
    "الفيوروسيمايد (Furosemide)",
    "الستاتينات (Statins)",
    "الأسبرين (Aspirin)",
    "الباراسيتامول (Paracetamol)",
    "المورفين (Morphine)",
    "لا يوجد"
]

DIAGNOSIS_LIST = [
    "Sepsis (الإنتان)",
    "Septic Shock (الصدمة الإنتانية)",
    "Pneumonia (الالتهاب الرئوي)",
    "ARDS (متلازمة الضائقة التنفسية الحادة)",
    "AKI (الفشل الكلوي الحاد)",
    "Heart Failure (فشل القلب)",
    "Hypertension (ارتفاع الضغط)",
    "Diabetes (السكري)",
    "Asthma (الربو)",
    "COPD (مرض الانسداد الرئوي المزمن)",
    "Stroke (السكتة الدماغية)",
    "Myocardial Infarction (احتشاء عضلة القلب)",
    "Liver Cirrhosis (تليف الكبد)",
    "Cancer (السرطان)",
    "Thyroid Disorder (اضطراب الغدة الدرقية)",
    "Anemia (فقر الدم)"
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
# 🌐 إعدادات التعدد اللغوي
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
        "assessment": "🧠 التقييم",
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
    
    # المستخدمين
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
    
    # المرضى
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
    
    # سجل الدخول والخروج
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
    
    # الأوامر الطبية
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
    
    # تقارير الممرض اليومية
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
        "permissions": ["view_patients", "add_vitals", "voice", "alerts", "receive_orders", "execute_orders", "daily_report"]
    },
    "nurse_ali": {
        "password": hash_password("ali123"),
        "role": "nurse",
        "name": "علي",
        "approved": True,
        "permissions": ["view_patients", "add_vitals", "voice", "alerts", "receive_orders", "execute_orders", "daily_report"]
    },
    "nurse_sara": {
        "password": hash_password("sara123"),
        "role": "nurse",
        "name": "سارة",
        "approved": True,
        "permissions": ["view_patients", "add_vitals", "voice", "alerts", "receive_orders", "execute_orders", "daily_report"]
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
        warning = f"⚠️ تم تخفيض الجرعة إلى الحد الأقصى ({med_info['max_dose']})"
    else:
        final_dose = base_dose
        warning = "✅ الجرعة ضمن الحد الآمن"
    
    return final_dose, med_info["frequency"], warning

def check_contraindications(patient, medication):
    warnings = []
    
    for allergy in patient.get('allergies', []):
        if "البنسلين" in allergy and medication in ["Meropenem", "Piperacillin-Tazobactam"]:
            warnings.append("🚫 حساسية للبنسلين! استخدم بديلاً.")
    
    if medication in ["Norepinephrine", "Dobutamine"] and patient['vitals']['systolic_bp'] > 180:
        warnings.append("⚠️ ضغط الدم مرتفع جداً!")
    
    if patient['labs']['creatinine'] > 2.5 and medication in ["Vancomycin", "Meropenem"]:
        warnings.append("⚠️ وظائف الكلى متدهورة! قلل الجرعة.")
    
    return warnings

# ======================================================================
# 🤖 الذكاء الاصطناعي
# ======================================================================

def generate_simulation_diagnosis(patient, lang):
    issues = []
    recommendations = []
    
    if patient['vitals']['systolic_bp'] < 90:
        issues.append("🔴 " + ("انخفاض حاد في ضغط الدم" if lang == "العربية" else "Severe hypotension"))
        recommendations.append("💉 " + ("ابدأ بالسوائل الوريدية فوراً" if lang == "العربية" else "Start IV fluids immediately"))
    
    if patient['vitals']['spo2'] < 90:
        issues.append("🔴 " + ("نقص أكسجة حاد" if lang == "العربية" else "Severe hypoxemia"))
        recommendations.append("🫁 " + ("أعطِ أكسجين عالي التدفق" if lang == "العربية" else "Administer high-flow oxygen"))
    
    if patient['labs']['lactate'] > 4:
        issues.append("🔴 " + ("ارتفاع اللاكتات - خطر الإنتان" if lang == "العربية" else "High lactate - Sepsis risk"))
        recommendations.append("🧪 " + ("أعد تقييم الإنتان" if lang == "العربية" else "Re-evaluate sepsis"))
    
    if patient['labs']['creatinine'] > 2:
        issues.append("🟡 " + ("ارتفاع الكرياتينين - خطر الفشل الكلوي" if lang == "العربية" else "High creatinine - AKI risk"))
        recommendations.append("💊 " + ("راقب السوائل" if lang == "العربية" else "Monitor fluids"))
    
    if patient['labs']['k'] > 5.5:
        issues.append("🔴 " + ("ارتفاع البوتاسيوم" if lang == "العربية" else "Hyperkalemia"))
        recommendations.append("💉 " + ("أعطِ كالسيوم جلوكونات" if lang == "العربية" else "Give Calcium gluconate"))
    
    if patient['labs']['lactate'] > 4 and patient['vitals']['systolic_bp'] < 90:
        main_diagnosis = "🩺 **Sepsis مع Septic Shock** (85%)"
    elif patient['labs']['creatinine'] > 2:
        main_diagnosis = "🩺 **فشل كلوي حاد** (75%)"
    else:
        main_diagnosis = "🩺 **حالة مستقرة نسبياً**"
        recommendations.append("📊 " + ("استمرار المراقبة" if lang == "العربية" else "Continue monitoring"))
    
    report = f"""
### 📋 {"التقرير السريري" if lang == "العربية" else "Clinical Report"}

---

#### 🎯 {"التشخيص الرئيسي" if lang == "العربية" else "Primary Diagnosis"}
{main_diagnosis}

---

#### ⚠️ {"المشاكل المكتشفة" if lang == "العربية" else "Detected Issues"}
"""
    for issue in issues:
        report += f"- {issue}\n"
    
    if not issues:
        report += "- ✅ " + ("لا توجد مشاكل حرجة" if lang == "العربية" else "No critical issues") + "\n"
    
    report += f"""

#### 📊 {"المؤشرات المحسوبة" if lang == "العربية" else "Calculated Indicators"}
- **BMI:** {calculate_bmi(patient['weight'], patient['height']):.1f}
- **{"الوزن المثالي" if lang == "العربية" else "Ideal Weight"}:** {calculate_ideal_weight(patient['height']):.1f} {"كجم" if lang == "العربية" else "kg"}
- **{"تصفية الكرياتينين" if lang == "العربية" else "Creatinine Clearance"}:** {calculate_creatinine_clearance(patient['age'], patient['weight'], patient['labs']['creatinine'], patient['gender']):.1f} mL/min

---

#### 💊 {"خطة العلاج المقترحة" if lang == "العربية" else "Treatment Plan"}
"""
    for i, rec in enumerate(recommendations, 1):
        report += f"{i}. {rec}\n"

    report += f"""

#### 📈 {"خطة المتابعة" if lang == "العربية" else "Follow-up Plan"}
- 📊 {"إعادة فحص Lactate خلال 2-4 ساعات" if lang == "العربية" else "Re-check Lactate in 2-4 hours"}
- 🩸 {"مراقبة ضغط الدم كل ساعة" if lang == "العربية" else "Monitor BP every hour"}

---
🤖 *{"تم إنشاء هذا التقرير بواسطة الذكاء الاصطناعي" if lang == "العربية" else "This report was generated by AI"}*
⚠️ *{"هذا التقرير استرشادي ويجب مراجعته من قبل الطبيب المختص" if lang == "العربية" else "This report is for guidance only"}*
"""
    return report

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
                "source": "Gemini AI (حقيقي)"
            }
        except:
            pass
    
    return {
        "success": True,
        "diagnosis": generate_simulation_diagnosis(patient, lang),
        "bmi": bmi,
        "ideal_weight": ideal_weight,
        "creatinine_clearance": creatinine_clearance,
        "source": "AI Simulator (المحاكاة)"
    }

# ======================================================================
# 🔔 التنبيهات
# ======================================================================

def check_alerts(patient, lang):
    alerts = []
    
    if patient['vitals']['systolic_bp'] < 90:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("انخفاض الضغط" if lang == "العربية" else "Hypotension"),
            "message": f"{'الضغط' if lang == 'العربية' else 'BP'}: {patient['vitals']['systolic_bp']} mmHg",
            "action": "💉 " + ("ابدأ بالسوائل الوريدية" if lang == "العربية" else "Start IV fluids")
        })
    
    if patient['vitals']['spo2'] < 90:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("نقص أكسجة" if lang == "العربية" else "Hypoxemia"),
            "message": f"SpO2: {patient['vitals']['spo2']}%",
            "action": "🫁 " + ("أعطِ أكسجين" if lang == "العربية" else "Give oxygen")
        })
    
    if patient['labs']['lactate'] > 4:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("ارتفاع اللاكتات" if lang == "العربية" else "High Lactate"),
            "message": f"Lactate: {patient['labs']['lactate']} mmol/L",
            "action": "🧪 " + ("أعد تقييم الإنتان" if lang == "العربية" else "Re-evaluate sepsis")
        })
    
    if patient['labs']['k'] > 5.5:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("ارتفاع البوتاسيوم" if lang == "العربية" else "Hyperkalemia"),
            "message": f"K: {patient['labs']['k']} mEq/L",
            "action": "💉 " + ("أعطِ كالسيوم جلوكونات" if lang == "العربية" else "Give Calcium gluconate")
        })
    
    if patient['sofa_score'] >= 4:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("خلل عضوي" if lang == "العربية" else "Organ Failure"),
            "message": f"SOFA: {patient['sofa_score']}",
            "action": "🆘 " + ("تقييم عاجل" if lang == "العربية" else "Urgent assessment")
        })
    
    return alerts

# ======================================================================
# 📱 إعدادات الصفحة
# ======================================================================

st.set_page_config(
    page_title="Mohammed ICU",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0c2340, #1a5276);
        padding: 35px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .main-header h1 { font-size: 48px; margin: 0; }
    .main-header p { font-size: 20px; opacity: 0.9; }
    .patient-header {
        background: linear-gradient(135deg, #0c2340, #1a5276);
        padding: 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
    }
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
    }
    .status-critical { background: #e74c3c; color: white; }
    .status-moderate { background: #f1c40f; color: black; }
    .status-low { background: #2ecc71; color: white; }
    .alert-critical {
        background: #fadbd8;
        border-right: 6px solid #e74c3c;
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
    }
    .success-box {
        background: #d5f5e3;
        border-right: 6px solid #27ae60;
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
    }
    .order-box {
        background: #eaf2f8;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-right: 4px solid #2e86c1;
    }
    .admin-box {
        background: #fef9e7;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-right: 4px solid #f39c12;
    }
    @media (max-width: 768px) {
        .stDataFrame { font-size: 12px !important; overflow-x: auto !important; }
        .stColumns { flex-direction: column !important; }
        .stButton button { width: 100% !important; padding: 15px !important; font-size: 18px !important; }
        .main-header h1 { font-size: 28px !important; }
        .patient-header h2 { font-size: 20px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ======================================================================
# 🌐 اختيار اللغة
# ======================================================================

if 'lang' not in st.session_state:
    st.session_state.lang = "العربية"

# ======================================================================
# 📦 البيانات
# ======================================================================

if 'patients' not in st.session_state:
    st.session_state.patients = [
        {
            "id": 1,
            "name": "أحمد محمد",
            "age": 65,
            "gender": "ذكر",
            "weight": 78,
            "height": 175,
            "chronic_diseases": ["السكري (Diabetes Mellitus)"],
            "allergies": ["البنسلين (Penicillin)"],
            "surgeries": ["قسطرة قلبية 2020"],
            "current_medications": ["الأنسولين (Insulin)"],
            "diagnosis": "Sepsis (الإنتان)",
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
            "chronic_diseases": ["الربو (Asthma)"],
            "allergies": ["لا يوجد"],
            "surgeries": ["لا يوجد"],
            "current_medications": ["لا يوجد"],
            "diagnosis": "Pneumonia (الالتهاب الرئوي)",
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
# 🔐 تسجيل الدخول
# ======================================================================

def login_page():
    lang = st.session_state.lang
    L = LANGUAGES[lang]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        selected_lang = st.selectbox("🌐", list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index(lang))
        if selected_lang != lang:
            st.session_state.lang = selected_lang
            st.rerun()
    
    st.markdown(f"""
    <div class="main-header">
        <h1>{L['app_title']}</h1>
        <p>{L['app_subtitle']}</p>
        <p style="font-size: 14px; opacity: 0.7;">🌐 {lang}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='text-align: center;'>{L['choose_role']}</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button(L['doctor'], use_container_width=True, type="primary"):
                st.session_state.role = "doctor"
                st.session_state.page = "login_form"
                st.rerun()
        with col_b:
            if st.button(L['nurse'], use_container_width=True, type="primary"):
                st.session_state.role = "nurse"
                st.session_state.page = "login_form"
                st.rerun()
        with col_c:
            if st.button(L['admin'], use_container_width=True, type="primary"):
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
    <div class="main-header">
        <h1 style="font-size: 36px;">{L['app_title']}</h1>
        <p style="font-size: 16px;">{L['app_subtitle']}</p>
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
# 📊 لوحة التحكم الرئيسية
# ======================================================================

def dashboard():
    lang = st.session_state.lang
    L = LANGUAGES[lang]
    
    with st.sidebar:
        selected_lang = st.selectbox("🌐 Language", list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index(lang))
        if selected_lang != lang:
            st.session_state.lang = selected_lang
            st.rerun()
        
        st.markdown("---")
        
        role_name = L['doctor'] if st.session_state.role == "doctor" else L['nurse'] if st.session_state.role == "nurse" else L['admin']
        st.markdown(f"### 👤 {st.session_state.user['name']}")
        st.markdown(f"📋 {role_name}")
        st.markdown(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
        st.markdown("---")
        
        if st.session_state.patients:
            patient_names = [p["name"] + " (" + p.get('bed_number', '') + ")" for p in st.session_state.patients]
            selected = st.selectbox(L['select_patient'], patient_names)
            idx = patient_names.index(selected)
            st.session_state.selected_patient = st.session_state.patients[idx]
        else:
            st.warning("⚠️ " + ("لا يوجد مرضى" if lang == "العربية" else "No patients"))
            st.session_state.selected_patient = None
        
        st.markdown("---")
        
        if GEMINI_AVAILABLE:
            st.success("✅ Gemini AI " + ("متصل" if lang == "العربية" else "Connected"))
        else:
            st.info("🔄 " + ("وضع المحاكاة" if lang == "العربية" else "Simulation Mode"))
        
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
        risk_translation = {
            "حرج": L['critical'],
            "متوسط": L['moderate'],
            "منخفض": L['low']
        }
        
        risk_class = "status-critical" if patient['risk_level'] == "حرج" else "status-moderate" if patient['risk_level'] == "متوسط" else "status-low"
        
        bed_info = patient.get('bed_number', '')
        
        st.markdown(f"""
        <div class="patient-header">
            <h2 style="margin: 0;">🩺 {patient['name']}</h2>
            <p>🧬 {'العمر' if lang == 'العربية' else 'Age'}: {patient['age']} {'سنة' if lang == 'العربية' else 'years'} | {patient['gender']} | {'الوزن' if lang == 'العربية' else 'Weight'}: {patient['weight']} {'كجم' if lang == 'العربية' else 'kg'}</p>
            <p>🛏️ {bed_info if bed_info else 'لا يوجد'}</p>
            <p>📋 {L['diagnosis']}: {patient['diagnosis']}</p>
            <span class="status-badge {risk_class}">{risk_translation.get(patient['risk_level'], patient['risk_level'])}</span>
        </div>
        """, unsafe_allow_html=True)
        
        tabs_list = [
            L['vitals'], 
            L['lab'], 
            L['assessment'], 
            L['ai'], 
            L['alerts'],
            L['radiology'],
            L['voice_record'],
            L['medical_orders']
        ]
        
        if st.session_state.role == "admin":
            tabs_list.append(L['admin_panel'])
            tabs_list.append("📋 " + L['daily_report'])
        
        tabs = st.tabs(tabs_list)
        
        # ===== تبويب 1: العلامات الحيوية =====
        with tabs[0]:
            st.subheader(L['vitals'])
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
                st.metric(L['cvp'], f"{vitals['cvp']}")
            with col3:
                st.metric(L['icp'], f"{vitals['icp']}")
        
        # ===== تبويب 2: المختبر =====
        with tabs[1]:
            st.subheader(L['lab'])
            labs = patient['labs']
            
            lab_data = {
                "الفحص" if lang == "العربية" else "Test": ["WBC", "HB", "PLT", "pH", "PaCO2", "PaO2", "HCO3", "Na", "K", "Ca", "Creatinine", "BUN", "ALT", "AST", "Bilirubin", "INR", "Troponin", "Lactate"],
                "النتيجة" if lang == "العربية" else "Result": [labs['wbc'], labs['hb'], labs['plt'], labs['ph'], labs['paco2'], labs['pao2'], labs['hco3'], labs['na'], labs['k'], labs['ca'], labs['creatinine'], labs['bun'], labs['alt'], labs['ast'], labs['bilirubin'], labs['inr'], labs['troponin'], labs['lactate']],
                "الوحدة" if lang == "العربية" else "Unit": ["×10³/µL", "g/dL", "×10³/µL", "", "mmHg", "mmHg", "mEq/L", "mEq/L", "mEq/L", "mEq/L", "mg/dL", "mg/dL", "U/L", "U/L", "mg/dL", "", "ng/mL", "mmol/L"]
            }
            df = pd.DataFrame(lab_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # ===== تبويب 3: التقييم =====
        with tabs[2]:
            st.subheader(L['assessment'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("SOFA Score", patient['sofa_score'])
            with col2:
                st.metric("NEWS2", patient['news2_score'])
            with col3:
                st.metric("GCS", patient['gcs_score'])
                st.metric(L['risk_level'], risk_translation.get(patient['risk_level'], patient['risk_level']))
        
        # ===== تبويب 4: الذكاء الاصطناعي =====
        with tabs[3]:
            st.subheader(L['ai'])
            
            if not has_permission(st.session_state.user, "ai_analysis"):
                st.warning("⚠️ " + ("ليس لديك صلاحية" if lang == "العربية" else "You don't have permission"))
            else:
                if st.button(L['ai_analysis'], use_container_width=True, type="primary"):
                    with st.spinner("🧠 " + ("جاري التحليل..." if lang == "العربية" else "Analyzing...")):
                        result = get_ai_diagnosis(patient, lang)
                        
                        if result["success"]:
                            st.markdown("### 📊 " + ("المؤشرات المحسوبة" if lang == "العربية" else "Calculated Indicators"))
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("BMI", f"{result['bmi']:.1f}")
                            with col2:
                                st.metric("Creatinine Clearance", f"{result['creatinine_clearance']:.1f} mL/min")
                            with col3:
                                st.metric(L['source'], result['source'])
                            
                            st.markdown("### 📋 " + ("التقرير السريري" if lang == "العربية" else "Clinical Report"))
                            st.markdown(result["diagnosis"])
                        else:
                            st.error(f"❌ {result['error']}")
        
        # ===== تبويب 5: التنبيهات =====
        with tabs[4]:
            st.subheader(L['alerts'])
            alerts = check_alerts(patient, lang)
            if alerts:
                for alert in alerts:
                    st.markdown(f"""
                    <div class="alert-critical">
                        <strong>{alert['title']}</strong>
                        <br>{alert['message']}
                        <br><strong style="color: #e74c3c;">🛑 {alert['action']}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">✅ ' + L['no_alerts'] + '</div>', unsafe_allow_html=True)
        
        # ===== تبويب 6: الأشعة =====
        with tabs[5]:
            st.subheader(L['radiology'])
            uploaded_file = st.file_uploader(L['upload_image'] + " (X-Ray, CT, MRI)", type=["jpg", "jpeg", "png", "dcm"])
            if uploaded_file:
                st.image(uploaded_file, caption="صورة الأشعة", use_container_width=True)
                st.success("✅ " + ("تم رفع الصورة بنجاح!" if lang == "العربية" else "Image uploaded!"))
        
        # ===== تبويب 7: التسجيل الصوتي =====
        with tabs[6]:
            st.subheader(L['voice_record'])
            audio_file = st.file_uploader("🎵 " + ("رفع ملف صوتي" if lang == "العربية" else "Upload Audio"), type=["wav", "mp3"])
            if audio_file:
                st.success("✅ " + ("تم رفع الملف الصوتي" if lang == "العربية" else "Audio uploaded"))
                notes = st.text_area("📝 " + ("ملاحظات" if lang == "العربية" else "Notes"))
                if st.button("💾 " + ("حفظ" if lang == "العربية" else "Save")):
                    st.success("✅ " + ("تم حفظ التسجيل الصوتي!" if lang == "العربية" else "Voice recording saved!"))
        
        # ===== تبويب 8: الأوامر الطبية =====
        with tabs[7]:
            st.subheader("📋 " + L['medical_orders'])
            
            is_doctor = st.session_state.role == "doctor"
            is_admin = st.session_state.role == "admin"
            
            # عرض الأوامر الحالية
            if patient['id'] in st.session_state.medical_orders:
                orders = st.session_state.medical_orders[patient['id']]
                st.markdown("### 📋 الأوامر الطبية الحالية")
                
                for i, order in enumerate(orders):
                    status_emoji = "⏳" if order.get('status') == 'pending' else "✅" if order.get('status') == 'received' else "✔️" if order.get('status') == 'executed' else "⏳"
                    st.markdown(f"""
                    <div class="order-box">
                        <strong>{status_emoji} 💊 {order['medication']}</strong>
                        <br>📊 الجرعة: {order['dose']:.1f} {order['unit']}
                        <br>⏰ التوقيت: {order['frequency']}
                        <br>💉 الطريق: {order['route']}
                        <br>📝 ملاحظات: {order.get('notes', 'لا يوجد')}
                        <br>🕐 وصف بواسطة: {order.get('prescribed_by', 'الطبيب')} في {order.get('prescribed_time', '')}
                        <br>📥 استلم بواسطة: {order.get('received_by_nurse', 'لم يستلم بعد')} {order.get('received_time', '')}
                        <br>🔄 نفذ بواسطة: {order.get('executed_by_nurse', 'لم ينفذ بعد')} {order.get('executed_time', '')}
                        <br><span style="color: {'orange' if order.get('status') == 'pending' else 'green' if order.get('status') == 'executed' else 'blue'}">الحالة: {order.get('status', 'معلق')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # إجراءات الممرض (استلام وتنفيذ)
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
                st.info("📝 لا توجد أوامر طبية حالياً لهذا المريض")
            
            # إضافة أمر طبي جديد (للطبيب فقط)
            if is_doctor or is_admin:
                st.markdown("---")
                st.markdown("### ➕ إضافة أمر طبي جديد")
                
                with st.form("new_order_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        medication = st.selectbox("💊 اختيار الدواء", list(MEDICATION_DATABASE.keys()))
                        weight = patient['weight']
                        age = patient['age']
                        creatinine = patient['labs']['creatinine']
                        
                        dose, frequency, warning = calculate_dose(medication, weight, age, creatinine)
                        med_info = MEDICATION_DATABASE[medication]
                        
                        st.info(f"""
                        ⚖️ وزن المريض: {weight} كجم
                        🧬 العمر: {age} سنة
                        🧪 الكرياتينين: {creatinine} mg/dL
                        """)
                        
                        st.markdown(f"""
                        <div style="background: #d5f5e3; padding: 15px; border-radius: 10px; margin: 10px 0;">
                            <strong>💉 الجرعة المحسوبة:</strong> {dose:.1f} mg
                            <br><strong>⏰ التوقيت:</strong> {frequency}
                            <br><strong>{warning}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        custom_dose = st.number_input("✏️ تعديل الجرعة (ملجم)", value=float(dose), step=100.0)
                        custom_frequency = st.text_input("⏰ التوقيت", value=frequency)
                        route = st.selectbox("💉 طريق الإعطاء", ["IV", "IM", "PO", "SC"])
                        notes = st.text_area("📝 ملاحظات إضافية")
                    
                    submitted = st.form_submit_button("💾 حفظ الأمر الطبي", use_container_width=True, type="primary")
                    
                    if submitted:
                        order = {
                            "medication": medication,
                            "dose": custom_dose,
                            "unit": "mg" if medication != "Heparin" else "units",
                            "frequency": custom_frequency,
                            "route": route,
                            "notes": notes,
                            "warning": warning,
                            "prescribed_by": st.session_state.user['name'],
                            "prescribed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "pending",
                            "received_by_nurse": "",
                            "received_time": "",
                            "executed_by_nurse": "",
                            "executed_time": "",
                            "monitoring": med_info.get("monitoring", [])
                        }
                        
                        if patient['id'] not in st.session_state.medical_orders:
                            st.session_state.medical_orders[patient['id']] = []
                        st.session_state.medical_orders[patient['id']].append(order)
                        
                        st.success(f"✅ تم إضافة الأمر الطبي لـ {medication} بنجاح!")
                        st.rerun()
        
        # ===== تبويب 9: لوحة المدير =====
        if st.session_state.role == "admin" and len(tabs) > 8:
            with tabs[8]:
                st.subheader("👑 " + L['admin_panel'])
                
                # سجل الدخول والخروج
                st.markdown("### 📝 " + L['visitor_log'])
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('''
                SELECT username, role, login_time, logout_time, session_duration 
                FROM login_logs 
                ORDER BY id DESC 
                LIMIT 50
                ''')
                logs = cursor.fetchall()
                conn.close()
                
                if logs:
                    log_data = {
                        "المستخدم": [l[0] for l in logs],
                        "الدور": [l[1] for l in logs],
                        "وقت الدخول": [l[2] for l in logs],
                        "وقت الخروج": [l[3] if l[3] else "لا يزال داخل" for l in logs],
                        "المدة": [l[4] if l[4] else "..." for l in logs]
                    }
                    df = pd.DataFrame(log_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("📝 لا توجد سجلات دخول")
                
                # الأوامر الطبية - تقرير مفصل
                st.markdown("---")
                st.markdown("### 📋 تقرير الأوامر الطبية")
                
                all_orders = []
                for pid, orders in st.session_state.medical_orders.items():
                    patient_name = next((p['name'] for p in st.session_state.patients if p['id'] == pid), f"مريض {pid}")
                    for order in orders:
                        all_orders.append({
                            "المريض": patient_name,
                            "الدواء": order['medication'],
                            "الجرعة": f"{order['dose']} {order['unit']}",
                            "التوقيت": order['frequency'],
                            "الطريق": order['route'],
                            "وصف بواسطة": order.get('prescribed_by', ''),
                            "وقت الوصف": order.get('prescribed_time', ''),
                            "استلم بواسطة": order.get('received_by_nurse', 'لم يستلم'),
                            "وقت الاستلام": order.get('received_time', ''),
                            "نفذ بواسطة": order.get('executed_by_nurse', 'لم ينفذ'),
                            "وقت التنفيذ": order.get('executed_time', ''),
                            "الحالة": order.get('status', 'معلق')
                        })
                
                if all_orders:
                    df_orders = pd.DataFrame(all_orders)
                    st.dataframe(df_orders, use_container_width=True, hide_index=True)
                else:
                    st.info("📝 لا توجد أوامر طبية")
        
        # ===== تبويب 10: التقرير اليومي =====
        if st.session_state.role == "admin" and len(tabs) > 9:
            with tabs[9]:
                st.subheader("📋 " + L['daily_report'])
                
                # تقارير الممرض اليومية
                st.markdown("### 🛏️ " + L['bed_report'])
                
                # اختيار السرير
                beds = list(set([p.get('bed_number', f"سرير {p['id']}") for p in st.session_state.patients]))
                selected_bed = st.selectbox("اختر السرير", beds)
                
                # اختيار الوردية
                shift = st.radio("الوردية", [L['morning'], L['evening']], horizontal=True)
                
                # نموذج التقرير اليومي
                with st.form("daily_report_form"):
                    st.markdown(f"### 📋 تقرير {shift} - {selected_bed}")
                    
                    patient_for_bed = next((p for p in st.session_state.patients if p.get('bed_number') == selected_bed), None)
                    if patient_for_bed:
                        st.write(f"**المريض:** {patient_for_bed['name']}")
                        st.write(f"**العمر:** {patient_for_bed['age']} سنة")
                        st.write(f"**التشخيص:** {patient_for_bed['diagnosis']}")
                    else:
                        st.warning("لا يوجد مريض في هذا السرير")
                    
                    st.markdown("---")
                    
                    # ملاحظات الممرض
                    notes = st.text_area("📝 ملاحظات الممرض", placeholder="اكتب ملاحظاتك هنا...")
                    
                    # ملخص العلامات الحيوية
                    st.markdown("### 📊 ملخص العلامات الحيوية")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        bp = st.text_input("ضغط الدم", placeholder="120/80")
                        hr = st.text_input("معدل النبض", placeholder="75")
                    with col2:
                        temp = st.text_input("درجة الحرارة", placeholder="37.0")
                        spo2 = st.text_input("SpO2", placeholder="98")
                    with col3:
                        rr = st.text_input("معدل التنفس", placeholder="16")
                        gcs = st.text_input("GCS", placeholder="15")
                    
                    submitted = st.form_submit_button("💾 حفظ التقرير", use_container_width=True)
                    
                    if submitted:
                        report = {
                            "bed": selected_bed,
                            "patient": patient_for_bed['name'] if patient_for_bed else "لا يوجد",
                            "shift": shift,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "time": datetime.now().strftime("%H:%M"),
                            "nurse": st.session_state.user['name'],
                            "notes": notes,
                            "vitals": {
                                "bp": bp,
                                "hr": hr,
                                "temp": temp,
                                "spo2": spo2,
                                "rr": rr,
                                "gcs": gcs
                            }
                        }
                        st.session_state.daily_reports.append(report)
                        st.success("✅ تم حفظ التقرير اليومي بنجاح!")
                        st.rerun()
                
                # عرض التقارير السابقة
                if st.session_state.daily_reports:
                    st.markdown("---")
                    st.markdown("### 📋 التقارير السابقة")
                    df_reports = pd.DataFrame(st.session_state.daily_reports)
                    st.dataframe(df_reports, use_container_width=True, hide_index=True)

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