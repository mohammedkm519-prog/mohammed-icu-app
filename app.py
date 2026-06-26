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
import re
from datetime import datetime, timedelta

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
        "upload_lab": "📸 رفع التحاليل",
        "assessment": "🧠 التقييم السريري",
        "ai": "🤖 الذكاء الاصطناعي",
        "alerts": "🔔 التنبيهات",
        "radiology": "🩻 الأشعة",
        "add_patient": "➕ إضافة مريض",
        "voice": "🎤 تسجيل صوتي",
        "orders": "📋 الأوامر الطبية",
        "blood_pressure": "🩸 ضغط الدم",
        "heart_rate": "💓 النبض",
        "temperature": "🌡️ الحرارة",
        "spo2": "💨 SpO2",
        "respiratory": "🫁 التنفس",
        "cvp": "📊 CVP",
        "icp": "🧠 ICP",
        "diagnosis": "📋 التشخيص",
        "risk_level": "مستوى الخطورة",
        "critical": "حرج",
        "moderate": "متوسط",
        "low": "منخفض",
        "no_alerts": "✅ لا يوجد تنبيهات",
        "ai_analysis": "🧠 تشغيل التحليل الذكي",
        "source": "📡 المصدر",
        "morning": "☀️ صباحاً",
        "evening": "🌙 مساءً",
        "full_name": "👤 الاسم الكامل",
        "age": "🧬 العمر",
        "gender": "⚤ الجنس",
        "weight": "⚖️ الوزن (كجم)",
        "height": "📏 الطول (سم)",
        "chronic_diseases": "💊 الأمراض المزمنة",
        "allergies": "⚠️ الحساسية",
        "current_medications": "💊 الأدوية الحالية",
        "bed_number": "🛏️ رقم السرير",
        "save": "💾 حفظ",
        "cancel": "❌ إلغاء",
        "extract_data": "📊 استخراج البيانات",
        "apply_data": "✅ تطبيق البيانات"
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
        "upload_lab": "📸 Upload Lab Results",
        "assessment": "🧠 Clinical Assessment",
        "ai": "🤖 AI Analysis",
        "alerts": "🔔 Alerts",
        "radiology": "🩻 Radiology",
        "add_patient": "➕ Add Patient",
        "voice": "🎤 Voice Record",
        "orders": "📋 Medical Orders",
        "blood_pressure": "🩸 Blood Pressure",
        "heart_rate": "💓 Heart Rate",
        "temperature": "🌡️ Temperature",
        "spo2": "💨 SpO2",
        "respiratory": "🫁 Respiratory Rate",
        "cvp": "📊 CVP",
        "icp": "🧠 ICP",
        "diagnosis": "📋 Diagnosis",
        "risk_level": "Risk Level",
        "critical": "Critical",
        "moderate": "Moderate",
        "low": "Low",
        "no_alerts": "✅ No alerts",
        "ai_analysis": "🧠 Run AI Analysis",
        "source": "📡 Source",
        "morning": "☀️ Morning",
        "evening": "🌙 Evening",
        "full_name": "👤 Full Name",
        "age": "🧬 Age",
        "gender": "⚤ Gender",
        "weight": "⚖️ Weight (kg)",
        "height": "📏 Height (cm)",
        "chronic_diseases": "💊 Chronic Diseases",
        "allergies": "⚠️ Allergies",
        "current_medications": "💊 Current Medications",
        "bed_number": "🛏️ Bed Number",
        "save": "💾 Save",
        "cancel": "❌ Cancel",
        "extract_data": "📊 Extract Data",
        "apply_data": "✅ Apply Data"
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
        "upload_lab": "📸 Laboratuvar Yükle",
        "assessment": "🧠 Klinik Değerlendirme",
        "ai": "🤖 Yapay Zeka",
        "alerts": "🔔 Uyarılar",
        "radiology": "🩻 Radyoloji",
        "add_patient": "➕ Hasta Ekle",
        "voice": "🎤 Ses Kaydı",
        "orders": "📋 Tıbbi Emirler",
        "blood_pressure": "🩸 Kan Basıncı",
        "heart_rate": "💓 Nabız",
        "temperature": "🌡️ Sıcaklık",
        "spo2": "💨 SpO2",
        "respiratory": "🫁 Solunum",
        "cvp": "📊 CVP",
        "icp": "🧠 ICP",
        "diagnosis": "📋 Teşhis",
        "risk_level": "Risk Seviyesi",
        "critical": "Kritik",
        "moderate": "Orta",
        "low": "Düşük",
        "no_alerts": "✅ Uyarı yok",
        "ai_analysis": "🧠 Yapay Zeka Analizi Çalıştır",
        "source": "📡 Kaynak",
        "morning": "☀️ Sabah",
        "evening": "🌙 Akşam",
        "full_name": "👤 Tam Ad",
        "age": "🧬 Yaş",
        "gender": "⚤ Cinsiyet",
        "weight": "⚖️ Kilo (kg)",
        "height": "📏 Boy (cm)",
        "chronic_diseases": "💊 Kronik Hastalıklar",
        "allergies": "⚠️ Alerjiler",
        "current_medications": "💊 Mevcut İlaçlar",
        "bed_number": "🛏️ Yatak Numarası",
        "save": "💾 Kaydet",
        "cancel": "❌ İptal",
        "extract_data": "📊 Veri Çıkar",
        "apply_data": "✅ Veriyi Uygula"
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
        "upload_lab": "📸 آپلود آزمایشگاه",
        "assessment": "🧠 ارزیابی بالینی",
        "ai": "🤖 هوش مصنوعی",
        "alerts": "🔔 هشدارها",
        "radiology": "🩻 رادیولوژی",
        "add_patient": "➕ افزودن بیمار",
        "voice": "🎤 ضبط صدا",
        "orders": "📋 دستورات پزشکی",
        "blood_pressure": "🩸 فشار خون",
        "heart_rate": "💓 ضربان قلب",
        "temperature": "🌡️ دما",
        "spo2": "💨 SpO2",
        "respiratory": "🫁 تنفس",
        "cvp": "📊 CVP",
        "icp": "🧠 ICP",
        "diagnosis": "📋 تشخیص",
        "risk_level": "سطح خطر",
        "critical": "بحرانی",
        "moderate": "متوسط",
        "low": "کم",
        "no_alerts": "✅ بدون هشدار",
        "ai_analysis": "🧠 اجرای تحلیل هوش مصنوعی",
        "source": "📡 منبع",
        "morning": "☀️ صبح",
        "evening": "🌙 عصر",
        "full_name": "👤 نام کامل",
        "age": "🧬 سن",
        "gender": "⚤ جنسیت",
        "weight": "⚖️ وزن (کیلوگرم)",
        "height": "📏 قد (سانتی‌متر)",
        "chronic_diseases": "💊 بیماری‌های مزمن",
        "allergies": "⚠️ حساسیت‌ها",
        "current_medications": "💊 داروهای فعلی",
        "bed_number": "🛏️ شماره تخت",
        "save": "💾 ذخیره",
        "cancel": "❌ لغو",
        "extract_data": "📊 استخراج داده",
        "apply_data": "✅ اعمال داده"
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
    print("✅ Gemini API متاحة")
