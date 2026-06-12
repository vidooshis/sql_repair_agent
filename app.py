import streamlit as st

st.set_page_config(
    page_title="Autonomous SQL Repair Agent",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
# 🤖 Autonomous SQL Repair Agent
""")
with st.container(border=True):

    st.markdown("""
### AI-Powered SQL Self-Healing System

This system automatically detects SQL failures,
performs root-cause analysis using DSPy,
generates repairs with Gemini,
validates execution safety,
and learns from historical incidents.
""")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "LLM Engine",
        "Gemini 2.5"
    )

with col2:
    st.metric(
        "Reasoning",
        "DSPy"
    )

with col3:
    st.metric(
        "Database",
        "SQLite"
    )

with col4:
    st.metric(
        "Memory",
        "Incident Cache"
    )


st.divider()

st.subheader("Core Features")

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):
        st.markdown("### 🏗 Dynamic Schema Creation")
        st.caption(
            "Create custom databases directly from the UI."
        )

    with st.container(border=True):
        st.markdown("### 🧠 DSPy RCA")
        st.caption(
            "Analyze SQL failures and identify root causes."
        )

    with st.container(border=True):
        st.markdown("### 🔧 Autonomous Repair")
        st.caption(
            "Generate executable SQL fixes."
        )

with col2:

    with st.container(border=True):
        st.markdown("### 🗂 Incident Memory")
        st.caption(
            "Reuse historical fixes instantly."
        )

    with st.container(border=True):
        st.markdown("### 🛡 Safety Validation")
        st.caption(
            "Risk scoring and approval workflow."
        )

    with st.container(border=True):
        st.markdown("### ⚡ Self-Healing Execution")
        st.caption(
            "Retry repaired queries automatically."
        )
st.divider()

st.subheader("🏛 Architecture")
cols = st.columns(6)

cols[0].success("Query")
cols[1].success("RCA")
cols[2].success("Repair")
cols[3].success("Validate")
cols[4].success("Execute")
cols[5].success("Memory")
st.success(
    "Ready to test autonomous SQL recovery? Build a schema and intentionally break queries to watch the agent self-heal."
)

if st.button(
    "Launch Database Builder",
    use_container_width=True,
):
    st.switch_page(
        "pages/1_Database_Builder.py"
    )