
import streamlit as st
import pandas as pd

st.set_page_config(page_title="جداول المناوبات الأسبوعية", layout="wide")
st.title("📅 نظام تتبع دوام الموظفين الأسبوعي + نسبة الحضور")

EXCEL_PATH = "employee_weekly_schedule_cleaned.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df["Employee No"] = df["Employee No"].astype(str).str.strip()
    df["Name (EN)"] = df["Name (EN)"].astype(str).str.strip()
    return df

df = load_data()

st.sidebar.header("🔎 بحث عن موظف")
search_input = st.sidebar.text_input("الاسم أو رقم الموظف")

results = df.copy()
if search_input:
    results = results[
        results["Employee No"].str.contains(search_input, case=False, na=False) |
        results["Name (EN)"].str.contains(search_input, case=False, na=False)
    ]

st.subheader("📄 نتائج البحث")
if results.empty:
    st.warning("لم يتم العثور على نتائج مطابقة.")
else:
    for i, row in results.iterrows():
        st.markdown(f"### 👤 {row['Name (EN)']} | رقم الموظف: {row['Employee No']}")
        st.write(f"🆔 الهوية: {row['ID']}")
        st.write(f"🧑‍💼 الوظيفة: {row['Position']}")
        st.write(f"🕘 الفترة: {row['Shift']}")

        # احتساب نسبة الحضور
        week_days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        total_days = len(week_days)
        present_days = sum([int(str(row[day]).strip() == "1") for day in week_days])
        attendance_percent = round((present_days / total_days) * 100, 2)

        st.write(f"✅ نسبة الحضور: **{attendance_percent}%** ({present_days} من {total_days})")

        if attendance_percent < 50:
            st.error("🚨 تنبيه: نسبة الحضور أقل من 50٪")
        elif attendance_percent < 80:
            st.warning("⚠️ ملاحظة: نسبة الحضور منخفضة")
        else:
            st.success("👌 الحضور ممتاز")

        # عرض الجدول الأسبوعي
        week = {
            "الأحد": row["SUN"],
            "الإثنين": row["MON"],
            "الثلاثاء": row["TUE"],
            "الأربعاء": row["WED"],
            "الخميس": row["THU"],
            "الجمعة": row["FRI"],
            "السبت": row["SAT"]
        }
        st.table(pd.DataFrame(week.items(), columns=["اليوم", "الحالة"]))
        st.info(f"📌 ملاحظات: {row['Comments'] if pd.notna(row['Comments']) else 'لا توجد'}")