except:
    GEMINI_AVAILABLE = False
    print("⚠️ Gemini غير متاحة")

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
    "Dobutamine": {"standard_dose": 5, "max_dose": 40, "frequency": "مستمر", "route": "IV", "renal_adjust": False, "monitoring": ["ضغط الدم", "النبض"]},
    "Furosemide": {"standard_dose": 20, "max_dose": 400, "frequency": "كل 12 ساعات", "route": "IV/PO", "renal_adjust": True, "monitoring": ["ضغط الدم", "البوتاسيوم"]},
    "Heparin": {"standard_dose": 18, "max_dose": 100, "frequency": "مستمر", "route": "IV", "renal_adjust": False, "monitoring": ["aPTT"]},
    "Insulin": {"standard_dose": 0.1, "max_dose": 10, "frequency": "مستمر", "route": "IV", "renal_adjust": False, "monitoring": ["سكر الدم", "البوتاسيوم"]},
    "Midazolam": {"standard_dose": 0.05, "max_dose": 10, "frequency": "كل 4 ساعات", "route": "IV", "renal_adjust": True, "monitoring": ["ضغط الدم", "التنفس"]}
}

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

def calculate_caloric_needs(weight, age, gender, height, stress_factor=1.2):
    if gender in ["ذكر", "Male"]:
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr * stress_factor

def calculate_fluid_needs(weight, stress_factor=1.5):
    return weight * 30 * stress_factor

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

# ======================================================================
# 📸 تحليل الصور باستخدام Gemini مباشرة
# ======================================================================

def encode_image(image_file):
    """تحويل الصورة إلى Base64"""
    return base64.b64encode(image_file.read()).decode('utf-8')

