# ======================================================================
# 🏥 MOHAMMED ICU - نظام العناية المركزة الذكي المتكامل
# ======================================================================
# يدعم 4 لغات: العربية 🇸🇦 | English 🇬🇧 | Türkçe 🇹🇷 | فارسی 🇮🇷
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
        "blood_pressure": "🩸 ضغط الدم",
        "heart_rate": "💓 النبض",
        "temperature": "🌡️ الحرارة",
        "spo2": "💨 SpO2",
        "respiratory": "🫁 التنفس",
        "cvp": "📊 CVP",
        "icp": "🧠 ICP",
        "diagnosis": "📋 التشخيص",
        "treatment": "💊 خطة العلاج",
        "risk_level": "مستوى الخطورة",
        "critical": "حرج",
        "moderate": "متوسط",
        "low": "منخفض",
        "no_alerts": "✅ لا يوجد تنبيهات",
        "ai_analysis": "🧠 تشغيل التحليل الذكي",
        "source": "📡 المصدر",
        "welcome_doctor": "👨‍⚕️ مرحباً دكتور!",
        "welcome_nurse": "👩‍⚕️ مرحباً ممرض!"
    },
    "English": {
        "app_title": "🏥 Mohammed ICU",
        "app_subtitle": "Advanced AI-Powered Intensive Care Unit",
        "choose_role": "Choose your role to enter the system",
        "doctor": "👨‍⚕️ Doctor",
        "nurse": "👩‍⚕️ Nurse",
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
        "blood_pressure": "🩸 Blood Pressure",
        "heart_rate": "💓 Heart Rate",
        "temperature": "🌡️ Temperature",
        "spo2": "💨 SpO2",
        "respiratory": "🫁 Respiratory Rate",
        "cvp": "📊 CVP",
        "icp": "🧠 ICP",
        "diagnosis": "📋 Diagnosis",
        "treatment": "💊 Treatment Plan",
        "risk_level": "Risk Level",
        "critical": "Critical",
        "moderate": "Moderate",
        "low": "Low",
        "no_alerts": "✅ No alerts",
        "ai_analysis": "🧠 Run AI Analysis",
        "source": "📡 Source",
        "welcome_doctor": "👨‍⚕️ Welcome Doctor!",
        "welcome_nurse": "👩‍⚕️ Welcome Nurse!"
    },
    "Türkçe": {
        "app_title": "🏥 Muhammed ICU",
        "app_subtitle": "Gelişmiş Yapay Zeka Destekli Yoğun Bakım Ünitesi",
        "choose_role": "Sisteme girmek için rolünüzü seçin",
        "doctor": "👨‍⚕️ Doktor",
        "nurse": "👩‍⚕️ Hemşire",
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
        "blood_pressure": "🩸 Kan Basıncı",
        "heart_rate": "💓 Nabız",
        "temperature": "🌡️ Sıcaklık",
        "spo2": "💨 SpO2",
        "respiratory": "🫁 Solunum",
        "cvp": "📊 CVP",
        "icp": "🧠 ICP",
        "diagnosis": "📋 Teşhis",
        "treatment": "💊 Tedavi Planı",
        "risk_level": "Risk Seviyesi",
        "critical": "Kritik",
        "moderate": "Orta",
        "low": "Düşük",
        "no_alerts": "✅ Uyarı yok",
        "ai_analysis": "🧠 Yapay Zeka Analizi Çalıştır",
        "source": "📡 Kaynak",
        "welcome_doctor": "👨‍⚕️ Hoş Geldiniz Doktor!",
        "welcome_nurse": "👩‍⚕️ Hoş Geldiniz Hemşire!"
    },
    "فارسی": {
        "app_title": "🏥 محمد ICU",
        "app_subtitle": "سیستم پیشرفته مراقبت‌های ویژه مبتنی بر هوش مصنوعی",
        "choose_role": "نقش خود را برای ورود به سیستم انتخاب کنید",
        "doctor": "👨‍⚕️ پزشک",
        "nurse": "👩‍⚕️ پرستار",
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
        "blood_pressure": "🩸 فشار خون",
        "heart_rate": "💓 ضربان قلب",
        "temperature": "🌡️ دما",
        "spo2": "💨 SpO2",
        "respiratory": "🫁 تنفس",
        "cvp": "📊 CVP",
        "icp": "🧠 ICP",
        "diagnosis": "📋 تشخیص",
        "treatment": "💊 برنامه درمانی",
        "risk_level": "سطح خطر",
        "critical": "بحرانی",
        "moderate": "متوسط",
        "low": "کم",
        "no_alerts": "✅ بدون هشدار",
        "ai_analysis": "🧠 اجرای تحلیل هوش مصنوعی",
        "source": "📡 منبع",
        "welcome_doctor": "👨‍⚕️ خوش آمدید پزشک!",
        "welcome_nurse": "👩‍⚕️ خوش آمدید پرستار!"
    }
}

