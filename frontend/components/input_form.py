import streamlit as st
import re

# List of top 20 IT companies
TOP_IT_COMPANIES = [
    "TCS", "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra", 
    "LTI Mindtree", "Mphasis", "Cognizant", "Oracle", "Microsoft",
    "Google", "IBM", "SAP", "Capgemini", "Accenture",
    "Amazon Web Services", "Adobe", "Cisco", "Dell Technologies", "Intel"
]

def validate_company_name(name):
    """Validates that the company name is alphanumeric and starts with a letter."""
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9\s]*$", name))

def input_form():
    """Creates an input form to accept company name from dropdown or search box."""
    st.sidebar.header("News Sentiment Analyzer")

    # Unique key for the dropdown to avoid duplicate ID errors
    selected_company = st.sidebar.selectbox(
        "Select a Company", TOP_IT_COMPANIES, key="company_dropdown_123"
    )

    # User-defined search field
    custom_company = st.sidebar.text_input("Or Type Company Name (Alphanumeric only)", key="custom_company_input_123")

    # Validate user input
    if custom_company:
        if validate_company_name(custom_company):
            company_name = custom_company.strip()
        else:
            st.sidebar.error("Invalid input! Company name must be alphanumeric and start with a letter.")
            return None, False
    else:
        company_name = selected_company  # Use dropdown selection if no custom input

    analyze_button = st.sidebar.button("Analyze Sentiment", key="analyze_button_123")

    return company_name, analyze_button
