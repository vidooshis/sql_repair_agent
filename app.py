import streamlit as st

st.set_page_config(
    page_title="Autonomous SQL Repair Agent",
    page_icon="🤖",
    layout="wide"
)

st.title(
    "🤖 Autonomous SQL Repair Agent"
)

st.markdown("""
Build databases dynamically and watch AI automatically
detect, analyze, repair, and execute broken SQL queries.
""")

st.divider()

st.subheader("How It Works")

st.markdown("""
1. Create a custom database schema

2. Insert sample data

3. Run SQL queries

4. Detect execution failures

5. Perform Root Cause Analysis (DSPy)

6. Generate corrected SQL

7. Validate repair safety

8. Retry execution automatically

9. Store successful fixes in incident memory
""")

st.divider()

st.subheader("Core Features")

col1, col2 = st.columns(2)

with col1:

    st.success("Dynamic Schema Creation")

    st.success("DSPy Root Cause Analysis")

    st.success("Autonomous SQL Repair")

with col2:

    st.success("Incident Memory")

    st.success("Safety Validation")

    st.success("Self-Healing Execution")

st.divider()

st.info(
    "Start by creating a database schema and adding sample data."
)

if st.button(
    "🚀 Start Building",
    use_container_width=True
):
    st.switch_page(
        "pages/create_schema.py"
    )