# ======================================================================
# 🔑 إعدادات Gemini API
# ======================================================================

GEMINI_API_KEY = "AQ.Ab8RN6I9tQyt3v3bUCQO67ozRjCYPNpdi4Ars-B5rFpz_fVaSg"

try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

# ======================================================================
# 👥 المستخدمون
# ======================================================================

AUTHORIZED_USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "name": "المدير",
        "approved": True,
        "permissions": ["all"]
    },
    "dr_ahmed": {
        "password": "doctor123",
        "role": "doctor",
        "name": "د. أحمد",
        "approved": True,
        "permissions": ["view_patients", "ai_analysis", "alerts"]
    },
    "nurse_fatima": {
        "password": "nurse123",
        "role": "nurse",
        "name": "فاطمة",
        "approved": True,
        "permissions": ["view_patients", "add_vitals", "alerts"]
    }
}

# ======================================================================
# 🧮 دوال الحسابات
# ======================================================================

def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m * height_m)

def calculate_ideal_weight(height):
    return 50 + 2.3 * (height - 152.4) / 2.54

def calculate_creatinine_clearance(age, weight, creatinine, gender):
    if gender == "ذكر" or gender == "Male" or gender == "Erkek" or gender == "مرد":
        return ((140 - age) * weight) / (72 * creatinine)
    else:
        return ((140 - age) * weight * 0.85) / (72 * creatinine)

def calculate_oxygenation_index(pao2, fio2=0.21):
    return pao2 / fio2

def calculate_caloric_needs(weight, age, gender, height, stress_factor=1.2):
    is_male = gender in ["ذكر", "Male", "Erkek", "مرد"]
    if is_male:
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr * stress_factor

def calculate_fluid_needs(weight, age, stress_factor=1.5):
    return weight * 30 * stress_factor

# ======================================================================
# 🤖 الذكاء الاصطناعي
# ======================================================================

