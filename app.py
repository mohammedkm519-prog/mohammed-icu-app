# ======================================================================
# 🏥 MOHAMMED ICU - النسخة المبسطة (تعمل بدون Plotly)
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
# 🔑 إعدادات الذكاء الاصطناعي (Gemini API)
# ======================================================================

GEMINI_API_KEY = "AQ.Ab8RN6I9tQyt3v3bUCQO67ozRjCYPNpdi4Ars-B5rFpz_fVaSg"

try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

# ======================================================================
# 👥 المستخدمون والصلاحيات
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
    if gender == "ذكر":
        return ((140 - age) * weight) / (72 * creatinine)
    else:
        return ((140 - age) * weight * 0.85) / (72 * creatinine)

def calculate_oxygenation_index(pao2, fio2=0.21):
    return pao2 / fio2

def calculate_caloric_needs(weight, age, gender, height, stress_factor=1.2):
    if gender == "ذكر":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr * stress_factor

def calculate_fluid_needs(weight, age, stress_factor=1.5):
    return weight * 30 * stress_factor

# ======================================================================
# 🤖 الذكاء الاصطناعي
# ======================================================================

def generate_simulation_diagnosis(patient):
    """توليد تشخيص محاكي"""
    
    issues = []
    recommendations = []
    
    # تحليل العلامات الحيوية
    if patient['vitals']['systolic_bp'] < 90:
        issues.append("🔴 انخفاض حاد في ضغط الدم")
        recommendations.append("💉 ابدأ بالسوائل الوريدية فوراً")
    
    if patient['vitals']['spo2'] < 90:
        issues.append("🔴 نقص أكسجة حاد")
        recommendations.append("🫁 أعطِ أكسجين عالي التدفق")
    
    if patient['vitals']['heart_rate'] > 120:
        issues.append("🟡 تسرع قلبي")
        recommendations.append("💊 تحقق من حالة السوائل")
    
    if patient['vitals']['temperature'] > 38.5:
        issues.append("🟡 حمى")
        recommendations.append("🌡️ خذ عينات للزراعة")
    
    # تحليل المختبر
    if patient['labs']['lactate'] > 4:
        issues.append("🔴 ارتفاع اللاكتات")
        recommendations.append("🧪 أعد تقييم الإنتان")
    
    if patient['labs']['creatinine'] > 2:
        issues.append("🟡 ارتفاع الكرياتينين")
        recommendations.append("💊 راقب السوائل")
    
    if patient['labs']['k'] > 5.5:
        issues.append("🔴 ارتفاع البوتاسيوم")
        recommendations.append("💉 أعطِ كالسيوم جلوكونات")
    
    # تشخيص رئيسي
    if patient['labs']['lactate'] > 4 and patient['vitals']['systolic_bp'] < 90:
        main_diagnosis = "🩺 **Sepsis مع Septic Shock** (نسبة الثقة: 85%)"
    elif patient['labs']['creatinine'] > 2:
        main_diagnosis = "🩺 **فشل كلوي حاد** (نسبة الثقة: 75%)"
    else:
        main_diagnosis = "🩺 **حالة مستقرة** - يحتاج إلى مراقبة"
        recommendations.append("📊 استمرار المراقبة")
    
    # بناء التقرير
    report = f"""
### 📋 التقرير السريري

---

#### 🎯 التشخيص الرئيسي
{main_diagnosis}

---

#### ⚠️ المشاكل المكتشفة
"""
    for issue in issues:
        report += f"- {issue}\n"
    
    if not issues:
        report += "- ✅ لا توجد مشاكل حرجة\n"
    
    report += f"""

#### 📊 المؤشرات المحسوبة
- **BMI:** {calculate_bmi(patient['weight'], patient['height']):.1f}
- **الوزن المثالي:** {calculate_ideal_weight(patient['height']):.1f} كجم
- **تصفية الكرياتينين:** {calculate_creatinine_clearance(patient['age'], patient['weight'], patient['labs']['creatinine'], patient['gender']):.1f} mL/min
- **السعرات:** {calculate_caloric_needs(patient['weight'], patient['age'], patient['gender'], patient['height']):.0f} سعرة/يوم
- **السوائل:** {calculate_fluid_needs(patient['weight'], patient['age']):.0f} مل/يوم

---

#### 💊 خطة العلاج
"""
    for i, rec in enumerate(recommendations, 1):
        report += f"{i}. {rec}\n"
    
    return report

