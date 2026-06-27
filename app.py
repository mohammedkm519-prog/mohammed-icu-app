import streamlit as st
import google.generativeai as genai
import base64
import re
import json
from PIL import Image

# ======================================================================
# 🔑 مفتاح Gemini API
# ======================================================================

GEMINI_API_KEY = "AQ.Ab8RN6I9tQyt3v3bUCQO67ozRjCYPNpdi4Ars-B5rFpz_fVaSg"
genai.configure(api_key=GEMINI_API_KEY)

# ======================================================================
# 📱 إعدادات الصفحة
# ======================================================================

st.set_page_config(
    page_title="Mohammed ICU - تحليل التحاليل",
    page_icon="🏥",
    layout="wide"
)

# ======================================================================
# 🏠 واجهة التطبيق
# ======================================================================

st.markdown("""
<div style="background: linear-gradient(135deg, #0c2340, #1a5276); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px;">
    <h1 style="font-size: 48px; margin: 0;">🏥 محمد ICU</h1>
    <p style="font-size: 20px; opacity: 0.9;">نظام العناية المركزة الذكي - رفع التحاليل</p>
</div>
""", unsafe_allow_html=True)

# ======================================================================
# 📸 رفع التحاليل
# ======================================================================

st.subheader("📸 رفع صورة التحاليل")

uploaded = st.file_uploader(
    "اختر صورة التحاليل (CBC, ABG, etc.)",
    type=["jpg", "jpeg", "png"],
    key="lab_upload"
)

if uploaded:
    # عرض الصورة
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(uploaded, caption="صورة التحاليل", use_column_width=True)
    
    with col2:
        if st.button("📊 تحليل الصورة بالذكاء الاصطناعي", use_container_width=True, type="primary"):
            with st.spinner("🧠 جاري تحليل الصورة واستخراج البيانات..."):
                try:
                    # تحويل الصورة إلى Base64
                    image_data = base64.b64encode(uploaded.read()).decode('utf-8')
                    
                    # تعليمات Gemini
                    prompt = """
                    أنت خبير في قراءة نتائج المختبرات الطبية من الصور.
                    
                    هذه صورة لورقة تحاليل طبية (CBC - Complete Blood Count).
                    
                    ابحث في الصورة عن هذه القيم الثلاث فقط:
                    
                    1. WBC (خلايا الدم البيضاء) - ابحث عن "White cell count" أو "WBC"
                    2. HB (الهيموغلوبين) - ابحث عن "Haemoglobin" أو "HB" أو "Hemoglobin"
                    3. PLT (الصفائح الدموية) - ابحث عن "Platelets" أو "PLT"
                    
                    أعد النتيجة بهذا الشكل (JSON فقط، لا شيء غيره):
                    {"wbc": 8.6, "hb": 9.8, "plt": 235}
                    
                    إذا لم تجد قيمة، لا تضعها في JSON.
                    تأكد من أن الأرقام دقيقة كما تظهر في الصورة.
                    """
                    
                    # استدعاء Gemini
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([
                        prompt,
                        {"mime_type": "image/jpeg", "data": image_data}
                    ])
                    
                    text = response.text
                    
                    # محاولة استخراج JSON
                    json_match = re.search(r'\{[^{}]*\}', text)
                    if json_match:
                        try:
                            data = json.loads(json_match.group())
                            if data:
                                st.success(f"✅ تم استخراج البيانات بنجاح!")
                                
                                # عرض البيانات في جدول
                                st.markdown("### 📊 البيانات المستخرجة")
                                
                                # تحويل البيانات إلى جدول
                                lab_data = []
                                for key, value in data.items():
                                    lab_data.append({
                                        "الفحص": key.upper(),
                                        "القيمة": value
                                    })
                                
                                df = pd.DataFrame(lab_data)
                                st.dataframe(df, use_container_width=True, hide_index=True)
                                
                                # عرض JSON
                                with st.expander("📄 عرض JSON"):
                                    st.json(data)
                            else:
                                st.warning("⚠️ لم يتم استخراج بيانات من الصورة")
                        except:
                            st.warning("⚠️ لم يتم استخراج بيانات من الصورة")
                    else:
                        st.warning("⚠️ لم يتم استخراج بيانات من الصورة")
                        with st.expander("📄 عرض النص المستخرج"):
                            st.text(text)
                        
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
                    st.info("💡 تأكد من صحة مفتاح Gemini API")

# ======================================================================
# 🦶 تذييل الصفحة
# ======================================================================

st.markdown("""
---
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <p>🏥 محمد ICU - نظام العناية المركزة الذكي</p>
    <p style="font-size: 12px;">تم إنشاء هذا التطبيق باستخدام Streamlit و Gemini AI</p>
</div>
""", unsafe_allow_html=True)