def generate_simulation_diagnosis(patient, lang):
    """توليد تشخيص محاكي حسب اللغة"""
    
    issues = []
    recommendations = []
    
    # تحليل العلامات الحيوية
    if patient['vitals']['systolic_bp'] < 90:
        issues.append("🔴 " + ("انخفاض حاد في ضغط الدم" if lang == "العربية" else "Severe hypotension" if lang == "English" else "Şiddetli hipotansiyon" if lang == "Türkçe" else "افت فشار خون شدید"))
        recommendations.append("💉 " + ("ابدأ بالسوائل الوريدية فوراً" if lang == "العربية" else "Start IV fluids immediately" if lang == "English" else "Hemen IV sıvı başlat" if lang == "Türkçe" else "شروع فوری مایعات وریدی"))
    
    if patient['vitals']['spo2'] < 90:
        issues.append("🔴 " + ("نقص أكسجة حاد" if lang == "العربية" else "Severe hypoxemia" if lang == "English" else "Şiddetli hipoksemi" if lang == "Türkçe" else "هیپوکسی شدید"))
        recommendations.append("🫁 " + ("أعطِ أكسجين عالي التدفق" if lang == "العربية" else "Administer high-flow oxygen" if lang == "English" else "Yüksek akımlı oksijen ver" if lang == "Türkçe" else "اکسیژن با جریان بالا"))
    
    if patient['labs']['lactate'] > 4:
        issues.append("🔴 " + ("ارتفاع اللاكتات - خطر الإنتان" if lang == "العربية" else "High lactate - Sepsis risk" if lang == "English" else "Yüksek laktat - Sepsis riski" if lang == "Türkçe" else "لاکتات بالا - خطر سپسیس"))
        recommendations.append("🧪 " + ("أعد تقييم الإنتان، أعطِ سوائل وريدية" if lang == "العربية" else "Re-evaluate sepsis, give IV fluids" if lang == "English" else "Sepsi yeniden değerlendir, IV sıvı ver" if lang == "Türkçe" else "سپسیس را دوباره ارزیابی کنید، مایعات وریدی بدهید"))
    
    if patient['labs']['creatinine'] > 2:
        issues.append("🟡 " + ("ارتفاع الكرياتينين - خطر الفشل الكلوي" if lang == "العربية" else "High creatinine - AKI risk" if lang == "English" else "Yüksek kreatinin - AKI riski" if lang == "Türkçe" else "کراتینین بالا - خطر نارسایی کلیه"))
        recommendations.append("💊 " + ("راقب السوائل، تجنب الأدوية السمية للكلية" if lang == "العربية" else "Monitor fluids, avoid nephrotoxic drugs" if lang == "English" else "Sıvıları izle, nefrotoksik ilaçlardan kaçın" if lang == "Türkçe" else "مایعات را کنترل کنید، از داروهای نفروتوکسیک اجتناب کنید"))
    
    if patient['labs']['k'] > 5.5:
        issues.append("🔴 " + ("ارتفاع البوتاسيوم - خطر توقف القلب" if lang == "العربية" else "Hyperkalemia - Cardiac arrest risk" if lang == "English" else "Hiperkalemi - Kardiyak arrest riski" if lang == "Türkçe" else "هیپرکالمی - خطر ایست قلبی"))
        recommendations.append("💉 " + ("أعطِ كالسيوم جلوكونات + إنسولين مع جلوكوز" if lang == "العربية" else "Give Calcium gluconate + Insulin with glucose" if lang == "English" else "Kalsiyum glukonat + Glukoz ile İnsülin ver" if lang == "Türkçe" else "کلسیم گلوکونات + انسولین با گلوکز بدهید"))
    
    # تشخيص رئيسي
    if patient['labs']['lactate'] > 4 and patient['vitals']['systolic_bp'] < 90:
        main_diagnosis = "🩺 **" + ("Sepsis مع Septic Shock" if lang == "العربية" else "Sepsis with Septic Shock" if lang == "English" else "Septik Şok ile Sepsis" if lang == "Türkçe" else "سپسیس با شوک سپتیک") + "** (85%)"
    elif patient['labs']['creatinine'] > 2:
        main_diagnosis = "🩺 **" + ("فشل كلوي حاد" if lang == "العربية" else "Acute Kidney Injury" if lang == "English" else "Akut Böbrek Hasarı" if lang == "Türkçe" else "آسیب حاد کلیه") + "** (75%)"
    else:
        main_diagnosis = "🩺 **" + ("حالة مستقرة - يحتاج إلى مراقبة" if lang == "العربية" else "Stable - Requires monitoring" if lang == "English" else "Stabil - İzlem gerektirir" if lang == "Türkçe" else "پایدار - نیاز به نظارت دارد") + "**"
        recommendations.append("📊 " + ("استمرار المراقبة وتقييم الحالة" if lang == "العربية" else "Continue monitoring and assessment" if lang == "English" else "İzleme ve değerlendirmeye devam et" if lang == "Türkçe" else "نظارت و ارزیابی را ادامه دهید"))
    
    # بناء التقرير
    report = f"""
### 📋 {"التقرير السريري" if lang == "العربية" else "Clinical Report" if lang == "English" else "Klinik Rapor" if lang == "Türkçe" else "گزارش بالینی"}

---

#### 🎯 {"التشخيص الرئيسي" if lang == "العربية" else "Primary Diagnosis" if lang == "English" else "Birincil Tanı" if lang == "Türkçe" else "تشخیص اولیه"}
{main_diagnosis}

---

#### ⚠️ {"المشاكل المكتشفة" if lang == "العربية" else "Detected Issues" if lang == "English" else "Tespit Edilen Sorunlar" if lang == "Türkçe" else "مشکلات شناسایی شده"}
"""
    for issue in issues:
        report += f"- {issue}\n"
    
    if not issues:
        report += "- ✅ " + ("لا توجد مشاكل حرجة" if lang == "العربية" else "No critical issues" if lang == "English" else "Kritik sorun yok" if lang == "Türkçe" else "هیچ مشکل بحرانی وجود ندارد") + "\n"
    
    report += f"""

#### 📊 {"المؤشرات المحسوبة" if lang == "العربية" else "Calculated Indicators" if lang == "English" else "Hesaplanan Göstergeler" if lang == "Türkçe" else "شاخص‌های محاسبه شده"}
- **BMI:** {calculate_bmi(patient['weight'], patient['height']):.1f}
- **{"الوزن المثالي" if lang == "العربية" else "Ideal Weight" if lang == "English" else "İdeal Kilo" if lang == "Türkçe" else "وزن ایده آل"}:** {calculate_ideal_weight(patient['height']):.1f} {"كجم" if lang == "العربية" else "kg"}
- **{"تصفية الكرياتينين" if lang == "العربية" else "Creatinine Clearance" if lang == "English" else "Kreatinin Klerensi" if lang == "Türkçe" else "کلیرانس کراتینین"}:** {calculate_creatinine_clearance(patient['age'], patient['weight'], patient['labs']['creatinine'], patient['gender']):.1f} mL/min
- **{"السعرات" if lang == "العربية" else "Calories" if lang == "English" else "Kalori" if lang == "Türkçe" else "کالری"}:** {calculate_caloric_needs(patient['weight'], patient['age'], patient['gender'], patient['height']):.0f} {"سعرة/يوم" if lang == "العربية" else "kcal/day"}
- **{"السوائل" if lang == "العربية" else "Fluids" if lang == "English" else "Sıvı" if lang == "Türkçe" else "مایعات"}:** {calculate_fluid_needs(patient['weight'], patient['age']):.0f} {"مل/يوم" if lang == "العربية" else "ml/day"}

---

#### 💊 {"خطة العلاج" if lang == "العربية" else "Treatment Plan" if lang == "English" else "Tedavi Planı" if lang == "Türkçe" else "برنامه درمانی"}
"""
    for i, rec in enumerate(recommendations, 1):
        report += f"{i}. {rec}\n"
    
    report += f"""

#### 📈 {"خطة المتابعة" if lang == "العربية" else "Follow-up Plan" if lang == "English" else "Takip Planı" if lang == "Türkçe" else "برنامه پیگیری"}
- 📊 {"إعادة فحص Lactate خلال 2-4 ساعات" if lang == "العربية" else "Re-check Lactate in 2-4 hours" if lang == "English" else "Laktatı 2-4 saat içinde tekrar kontrol et" if lang == "Türkçe" else "لاکتات را در 2-4 ساعت دوباره بررسی کنید"}
- 🩸 {"مراقبة ضغط الدم كل ساعة" if lang == "العربية" else "Monitor BP every hour" if lang == "English" else "KB'yi her saat izle" if lang == "Türkçe" else "فشار خون را هر ساعت کنترل کنید"}
- 🧪 {"إعادة تحليل الكرياتينين بعد 24 ساعة" if lang == "العربية" else "Re-check Creatinine after 24 hours" if lang == "English" else "Kreatinini 24 saat sonra tekrar kontrol et" if lang == "Türkçe" else "کراتینین را بعد از 24 ساعت دوباره بررسی کنید"}

---
🤖 *{"تم إنشاء هذا التقرير بواسطة الذكاء الاصطناعي" if lang == "العربية" else "This report was generated by AI" if lang == "English" else "Bu rapor yapay zeka tarafından oluşturuldu" if lang == "Türkçe" else "این گزارش توسط هوش مصنوعی تولید شده است"}*
⚠️ *{"هذا التقرير استرشادي ويجب مراجعته من قبل الطبيب المختص" if lang == "العربية" else "This report is for guidance only and must be reviewed by a specialist" if lang == "English" else "Bu rapor sadece rehberlik amaçlıdır ve bir uzman tarafından incelenmelidir" if lang == "Türkçe" else "این گزارش فقط برای راهنمایی است و باید توسط پزشک متخصص بررسی شود"}*
"""
    
    return report

