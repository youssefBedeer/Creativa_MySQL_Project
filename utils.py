import streamlit as st
from commands.factory import CommandFactory

def dynamic_form(table_name):
    """
    Builds a dynamic Streamlit form for any table.
    Returns a dict with user inputs or None if errors exist.
    """
    try:
        columns_info = CommandFactory.create_command("show_columns", table_name).execute()
    except Exception as e:
        st.error(f"❌ Error fetching columns: {e}")
        return None

    data = {}
    errors = []

    for col in columns_info:
        col_name = col['Field']
        col_type = col['Type']
        is_nullable = col['Null'] == 'YES'
        max_length = None
        if '(' in col_type:
            try:
                max_length = int(col_type.split('(')[1].split(')')[0])
            except:
                pass

        if col_name in ["id", "created_at"]:
            continue

        # اختيار نوع الإدخال
        if "int" in col_type:
            value = st.number_input(f"{col_name}", value=0, step=1)
        elif "decimal" in col_type or "float" in col_type:
            value = st.number_input(f"{col_name}", value=0.0, format="%.2f")
        elif "text" in col_type:
            value = st.text_area(f"{col_name}")
        else:  # varchar or others
            value = st.text_input(f"{col_name}")

        # تحقق من NOT NULL
        if not is_nullable and (value == "" or value is None):
            errors.append(f"{col_name} is required")

        # تحقق من طول النصوص
        if max_length and isinstance(value, str) and len(value) > max_length:
            errors.append(f"{col_name} must be at most {max_length} characters")

        data[col_name] = value

    if errors:
        for err in errors:
            st.warning(f"❌ {err}")
        return None

    return data