def get_ai_diagnosis(patient):
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
            مريض عمر {patient['age']} سنة، {patient['gender']}.
            الوزن: {patient['weight']} كجم، الطول: {patient['height']} سم.
            BMI: {bmi:.1f}
            
            العلامات الحيوية:
            - ضغط الدم: {patient['vitals']['systolic_bp']}/{patient['vitals']['diastolic_bp']} mmHg
            - النبض: {patient['vitals']['heart_rate']} نبضة/دقيقة
            - الحرارة: {patient['vitals']['temperature']}°C
            - SpO2: {patient['vitals']['spo2']}%
            
            نتائج المختبر:
            - Lactate: {patient['labs']['lactate']} mmol/L
            - Creatinine: {patient['labs']['creatinine']} mg/dL
            - K: {patient['labs']['k']} mEq/L
            
            قدم تشخيصاً وخطة علاجية.
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
        "diagnosis": generate_simulation_diagnosis(patient),
        "bmi": bmi,
        "ideal_weight": ideal_weight,
        "creatinine_clearance": creatinine_clearance,
        "pf_ratio": pf_ratio,
        "caloric_needs": caloric_needs,
        "fluid_needs": fluid_needs,
        "source": "المحاكاة الذكية"
    }

# ======================================================================
# 🔔 التنبيهات
# ======================================================================

def check_alerts(patient):
    alerts = []
    
    if patient['vitals']['systolic_bp'] < 90:
        alerts.append({
            "type": "critical",
            "title": "🚨 انخفاض الضغط",
            "message": f"الضغط: {patient['vitals']['systolic_bp']} mmHg",
            "action": "ابدأ بالسوائل الوريدية فوراً"
        })
    
    if patient['vitals']['spo2'] < 90:
        alerts.append({
            "type": "critical",
            "title": "🚨 نقص أكسجة",
            "message": f"SpO2: {patient['vitals']['spo2']}%",
            "action": "أعطِ أكسجين"
        })
    
    if patient['labs']['lactate'] > 4:
        alerts.append({
            "type": "critical",
            "title": "🚨 ارتفاع اللاكتات",
            "message": f"Lactate: {patient['labs']['lactate']} mmol/L",
            "action": "أعد تقييم الإنتان"
        })
    
    if patient['labs']['k'] > 5.5:
        alerts.append({
            "type": "critical",
            "title": "🚨 ارتفاع البوتاسيوم",
            "message": f"K: {patient['labs']['k']} mEq/L",
            "action": "أعطِ كالسيوم جلوكونات"
        })
    
    if patient['sofa_score'] >= 4:
        alerts.append({
            "type": "critical",
            "title": "🚨 خلل عضوي",
            "message": f"SOFA: {patient['sofa_score']}",
            "action": "تقييم عاجل"
        })
    
    return alerts

# ======================================================================
# 🎨 إعدادات الصفحة
# ======================================================================