def get_ai_diagnosis(patient, lang):
    """تشخيص باستخدام Gemini أو المحاكاة"""
    
    bmi = calculate_bmi(patient['weight'], patient['height'])
    ideal_weight = calculate_ideal_weight(patient['height'])
    creatinine_clearance = calculate_creatinine_clearance(
        patient['age'], patient['weight'], 
        patient['labs']['creatinine'], patient['gender']
    )
    pf_ratio = calculate_oxygenation_index(patient['labs']['pao2'])
    caloric_needs = calculate_caloric_needs(
        patient['weight'], patient['age'], 
        patient['gender'], patient['height']
    )
    fluid_needs = calculate_fluid_needs(patient['weight'], patient['age'])
    
    # محاولة استخدام Gemini
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
            - Lactate: {patient['labs']['lactate']} mmol/L
            - Creatinine: {patient['labs']['creatinine']} mg/dL
            - K: {patient['labs']['k']} mEq/L
            - WBC: {patient['labs']['wbc']} ×10³/µL
            
            Provide diagnosis and treatment plan.
            Respond in the same language as the user's request.
            """
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(context)
            
            return {
                "success": True,
                "diagnosis": response.text,
                "bmi": bmi,
                "ideal_weight": ideal_weight,
                "creatinine_clearance": creatinine_clearance,
                "pf_ratio": pf_ratio,
                "caloric_needs": caloric_needs,
                "fluid_needs": fluid_needs,
                "source": "Gemini AI"
            }
        except:
            pass
    
    # المحاكاة
    return {
        "success": True,
        "diagnosis": generate_simulation_diagnosis(patient, lang),
        "bmi": bmi,
        "ideal_weight": ideal_weight,
        "creatinine_clearance": creatinine_clearance,
        "pf_ratio": pf_ratio,
        "caloric_needs": caloric_needs,
        "fluid_needs": fluid_needs,
        "source": "AI Simulator"
    }

# ======================================================================
# 🔔 التنبيهات
# ======================================================================

def check_alerts(patient, lang):
    alerts = []
    
    if patient['vitals']['systolic_bp'] < 90:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("انخفاض الضغط" if lang == "العربية" else "Hypotension" if lang == "English" else "Hipotansiyon" if lang == "Türkçe" else "هیپوتانسیون"),
            "message": f"{'الضغط' if lang == 'العربية' else 'BP'}: {patient['vitals']['systolic_bp']} mmHg",
            "action": "💉 " + ("ابدأ بالسوائل الوريدية" if lang == "العربية" else "Start IV fluids" if lang == "English" else "IV sıvı başlat" if lang == "Türkçe" else "شروع مایعات وریدی")
        })
    
    if patient['vitals']['spo2'] < 90:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("نقص أكسجة" if lang == "العربية" else "Hypoxemia" if lang == "English" else "Hipoksemi" if lang == "Türkçe" else "هیپوکسی"),
            "message": f"SpO2: {patient['vitals']['spo2']}%",
            "action": "🫁 " + ("أعطِ أكسجين" if lang == "العربية" else "Give oxygen" if lang == "English" else "Oksijen ver" if lang == "Türkçe" else "اکسیژن بدهید")
        })
    
    if patient['labs']['lactate'] > 4:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("ارتفاع اللاكتات" if lang == "العربية" else "High Lactate" if lang == "English" else "Yüksek Laktat" if lang == "Türkçe" else "لاکتات بالا"),
            "message": f"Lactate: {patient['labs']['lactate']} mmol/L",
            "action": "🧪 " + ("أعد تقييم الإنتان" if lang == "العربية" else "Re-evaluate sepsis" if lang == "English" else "Sepsi yeniden değerlendir" if lang == "Türkçe" else "سپسیس را دوباره ارزیابی کنید")
        })
    
    if patient['labs']['k'] > 5.5:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("ارتفاع البوتاسيوم" if lang == "العربية" else "Hyperkalemia" if lang == "English" else "Hiperkalemi" if lang == "Türkçe" else "هیپرکالمی"),
            "message": f"K: {patient['labs']['k']} mEq/L",
            "action": "💉 " + ("أعطِ كالسيوم جلوكونات" if lang == "العربية" else "Give Calcium gluconate" if lang == "English" else "Kalsiyum glukonat ver" if lang == "Türkçe" else "کلسیم گلوکونات بدهید")
        })
    
    if patient['sofa_score'] >= 4:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("خلل عضوي" if lang == "العربية" else "Organ Failure" if lang == "English" else "Organ Yetmezliği" if lang == "Türkçe" else "نارسایی اندام"),
            "message": f"SOFA: {patient['sofa_score']}",
            "action": "🆘 " + ("تقييم عاجل" if lang == "العربية" else "Urgent assessment" if lang == "English" else "Acil değerlendirme" if lang == "Türkçe" else "ارزیابی فوری")
        })
    
    return alerts

# ======================================================================
# 📱 إعدادات الصفحة (متوافق مع الموبايل)
# ======================================================================

st.set_page_config(
    page_title="Mohammed ICU",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
            "chronic_diseases": ["السكري", "ارتفاع الضغط"],
            "allergies": ["البنسلين"],
            "surgeries": ["قسطرة قلبية 2020"],
            "current_medications": ["الأنسولين", "الليسينوبريل"],
            "diagnosis": "Sepsis",
            "status": "حرج",
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
            "current_medications": ["البخاخات"],
            "diagnosis": "Pneumonia",
            "status": "متوسط",
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

if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = st.session_state.patients[0]

if 'page' not in st.session_state:
    st.session_state.page = "login"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user' not in st.session_state:
    st.session_state.user = None

if 'role' not in st.session_state:
    st.session_state.role = None

# ======================================================================
# 🔐 تسجيل الدخول
# ======================================================================

def check_login(username, password):
    if username in AUTHORIZED_USERS:
        user = AUTHORIZED_USERS[username]
        if user["password"] == password and user.get("approved", False):
            return user
    return None

def has_permission(user, permission):
    if not user:
        return False
    if user.get("role") == "admin":
        return True
    return True if "all" in user.get("permissions", []) else permission in user.get("permissions", [])

# ======================================================================
# 🏠 صفحة الدخول الرئيسية
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
    
    # الشعار والعنوان
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0c2340, #1a5276); padding: 35px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 48px; margin: 0;">{L['app_title']}</h1>
        <p style="font-size: 20px; opacity: 0.9;">{L['app_subtitle']}</p>
        <p style="font-size: 16px; opacity: 0.7;">🌐 {lang}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='text-align: center;'>{L['choose_role']}</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b = st.columns(2)
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

# ======================================================================
# 🔐 نموذج تسجيل الدخول
# ======================================================================

def login_form():
    lang = st.session_state.lang
    L = LANGUAGES[lang]
    
    # اختيار اللغة
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
        <p style="font-size: 14px; opacity: 0.6;">{st.session_state.role} | 🌐 {lang}</p>
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
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("❌ " + ("بيانات غير صحيحة" if lang == "العربية" else "Invalid credentials" if lang == "English" else "Geçersiz bilgiler" if lang == "Türkçe" else "اطلاعات نامعتبر"))
            
            st.caption(f"📝 admin / admin123")

# ======================================================================
# 📊 لوحة التحكم الرئيسية
# ======================================================================

def dashboard():
    lang = st.session_state.lang
    L = LANGUAGES[lang]
    
    # اختيار اللغة في الشريط الجانبي
    with st.sidebar:
        selected_lang = st.selectbox("🌐 Language", list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index(lang))
        if selected_lang != lang:
            st.session_state.lang = selected_lang
            st.rerun()
        
        st.markdown("---")
        
        # معلومات المستخدم
        role_name = L['doctor'] if st.session_state.role == "doctor" else L['nurse']
        st.markdown(f"### 👤 {st.session_state.user['name']}")
        st.markdown(f"📋 {role_name}")
        st.markdown("---")
        
        # اختيار المريض
        patient_names = [p["name"] for p in st.session_state.patients]
        selected = st.selectbox(L['select_patient'], patient_names)
        st.session_state.selected_patient = next(p for p in st.session_state.patients if p["name"] == selected)
        
        st.markdown("---")
        
        # حالة Gemini
        if GEMINI_AVAILABLE:
            st.success("✅ Gemini AI " + ("متصل" if lang == "العربية" else "Connected" if lang == "English" else "Bağlı" if lang == "Türkçe" else "متصل"))
        else:
            st.info("🔄 " + ("وضع المحاكاة" if lang == "العربية" else "Simulation Mode" if lang == "English" else "Simülasyon Modu" if lang == "Türkçe" else "حالت شبیه‌سازی"))
        
        st.markdown("---")
        if st.button(L['logout'], use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # المحتوى الرئيسي
    patient = st.session_state.selected_patient
    
    if patient:
        # ترجمة مستوى الخطورة
        risk_translation = {
            "حرج": L['critical'],
            "متوسط": L['moderate'],
            "منخفض": L['low']
        }
        
        risk_class = "status-critical" if patient['risk_level'] == "حرج" else "status-moderate" if patient['risk_level'] == "متوسط" else "status-low"
        
        # رأس المريض
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0c2340, #1a5276); padding: 25px; border-radius: 12px; color: white; margin-bottom: 25px;">
            <h2 style="margin: 0;">🩺 {patient['name']}</h2>
            <p>🧬 {L['username']}: {patient['age']} {'سنة' if lang == 'العربية' else 'years' if lang == 'English' else 'yaş' if lang == 'Türkçe' else 'سال'} | {patient['gender']} | {L['source']}: {patient['weight']} {'كجم' if lang == 'العربية' else 'kg'}</p>
            <p>📋 {L['diagnosis']}: {patient['diagnosis']}</p>
            <span style="display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 14px; background: {'#e74c3c' if patient['risk_level'] == 'حرج' else '#f1c40f' if patient['risk_level'] == 'متوسط' else '#2ecc71'}; color: {'white' if patient['risk_level'] == 'حرج' else 'black' if patient['risk_level'] == 'متوسط' else 'white'};">
                {risk_translation.get(patient['risk_level'], patient['risk_level'])}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # علامات التبويب
        tabs = st.tabs([L['vitals'], L['lab'], L['assessment'], L['ai'], L['alerts']])
        
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
                "الفحص" if lang == "العربية" else "Test" if lang == "English" else "Test" if lang == "Türkçe" else "آزمایش": ["WBC", "HB", "PLT", "pH", "PaCO2", "PaO2", "HCO3", "Na", "K", "Ca", "Creatinine", "BUN", "ALT", "AST", "Bilirubin", "INR", "Troponin", "Lactate"],
                "النتيجة" if lang == "العربية" else "Result" if lang == "English" else "Sonuç" if lang == "Türkçe" else "نتیجه": [labs['wbc'], labs['hb'], labs['plt'], labs['ph'], labs['paco2'], labs['pao2'], labs['hco3'], labs['na'], labs['k'], labs['ca'], labs['creatinine'], labs['bun'], labs['alt'], labs['ast'], labs['bilirubin'], labs['inr'], labs['troponin'], labs['lactate']],
                "الوحدة" if lang == "العربية" else "Unit" if lang == "English" else "Birim" if lang == "Türkçe" else "واحد": ["×10³/µL", "g/dL", "×10³/µL", "", "mmHg", "mmHg", "mEq/L", "mEq/L", "mEq/L", "mEq/L", "mg/dL", "mg/dL", "U/L", "U/L", "mg/dL", "", "ng/mL", "mmol/L"]
            }
            df = pd.DataFrame(lab_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # ===== تبويب 3: التقييم =====
        with tabs[2]:
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
                st.metric(L['risk_level'], risk_translation.get(patient['risk_level'], patient['risk_level']))
            
            if patient['sofa_score'] >= 4:
                st.error("🚨 SOFA ≥ 4: " + ("خلل عضوي حاد" if lang == "العربية" else "Severe organ failure" if lang == "English" else "Şiddetli organ yetmezliği" if lang == "Türkçe" else "نارسایی شدید اندام"))
            if patient['news2_score'] >= 7:
                st.error("🚨 NEWS2 ≥ 7: " + ("حالة حرجة" if lang == "العربية" else "Critical condition" if lang == "English" else "Kritik durum" if lang == "Türkçe" else "وضعیت بحرانی"))
        
        # ===== تبويب 4: الذكاء الاصطناعي =====
        with tabs[3]:
            st.subheader(L['ai'])
            
            if not has_permission(st.session_state.user, "ai_analysis"):
                st.warning("⚠️ " + ("ليس لديك صلاحية" if lang == "العربية" else "You don't have permission" if lang == "English" else "Yetkiniz yok" if lang == "Türkçe" else "شما مجوز ندارید"))
            else:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info(f"{L['source']}: {('Gemini AI' if GEMINI_AVAILABLE else 'AI Simulator')}")
                
                if st.button(L['ai_analysis'], use_container_width=True, type="primary"):
                    with st.spinner("🧠 " + ("جاري التحليل..." if lang == "العربية" else "Analyzing..." if lang == "English" else "Analiz ediliyor..." if lang == "Türkçe" else "در حال تحلیل...")):
                        result = get_ai_diagnosis(patient, lang)
                        
                        if result["success"]:
                            st.markdown("### 📊 " + ("المؤشرات المحسوبة" if lang == "العربية" else "Calculated Indicators" if lang == "English" else "Hesaplanan Göstergeler" if lang == "Türkçe" else "شاخص‌های محاسبه شده"))
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("BMI", f"{result['bmi']:.1f}")
                                st.metric(L['risk_level'], L['moderate'] if result['bmi'] > 25 else L['low'])
                            with col2:
                                st.metric("Creatinine Clearance", f"{result['creatinine_clearance']:.1f} mL/min")
                                st.metric("P/F Ratio", f"{result['pf_ratio']:.1f}")
                            with col3:
                                st.metric("Calories", f"{result['caloric_needs']:.0f} kcal")
                                st.metric("Fluids", f"{result['fluid_needs']:.0f} mL")
                            
                            st.markdown("### 📋 " + ("التقرير السريري" if lang == "العربية" else "Clinical Report" if lang == "English" else "Klinik Rapor" if lang == "Türkçe" else "گزارش بالینی"))
                            st.markdown(result["diagnosis"])
                            
                            if "source" in result:
                                st.info(f"✅ {L['source']}: {result['source']}")
                        else:
                            st.error(f"❌ {result['error']}")
        
        # ===== تبويب 5: التنبيهات =====
        with tabs[4]:
            st.subheader(L['alerts'])
            
            if not has_permission(st.session_state.user, "alerts"):
                st.warning("⚠️ " + ("ليس لديك صلاحية" if lang == "العربية" else "You don't have permission" if lang == "English" else "Yetkiniz yok" if lang == "Türkçe" else "شما مجوز ندارید"))
            else:
                alerts = check_alerts(patient, lang)
                if alerts:
                    for alert in alerts:
                        st.markdown(f"""
                        <div style="background: #fadbd8; border-right: 6px solid #e74c3c; padding: 15px; border-radius: 10px; margin: 8px 0;">
                            <strong>{alert['title']}</strong>
                            <br>{alert['message']}
                            <br><strong style="color: #e74c3c;">🛑 {alert['action']}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: #d5f5e3; border-right: 6px solid #27ae60; padding: 15px; border-radius: 10px; margin: 8px 0;">
                        ✅ {L['no_alerts']}
                    </div>
                    """, unsafe_allow_html=True)

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