def extract_numbers_from_text(text):
    """استخراج الأرقام من النص باستخدام تعابير نمطية"""
    numbers = {}
    
    lab_keys = {
        'wbc': ['wbc', 'white cell count', 'white blood cell', 'خلايا الدم البيضاء', 'كريات الدم البيضاء', 'white cell'],
        'hb': ['hb', 'hemoglobin', 'haemoglobin', 'الهيموغلوبين', 'الهيموجلوبين'],
        'plt': ['plt', 'platelet', 'platelets count', 'الصفائح', 'الصفائح الدموية'],
        'ph': ['ph', 'الرقم الهيدروجيني'],
        'paco2': ['paco2', 'pa co2', 'ضغط ثاني أكسيد الكربون'],
        'pao2': ['pao2', 'pa o2', 'ضغط الأكسجين'],
        'hco3': ['hco3', 'bicarbonate', 'بيكربونات'],
        'na': ['na', 'sodium', 'صوديوم'],
        'k': ['k', 'potassium', 'بوتاسيوم'],
        'ca': ['ca', 'calcium', 'كالسيوم'],
        'creatinine': ['creatinine', 'كرياتينين'],
        'bun': ['bun', 'urea', 'يوريا'],
        'alt': ['alt', 'sgpt', 'الترانساميناز'],
        'ast': ['ast', 'sgot', 'الترانساميناز'],
        'bilirubin': ['bilirubin', 'بيليروبين'],
        'inr': ['inr', 'نسبة التطبيع الدولي'],
        'troponin': ['troponin', 'تروبونين'],
        'lactate': ['lactate', 'lactic acid', 'لاكتات', 'حمض اللبنيك']
    }
    
    for key, search_terms in lab_keys.items():
        for term in search_terms:
            patterns = [
                rf'{term}[\s:]*([\d.]+)',
                rf'([\d.]+)\s*{term}',
                rf'{term}.*?([\d.]+)',
                rf'([\d.]+).*?{term}'
            ]
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    try:
                        numbers[key] = float(matches[0])
                        break
                    except:
                        pass
            if key in numbers:
                break
    
    return numbers

def analyze_lab_image_with_gemini(image_file):
    """تحليل صورة التحاليل باستخدام Gemini مباشرة"""
    
    if not GEMINI_AVAILABLE:
        return {
            "success": False,
            "error": "Gemini API غير متاحة. يرجى التحقق من الاتصال.",
            "data": {}
        }
    
    try:
        # حفظ الصورة كـ base64
        image_data = encode_image(image_file)
        
        # إعادة تعيين مؤشر الملف
        image_file.seek(0)
        
        prompt = """
        أنت نظام ذكاء اصطناعي متخصص في قراءة نتائج المختبرات الطبية بدقة عالية.
        
        هذه صورة لورقة تحاليل طبية. استخرج جميع الأرقام والنتائج الموجودة في الصورة بدقة متناهية.
        
        ركز على استخراج هذه القيم تحديداً:
        - WBC (خلايا الدم البيضاء) - ابحث عن "White cell count" أو "WBC"
        - HB (الهيموغلوبين) - ابحث عن "Haemoglobin" أو "HB"  
        - PLT (الصفائح الدموية) - ابحث عن "Platelets" أو "PLT"
        - pH - ابحث عن "pH"
        - PaCO2 - ابحث عن "PaCO2" أو "Pa CO2"
        - PaO2 - ابحث عن "PaO2" أو "Pa O2"
        - HCO3 - ابحث عن "HCO3" أو "Bicarbonate"
        - Na (الصوديوم) - ابحث عن "Na" أو "Sodium"
        - K (البوتاسيوم) - ابحث عن "K" أو "Potassium"
        - Ca (الكالسيوم) - ابحث عن "Ca" أو "Calcium"
        - Creatinine (الكرياتينين) - ابحث عن "Creatinine"
        - BUN - ابحث عن "BUN" أو "Urea"
        - ALT - ابحث عن "ALT" أو "SGPT"
        - AST - ابحث عن "AST" أو "SGOT"
        - Bilirubin (البيليروبين) - ابحث عن "Bilirubin"
        - INR - ابحث عن "INR"
        - Troponin - ابحث عن "Troponin"
        - Lactate (اللاكتات) - ابحث عن "Lactate" أو "Lactic acid"
        
        قم بإرجاع النتائج في شكل JSON فقط، بدون أي نص إضافي.
        
        مثال:
        {
            "wbc": 12.5,
            "hb": 13.5,
            "plt": 250,
            "ph": 7.4,
            "paco2": 38,
            "pao2": 85,
            "hco3": 24,
            "na": 140,
            "k": 4.2,
            "ca": 9.0,
            "creatinine": 0.8,
            "bun": 15,
            "alt": 30,
            "ast": 28,
            "bilirubin": 0.6,
            "inr": 1.0,
            "troponin": 0.01,
            "lactate": 1.2
        }
        
        إذا لم تجد قيمة معينة، اتركها فارغة أو لا تضعها في JSON.
        تأكد من دقة الأرقام المستخرجة.
        """
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])
        text = response.text
        
        # محاولة استخراج JSON من الرد
        json_match = re.search(r'\{[^{}]*\}', text)
        if json_match:
            try:
                data = json.loads(json_match.group())
                if data and len(data) > 0:
                    return {
                        "success": True,
                        "data": data,
                        "source": "Gemini AI",
                        "raw_text": text
                    }
            except:
                pass
        
        # محاولة استخراج الأرقام من النص
        data = extract_numbers_from_text(text)
        if data:
            return {
                "success": True,
                "data": data,
                "source": "Gemini AI (استخراج من النص)",
                "raw_text": text
            }
        
        return {
            "success": False,
            "error": "لم يتم العثور على بيانات في الصورة. تأكد من وضوح الصورة.",
            "data": {}
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"خطأ في Gemini: {str(e)}",
            "data": {}
        }

