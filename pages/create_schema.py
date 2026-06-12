import streamlit as st
import pandas as pd
from core.db_manager import create_table
from core.db_manager import insert_row
from core.db_manager import fetch_table
import uuid
import os
if "db_path" not in st.session_state:

    os.makedirs(
        "database",
        exist_ok=True
    )

    st.session_state.db_path = (
        f"database/{uuid.uuid4().hex}.db"
    )

if "form_version" not in st.session_state:
    st.session_state.form_version = 0


st.set_page_config(
    page_title="Database Builder"
)

st.title(
    "Database Builder"
)

table_name = st.text_input(
    "Table Name",
    placeholder="e.g. employees"
)

if "columns" not in st.session_state:

    st.session_state.columns = [
        {
            "name": "",
            "type": "TEXT"
        }
    ]

for index, column in enumerate(
    st.session_state.columns
):

    col1, col2 = st.columns(2)

    with col1:

        column["name"] = st.text_input(
            f"Column Name {index}",
            placeholder="e.g. first_name",
            value=column["name"]
        )

    with col2:

        column["type"] = st.selectbox(
            f"Type {index}",
            ["TEXT", "INTEGER", "REAL", "BOOLEAN"],
            key=f"type_{index}"
        )

if st.button(
    "+ Add Column"
):

    st.session_state.columns.append(
        {
            "name": "",
            "type": "TEXT"
        }
    )

    st.rerun()


if st.button("Create Table"):

    if not table_name.strip():

        st.error(
            "Table name is required"
        )

        st.stop()

    for column in st.session_state.columns:

        if not column["name"].strip():

            st.error(
                "Column names cannot be empty"
            )

            st.stop()

    column_names = [
        col["name"].strip()
        for col in st.session_state.columns
    ]

    if len(column_names) != len(set(column_names)):

        st.error(
            "Duplicate column names detected"
        )

        st.stop()

    columns = [
        (col["name"], col["type"])
        for col in st.session_state.columns
    ]

    create_table(
        table_name,
        columns
    )

    st.session_state.active_table = table_name

    st.session_state.active_columns = columns

    st.success(
        f"{table_name} created"
    )

st.subheader("Current Schema")


schema_df = pd.DataFrame(
    st.session_state.columns
)

schema_df.columns = [
    "Column Name",
    "Data Type"
]

st.dataframe(
    schema_df.style.set_properties(
        **{
            "text-align": "center"
        }
    ),
    use_container_width=True,
    hide_index=True
)
if "active_table" in st.session_state:

    st.divider()

    st.subheader("Add Row")


if (
    "active_table" in st.session_state
    and
    "active_columns" in st.session_state
):

    st.divider()

    with st.form(
        f"add_row_form_{st.session_state.form_version}"
    ):

        row_data = {}

        for column_name, datatype in st.session_state.active_columns:

            if datatype == "INTEGER":

                value = st.number_input(
                    column_name,
                    step=1,
                    value=0,
                    key=f"row_{column_name}_{st.session_state.form_version}"
                )

            elif datatype == "REAL":

                value = st.number_input(
                    column_name,
                    value=0.0,
                    key=f"row_{column_name}_{st.session_state.form_version}"
                )

            elif datatype == "BOOLEAN":

                value = st.checkbox(
                    column_name,
                    key=f"row_{column_name}_{st.session_state.form_version}"
                )

            else:

                value = st.text_input(
                    column_name,
                    placeholder="Please enter a value",
                    key=f"row_{column_name}_{st.session_state.form_version}"
                )

            row_data[column_name] = value

        submitted = st.form_submit_button(
            "Add Row"
        )

    if submitted:

        invalid_fields = []

        for key, value in row_data.items():

            if (
                isinstance(value, str)
                and
                value.strip() == ""
            ):
                invalid_fields.append(key)

        if invalid_fields:

            st.error(
                f"Please fill in: {', '.join(invalid_fields)}"
            )

        else:

            insert_row(
                st.session_state.active_table,
                row_data
            )

            st.session_state.form_version += 1

            st.rerun()
if "active_table" in st.session_state:

    st.divider()

    st.subheader("Current Table")
    
    df = fetch_table(
        st.session_state.active_table
    )
    styled_df = (
        df.style
        .set_properties(
            **{
                "text-align": "center"
            }
        )
    )
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()
if st.button(
    "🚀 Let's Start Querying",
    use_container_width=True
):
    st.switch_page(
        "pages/query_assistant.py"
    )

if st.button(
    "🗑 Start New Database",
    use_container_width=True
):

    keys_to_remove = [
        "active_table",
        "active_columns",
        "columns",
        "form_version",
        "db_path"
    ]

    for key in keys_to_remove:

        if key in st.session_state:
            del st.session_state[key]

    st.rerun()