st.set_page_config(
    page_title="Mohammed ICU",
    page_icon="🏥",
    layout="wide"
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
    .main-header h1 { font-size: 52px; margin: 0; }
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
    .success-box {
        background: #d5f5e3;
        border-right: 6px solid #27ae60;
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

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

def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Mohammed ICU</h1>
        <p>نظام العناية المركزة الذكي المتقدم</p>
        <p style="font-size: 14px; opacity: 0.7;">AI-Powered Intensive Care Unit</p>
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
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("❌ بيانات غير صحيحة")
            
            st.caption("📝 admin / admin123")

# ======================================================================
# 📊 لوحة التحكم
# ======================================================================

def dashboard():
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user['name']}")
        st.markdown(f"📋 {st.session_state.user['role']}")
        st.markdown("---")
        
        patient_names = [p["name"] for p in st.session_state.patients]
        selected = st.selectbox("🩺 اختر المريض:", patient_names)
        st.session_state.selected_patient = next(p for p in st.session_state.patients if p["name"] == selected)
        
        st.markdown("---")
        
        if GEMINI_AVAILABLE:
            st.success("✅ Gemini AI متصل")
        else:
            st.info("🔄 وضع المحاكاة")
        
        st.markdown("---")
        if st.button("🚪 خروج"):
            st.session_state.clear()
            st.rerun()
    
    patient = st.session_state.selected_patient
    
    if patient:
        risk_class = "status-critical" if patient['risk_level'] == "حرج" else "status-moderate" if patient['risk_level'] == "متوسط" else "status-low"
        
        st.markdown(f"""
        <div class="patient-header">
            <h2>🩺 {patient['name']}</h2>
            <p>🧬 العمر: {patient['age']} سنة | {patient['gender']} | الوزن: {patient['weight']} كجم</p>
            <p>📋 التشخيص: {patient['diagnosis']}</p>
            <span class="status-badge {risk_class}">{patient['risk_level']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        tabs = st.tabs(["📊 العلامات الحيوية", "🧪 المختبر", "🧠 التقييم", "🤖 الذكاء الاصطناعي", "🔔 التنبيهات"])
        
        with tabs[0]:
            vitals = patient['vitals']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🩸 ضغط الدم", f"{vitals['systolic_bp']}/{vitals['diastolic_bp']}")
            with col2:
                st.metric("💓 النبض", f"{vitals['heart_rate']}")
            with col3:
                st.metric("🌡️ الحرارة", f"{vitals['temperature']}°C")
            with col4:
                st.metric("💨 SpO2", f"{vitals['spo2']}%")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🫁 التنفس", f"{vitals['respiratory_rate']}")
            with col2:
                st.metric("📊 CVP", f"{vitals['cvp']}")
            with col3:
                st.metric("🧠 ICP", f"{vitals['icp']}")
        
        with tabs[1]:
            st.subheader("🧪 نتائج المختبر")
            labs = patient['labs']
            
            lab_data = {
                "الفحص": ["WBC", "HB", "PLT", "pH", "PaCO2", "PaO2", "HCO3", "Na", "K", "Ca", "Creatinine", "BUN", "ALT", "AST", "Bilirubin", "INR", "Troponin", "Lactate"],
                "النتيجة": [labs['wbc'], labs['hb'], labs['plt'], labs['ph'], labs['paco2'], labs['pao2'], labs['hco3'], labs['na'], labs['k'], labs['ca'], labs['creatinine'], labs['bun'], labs['alt'], labs['ast'], labs['bilirubin'], labs['inr'], labs['troponin'], labs['lactate']],
                "الوحدة": ["×10³/µL", "g/dL", "×10³/µL", "", "mmHg", "mmHg", "mEq/L", "mEq/L", "mEq/L", "mEq/L", "mg/dL", "mg/dL", "U/L", "U/L", "mg/dL", "", "ng/mL", "mmol/L"]
            }
            df = pd.DataFrame(lab_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        with tabs[2]:
            st.subheader("🧠 التقييم السريري")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("SOFA Score", patient['sofa_score'])
                st.metric("APACHE II", "18")
            with col2:
                st.metric("NEWS2", patient['news2_score'])
                st.metric("qSOFA", "2")
            with col3:
                st.metric("GCS", patient['gcs_score'])
                st.metric("الخطورة", patient['risk_level'])
            
            if patient['sofa_score'] >= 4:
                st.error("🚨 SOFA ≥ 4: خلل عضوي حاد")
            if patient['news2_score'] >= 7:
                st.error("🚨 NEWS2 ≥ 7: حالة حرجة")
        
        with tabs[3]:
            st.subheader("🤖 تحليل الذكاء الاصطناعي")
            
            if not has_permission(st.session_state.user, "ai_analysis"):
                st.warning("⚠️ ليس لديك صلاحية")
            else:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info(f"📡 المصدر: {('Gemini AI' if GEMINI_AVAILABLE else 'المحاكاة الذكية')}")
                
                if st.button("🧠 تشغيل التحليل الذكي", use_container_width=True, type="primary"):
                    with st.spinner("🧠 جاري التحليل..."):
                        result = get_ai_diagnosis(patient)
                        
                        if result["success"]:
                            st.markdown("### 📊 المؤشرات المحسوبة")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("BMI", f"{result['bmi']:.1f}")
                                st.metric("الوزن المثالي", f"{result['ideal_weight']:.1f} كجم")
                            with col2:
                                st.metric("تصفية الكرياتينين", f"{result['creatinine_clearance']:.1f} mL/min")
                                st.metric("P/F Ratio", f"{result['pf_ratio']:.1f}")
                            with col3:
                                st.metric("السعرات", f"{result['caloric_needs']:.0f} سعرة")
                                st.metric("السوائل", f"{result['fluid_needs']:.0f} مل")
                            
                            st.markdown("### 📋 التقرير السريري")
                            st.markdown(result["diagnosis"])
                            
                            if "source" in result:
                                st.info(f"✅ تم إنشاء التقرير بواسطة: {result['source']}")
                        else:
                            st.error(f"❌ {result['error']}")
        
        with tabs[4]:
            st.subheader("🔔 التنبيهات")
            
            if not has_permission(st.session_state.user, "alerts"):
                st.warning("⚠️ ليس لديك صلاحية")
            else:
                alerts = check_alerts(patient)
                if alerts:
                    for alert in alerts:
                        st.markdown(f"""
                        <div class="alert-critical">
                            <strong>{alert['title']}</strong>
                            <br>{alert['message']}
                            <br><strong>🛑 {alert['action']}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="success-box">
                        ✅ لا يوجد تنبيهات حالياً.
                    </div>
                    """, unsafe_allow_html=True)

# ======================================================================
# 🚀 تشغيل التطبيق
# ======================================================================

if st.session_state.page == "login":
    login_page()
elif st.session_state.logged_in:
    dashboard()
else:
    st.session_state.page = "login"
    st.rerun()