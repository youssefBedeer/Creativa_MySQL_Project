import streamlit as st 
from db_connection import Database 
from commands.factory import CommandFactory
from utils import dynamic_form

# ---------------- جلب أسماء الجداول من قاعدة البيانات ----------------
db = Database(db="company")
db.cursor.execute("SHOW TABLES")
tables = [row[f"Tables_in_{db.database}"] for row in db.cursor.fetchall()]

# اختيار الجدول بشكل ديناميكي
table_name = st.selectbox("اختر الجدول:", tables)

# ---------------- عرض الجدول ----------------
if st.button("📄 عرض الجدول"):
    cmd = CommandFactory.create_command("show_table", table_name, [])
    df = cmd.execute()
    if df.empty:
        st.info("⚠️ الجدول فارغ")
    else:
        st.dataframe(df)

# ---------------- إضافة صف جديد ----------------
# جلب الأعمدة مع معلومات النوع
st.subheader("➕ Add New Row")

data = dynamic_form(f"{table_name}")  # أي جدول

if data and st.button("Add Row"):
    try:
        CommandFactory.create_command("add_row", table_name, data).execute()
        st.success("✅ Added Successfully")
    except Exception as e:
        st.error(f"❌ Error adding row: {e}")



# ---------------- حذف صف ----------------
st.subheader("🗑️ Delete Row WHERE")
delete_column = st.text_input("Column Name")
delete_value = st.text_input("Value")
if st.button("Delete"):
    if delete_column and delete_value:
        cmd = CommandFactory.create_command("delete_row", table_name, delete_column, delete_value)
        cmd.execute()
        st.success(f"✅ Deleted -->{delete_column} = {delete_value}")
    else:
        st.warning("⚠️ Add ")