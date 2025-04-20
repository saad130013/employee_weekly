import pandas as pd

def load_excel_data(file_path):
    """قراءة جميع الجداول في ملف الإكسل وتنظيف البيانات"""
    xls = pd.ExcelFile(file_path)
    sheets_data = {}
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=1)
        df = df.dropna(how='all')  # حذف الصفوف الفارغة تماماً
        sheets_data[sheet_name] = df
    
    return sheets_data

def search_employee(sheets_data, search_term):
    """البحث عن الموظف في جميع الجداول"""
    results = []
    
    for sheet_name, df in sheets_data.items():
        # البحث في الأعمدة الرئيسية
        mask = (
            df['NAME (ENG)'].astype(str).str.contains(search_term, case=False, na=False) |
            df['NAME (AR)'].astype(str).str.contains(search_term, case=False, na=False) |
            df['EMP#'].astype(str).str.contains(search_term, na=False)
        )
        
        filtered = df[mask]
        if not filtered.empty:
            results.append({
                "Sheet": sheet_name,
                "Data": filtered.to_dict("records")
            })
    
    return results

def display_results(results):
    """عرض النتائج بطريقة منظمة"""
    if not results:
        print("\n❌ لم يتم العثور على أي نتائج!")
        return
    
    print("\n🔍 نتائج البحث:")
    for idx, result in enumerate(results, 1):
        print(f"\n{'='*40}\nالجدول: {result['Sheet']}\n{'='*40}")
        
        for emp in result['Data']:
            print(f"\nالموظف #{idx}:")
            for key, value in emp.items():
                if pd.notna(value):  # تجاهل القيم الفارغة
                    print(f"- {key}: {value}")
            idx += 1

def main():
    """واجهة المستخدم الرئيسية"""
    file_path = "DUTY ROSTER MAR 2025.V.2.xlsx"
    
    try:
        print("📂 جار تحميل الملف...")
        sheets_data = load_excel_data(file_path)
        print("✅ تم تحميل الملف بنجاح!")
        
        while True:
            search_term = input("\n🔍 أدخل اسم الموظف أو رقم الموظف (أو 'خروج' للإنهاء): ").strip()
            
            if search_term.lower() == 'خروج':
                print("\n🚪 تم إنهاء البرنامج.")
                break
                
            if not search_term:
                print("⚠️ الرجاء إدخال مصطلح بحث!")
                continue
                
            results = search_employee(sheets_data, search_term)
            display_results(results)
            
    except Exception as e:
        print(f"\n❌ حدث خطأ: {str(e)}")

if __name__ == "__main__":
    main()
