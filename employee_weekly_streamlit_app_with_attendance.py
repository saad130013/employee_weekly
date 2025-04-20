
import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام حضور الموظف", layout="wide")
st.title("🔎 نظام البحث عن الموظف")

# تحميل بيانات الموظفين
@st.cache_data
def load_data():
    return pd.read_excel("DUTY_ROSTER_MAR_2025.V.2.xlsx")

df = load_data()

search_type = st.radio("نوع البحث:", ["بالاسم", "برقم الموظف"])
search_value = st.text_input("🧑‍💼 الاسم أو رقم الموظف")

# البحث
if search_value:
    if search_type == "بالاسم":
        result = df[df["Name"].str.contains(search_value, case=False, na=False)]
    else:
        result = df[df["ID"].astype(str).str.contains(search_value, na=False)]

    if not result.empty:
        for _, row in result.iterrows():
            st.markdown("---")
            st.markdown(f"### 🧍‍♂️ {row['Name']} | رقم الموظف: {row['ID']}")
            st.markdown(f"🏢 الوظيفة: {row.get('Position', 'غير محدد')}")
            st.markdown(f"📅 الفترة: {row.get('Shift', 'غير محددة')}")
            
            # جدول الحضور
            attendance = {
                "اليوم": ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"],
                "الحالة": [row.get(day, "غير مسجل") for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]]
            }
            att_df = pd.DataFrame(attendance)
            st.write(att_df)

            # نسبة الحضور
            present_days = sum(1 for v in attendance["الحالة"] if str(v).strip() == "1")
            total_days = len(attendance["الحالة"])
            percent = round((present_days / total_days) * 100, 2)
            st.success(f"✅ نسبة الحضور: %{percent} ({present_days} من {total_days})")
            if percent < 70:
                st.warning("⚠️ ملاحظة: نسبة الحضور منخفضة")
    else:
        st.warning("🚫 لا توجد نتائج مطابقة")
