import streamlit as st
import pandas as pd

from core.executor import QueryExecutor
from core.schema import get_schema
from core.error_parser import parse_error
from core.validator import QueryValidator

from agents.rca_agent import RCAAgent
from agents.repair_agent import RepairAgent

from memory.memory_manager import (
    find_incident,
    save_incident
)


# --------------------------------------------------
# Guard
# --------------------------------------------------

if "active_table" not in st.session_state:

    st.warning(
        "Please create a table first."
    )

    if st.button(
        "Go To Database Builder"
    ):
        st.switch_page(
            "pages/create_schema.py"
        )

    st.stop()


# --------------------------------------------------
# Page
# --------------------------------------------------

st.title(
    "SQL Repair Assistant"
)

st.subheader(
    "Current Schema"
)

schema = get_schema()

st.json(schema)

query = st.text_area(
    "SQL Query",
    placeholder="""
SELECT name
FROM employees
"""
)


# --------------------------------------------------
# Run Query
# --------------------------------------------------

if st.button(
    "Run Query",
    use_container_width=True
):

    executor = QueryExecutor()

    result = executor.execute(query)

    # ----------------------------------------------
    # SUCCESS
    # ----------------------------------------------

    if result["success"]:

        st.success(
            "Query Executed Successfully"
        )

        df = pd.DataFrame(
            result["result"]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.stop()

    # ----------------------------------------------
    # FAILURE
    # ----------------------------------------------

    with st.expander(
        " Original Error",
        expanded=True
    ):
        st.code(
            result["error"]
        )
    
    parsed_error = parse_error(
        result["error"]
    )

    memory_hit = find_incident(
        parsed_error["type"],
        parsed_error["value"]
    )

    # ==============================================
    # MEMORY RECOVERY
    # ==============================================

    if memory_hit:

        st.success(
            "Recovered Using Historical Incident"
        )

        with st.expander(
            "Historical Repair",
            expanded=True
        ):
            st.code(
                memory_hit["corrected_query"],
                language="sql"
            )

        validation = QueryValidator.validate(
            memory_hit["corrected_query"]
        )
    

        st.info(
            "Confidence: Historical Match"
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            accept_memory = st.button(
                " ✅ Accept Historical Repair",
                use_container_width=True
            )

        with col2:

            reject_memory = st.button(
                " ❌ Reject Historical Repair",
                use_container_width=True
            )

        if reject_memory:

            st.warning(
                "Historical repair rejected."
            )

            st.stop()

        if not accept_memory:

            st.stop()
        
        retry_result = executor.execute(
            memory_hit["corrected_query"]
        )
        if retry_result["success"]:

            st.success(
                "Query Recovered"
            )
            st.success(
                "Repair Approved and Executed"
            )

            df = pd.DataFrame(
                retry_result["result"]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.error(
                "Historical repair failed."
            )

        st.stop()

    # ==============================================
    # RCA
    # ==============================================

    st.warning(
        "No historical repair found."
    )

    rca_agent = RCAAgent()

    rca_response = rca_agent(
        query=query,
        error=result["error"],
        database_schema=schema
    )

    with st.expander(
        "Root Cause Analysis",
        expanded=True
    ):
        st.write(
            rca_response.root_cause
        )

    # ==============================================
    # REPAIR
    # ==============================================

    repair_agent = RepairAgent()

    repair_response = repair_agent(
        query=query,
        root_cause=rca_response.root_cause,
        database_schema=schema
    )


    with st.expander(
        "Suggested Repair",
        expanded=True
    ):
        st.code(
            repair_response.corrected_query,
            language="sql"
        )
    st.subheader(
        "Repair Diff"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**Original Query**")

        st.code(
            query,
            language="sql"
        )

    with col2:

        st.markdown("**Repaired Query**")

        st.code(
            repair_response.corrected_query,
            language="sql"
        )
    # ==============================================
    # VALIDATION
    # ==============================================

    validation = QueryValidator.validate(
        repair_response.corrected_query
    )
    if parsed_error["type"] == "missing_table":

        validation["requires_approval"] = True

        validation["reason"] = (
            "Repair changed referenced table. "
            "Please verify intent."
        )
    confidence_ok = QueryValidator.validate_confidence(
        repair_response.confidence
    )

    if not confidence_ok:

        validation["requires_approval"] = True

        validation["reason"] = (
            "Repair confidence is below threshold."
        )
    st.subheader(
        "🛡 Safety Validation"
    )

    st.info(
        f"Risk Level: {validation['risk_level']}"
    )

    try:

        confidence = round(
            float(repair_response.confidence),
            2
        )

    except:

        confidence = "Unknown"

    st.info(
        f"Confidence: {confidence}"
    )

    if validation.get("reason"):

        st.warning(
            validation["reason"]
        )

    # ==============================================
    # HUMAN APPROVAL
    # ==============================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        accept = st.button(
            "✅ Accept Repair",
            use_container_width=True
        )

    with col2:

        reject = st.button(
            "❌ Reject Repair",
            use_container_width=True
        )

    if reject:

        st.warning(
            "Repair rejected. Please try another query."
        )

        st.stop()

    if not accept:

        st.stop()
        
    # ==============================================
    # RETRY
    # ==============================================

    retry_result = executor.execute(
        repair_response.corrected_query
    )

    if retry_result["success"]:

        save_incident(
            parsed_error["type"],
            parsed_error["value"],
            repair_response.corrected_query
        )

        st.success(
            "Query Recovered"
        )
        st.success(
            "Repair Approved and Executed"
        )

        df = pd.DataFrame(
            retry_result["result"]
        )

        st.dataframe(
            df,
            use_container_width=True
        )
        if st.button(
            "Run Another Query",
            use_container_width=True
        ):

            st.rerun()

    else:

        st.error(
            "Repair failed."
        )

        with st.expander(
            "Retry Error",
            expanded=True
        ):
            st.code(
                retry_result["error"]
            )