def analyze_radiology_image(image_file):
    """تحليل صورة الأشعة باستخدام Gemini"""
    
    if not GEMINI_AVAILABLE:
        return {
            "success": False,
            "error": "Gemini API غير متاحة"
        }
    
    try:
        image_data = encode_image(image_file)
        image_file.seek(0)
        
        prompt = """
        أنت طبيب أشعة خبير ومتخصص في قراءة الصور الطبية.
        
        قم بتحليل هذه الصورة الطبية (X-Ray، CT، أو MRI) وقدم تقريراً مفصلاً.
        
        قدم تقريراً يشمل:
        1. وصف الصورة
        2. المناطق الطبيعية
        3. مناطق الشذوذ (إن وجدت)
        4. التشخيص المحتمل
        5. مستوى الخطورة
        6. التوصيات
        """
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])
        
        return {
            "success": True,
            "analysis": response.text,
            "source": "Gemini AI"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ======================================================================
# 🤖 الذكاء الاصطناعي للتشخيص
# ======================================================================

def generate_advanced_diagnosis(patient):
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
    creatinine_clearance = calculate_creatinine_clearance(patient['age'], patient['weight'], creatinine, patient['gender'])
    caloric_needs = calculate_caloric_needs(patient['weight'], patient['age'], patient['gender'], patient['height'])
    fluid_needs = calculate_fluid_needs(patient['weight'])
    
    report = f"""
### التقرير السريري المتقدم

---

#### معلومات المريض
- الاسم: {patient['name']}
- العمر: {patient['age']} سنة
- الجنس: {patient['gender']}
- الوزن: {patient['weight']} كجم
- الطول: {patient['height']} سم
- BMI: {bmi:.1f}

---

#### تحليل العلامات الحيوية
- ضغط الدم: {bp}/{patient['vitals']['diastolic_bp']} mmHg
- معدل النبض: {hr} نبضة/دقيقة
- درجة الحرارة: {temp}°C
- SpO2: {spo2}%
- معدل التنفس: {rr} نفس/دقيقة

---

#### تحليل المختبر
- WBC: {wbc}
- Lactate: {lactate}
- Creatinine: {creatinine}
- Potassium: {potassium}
- pH: {ph}
- PaO2: {pao2}

---

#### التشخيص التفريقي
"""
    diagnoses = []
    if lactate > 4 and bp < 90:
        diagnoses.append(("Sepsis مع Septic Shock", 92, ["Lactate > 4", "ضغط منخفض"]))
    elif lactate > 4:
        diagnoses.append(("Sepsis", 78, ["Lactate > 4"]))
    elif creatinine > 2:
        diagnoses.append(("AKI", 75, ["Creatinine > 2"]))
    if not diagnoses:
        diagnoses.append(("حالة مستقرة", 60, ["جميع المؤشرات طبيعية"]))
    
    for diag, conf, evidence in diagnoses:
        report += f"- {diag} (نسبة الثقة: {conf}%) - الأدلة: {', '.join(evidence)}\n"
    
    report += f"""
---
#### خطة العلاج
1. السوائل الوريدية: {patient['weight'] * 30:.0f}ml
2. المضادات الحيوية: حسب الحساسية
3. مراقبة العلامات الحيوية كل ساعة
4. إعادة الفحوصات المخبرية خلال 4-6 ساعات
"""
    return report

def get_ai_diagnosis(patient):
    if GEMINI_AVAILABLE:
        try:
            context = f"""
            Patient: {patient['name']}, Age: {patient['age']}, Gender: {patient['gender']}
            Weight: {patient['weight']}kg, Height: {patient['height']}cm
            BP: {patient['vitals']['systolic_bp']}/{patient['vitals']['diastolic_bp']} mmHg
            HR: {patient['vitals']['heart_rate']} bpm
            Temp: {patient['vitals']['temperature']}°C
            SpO2: {patient['vitals']['spo2']}%
            RR: {patient['vitals']['respiratory_rate']}
            
            Labs:
            WBC: {patient['labs']['wbc']}
            HB: {patient['labs']['hb']}
            PLT: {patient['labs']['plt']}
            pH: {patient['labs']['ph']}
            PaCO2: {patient['labs']['paco2']}
            PaO2: {patient['labs']['pao2']}
            HCO3: {patient['labs']['hco3']}
            Na: {patient['labs']['na']}
            K: {patient['labs']['k']}
            Ca: {patient['labs']['ca']}
            Creatinine: {patient['labs']['creatinine']}
            BUN: {patient['labs']['bun']}
            ALT: {patient['labs']['alt']}
            AST: {patient['labs']['ast']}
            Bilirubin: {patient['labs']['bilirubin']}
            INR: {patient['labs']['inr']}
            Troponin: {patient['labs']['troponin']}
            Lactate: {patient['labs']['lactate']}
            
            Chronic Diseases: {', '.join(patient['chronic_diseases'])}
            Allergies: {', '.join(patient['allergies'])}
            Current Medications: {', '.join(patient['current_medications'])}
            
            SOFA: {patient['sofa_score']}
            NEWS2: {patient['news2_score']}
            GCS: {patient['gcs_score']}
            
            Provide a comprehensive diagnosis and treatment plan in Arabic.
            Include: primary diagnosis, differential diagnoses, treatment plan, and monitoring recommendations.
            """
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(context)
            return {"success": True, "diagnosis": response.text, "source": "Gemini AI"}
        except:
            pass
    
    return {"success": True, "diagnosis": generate_advanced_diagnosis(patient), "source": "AI Simulator"}

# ======================================================================
# 🔔 التنبيهات
# ======================================================================

def check_alerts(patient):
    alerts = []
    if patient['vitals']['systolic_bp'] < 90:
        alerts.append({"type": "critical", "title": "انخفاض الضغط", "message": f"الضغط: {patient['vitals']['systolic_bp']} mmHg", "action": "ابدأ بالسوائل الوريدية"})
    if patient['vitals']['spo2'] < 90:
        alerts.append({"type": "critical", "title": "نقص أكسجة", "message": f"SpO2: {patient['vitals']['spo2']}%", "action": "أعطِ أكسجين"})
    if patient['labs']['lactate'] > 4:
        alerts.append({"type": "critical", "title": "ارتفاع اللاكتات", "message": f"Lactate: {patient['labs']['lactate']} mmol/L", "action": "أعد تقييم الإنتان"})
    if patient['labs']['k'] > 5.5:
        alerts.append({"type": "critical", "title": "ارتفاع البوتاسيوم", "message": f"K: {patient['labs']['k']} mEq/L", "action": "أعطِ كالسيوم جلوكونات"})
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

if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = {}

if 'extracted_lab_data' not in st.session_state:
    st.session_state.extracted_lab_data = {}

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
# 📊 لوحة التحكم الرئيسية
# ======================================================================

def dashboard():
    lang = st.session_state.lang
    L = LANGUAGES[lang]
    
    with st.sidebar:
        selected_lang = st.selectbox("🌐", list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index(lang))
        if selected_lang != lang:
            st.session_state.lang = selected_lang
            st.rerun()
        
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
        st.metric(L['critical'], critical)
        st.metric(L['moderate'], moderate)
        st.metric(L['low'], low)
        
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
            <p>{L['age']}: {patient['age']} سنة | {patient['gender']} | {L['weight']}: {patient['weight']} كجم</p>
            <p>{L['bed_number']}: {patient.get('bed_number', 'لا يوجد')}</p>
            <p>{L['diagnosis']}: {patient['diagnosis']}</p>
            <span style="display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 14px; background: {'#e74c3c' if patient['risk_level'] == 'حرج' else '#f1c40f' if patient['risk_level'] == 'متوسط' else '#2ecc71'}; color: {'white' if patient['risk_level'] == 'حرج' else 'black' if patient['risk_level'] == 'متوسط' else 'white'};">{patient['risk_level']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        tabs = st.tabs([
            L['vitals'],
            L['lab'],
            L['upload_lab'],
            L['assessment'],
            L['ai'],
            L['alerts'],
            L['radiology'],
            L['add_patient'],
            L['voice'],
            L['orders']
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
                st.metric(L['cvp'], f"{vitals['cvp']}")
            with col3:
                st.metric(L['icp'], f"{vitals['icp']}")
        
        # ===== المختبر =====
        with tabs[1]:
            labs = patient['labs']
            lab_data = {
                "الفحص": ["WBC", "HB", "PLT", "pH", "PaCO2", "PaO2", "HCO3", "Na", "K", "Ca", "Creatinine", "BUN", "ALT", "AST", "Bilirubin", "INR", "Troponin", "Lactate"],
                "النتيجة": [labs['wbc'], labs['hb'], labs['plt'], labs['ph'], labs['paco2'], labs['pao2'], labs['hco3'], labs['na'], labs['k'], labs['ca'], labs['creatinine'], labs['bun'], labs['alt'], labs['ast'], labs['bilirubin'], labs['inr'], labs['troponin'], labs['lactate']],
                "الوحدة": ["×10³/µL", "g/dL", "×10³/µL", "", "mmHg", "mmHg", "mEq/L", "mEq/L", "mEq/L", "mEq/L", "mg/dL", "mg/dL", "U/L", "U/L", "mg/dL", "", "ng/mL", "mmol/L"]
            }
            df = pd.DataFrame(lab_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # ===== رفع التحاليل =====
        with tabs[2]:
            st.subheader(L['upload_lab'])
            st.markdown("قم برفع صورة لورقة التحاليل وسيقوم الذكاء الاصطناعي بقراءة الأرقام تلقائياً")
            
            uploaded_lab = st.file_uploader(
                "رفع صورة التحاليل (CBC, ABG, etc.)",
                type=["jpg", "jpeg", "png"],
                key="lab_upload"
            )
            
            if uploaded_lab:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(uploaded_lab, caption="صورة التحاليل", use_column_width=True)
                
                with col2:
                    st.info("🤖 سيتم استخدام Gemini AI لقراءة الصورة")
                    
                    if st.button(L['extract_data'], use_container_width=True, type="primary"):
                        with st.spinner("جاري تحليل الصورة واستخراج البيانات..."):
                            result = analyze_lab_image_with_gemini(uploaded_lab)
                            
                            if result["success"]:
                                st.success(f"✅ تم استخراج البيانات بنجاح! (المصدر: {result.get('source', 'غير معروف')})")
                                st.session_state.extracted_lab_data = result["data"]
                                
                                if result["data"]:
                                    lab_data_display = []
                                    for key, value in result["data"].items():
                                        lab_data_display.append({
                                            "الفحص": key.upper(),
                                            "القيمة": value
                                        })
                                    df = pd.DataFrame(lab_data_display)
                                    st.dataframe(df, use_container_width=True, hide_index=True)
                                    
                                    if st.button(L['apply_data'], use_container_width=True):
                                        for key, value in result["data"].items():
                                            if key in patient['labs']:
                                                try:
                                                    patient['labs'][key] = float(value)
                                                except:
                                                    patient['labs'][key] = value
                                        st.success("✅ تم تحديث تحاليل المريض بنجاح!")
                                        st.rerun()
                                else:
                                    st.warning("⚠️ لم يتم استخراج بيانات من الصورة.")
                                
                                if result.get("raw_text"):
                                    with st.expander("📄 عرض النص المستخرج"):
                                        st.text(result["raw_text"])
                            else:
                                st.error(f"❌ خطأ في التحليل: {result.get('error', 'غير معروف')}")
                                st.info("💡 يمكنك إدخال البيانات يدوياً في تبويب المختبر")
                
                if st.button(L['save'], use_container_width=True):
                    if patient['id'] not in st.session_state.uploaded_images:
                        st.session_state.uploaded_images[patient['id']] = []
                    image_data = base64.b64encode(uploaded_lab.read()).decode('utf-8')
                    st.session_state.uploaded_images[patient['id']].append({
                        "type": "lab",
                        "data": image_data,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.success("✅ تم حفظ الصورة بنجاح!")
        
        # ===== التقييم السريري =====
        with tabs[3]:
            st.subheader(L['assessment'])
            
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
            
            if patient['sofa_score'] >= 4:
                st.error(f"🚨 SOFA Score = {patient['sofa_score']} - خلل عضوي حاد")
            if patient['news2_score'] >= 7:
                st.error(f"🚨 NEWS2 = {patient['news2_score']} - حالة حرجة")
        
        # ===== الذكاء الاصطناعي =====
        with tabs[4]:
            st.subheader(L['ai'])
            
            if not has_permission(st.session_state.user, "ai_analysis"):
                st.warning("⚠️ " + ("ليس لديك صلاحية" if lang == "العربية" else "No permission"))
            else:
                st.info("🤖 يستخدم Gemini AI للتشخيص المتقدم")
                
                if st.button(L['ai_analysis'], use_container_width=True, type="primary"):
                    with st.spinner("🧠 " + ("جاري التحليل..." if lang == "العربية" else "Analyzing...")):
                        result = get_ai_diagnosis(patient)
                        if result["success"]:
                            st.markdown("### 📋 " + ("التقرير السريري" if lang == "العربية" else "Clinical Report"))
                            st.markdown(result["diagnosis"])
                            st.info(f"{L['source']}: {result['source']}")
        
        # ===== التنبيهات =====
        with tabs[5]:
            st.subheader(L['alerts'])
            alerts = check_alerts(patient)
            if alerts:
                for alert in alerts:
                    st.warning(f"**{alert['title']}**\n\n{alert['message']}\n\n🛑 {alert['action']}")
            else:
                st.success(L['no_alerts'])
        
        # ===== الأشعة =====
        with tabs[6]:
            st.subheader(L['radiology'])
            uploaded_rad = st.file_uploader("رفع صورة الأشعة", type=["jpg", "jpeg", "png"])
            if uploaded_rad:
                st.image(uploaded_rad, caption="صورة الأشعة", use_column_width=True)
                if st.button("تحليل الأشعة", use_container_width=True):
                    with st.spinner("جاري تحليل الصورة..."):
                        result = analyze_radiology_image(uploaded_rad)
                        if result["success"]:
                            st.markdown("### تقرير الأشعة")
                            st.markdown(result["analysis"])
                            st.info(f"📡 المصدر: {result.get('source', 'غير معروف')}")
                        else:
                            st.error(f"❌ خطأ: {result.get('error', 'غير معروف')}")
        
        # ===== إضافة مريض =====
        with tabs[7]:
            st.subheader(L['add_patient'])
            
            with st.expander("بيانات المريض الجديد", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input(L['full_name'], placeholder="مثال: محمد علي")
                    new_age = st.number_input(L['age'], min_value=1, max_value=120, value=40)
                    new_gender = st.selectbox(L['gender'], ["ذكر", "أنثى"])
                    new_weight = st.number_input(L['weight'], min_value=20, max_value=300, value=70)
                    new_height = st.number_input(L['height'], min_value=100, max_value=250, value=170)
                    new_bed = st.text_input(L['bed_number'], placeholder="مثال: سرير 3")
                
                with col2:
                    new_diagnosis = st.selectbox(L['diagnosis'], DIAGNOSIS_LIST)
                    new_risk = st.selectbox(L['risk_level'], ["منخفض", "متوسط", "مرتفع", "حرج"])
                    new_chronic = st.multiselect(L['chronic_diseases'], CHRONIC_DISEASES_LIST, default=["لا يوجد"])
                    new_allergies = st.multiselect(L['allergies'], ALLERGIES_LIST, default=["لا يوجد"])
                    new_medications = st.multiselect(L['current_medications'], MEDICATIONS_LIST, default=["لا يوجد"])
                
                st.markdown("---")
                st.markdown("#### العلامات الحيوية الأساسية")
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_bp_sys = st.number_input("الضغط الانقباضي", min_value=60, max_value=250, value=120)
                    new_bp_dia = st.number_input("الضغط الانبساطي", min_value=30, max_value=150, value=80)
                with col2:
                    new_hr = st.number_input("معدل النبض", min_value=30, max_value=200, value=75)
                    new_temp = st.number_input("درجة الحرارة", min_value=35.0, max_value=42.0, value=37.0)
                with col3:
                    new_spo2 = st.number_input("SpO2", min_value=70, max_value=100, value=98)
                    new_rr = st.number_input("معدل التنفس", min_value=8, max_value=40, value=16)
                
                if st.button(L['add_patient'], use_container_width=True, type="primary"):
                    if new_name:
                        new_patient = {
                            "id": len(st.session_state.patients) + 1,
                            "name": new_name,
                            "age": new_age,
                            "gender": new_gender,
                            "weight": new_weight,
                            "height": new_height,
                            "chronic_diseases": new_chronic if new_chronic else ["لا يوجد"],
                            "allergies": new_allergies if new_allergies else ["لا يوجد"],
                            "surgeries": ["لا يوجد"],
                            "current_medications": new_medications if new_medications else ["لا يوجد"],
                            "diagnosis": new_diagnosis,
                            "status": new_risk,
                            "bed_number": new_bed if new_bed else "لا يوجد",
                            "vitals": {
                                "systolic_bp": new_bp_sys,
                                "diastolic_bp": new_bp_dia,
                                "heart_rate": new_hr,
                                "temperature": new_temp,
                                "respiratory_rate": new_rr,
                                "spo2": new_spo2,
                                "cvp": 6,
                                "icp": 10,
                                "ecg": "طبيعي"
                            },
                            "labs": {
                                "wbc": 7.0,
                                "hb": 13.5,
                                "plt": 250,
                                "ph": 7.40,
                                "paco2": 38,
                                "pao2": 85,
                                "hco3": 24,
                                "na": 140,
                                "k": 4.2,
                                "ca": 9.0,
                                "creatinine": 0.8,
                                "bun": 15,
                                "alt": 30,
                                "ast": 28,
                                "bilirubin": 0.6,
                                "pt": 12.0,
                                "inr": 1.0,
                                "troponin": 0.01,
                                "lactate": 1.2
                            },
                            "sofa_score": 0,
                            "news2_score": 1,
                            "gcs_score": 15,
                            "risk_level": new_risk
                        }
                        st.session_state.patients.append(new_patient)
                        st.success(f"✅ تم إضافة المريض {new_name} بنجاح!")
                        st.rerun()
                    else:
                        st.warning("⚠️ الرجاء إدخال الاسم")
        
        # ===== تسجيل صوتي =====
        with tabs[8]:
            st.subheader(L['voice'])
            audio = st.file_uploader("رفع ملف صوتي", type=["wav", "mp3"])
            if audio:
                st.success("✅ تم رفع الملف الصوتي")
                notes = st.text_area("📝 ملاحظات إضافية")
                if st.button(L['save']):
                    st.success("✅ تم حفظ التسجيل الصوتي")
        
        # ===== الأوامر الطبية =====
        with tabs[9]:
            st.subheader(L['orders'])
            
            is_doctor = st.session_state.role == "doctor"
            is_admin = st.session_state.role == "admin"
            
            if patient['id'] in st.session_state.medical_orders:
                orders = st.session_state.medical_orders[patient['id']]
                for i, order in enumerate(orders):
                    status = order.get('status', 'معلق')
                    status_color = "orange" if status == 'pending' else "blue" if status == 'received' else "green"
                    st.markdown(f"""
                    <div style="background: #eaf2f8; padding: 15px; border-radius: 10px; margin: 10px 0; border-right: 4px solid #2e86c1;">
                        <strong>💊 {order['medication']}</strong>
                        <br>الجرعة: {order['dose']:.1f} {order['unit']}
                        <br>التوقيت: {order['frequency']}
                        <br>الطريق: {order['route']}
                        <br>وصف بواسطة: {order.get('prescribed_by', 'الطبيب')} في {order.get('prescribed_time', '')}
                        <br>استلم بواسطة: {order.get('received_by_nurse', 'لم يستلم')}
                        <br>نفذ بواسطة: {order.get('executed_by_nurse', 'لم ينفذ')}
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
                st.info("📝 لا توجد أوامر طبية حالياً")
            
            if is_doctor or is_admin:
                st.markdown("---")
                st.markdown("### ➕ إضافة أمر طبي جديد")
                
                with st.form("new_order"):
                    col1, col2 = st.columns(2)
                    with col1:
                        medication = st.selectbox("💊 اختيار الدواء", list(MEDICATION_DATABASE.keys()))
                        weight = patient['weight']
                        age = patient['age']
                        creatinine = patient['labs']['creatinine']
                        dose, frequency, warning = calculate_dose(medication, weight, age, creatinine)
                        st.info(f"""
                        ⚖️ وزن المريض: {weight} كجم
                        🧬 العمر: {age} سنة
                        🧪 الكرياتينين: {creatinine} mg/dL
                        """)
                        st.markdown(f"""
                        <div style="background: #d5f5e3; padding: 15px; border-radius: 10px;">
                            <strong>💉 الجرعة المحسوبة:</strong> {dose:.1f} mg
                            <br><strong>⏰ التوقيت:</strong> {frequency}
                            <br><strong>{warning}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        custom_dose = st.number_input("✏️ تعديل الجرعة (ملجم)", value=float(dose), step=100.0)
                        route = st.selectbox("💉 طريق الإعطاء", ["IV", "IM", "PO", "SC"])
                        notes = st.text_area("📝 ملاحظات إضافية")
                    
                    if st.form_submit_button("💾 حفظ الأمر الطبي", use_container_width=True, type="primary"):
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
                        st.success(f"✅ تم إضافة الأمر الطبي لـ {medication} بنجاح!")
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