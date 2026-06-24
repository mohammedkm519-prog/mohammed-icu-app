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
    "dr_sara": {
        "password": "sara123",
        "role": "doctor",
        "name": "د. سارة",
        "approved": True,
        "permissions": ["view_patients", "ai_analysis", "alerts"]
    },
    "nurse_fatima": {
        "password": "nurse123",
        "role": "nurse",
        "name": "فاطمة",
        "approved": True,
        "permissions": ["view_patients", "add_vitals", "alerts"]
    },
    "nurse_ali": {
        "password": "ali123",
        "role": "nurse",
        "name": "علي",
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
    is_male = gender in ["ذكر", "Male", "Erkek", "مرد"]
    if is_male:
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
    issues = []
    recommendations = []
    
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
    
    if patient['labs']['wbc'] > 15:
        issues.append("🟡 " + ("ارتفاع كريات الدم البيضاء - خطر العدوى" if lang == "العربية" else "High WBC - Infection risk" if lang == "English" else "Yüksek WBC - Enfeksiyon riski" if lang == "Türkçe" else "WBC بالا - خطر عفونت"))
        recommendations.append("🦠 " + ("ابحث عن مصدر العدوى، ابدأ بالمضادات الحيوية" if lang == "العربية" else "Find infection source, start antibiotics" if lang == "English" else "Enfeksiyon kaynağını bul, antibiyotik başla" if lang == "Türkçe" else "منبع عفونت را پیدا کنید، آنتی‌بیوتیک شروع کنید"))
    
    if patient['vitals']['heart_rate'] > 120:
        issues.append("🟡 " + ("تسرع قلبي" if lang == "العربية" else "Tachycardia" if lang == "English" else "Taşikardi" if lang == "Türkçe" else "تاکیکاردی"))
        recommendations.append("💊 " + ("تحقق من حالة السوائل، فكر في Beta-blockers" if lang == "العربية" else "Check fluid status, consider Beta-blockers" if lang == "English" else "Sıvı durumunu kontrol et, Beta-blokerleri düşün" if lang == "Türkçe" else "وضعیت مایعات را بررسی کنید، بتا بلوکرها را در نظر بگیرید"))
    
    if patient['vitals']['temperature'] > 38.5:
        issues.append("🟡 " + ("حمى" if lang == "العربية" else "Fever" if lang == "English" else "Ateş" if lang == "Türkçe" else "تب"))
        recommendations.append("🌡️ " + ("خذ عينات للزراعة، أعطِ خافض حرارة" if lang == "العربية" else "Take cultures, give antipyretic" if lang == "English" else "Kültür al, ateş düşürücü ver" if lang == "Türkçe" else "کشت بگیرید، ضد تب بدهید"))
    
    # تشخيص رئيسي
    if patient['labs']['lactate'] > 4 and patient['vitals']['systolic_bp'] < 90:
        main_diagnosis = "🩺 **" + ("Sepsis مع Septic Shock" if lang == "العربية" else "Sepsis with Septic Shock" if lang == "English" else "Septik Şok ile Sepsis" if lang == "Türkçe" else "سپسیس با شوک سپتیک") + "** (85%)"
    elif patient['labs']['creatinine'] > 2:
        main_diagnosis = "🩺 **" + ("فشل كلوي حاد" if lang == "العربية" else "Acute Kidney Injury" if lang == "English" else "Akut Böbrek Hasarı" if lang == "Türkçe" else "آسیب حاد کلیه") + "** (75%)"
    elif patient['vitals']['systolic_bp'] > 140:
        main_diagnosis = "🩺 **" + ("ارتفاع ضغط الدم غير المسيطر عليه" if lang == "العربية" else "Uncontrolled Hypertension" if lang == "English" else "Kontrolsüz Hipertansiyon" if lang == "Türkçe" else "فشار خون کنترل نشده") + "** (80%)"
    elif patient['vitals']['spo2'] < 92:
        main_diagnosis = "🩺 **" + ("نقص أكسجة - خطر ARDS" if lang == "العربية" else "Hypoxemia - ARDS risk" if lang == "English" else "Hipoksemi - ARDS riski" if lang == "Türkçe" else "هیپوکسی - خطر ARDS") + "** (70%)"
    else:
        main_diagnosis = "🩺 **" + ("حالة مستقرة نسبياً - يحتاج إلى مراقبة" if lang == "العربية" else "Relatively stable - Requires monitoring" if lang == "English" else "Nispeten stabil - İzlem gerektirir" if lang == "Türkçe" else "نسبتاً پایدار - نیاز به نظارت دارد") + "**"
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
- **BMI:** {calculate_bmi(patient['weight'], patient['height']):.1f} ({"طبيعي" if calculate_bmi(patient['weight'], patient['height']) < 25 else "مرتفع" if lang == "العربية" else "Normal" if lang == "English" else "Normal" if lang == "Türkçe" else "طبیعی"})
- **{"الوزن المثالي" if lang == "العربية" else "Ideal Weight" if lang == "English" else "İdeal Kilo" if lang == "Türkçe" else "وزن ایده آل"}:** {calculate_ideal_weight(patient['height']):.1f} {"كجم" if lang == "العربية" else "kg"}
- **{"تصفية الكرياتينين" if lang == "العربية" else "Creatinine Clearance" if lang == "English" else "Kreatinin Klerensi" if lang == "Türkçe" else "کلیرانس کراتینین"}:** {calculate_creatinine_clearance(patient['age'], patient['weight'], patient['labs']['creatinine'], patient['gender']):.1f} mL/min
- **{"السعرات" if lang == "العربية" else "Calories" if lang == "English" else "Kalori" if lang == "Türkçe" else "کالری"}:** {calculate_caloric_needs(patient['weight'], patient['age'], patient['gender'], patient['height']):.0f} {"سعرة/يوم" if lang == "العربية" else "kcal/day"}
- **{"السوائل" if lang == "العربية" else "Fluids" if lang == "English" else "Sıvı" if lang == "Türkçe" else "مایعات"}:** {calculate_fluid_needs(patient['weight'], patient['age']):.0f} {"مل/يوم" if lang == "العربية" else "ml/day"}

---

#### 💊 {"خطة العلاج المقترحة" if lang == "العربية" else "Treatment Plan" if lang == "English" else "Tedavi Planı" if lang == "Türkçe" else "برنامه درمانی پیشنهادی"}
"""
    for i, rec in enumerate(recommendations, 1):
        report += f"{i}. {rec}\n"
    
    if not recommendations:
        report += "- " + ("لا توجد توصيات حالياً" if lang == "العربية" else "No recommendations currently" if lang == "English" else "Şu anda öneri yok" if lang == "Türkçe" else "در حال حاضر توصیه‌ای وجود ندارد")
    
    report += f"""

#### 📈 {"خطة المتابعة" if lang == "العربية" else "Follow-up Plan" if lang == "English" else "Takip Planı" if lang == "Türkçe" else "برنامه پیگیری"}
- 📊 {"إعادة فحص Lactate خلال 2-4 ساعات" if lang == "العربية" else "Re-check Lactate in 2-4 hours" if lang == "English" else "Laktatı 2-4 saat içinde tekrar kontrol et" if lang == "Türkçe" else "لاکتات را در 2-4 ساعت دوباره بررسی کنید"}
- 🩸 {"مراقبة ضغط الدم كل ساعة" if lang == "العربية" else "Monitor BP every hour" if lang == "English" else "KB'yi her saat izle" if lang == "Türkçe" else "فشار خون را هر ساعت کنترل کنید"}
- 🧪 {"إعادة تحليل الكرياتينين بعد 24 ساعة" if lang == "العربية" else "Re-check Creatinine after 24 hours" if lang == "English" else "Kreatinini 24 saat sonra tekrar kontrol et" if lang == "Türkçe" else "کراتینین را بعد از 24 ساعت دوباره بررسی کنید"}
- 🔔 {"تنبيه: أي تدهور في العلامات الحيوية يستدعي تدخلاً فورياً" if lang == "العربية" else "Alert: Any deterioration in vital signs requires immediate intervention" if lang == "English" else "Uyarı: Vital bulgulardaki herhangi bir bozulma acil müdahale gerektirir" if lang == "Türkçe" else "هشدار: هر گونه بدتر شدن علائم حیاتی نیاز به مداخله فوری دارد"}

---
🤖 *{"تم إنشاء هذا التقرير بواسطة الذكاء الاصطناعي" if lang == "العربية" else "This report was generated by AI" if lang == "English" else "Bu rapor yapay zeka tarafından oluşturuldu" if lang == "Türkçe" else "این گزارش توسط هوش مصنوعی تولید شده است"}*
⚠️ *{"هذا التقرير استرشادي ويجب مراجعته من قبل الطبيب المختص" if lang == "العربية" else "This report is for guidance only and must be reviewed by a specialist" if lang == "English" else "Bu rapor sadece rehberlik amaçlıdır ve bir uzman tarafından incelenmelidir" if lang == "Türkçe" else "این گزارش فقط برای راهنمایی است و باید توسط پزشک متخصص بررسی شود"}*
"""
    
    return report

def get_ai_diagnosis(patient, lang):
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
            - RR: {patient['vitals']['respiratory_rate']}
            - CVP: {patient['vitals']['cvp']}
            - ICP: {patient['vitals']['icp']}
            
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
            
            Calculated:
            - Creatinine Clearance: {creatinine_clearance:.1f} mL/min
            - P/F Ratio: {pf_ratio:.1f}
            - Caloric Needs: {caloric_needs:.0f} kcal/day
            - Fluid Needs: {fluid_needs:.0f} ml/day
            
            Scores:
            - SOFA: {patient['sofa_score']}
            - NEWS2: {patient['news2_score']}
            - GCS: {patient['gcs_score']}
            
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
                "pf_ratio": pf_ratio,
                "caloric_needs": caloric_needs,
                "fluid_needs": fluid_needs,
                "source": "Gemini AI"
            }
        except:
            pass
    
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
    
    if patient['news2_score'] >= 7:
        alerts.append({
            "type": "critical",
            "title": "🚨 " + ("حالة حرجة" if lang == "العربية" else "Critical Condition" if lang == "English" else "Kritik Durum" if lang == "Türkçe" else "وضعیت بحرانی"),
            "message": f"NEWS2: {patient['news2_score']}",
            "action": "🆘 " + ("مراقبة مستمرة وتدخل فوري" if lang == "العربية" else "Continuous monitoring and immediate intervention" if lang == "English" else "Sürekli izleme ve acil müdahale" if lang == "Türkçe" else "نظارت مستمر و مداخله فوری")
        })
    
    if patient['labs']['creatinine'] > 2:
        alerts.append({
            "type": "high",
            "title": "⚠️ " + ("ارتفاع الكرياتينين" if lang == "العربية" else "High Creatinine" if lang == "English" else "Yüksek Kreatinin" if lang == "Türkçe" else "کراتینین بالا"),
            "message": f"Creatinine: {patient['labs']['creatinine']} mg/dL",
            "action": "💊 " + ("راقب السوائل، تجنب الأدوية السمية" if lang == "العربية" else "Monitor fluids, avoid nephrotoxic drugs" if lang == "English" else "Sıvıları izle, nefrotoksik ilaçlardan kaçın" if lang == "Türkçe" else "مایعات را کنترل کنید، از داروهای نفروتوکسیک اجتناب کنید")
        })
    
    if patient['labs']['wbc'] > 15:
        alerts.append({
            "type": "high",
            "title": "⚠️ " + ("ارتفاع كريات الدم البيضاء" if lang == "العربية" else "High WBC" if lang == "English" else "Yüksek WBC" if lang == "Türkçe" else "WBC بالا"),
            "message": f"WBC: {patient['labs']['wbc']} ×10³/µL",
            "action": "🦠 " + ("ابحث عن مصدر العدوى" if lang == "العربية" else "Find infection source" if lang == "English" else "Enfeksiyon kaynağını bul" if lang == "Türkçe" else "منبع عفونت را پیدا کنید")
        })
    
    if patient['vitals']['heart_rate'] > 120:
        alerts.append({
            "type": "high",
            "title": "⚠️ " + ("تسرع قلبي" if lang == "العربية" else "Tachycardia" if lang == "English" else "Taşikardi" if lang == "Türkçe" else "تاکیکاردی"),
            "message": f"HR: {patient['vitals']['heart_rate']} bpm",
            "action": "💊 " + ("تحقق من حالة السوائل" if lang == "العربية" else "Check fluid status" if lang == "English" else "Sıvı durumunu kontrol et" if lang == "Türkçe" else "وضعیت مایعات را بررسی کنید")
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

# CSS للتوافق مع الموبايل
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
    .vital-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border-bottom: 4px solid #2e86c1;
    }
    .vital-value { font-size: 32px; font-weight: bold; color: #0c2340; }
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
    .alert-high {
        background: #fdebd0;
        border-right: 6px solid #e67e22;
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
    @media (max-width: 768px) {
        .stDataFrame { font-size: 12px !important; overflow-x: auto !important; }
        .stColumns { flex-direction: column !important; }
        .stButton button { width: 100% !important; padding: 15px !important; font-size: 18px !important; }
        .main-header h1 { font-size: 28px !important; }
        .main-header p { font-size: 16px !important; }
        .vital-value { font-size: 24px !important; }
        .patient-header h2 { font-size: 20px !important; }
        .patient-header p { font-size: 14px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ======================================================================
# 🌐 اختيار اللغة
# ======================================================================

if 'lang' not in st.session_state:
    st.session_state.lang = "العربية"

# ======================================================================
# 📦 البيانات - المرضى (4 مرضى)
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
        },
        {
            "id": 3,
            "name": "محمد إبراهيم",
            "age": 55,
            "gender": "ذكر",
            "weight": 80,
            "height": 172,
            "chronic_diseases": ["ارتفاع الضغط", "السكري"],
            "allergies": ["لا يوجد"],
            "surgeries": ["لا يوجد"],
            "current_medications": ["الاملوديبين", "الميتفورمين"],
            "diagnosis": "Hypertension",
            "status": "متوسط",
            "vitals": {
                "systolic_bp": 145,
                "diastolic_bp": 90,
                "heart_rate": 78,
                "temperature": 36.8,
                "respiratory_rate": 16,
                "spo2": 97,
                "cvp": 6,
                "icp": 10,
                "ecg": "طبيعي"
            },
            "labs": {
                "wbc": 7.5,
                "hb": 14.0,
                "plt": 280,
                "ph": 7.40,
                "paco2": 38,
                "pao2": 85,
                "hco3": 24,
                "na": 140,
                "k": 4.2,
                "ca": 9.2,
                "creatinine": 0.9,
                "bun": 15,
                "alt": 30,
                "ast": 28,
                "bilirubin": 0.6,
                "pt": 12.0,
                "inr": 1.0,
                "troponin": 0.01,
                "lactate": 1.2
            },
            "sofa_score": 1,
            "news2_score": 2,
            "gcs_score": 15,
            "risk_level": "منخفض"
        },
        {
            "id": 4,
            "name": "فاطمة علي",
            "age": 38,
            "gender": "أنثى",
            "weight": 65,
            "height": 160,
            "chronic_diseases": ["الربو"],
            "allergies": ["البنسلين"],
            "surgeries": ["عملية قيصرية 2019"],
            "current_medications": ["البخاخات", "الستيرويدات"],
            "diagnosis": "Asthma Exacerbation",
            "status": "متوسط",
            "vitals": {
                "systolic_bp": 120,
                "diastolic_bp": 75,
                "heart_rate": 92,
                "temperature": 37.2,
                "respiratory_rate": 22,
                "spo2": 93,
                "cvp": 7,
                "icp": 11,
                "ecg": "طبيعي"
            },
            "labs": {
                "wbc": 10.2,
                "hb": 13.0,
                "plt": 300,
                "ph": 7.38,
                "paco2": 40,
                "pao2": 70,
                "hco3": 23,
                "na": 138,
                "k": 4.0,
                "ca": 9.0,
                "creatinine": 0.7,
                "bun": 14,
                "alt": 25,
                "ast": 30,
                "bilirubin": 0.5,
                "pt": 11.5,
                "inr": 0.9,
                "troponin": 0.01,
                "lactate": 1.5
            },
            "sofa_score": 2,
            "news2_score": 4,
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
    
    with st.sidebar:
        selected_lang = st.selectbox("🌐 Language", list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index(lang))
        if selected_lang != lang:
            st.session_state.lang = selected_lang
            st.rerun()
        
        st.markdown("---")
        
        role_name = L['doctor'] if st.session_state.role == "doctor" else L['nurse']
        st.markdown(f"### 👤 {st.session_state.user['name']}")
        st.markdown(f"📋 {role_name}")
        st.markdown("---")
        
        patient_names = [p["name"] for p in st.session_state.patients]
        selected = st.selectbox(L['select_patient'], patient_names)
        st.session_state.selected_patient = next(p for p in st.session_state.patients if p["name"] == selected)
        
        st.markdown("---")
        
        if GEMINI_AVAILABLE:
            st.success("✅ Gemini AI " + ("متصل" if lang == "العربية" else "Connected" if lang == "English" else "Bağlı" if lang == "Türkçe" else "متصل"))
        else:
            st.info("🔄 " + ("وضع المحاكاة" if lang == "العربية" else "Simulation Mode" if lang == "English" else "Simülasyon Modu" if lang == "Türkçe" else "حالت شبیه‌سازی"))
        
        st.markdown("---")
        if st.button(L['logout'], use_container_width=True):
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
        
        st.markdown(f"""
        <div class="patient-header">
            <h2 style="margin: 0;">🩺 {patient['name']}</h2>
            <p>🧬 {'العمر' if lang == 'العربية' else 'Age' if lang == 'English' else 'Yaş' if lang == 'Türkçe' else 'سن'}: {patient['age']} {'سنة' if lang == 'العربية' else 'years' if lang == 'English' else 'yaş' if lang == 'Türkçe' else 'سال'} | {patient['gender']} | {'الوزن' if lang == 'العربية' else 'Weight' if lang == 'English' else 'Kilo' if lang == 'Türkçe' else 'وزن'}: {patient['weight']} {'كجم' if lang == 'العربية' else 'kg'}</p>
            <p>📋 {L['diagnosis']}: {patient['diagnosis']}</p>
            <span class="status-badge {risk_class}">{risk_translation.get(patient['risk_level'], patient['risk_level'])}</span>
        </div>
        """, unsafe_allow_html=True)
        
        tabs = st.tabs([L['vitals'], L['lab'], L['assessment'], L['ai'], L['alerts']])
        
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
        
        with tabs[4]:
            st.subheader(L['alerts'])
            
            if not has_permission(st.session_state.user, "alerts"):
                st.warning("⚠️ " + ("ليس لديك صلاحية" if lang == "العربية" else "You don't have permission" if lang == "English" else "Yetkiniz yok" if lang == "Türkçe" else "شما مجوز ندارید"))
            else:
                alerts = check_alerts(patient, lang)
                if alerts:
                    for alert in alerts:
                        alert_class = "alert-critical" if alert["type"] == "critical" else "alert-high"
                        st.markdown(f"""
                        <div class="{alert_class}">
                            <strong>{alert['title']}</strong>
                            <br>{alert['message']}
                            <br><strong style="color: {'#e74c3c' if alert['type'] == 'critical' else '#e67e22'};">🛑 {alert['action']}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="success-box">
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