import streamlit as st
import pandas as pd
import openai
import time
from datetime import datetime
from streamlit_option_menu import option_menu
import os
import random

import matplotlib.pyplot as plt
import seaborn as sns


# Add the function here, at the top level of the file
def generate_ai_summary(file, folder, project):
    """Generate realistic AI summaries based on document type and project context"""

    # Term Sheet summary
    if file == "Term Sheet.docx":
        return """### Key Transaction Terms

This Term Sheet outlines preliminary terms and conditions for a proposed €450 million senior secured term loan facility for the acquisition financing of target renewable energy assets across Southern Europe.

**Transaction Parties:**
- **Borrower:** Olympus Renewables Bidco Ltd.
- **Guarantors:** All material subsidiaries (representing at least 80% of group EBITDA)
- **Arrangers:** RMB, Société Générale, Barclays
- **Facility Agent:** RMB

**Key Financial Terms:**
- **Facility Amount:** €450,000,000
- **Tenor:** 5+1+1 years (with extension options)
- **Margin:** E+275bps (subject to leverage ratchet)
- **Upfront Fee:** 125bps
- **Commitment Fee:** 35% of applicable margin on undrawn amounts
- **Financial Covenants:** Leverage ratio ≤4.5x, Interest cover ≥3.0x, DSCR ≥1.2x

**Security Package:**
- First-ranking security over assets and shares of key operating entities
- Assignment of material project documents and receivables
- Pledge over project accounts
"""

    # Credit Approval summary
    elif file == "Credit Approval.pdf":
        return """### Credit Committee Decision Summary

**Application:** New credit application for Project Olympus renewable energy portfolio financing  
**Decision:** Approved with conditions  
**Risk Rating:** BB+ / Acceptable (3.0)  
**LGD:** 30%  
**Committee Date:** March 8, 2023  

**Transaction Overview:**  
The credit application relates to a €450m senior secured term loan to finance the acquisition of operational renewable energy assets in Spain, Portugal and Italy. Assets consist of 12 solar farms and 5 wind farms with an average operational history of 6.4 years.

**Key Strengths:**  
- Strong cash generation with long-term PPAs covering 70% of production  
- Geographical diversification mitigating weather-related production risk  
- Experienced management team with proven track record  
- Favorable regulatory environment for renewable energy in target markets
"""

    # Default summary for other files
    else:
        return f"""### AI Summary of {file}

This document from the {folder} folder in the {project} project appears to be a {file.split('.')[-1].upper()} file.

The document contains important information related to the {project} transaction and should be reviewed in detail by the team.

Key elements likely include financial terms, legal provisions, or analytical data depending on the document type.
"""


# -------------------
# OPENAI SETUP
# -------------------
# If deploying on Streamlit Cloud, store your OpenAI key in the "Secrets" section.
# e.g. st.secrets["OPENAI_API_KEY"] = "sk-xxx"
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# ------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Donna",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add this critical styling fix immediately after:
st.markdown("""
<style>
/* Direct targeting of multiselect element backgrounds */
div.stMultiSelect div[data-baseweb="select"] {
    background-color: white !important;
    border-radius: 8px !important;
    border: 1px solid #ddd !important;
}

/* Force pill-style tags */
div[data-baseweb="tag"] {
    background-color: #f5f5f5 !important;
    color: #333 !important;
    border-radius: 16px !important;
    border: 1px solid #e0e0e0 !important;
    padding: 2px 8px !important;
    margin: 2px 4px 2px 0 !important;
}

/* Force all listbox and option elements to white */
div[role="listbox"],
div[role="option"] {
    background-color: white !important;
    color: #333 !important;
}

/* Fix spacing in containers */
.kb-container, .projects-container {
    padding: 15px !important;
    margin-bottom: 20px !important;
    background-color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Add this at the beginning of app.py where other CSS is defined
st.markdown("""
<style>
/* Clean styling for selection cards */
.card-container {
    background-color: white;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.kb-card {
    border-left: 3px solid #ff4b8b;
}

.projects-card {
    border-left: 3px solid #3f8cff;
}

/* Simple header styling */
.card-header {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 8px;
    color: #333;
}

/* Make sure selection boxes have white backgrounds */
div[data-testid="stMultiSelect"] div,
div[data-baseweb="select"] {
    background-color: white !important;
}

/* Style the tags */
div[data-baseweb="tag"] {
    background-color: #f5f5f5 !important;
    border: 1px solid #e0e0e0 !important;
    color: #333 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- CLEAN CSS WITH PROPER VISIBILITY -----------
custom_css = """
<style>
/* Core styling */
.stApp {
    background-color: white;
}

[data-testid="stSidebar"] {
    background-color: #17191e;
}

/* Special visible button styling - using inline styles */
.main button, .main .stButton > button {
    background-color: #17191e !important;
    color: white !important;
    border: none !important;
    padding: 10px 16px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    border-radius: 4px !important;
    cursor: pointer !important;
    display: inline-block !important;
}

/* Make the button text explicitly visible with !important */
.main button span, .main .stButton > button span {
    color: white !important;
    font-weight: 600 !important;
}

/* Style for button text specifically */
.stButton button > div {
    color: white !important;
    opacity: 1 !important;
}

.stButton button > div > p {
    color: white !important;
    opacity: 1 !important;
}

/* This specifically targets the SVG inside buttons if present */
.stButton button svg {
    fill: white !important;
}

/* Add inline CSS to button text */
.stButton button:before {
    content: "";
    display: inline-block;
}

/* Button text style when hovering */
.stButton button:hover {
    background-color: #2c2e33 !important;
}

.stButton button:hover span {
    color: white !important;
}

/* Simple, elegant Donna logo */
.logo-text {
    color: white !important;
    font-size: 24px !important;
    font-weight: 400 !important;
    padding: 25px 20px !important;
    font-family: serif !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
    margin-bottom: 10px !important;
}

/* Force all text to be black for visibility */
h1, h2, h3, h4, h5, h6, p, span, label, div, .stMarkdown {
    color: black !important;
}

/* Fix sidebar text to be white */
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] span, 
[data-testid="stSidebar"] div, 
[data-testid="stSidebar"] a, 
[data-testid="stSidebar"] label {
    color: white !important;
}

/* Style workflow cards */
.workflow-card {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    background-color: white;
}

.workflow-card h3 {
    color: black !important;
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.workflow-card p {
    color: #4b5563 !important;
    font-size: 14px;
    margin-bottom: 0.5rem;
}

.workflow-meta {
    color: #6b7280 !important;
    font-size: 14px;
    margin-top: 1rem;
}

/* Category pills */
.category-pills {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 2rem;
}

.category-pill {
    background-color: #f3f4f6;
    color: #111827 !important;
    padding: 0.5rem 1.25rem;
    border-radius: 2rem;
    font-size: 14px;
    display: inline-block;
}

.category-pill.active {
    background-color: #17191e;
    color: white !important;
}

/* Fix input fields */
input[type="text"], input[type="number"], textarea {
    background-color: white !important;
    color: black !important;
    border: 1px solid #d1d5db !important;
}

/* Make the number input fields clearly visible */
[data-testid="stNumberInput"] input {
    color: black !important;
    background-color: white !important;
}

/* Ensure stSelectbox text is visible */
[data-testid="stSelectbox"] {
    color: black !important;
}

/* Fix text in file uploader */
[data-testid="stFileUploader"] span {
    color: black !important;
}

/* Results & calculation tables */
.result-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

.result-table th {
    background-color: #f3f4f6;
    padding: 0.5rem 1rem;
    text-align: left;
    font-weight: 500;
    border: 1px solid #e5e7eb;
}

.result-table td {
    padding: 0.5rem 1rem;
    border: 1px solid #e5e7eb;
}

.result-table tr:nth-child(even) {
    background-color: #f9fafb;
}

/* Professional header styling with LARGER TEXT */
.donna-header, .example-header {
    font-size: 20px !important;
    font-weight: 600 !important;
    margin: 5px 0 15px 0 !important;
    padding: 10px 15px !important;
    color: white !important;
    background: linear-gradient(90deg, #222428 0%, #2c2e36 100%) !important;
    border-left: 4px solid #E83E8C !important;
    border-radius: 0 4px 4px 0 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    display: flex !important;
    align-items: center !important;
}

/* Project header styling with different accent color */
.project-header {
    border-left: 4px solid #007BFF !important;
}

/* Example questions header styling with different accent color */
.example-header {
    border-left: 4px solid #FFC107 !important;
}

/* Make emoji in headers larger too */
.donna-header:before, .example-header:before {
    margin-right: 10px !important;
    font-size: 22px !important;
}

/* Subtitle styling */
.donna-subtitle {
    margin-top: -8px !important;
    margin-bottom: 12px !important;
    color: #aaaaaa !important;
    font-size: 13px !important;
    padding-left: 5px !important;
}

/* Sleek Dropdown Styling - matches the image */
[data-baseweb="select"], .stSelectbox > div:first-child {
    background-color: #0D1117 !important;
    border: 1px solid #30B8F4 !important;
    border-radius: 8px !important;
    color: white !important;
    padding: 8px !important;
}

/* Dropdown arrow icon */
[data-baseweb="select"] svg, .stSelectbox svg {
    color: #30B8F4 !important;
    fill: #30B8F4 !important;
    margin-right: 5px !important;
}

/* The dropdown menu items */
[data-baseweb="menu"] {
    background-color: #0D1117 !important;
    border: 1px solid #30B8F4 !important;
    border-radius: 8px !important;
    margin-top: 4px !important;
}

/* Individual dropdown menu items */
[data-baseweb="menu"] div[role="option"] {
    color: white !important;
    padding: 10px 15px !important;
    font-size: 15px !important;
}

/* Hover state for dropdown items */
[data-baseweb="menu"] div[role="option"]:hover {
    background-color: #191F2B !important;
    cursor: pointer !important;
}

/* Selected item in dropdown */
[data-baseweb="menu"] div[aria-selected="true"] {
    background-color: #191F2B !important;
    color: #30B8F4 !important;
}

/* Multi-select dropdown tags */
[data-baseweb="tag"] {
    background-color: #191F2B !important;
    border: none !important;
    border-radius: 4px !important;
    color: white !important;
}

/* Multi-select dropdown tag close button */
[data-baseweb="tag"] span {
    color: #30B8F4 !important;
}

/* Make select box text white */
.stSelectbox label, .stMultiSelect label {
    color: white !important;
}

/* Knowledge Base Section - Pink Accent */
.knowledge-select [data-baseweb="select"], 
.knowledge-select .stSelectbox > div:first-child,
.knowledge-select .stMultiSelect > div:first-child {
    border: 1px solid #E83E8C !important; /* Pink border */
    background-color: rgba(232, 62, 140, 0.05) !important; /* Light pink background */
}

.knowledge-select [data-baseweb="select"] svg,
.knowledge-select .stSelectbox svg,
.knowledge-select .stMultiSelect svg {
    color: #E83E8C !important;
    fill: #E83E8C !important;
}

.knowledge-select [data-baseweb="tag"] {
    background-color: rgba(232, 62, 140, 0.1) !important;
    border: 1px solid rgba(232, 62, 140, 0.3) !important;
}

/* Projects Section - Blue Accent */
.project-select [data-baseweb="select"],
.project-select .stSelectbox > div:first-child,
.project-select .stMultiSelect > div:first-child {
    border: 1px solid #007BFF !important; /* Blue border */
    background-color: rgba(0, 123, 255, 0.05) !important; /* Light blue background */
}

.project-select [data-baseweb="select"] svg,
.project-select .stSelectbox svg,
.project-select .stMultiSelect svg {
    color: #007BFF !important;
    fill: #007BFF !important;
}

.project-select [data-baseweb="tag"] {
    background-color: rgba(0, 123, 255, 0.1) !important;
    border: 1px solid rgba(0, 123, 255, 0.3) !important;
}

/* Example Questions - Yellow Accent */
.example-questions button {
    border-left: 3px solid #FFC107 !important; /* Yellow left border */
    background-color: rgba(255, 193, 7, 0.05) !important; /* Light yellow background */
}

.example-questions button:hover {
    background-color: rgba(255, 193, 7, 0.1) !important;
}

/* Ensure dropdown text is visible on dark backgrounds */
[data-baseweb="menu"] div[role="option"] {
    color: white !important;
    background-color: #17191e !important;
}

[data-baseweb="menu"] div[role="option"]:hover {
    background-color: #2c2e33 !important;
}

/* Fix dropdown styling to match section banners */
/* Knowledge Base - Pink accents */
.stMultiSelect [data-baseweb="select"] {
    background-color: #17191e !important;
    border: 1px solid #E83E8C !important;
    border-radius: 4px !important;
}

/* Dropdown menu */
[data-baseweb="menu"] {
    background-color: #17191e !important;
    color: white !important;
    border: 1px solid #E83E8C !important;
}

/* Menu items */
[data-baseweb="menu"] div[role="option"] {
    background-color: #17191e !important;
    color: white !important;
}

/* Hover state for menu items */
[data-baseweb="menu"] div[role="option"]:hover {
    background-color: #2a2c32 !important;
}

/* Selected items in multiselect */
[data-baseweb="tag"] {
    background-color: #292d33 !important;
    border: none !important;
    color: white !important;
}

/* Tag text */
[data-baseweb="tag"] span {
    color: white !important;
}

/* Close button in tags */
[data-baseweb="tag"] button {
    background-color: transparent !important;
}

/* Close button icon */
[data-baseweb="tag"] button svg {
    fill: #E83E8C !important;
}

/* Differently styled dropdown for Projects section */
.project-select [data-baseweb="select"] {
    border-color: #007BFF !important;
}

.project-select [data-baseweb="menu"] {
    border-color: #007BFF !important;
}

/* Example questions styling */
.example-questions button {
    border-left: 3px solid #FFC107 !important;
}

/* Fix for multiselect dropdown text and highlight colors */
/* Make dropdown text white for readability */
[data-baseweb="select"] span, 
[data-baseweb="menu"] div[role="option"] {
    color: white !important;
}

/* Make selected items in dropdown have pink border and better contrast */
[data-baseweb="tag"] {
    background-color: #292d33 !important;
    border: 1px solid #E83E8C !important;
    color: white !important;
    margin: 2px !important;
}

/* Ensure dropdown menu options are readable with proper contrast */
[data-baseweb="menu"] div[role="option"] {
    background-color: #17191e !important;
    color: white !important;
    padding: 8px 16px !important;
}

/* Hover and selected states for dropdown options */
[data-baseweb="menu"] div[role="option"]:hover,
[data-baseweb="menu"] div[aria-selected="true"] {
    background-color: #292d33 !important;
    border-left: 2px solid #E83E8C !important;
}

/* Fix dropdown placeholder and selected text */
[data-baseweb="select"] [data-testid="stMarkdown"] p {
    color: white !important;
}

/* Dropdown checkmarks should match the accent color */
[data-baseweb="menu"] div[role="option"] svg {
    fill: #E83E8C !important;
}

/* Blue accent for project section */
.project-select [data-baseweb="tag"] {
    border-color: #007BFF !important;
}

.project-select [data-baseweb="menu"] div[role="option"]:hover,
.project-select [data-baseweb="menu"] div[aria-selected="true"] {
    border-left-color: #007BFF !important;
}

.project-select [data-baseweb="menu"] div[role="option"] svg {
    fill: #007BFF !important;
}

/* Fix dropdown text and color issues - simple and clean approach */

/* Make ALL text in dropdowns and menus white */
[data-baseweb="select"] span,
[data-baseweb="select"] div,
[data-baseweb="menu"] div,
[data-baseweb="menu"] span,
[data-baseweb="popover"] div,
[data-baseweb="popover"] span {
    color: white !important;
}

/* Remove any bright rings and use subtle borders */
[data-baseweb="select"], .stSelectbox > div:first-child {
    border: 1px solid #555 !important;
    box-shadow: none !important;
    border-radius: 4px !important;
}

/* Knowledge Base section - subtle pink accent */
.knowledge-select [data-baseweb="select"] {
    border-color: rgba(232, 62, 140, 0.6) !important;
}

/* Projects section - subtle blue accent */
.project-select [data-baseweb="select"] {
    border-color: rgba(0, 123, 255, 0.6) !important;
}

/* Make dropdown menu dark with white text */
[data-baseweb="menu"] {
    background-color: #17191e !important;
    border: 1px solid #555 !important;
}

/* Menu items white text and dark bg */
[data-baseweb="menu"] div[role="option"] {
    background-color: #17191e !important;
    color: white !important;
}

/* Hover state for menu items - subtle highlight */
[data-baseweb="menu"] div[role="option"]:hover {
    background-color: #2a2c32 !important;
}

/* Remove any orange/bright highlighting */
[data-baseweb="select"]:focus-within,
[data-baseweb="select"]:focus,
[data-baseweb="select"]:active {
    outline: none !important;
    box-shadow: none !important;
}

/* Make project tags BLUE (with !important and higher specificity) */
.project-select [data-baseweb="tag"],
div.project-select [data-baseweb="tag"],
.project-select div[data-baseweb="tag"],
div[class*="project-select"] [data-baseweb="tag"],
[class*="project-select"] [data-baseweb="tag"] {
    border: 1px solid #007BFF !important;
    background-color: rgba(0, 123, 255, 0.15) !important;
    color: white !important;
}

/* Override ANY pink coloring for project tags specifically */
.project-select [data-baseweb="tag"] {
    border-color: #007BFF !important;
}

/* Hide "Selected:" text display */
.selected-knowledge, 
.selected-projects,
div.selected-knowledge, 
div.selected-projects {
    display: none !important;
}

/* Improved Assistant Right Sidebar Styling */
/* Create a unified card-like appearance for each section */
.assistant-sidebar-section {
    background-color: #1e2025;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
    border: 1px solid #292d33;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Improve header spacing and visual hierarchy */
.donna-header, .example-header, .knowledge-header, .project-header {
    margin-top: 0 !important;
    margin-bottom: 12px !important;
}

/* Better subtitle styling */
.donna-subtitle {
    margin-bottom: 15px !important;
    opacity: 0.7;
    font-size: 14px !important;
}

/* More space around the multiselect components */
.knowledge-select, .project-select {
    margin-bottom: 12px;
}

/* Nice subtle hover effect for buttons */
.example-questions button:hover {
    transform: translateY(-1px);
    transition: all 0.2s ease;
}

/* Space between items in the example questions */
.example-questions button {
    margin-bottom: 8px !important;
}

/* Remove any unwanted bottom margin from the last button */
.example-questions button:last-child {
    margin-bottom: 0 !important;
}

/* Create visual separation between sections */
.assistant-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(100,100,100,0.1), rgba(100,100,100,0.5), rgba(100,100,100,0.1));
    margin: 20px 0;
    border: none;
}

/* Create a clean white vertical stepper UI exactly like the image */
.stepper-container {
    background-color: white;
    border-radius: 8px;
    padding: 25px 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    position: relative;
    margin: 10px 0 20px 0;
}

/* Vertical line connecting steps */
.stepper-line {
    position: absolute;
    top: 70px;
    bottom: 70px;
    left: 35px;
    width: 2px;
    background-color: #e0e0e0;
    z-index: 1;
}

/* Step indicator dots */
.stepper-dot {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: #a0a0a0;
    display: inline-block;
    margin-right: 15px;
    z-index: 2;
    position: relative;
}

.stepper-dot.active {
    background-color: #3f8cff; /* Blue for active state */
}

/* Step layout and spacing */
.stepper-step {
    margin-bottom: 30px;
    position: relative;
}

.stepper-step:last-child {
    margin-bottom: 0;
}

/* Step content styling */
.stepper-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.stepper-title {
    font-size: 16px;
    font-weight: 600;
    color: #111;
    margin: 0;
}

.stepper-detail {
    margin-left: 35px;
    color: #666;
    font-size: 13px;
    margin-bottom: 6px;
}

.stepper-content {
    margin-left: 35px;
    margin-bottom: 8px;
}

/* White selection dropdowns with proper colors */
.stepper-content .stMultiSelect [data-baseweb="select"] {
    background-color: white !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 4px !important;
    color: #333 !important;
}

/* Selected tags styling - match dark tags in screenshot */
.stepper-content [data-baseweb="tag"] {
    background-color: #1d1d1d !important;
    color: white !important;
    border-radius: 4px !important;
    margin: 2px !important;
    padding: 2px 8px !important;
    font-size: 12px !important;
}

/* Selected tag close button */
.stepper-content [data-baseweb="tag"] button svg {
    fill: white !important;
}

/* Dropdown options styling */
.stepper-content [data-baseweb="menu"],
.stepper-content [data-baseweb="menu"] div[role="option"] {
    background-color: white !important;
    color: #333 !important;
}

/* Remove colored borders */
.stepper-content .knowledge-select [data-baseweb="select"],
.stepper-content .project-select [data-baseweb="select"] {
    border: 1px solid #e0e0e0 !important;
}

/* Fix menu hover state */
.stepper-content [data-baseweb="menu"] div[role="option"]:hover {
    background-color: #f5f5f5 !important;
}

/* Fix menu selected state */
.stepper-content [data-baseweb="menu"] div[aria-selected="true"] {
    background-color: #f0f0f0 !important;
}

/* Clean, simple panel for selections */
.selection-panel {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    margin: 10px 0 20px 0;
}

/* Section headers */
.panel-header {
    font-size: 16px;
    font-weight: 600;
    color: #111;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
}

/* Icons for headers */
.panel-header-icon {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    margin-right: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.panel-header-icon.knowledge {
    background-color: #E83E8C;
}

.panel-header-icon.projects {
    background-color: #3f8cff;
}

/* Clean selection inputs */
.selection-panel [data-baseweb="select"] {
    background-color: white !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 4px !important;
    color: #333 !important;
    margin-bottom: 20px;
}

/* Selected tags styling */
.selection-panel [data-baseweb="tag"] {
    background-color: #1d1d1d !important;
    color: white !important;
    border-radius: 4px !important;
    margin: 2px !important;
    padding: 2px 8px !important;
    font-size: 12px !important;
}

/* Menu styling */
.selection-panel [data-baseweb="menu"],
.selection-panel [data-baseweb="menu"] div[role="option"] {
    background-color: white !important;
    color: #333 !important;
}

.selection-panel [data-baseweb="menu"] div[role="option"]:hover {
    background-color: #f5f5f5 !important;
}

/* View Project Button Styling - white with black text and border */
[data-testid="baseButton-secondary"] {
    background-color: white !important;
    color: black !important;
    border: 1px solid black !important;
    font-weight: 400 !important;
}

/* Ensure the text inside the button is black */
[data-testid="baseButton-secondary"] p {
    color: black !important;
}

/* Hover state */
[data-testid="baseButton-secondary"]:hover {
    background-color: #f5f5f5 !important;
    border-color: #333 !important;
}

/* File actions and AI Summary button */
.file-actions {
    margin-left: 20px;
}

.ai-summary-btn {
    background-color: #f0f0f0;
    color: #333;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 12px;
    cursor: pointer;
}

.ai-summary-btn:hover {
    background-color: #e0e0e0;
}

/* Full-width summary container */
.full-width-summary {
    background-color: white;
    border-left: 4px solid #3f8cff;
    margin: 15px 0 25px 35px;
    padding: 18px 20px;
    border-radius: 6px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    width: 90%;
    max-width: 900px;
    position: relative;
}

/* Add some styling to make headers look good in the summary */
.full-width-summary h3 {
    color: #1e2025 !important;
    font-size: 17px;
    margin: 0 0 15px 0;
    padding: 0;
    font-weight: 600;
}

.full-width-summary h4 {
    color: #333 !important;
    font-size: 15px;
    font-weight: 600;
    margin: 15px 0 8px 0;
}

.full-width-summary p {
    margin: 8px 0;
    line-height: 1.5;
    color: #555 !important;
}

.full-width-summary ul, .full-width-summary ol {
    margin: 12px 0;
    padding-left: 25px;
}

.full-width-summary li {
    margin: 6px 0;
    color: #555 !important;
}

.full-width-summary strong {
    font-weight: 600;
    color: #333 !important;
}

/* Style the AI button to be more compact and sleeker */
div[data-testid="column"] button[key*="ai_"] {
    padding: 4px 8px !important;
    height: 30px !important;
    min-height: 30px !important;
    width: auto !important;
    min-width: 40px !important;
    margin: 0 !important;
    background-color: #3f8cff !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    font-size: 12px !important;
    line-height: 1 !important;
    font-weight: 500 !important;
    /* Remove text transform and letter spacing which might cause wrapping issues */
    text-transform: none !important;
    letter-spacing: normal !important;
    white-space: nowrap !important;
    display: inline-block !important;
}

/* Style the AI button hover state */
div[data-testid="column"] button[key*="ai_"]:hover {
    background-color: #2a75e8 !important;
    transform: translateY(-1px) !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
}

/* Style the AI button to be silver with black text */
div[data-testid="column"] button[key*="ai_"] {
    padding: 4px 10px !important;
    height: auto !important;
    min-height: 28px !important;
    width: auto !important;
    margin: 0 !important;
    background-color: #e0e0e0 !important; /* Light silver/gray */
    color: #333333 !important; /* Dark gray, almost black text */
    border: 1px solid #cccccc !important; /* Subtle border */
    border-radius: 4px !important;
    font-size: 11px !important;
    line-height: 1.2 !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    display: inline-block !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important; /* Subtle shadow */
}

/* Style the AI button hover state */
div[data-testid="column"] button[key*="ai_"]:hover {
    background-color: #d0d0d0 !important; /* Slightly darker on hover */
    transform: translateY(0px) !important;
    transition: all 0.2s ease !important;
    border-color: #bbbbbb !important;
}

/* Styles to fix black div bars in summaries */
.full-width-summary div {
    background-color: transparent !important;
    border: none !important;
}

/* Make the AI Summary button more compact */
div[data-testid="column"] button[key*="ai_"] {
    padding: 3px 8px !important;
    height: auto !important;
    min-height: 26px !important;
    font-size: 11px !important;
    background-color: #e0e0e0 !important;
    color: #333 !important;
    border: 1px solid #ccc !important;
    margin-top: 0 !important;
}

/* Make AI Summary button smaller */
div[data-testid="column"]:nth-child(3) button {
    font-size: 8px !important;
    padding: 1px 3px !important;
    height: 20px !important;
    min-height: 20px !important;
    margin: 0 !important;
}

/* Make AI Summary button much smaller */
div[data-testid="column"]:nth-child(3) button {
    font-size: 8px !important;
    padding: 0 !important;
    height: 16px !important;
    min-height: 16px !important;
    line-height: 0.8 !important;
    width: auto !important;
    background-color: #e0e0e0 !important;
    color: #333 !important;
    border: 1px solid #ccc !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Add these styles to make the Assistant interface more polished
st.markdown('''
<style>
/* Card-like styling for selection panels */
.selection-card {
    background: white;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    border-left: 3px solid #ff4b8b;
}

.selection-card-projects {
    border-left: 3px solid #3f8cff;
}

/* Improved header styling */
.selection-card h4 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 15px;
    font-weight: 600;
    color: #333;
    display: flex;
    align-items: center;
}

.selection-card h4::before {
    content: "";
    display: inline-block;
    width: 8px;
    height: 8px;
    margin-right: 8px;
    border-radius: 50%;
    background-color: #ff4b8b;
}

.selection-card-projects h4::before {
    background-color: #3f8cff;
}

/* Style the multiselect boxes */
.stMultiSelect > div:first-child {
    background-color: white !important;
    border-radius: 4px !important;
    border: 1px solid #ddd !important;
}

/* Remove margin from multiselect container */
.selection-card .stMultiSelect {
    margin-bottom: 10px !important;
}

/* Style the selected items */
.stMultiSelect [data-baseweb="tag"] {
    background-color: #f8f8f8 !important;
    border: 1px solid #eee !important;
}

/* Reduce spacing around the multiselect label */
.stMultiSelect label {
    margin-bottom: 3px !important;
    font-size: 13px !important;
    color: #666 !important;
}

/* Make the selection boxes appear inside the cards with white background */
.selection-card .stMultiSelect,
.selection-card div[data-testid="stMultiSelect"] {
    margin-top: 5px !important;
    width: 100% !important;
}

/* Target the selection box container directly */
.selection-card div[data-baseweb="select"] {
    background-color: white !important;
    border-radius: 4px !important;
    border: 1px solid #ddd !important;
}

/* Fix the dropdown menu */
div[data-baseweb="popover"] div[data-baseweb="menu"] {
    background-color: white !important;
    color: #333 !important;
    border: 1px solid #ddd !important;
    border-radius: 4px !important;
    z-index: 1000 !important;
}

/* Fix the selected items */
.selection-card div[data-baseweb="tag"] {
    background-color: #f0f0f0 !important;
    border: 1px solid #ddd !important;
    color: #333 !important;
}

/* Fix the multiselect text color */
.selection-card .stMultiSelect input,
.selection-card div[data-baseweb="select"] span {
    color: #333 !important;
}

/* Remove extra spacing in the card */
.selection-card > div {
    padding-bottom: 0 !important;
    margin-bottom: 0 !important;
}
</style>
''', unsafe_allow_html=True)

# Completely new CSS approach for fixing the selection boxes
st.markdown('''
<style>
/* Override for Streamlit selectors directly - very aggressive to ensure it works */
.stMultiSelect div,
div[data-testid="stMultiSelect"] div,
div[data-baseweb="select"] div,
div[data-baseweb="popover"] div, 
div[data-baseweb="select"] div[role="listbox"],
div[data-baseweb="select"] div[role="presentation"],
div[data-baseweb="select"] ul,
div[data-baseweb="select"] span {
    background-color: white !important;
    color: #333 !important;
}

/* Make sure the outer container of the multiselect is white */
.stMultiSelect > div:first-child,
div[data-testid="stMultiSelect"] > div:first-child {
    background-color: white !important;
    border: 1px solid #ddd !important;
    border-radius: 4px !important;
}

/* Style the clear button */
div[data-baseweb="select"] svg {
    fill: #666 !important;
}

/* Important: Specifically target the tags/pills inside the multiselect */
div[data-baseweb="tag"] {
    background-color: #f0f0f0 !important;
    border: 1px solid #ddd !important;
    color: #333 !important;
}

/* No background animations on hover */
div[data-baseweb="select"] div:hover,
div[data-baseweb="select"] div:focus,
div[data-baseweb="menu"] div:hover {
    background-color: #f5f5f5 !important;
}

/* The dropdown menu needs to be explicitly white */
div[role="listbox"],
div[data-baseweb="menu"],
div[data-baseweb="popover"] {
    background-color: white !important;
    border: 1px solid #ddd !important;
    color: #333 !important;
}
</style>
''', unsafe_allow_html=True)

# ----------- SESSION STATE INIT -----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "projects" not in st.session_state:
    st.session_state.projects = {}
if "current_project" not in st.session_state:
    st.session_state.current_project = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"
if "current_workflow" not in st.session_state:
    st.session_state.current_workflow = None

# -------------------------------------------
# SIDEBAR
# -------------------------------------------
st.markdown("""
<style>
/* Style for sidebar navigation with icon */
.sidebar-donna {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 5px 0;
}
.sidebar-donna img {
    width: 24px;
    height: 24px;
    border-radius: 50%;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    # Simple text logo
    st.markdown('<div class="logo-text">Donna</div>', unsafe_allow_html=True)

    # Navigation
    selected = option_menu(
        menu_title=None,
        options=["Assistant", "Vault", "Workflows"],
        icons=["chat", "folder", "grid"],
        menu_icon=None,
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "rgba(255, 255, 255, 0.7)", "font-size": "16px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "padding": "0.75rem 1.5rem",
                "color": "rgba(255, 255, 255, 0.8)"
            },
            "nav-link-selected": {
                "background-color": "#2a2c32",
                "color": "white"
            },
        }
    )


# -------------------------------------------
# HELPER FUNCTION TO READ EXCEL/CSV
# -------------------------------------------
def load_data(file):
    """Attempts to read an Excel or CSV file and return a DataFrame. Returns None on error."""
    try:
        if isinstance(file, str):
            # local path
            if file.endswith(".xlsx"):
                return pd.read_excel(file)
            elif file.endswith(".csv"):
                return pd.read_csv(file)
            else:
                return None
        else:
            # user-uploaded file
            if file.name.endswith(".xlsx"):
                return pd.read_excel(file)
            elif file.name.endswith(".csv"):
                return pd.read_csv(file)
            else:
                return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


# -------------------------------------------
# BOND ANALYSIS WORKFLOW
# -------------------------------------------
def show_bond_analysis_workflow():
    """
    Enhanced Bond Data Analysis with interactive controls & multiple tabs:
    1) Nominal Amount (boxplot) by Instrument Status
    2) Count of Issues by Maturity Year
    3) Top 10 Issuers by Nominal Amount
    """
    st.subheader("Bond Data Analysis – Interactive Plots")

    # Default path
    default_file_path = os.path.join("data", "data.xlsx")

    st.write("**Upload a more recent bond dataset** (XLSX or CSV). Otherwise, it loads `data/data.xlsx` by default.")
    user_file = st.file_uploader("Upload your bond data", type=["xlsx", "csv"])

    # Load data
    if user_file:
        df = load_data(user_file)
        if df is not None:
            st.success(f"Using uploaded file: {user_file.name}")
        else:
            st.error("Could not load the uploaded file. Please try again.")
            return
    else:
        if os.path.exists(default_file_path):
            df = load_data(default_file_path)
            st.warning("No file uploaded; using default `data/data.xlsx`.")
        else:
            st.error("No file uploaded, and `data/data.xlsx` not found. Please check your setup.")
            return

    # Validate data
    if df is None or df.empty:
        st.error("No valid bond data loaded. Check your file or default path.")
        return

    st.markdown("### Data Preview (Top 5 Rows)")
    st.dataframe(df.head(), use_container_width=True)
    st.markdown(f"**Total Rows**: {len(df):,}")

    # Basic cleaning / type conversions
    # Possibly filter columns if needed
    if "Issue Date" in df.columns:
        df["Issue Date"] = pd.to_datetime(df["Issue Date"], errors="coerce")
    if "Maturity Date Year" in df.columns:
        df["Maturity Date Year"] = pd.to_numeric(df["Maturity Date Year"], errors="coerce")
    if "Nominal Amount" in df.columns:
        df["Nominal Amount"] = pd.to_numeric(df["Nominal Amount"], errors="coerce")

    # Create 3 separate tabs for the charts
    tabs = st.tabs(["Distribution Plot", "Count by Year", "Top Issuers"])

    # ------------------------------------------
    # TAB 1: Distribution of Nominal Amount
    # ------------------------------------------
    with tabs[0]:
        st.markdown("#### 1) Distribution of Nominal Amount by Instrument Status")
        if not {"Instrument Status", "Nominal Amount"}.issubset(df.columns):
            st.warning("Missing columns 'Instrument Status' or 'Nominal Amount'. Cannot create this plot.")
        else:
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            sns.boxplot(
                x="Instrument Status",
                y="Nominal Amount",
                data=df,
                palette="Set2",
                ax=ax1
            )
            ax1.set_title("Distribution of Nominal Amount by Instrument Status")
            ax1.set_xlabel("Instrument Status")
            ax1.set_ylabel("Nominal Amount")
            plt.xticks(rotation=45)
            st.pyplot(fig1)

    # ------------------------------------------
    # TAB 2: Count of Issues by Maturity Year
    # ------------------------------------------
    with tabs[1]:
        st.markdown("#### 2) Count of Issues by Maturity Year")

        if "Maturity Date Year" not in df.columns:
            st.warning("Missing 'Maturity Date Year' column. Cannot create this plot.")
        else:
            # Let user pick a range or single year
            valid_years = df["Maturity Date Year"].dropna().unique()
            if len(valid_years) == 0:
                st.warning("No valid maturity year data found.")
            else:
                min_year, max_year = int(valid_years.min()), int(valid_years.max())
                selected_year = st.slider(
                    "Select a Maturity Year",
                    min_value=min_year,
                    max_value=max_year,
                    value=min_year
                )
                year_data = df[df["Maturity Date Year"] == selected_year].copy()
                if year_data.empty:
                    st.info(f"No data for year = {selected_year}.")
                else:
                    fig2, ax2 = plt.subplots(figsize=(8, 5))
                    sns.countplot(
                        y="Instrument Status",
                        data=year_data,
                        palette="coolwarm",
                        ax=ax2
                    )
                    ax2.set_title(f"Instrument Status Distribution in {selected_year}")
                    ax2.set_ylabel("Instrument Status")
                    ax2.set_xlabel("Count")
                    st.pyplot(fig2)

    # ------------------------------------------
    # TAB 3: Top Issuers by Nominal Amount
    # ------------------------------------------
    with tabs[2]:
        st.markdown("#### 3) Top Issuers by Nominal Amount")
        if not {"Issuer Name", "Nominal Amount"}.issubset(df.columns):
            st.warning("Missing 'Issuer Name' or 'Nominal Amount'. Cannot create this plot.")
        else:
            max_issuers = 15
            top_n = st.slider("How many top issuers?", 1, max_issuers, 5, step=1)
            grouped = df.groupby("Issuer Name")["Nominal Amount"].sum().nlargest(top_n)
            if grouped.empty:
                st.info("No valid issuer data found.")
            else:
                fig3, ax3 = plt.subplots(figsize=(8, 5))
                grouped.plot(kind="bar", ax=ax3, color="skyblue")
                ax3.set_title(f"Top {top_n} Issuers by Total Nominal Amount")
                ax3.set_xlabel("Issuer Name")
                ax3.set_ylabel("Total Nominal Amount")
                plt.xticks(rotation=60)
                plt.tight_layout()
                st.pyplot(fig3)

    st.success("Interactive Bond Data Analysis complete! Adjust year/issuer/top-n to see different views.")


# -------------------------------------------
# MAIN CONTENT
# -------------------------------------------
if selected == "Assistant":
    # *** Assistant Code ***
    # Add extra styling for dropdowns, etc.
    st.markdown("""
    <style>
    /* Example question styling, fix for dropdown text, etc. */
    div[data-testid="stButton"] > button {
        background-color: #111418 !important;
        color: white !important;
        text-align: center !important;
        padding: 10px !important;
        height: 40px !important;
        margin-top: 8px !important;
        margin-bottom: 0 !important;
        border-radius: 5px !important;
        width: 100% !important;
        font-size: 14px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="menu"] {
        background-color: #1E1E1E !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Layout
    chat_col, options_col = st.columns([2, 1])
    
    with chat_col:
        # Add back the "Chat with the assistant" header with larger font size
        st.markdown("""
        <h1 style="font-size: 36px; margin-bottom: 20px; font-weight: 600;">Chat with the assistant</h1>
        """, unsafe_allow_html=True)
        
        # Display description text
        st.write("This is where you can ask questions based on the knowledge corpus selected on the right. Donna will do her best to answer and provide relevant sources for your queries.")
        
        # Create a container for the chat history first
        chat_container = st.container()
        
        # Create a separate container specifically for the input at the bottom
        input_container = st.container()
        
        # Now handle the input in the bottom container
        with input_container:
            prompt = st.chat_input("Ask your question here...")
            if prompt:
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                with st.spinner("Thinking..."):
                    try:
                        selected_bases = st.session_state.get("selected_knowledge_bases", ["General Knowledge"])
                        selected_projects = st.session_state.get("selected_projects", [])

                        context = f"Using knowledge from: {', '.join(selected_bases)}"
                        if selected_projects:
                            context += f" and projects: {', '.join(selected_projects)}"

                        time.sleep(min(len(prompt) * 0.01, 2))

                        response = openai.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {
                                    "role": "system", 
                                    "content": f"You are Donna, a financial assistant with expertise in banking and finance. {context}"
                                },
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=1200
                        )
                        response_text = response.choices[0].message.content
                    except Exception as e:
                        response_text = (
                            f"I'm having trouble connecting to my knowledge base right now. "
                            f"Error: {str(e)[:100]}... Please try again shortly."
                        )

                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                
                # Force a rerun so the history is shown first, then input
                st.rerun()
        
        # Display the chat history in the upper container
        with chat_container:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                        <div style="background-color: #e6f7ff; padding: 10px 15px; border-radius: 15px 15px 0 15px; max-width: 80%; color: black;">
                            {message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:  # assistant message
                    st.markdown(f"""
                    <div style="display: flex; margin-bottom: 10px;">
                        <div style="background-color: #f0f0f0; padding: 10px 15px; border-radius: 15px 15px 15px 0; max-width: 80%; color: black;">
                            {message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # RESTORE THE RIGHT SIDEBAR WITH OPTIONS
    with options_col:
        # Clean, minimal styling for selection areas
        st.markdown("""
        <style>
        /* Section styling with colored left borders */
        .kb-section {
            padding-left: 12px !important;
            border-left: 3px solid #ff4b8b !important;
            margin-bottom: 24px !important;
        }
        
        .projects-section {
            padding-left: 12px !important;
            border-left: 3px solid #3f8cff !important;
            margin-bottom: 24px !important;
        }
        
        /* Section headers */
        .section-header {
            font-size: 16px !important;
            font-weight: 600 !important;
            color: #333 !important;
            margin-bottom: 12px !important;
        }
        
        /* Clean multiselect styling */
        div[data-baseweb="select"] {
            background-color: white !important;
            border: 1px solid #ddd !important;
            border-radius: 4px !important;
        }
        
        /* Force all multiselect elements to have white backgrounds */
        div[data-testid="stMultiSelect"] div,
        div[data-baseweb="select"] div,
        div[data-baseweb="select"] span,
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] div,
        div[role="listbox"],
        div[role="listbox"] div {
            background-color: white !important;
        }
        
        /* Style the selected tags */
        div[data-baseweb="tag"] {
            background-color: #f5f5f5 !important;
            color: #333 !important;
            border-radius: 16px !important;
            border: 1px solid #e0e0e0 !important;
            padding: 2px 8px !important;
            margin: 2px 4px 2px 0 !important;
        }
        
        /* Clean label styling */
        div[data-testid="stMultiSelect"] label {
            font-size: 13px !important;
            color: #666 !important;
            font-weight: normal !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Knowledge Base section - simple with left border
        st.markdown('<div class="kb-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Knowledge Base</div>', unsafe_allow_html=True)
        
        selected_knowledge = st.multiselect(
            "Select knowledge sources",
            options=["General Knowledge", "Financial Regulations", "Banking Procedures", "Credit Analysis", "Market Data"],
            default=st.session_state.get("selected_knowledge_bases", ["General Knowledge"]),
            key="kb_multiselect"
        )
        st.session_state.selected_knowledge_bases = selected_knowledge if selected_knowledge else ["General Knowledge"]
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Projects section - simple with left border
        st.markdown('<div class="projects-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Projects</div>', unsafe_allow_html=True)
        
        selected_projects = st.multiselect(
            "Select relevant projects",
            options=["Olympus", "Hades", "Athens", "Sparta", "Troy", "Apollo"],
            default=st.session_state.get("selected_projects", ["Athens", "Sparta", "Hades"]),
            key="projects_multiselect"
        )
        st.session_state.selected_projects = selected_projects
        
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Vault":
    st.title("Document Vault")

    # Define project descriptions (would normally come from a database)
    project_descriptions = {
        "Olympus": "Strategic financing for renewable energy portfolio expansion across Europe. Key focus on solar and wind assets.",
        "Hades": "Debt restructuring and refinancing for mining conglomerate facing liquidity challenges.",
        "Athens": "Project finance for infrastructure development including toll roads and municipal facilities.",
        "Sparta": "Leveraged buyout of defense technology firm with multiple tranches of debt.",
        "Troy": "Cross-border acquisition financing with complex FX considerations and regulatory approvals.",
        "Apollo": "Green bond issuance for sustainability-linked projects across multiple jurisdictions."
    }

    # Define mock project dates
    project_dates = {
        "Olympus": "Created: 12 Mar 2023",
        "Hades": "Created: 05 Jun 2023",
        "Athens": "Created: 22 Jan 2023",
        "Sparta": "Created: 14 Apr 2023",
        "Troy": "Created: 30 Sep 2023",
        "Apollo": "Created: 08 Nov 2023"
    }

    # Add CSS for project cards and file explorer
    st.markdown("""
    <style>
    /* Project Card Styling */
    .project-card {
        background-color: #1e2025;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #292d33;
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .project-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border-color: #3f8cff;
    }

    .project-card h3 {
        margin-top: 0;
        color: white !important;
        font-size: 18px;
        font-weight: 500;
    }

    .project-card p {
        color: #a0a0a0 !important;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .project-date {
        color: #777 !important;
        font-size: 12px;
    }

    .project-stats {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
        border-top: 1px solid #333;
        padding-top: 10px;
    }

    .project-stat {
        color: #999 !important;
        font-size: 13px;
    }

    /* File Explorer Styling */
    .file-explorer {
        background-color: #1e2025;
        border-radius: 8px;
        padding: 5px;
        border: 1px solid #292d33;
        margin-top: 20px;
    }

    .file-explorer-header {
        display: flex;
        justify-content: space-between;
        padding: 10px 15px;
        background-color: #292d33;
        border-radius: 6px 6px 0 0;
        margin-bottom: 10px;
    }

    .file-explorer-header h3 {
        margin: 0;
        color: white !important;
        font-size: 16px;
    }

    .folder {
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 4px;
        cursor: pointer;
        display: flex;
        align-items: center;
    }

    .folder:hover {
        background-color: #292d33;
    }

    .folder-icon {
        color: #3f8cff !important;
        margin-right: 10px;
    }

    .file {
        padding: 8px 15px 8px 35px;
        margin: 2px 0;
        border-radius: 4px;
        cursor: pointer;
        display: flex;
        align-items: center;
    }

    .file:hover {
        background-color: #292d33;
    }

    .file-icon {
        margin-right: 10px;
        color: #999 !important;
    }

    .file-date {
        margin-left: auto;
        color: #777 !important;
        font-size: 12px;
    }

    .breadcrumb {
        display: flex;
        align-items: center;
        padding: 5px 15px;
        background-color: #252830;
        border-radius: 4px;
        margin-bottom: 15px;
    }

    .breadcrumb-item {
        color: #999 !important;
        font-size: 14px;
    }

    .breadcrumb-separator {
        margin: 0 8px;
        color: #666 !important;
    }

    .action-bar {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
    }

    .search-box {
        flex-grow: 1;
        background-color: #252830;
        border: 1px solid #333;
        border-radius: 4px;
        padding: 6px 12px;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Add the ability to create new projects
    with st.expander("Create New Project"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_project = st.text_input("Project Name", key="new_project_input")
        with col2:
            st.write("")
            st.write("")
            if st.button("Create Project", use_container_width=True) and new_project:
                if new_project not in st.session_state.projects:
                    st.session_state.projects[new_project] = {
                        "files": [],
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "description": "New project"
                    }
                    st.success(f"Created project: {new_project}")

    # Project View
    if "current_vault_project" not in st.session_state:
        st.session_state.current_vault_project = None

    # If not viewing a specific project, show the project cards
    if not st.session_state.current_vault_project:
        st.subheader("Recent Projects")

        # Get projects from either the hard-coded list or session state
        # For now, we'll use a combination to ensure we have projects to display
        all_projects = list(project_descriptions.keys())
        if st.session_state.projects:
            # Add any projects from session state that aren't in our hard-coded list
            for proj in st.session_state.projects:
                if proj not in all_projects:
                    all_projects.append(proj)

        # Create project cards in a 2-column layout
        for i in range(0, len(all_projects), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(all_projects):
                    proj = all_projects[i + j]
                    with cols[j]:
                        # Get project info - use defaults if not in our dictionaries
                        desc = project_descriptions.get(proj, "Project description not available")
                        date = project_dates.get(proj, "Created: Recently")

                        # Count files and collaborators (mock data)
                        file_count = len(st.session_state.projects.get(proj, {}).get("files", [])) or (
                                proj.startswith("O") and 12 or 8)
                        collab_count = 3 + (hash(proj) % 5)  # Random number of collaborators based on project name

                        # Create clickable card
                        card_html = f"""
                        <div class="project-card" onclick="
                            var elements = window.parent.document.getElementsByTagName('button');
                            for (var i = 0; i < elements.length; i++) {{
                                if (elements[i].innerText.includes('View {proj}')) {{
                                    elements[i].click();
                                    break;
                                }}
                            }}">
                            <h3>{proj}</h3>
                            <p>{desc}</p>
                            <div class="project-date">{date}</div>
                            <div class="project-stats">
                                <div class="project-stat">📄 {file_count} files</div>
                                <div class="project-stat">👥 {collab_count} collaborators</div>
                            </div>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)

                        # Hidden button that JavaScript can click (Streamlit limitation workaround)
                        if st.button(f"View {proj}", key=f"view_{proj}", help="View project details"):
                            st.session_state.current_vault_project = proj
                            st.rerun()

    # Project detail view with SharePoint-like file explorer
    else:
        project = st.session_state.current_vault_project

        # Back button
        col1, col2 = st.columns([1, 6])
        with col1:
            if st.button("← Back to Projects"):
                st.session_state.current_vault_project = None
                st.rerun()

        with col2:
            st.subheader(project)

        desc = project_descriptions.get(project, "Project description not available")
        st.markdown(f"<p style='color:#a0a0a0;margin-bottom:20px;'>{desc}</p>", unsafe_allow_html=True)

        # Action bar
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown("<div class='search-box'>🔍 Search in this project...</div>", unsafe_allow_html=True)
        with col2:
            st.button("New Folder", use_container_width=True)
        with col3:
            upload_btn = st.button("Upload", use_container_width=True, type="primary")

        # Breadcrumb navigation
        st.markdown("""
        <div class="breadcrumb">
            <span class="breadcrumb-item">Home</span>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-item">Vault</span>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-item" style="color:#3f8cff !important;">{0}</span>
        </div>
        """.format(project), unsafe_allow_html=True)

        # File Explorer
        st.markdown("<div class='file-explorer'>", unsafe_allow_html=True)

        # Mock file structure with different folders based on project name
        folders = {
            "Documentation": ["Term Sheet.docx", "Credit Approval.pdf", "Board Presentation.pptx"],
            "Legal": ["Facility Agreement.pdf", "Security Documents.pdf", "Legal Opinion.docx"],
            "Models": ["Financial Model v1.xlsx", "Scenario Analysis.xlsx"],
            "Credit": ["Credit Memo.pdf", "Risk Assessment.docx"]
        }

        # Add some project-specific folders
        if project == "Olympus":
            folders["Renewable Assets"] = ["Wind Portfolio.xlsx", "Solar Valuation.pdf"]
        elif project == "Hades":
            folders["Restructuring"] = ["Debt Schedule.xlsx", "Creditor Presentation.pdf"]
        elif project == "Athens":
            folders["Infrastructure"] = ["Traffic Study.pdf", "Construction Timeline.xlsx"]
        elif project == "Sparta":
            folders["Due Diligence"] = ["Technical DD.pdf", "Commercial DD.pdf"]

        # Show folders
        for folder, files in folders.items():
            st.markdown(f"""
            <div class="folder">
                <span class="folder-icon">📁</span> {folder}
            </div>
            """, unsafe_allow_html=True)

            # Show 2 files per folder as examples
            for i, file in enumerate(files[:2]):
                date = f"{10 + i} {['Jan', 'Feb', 'Mar', 'Apr', 'May'][i % 5]} 2023"
                file_icon = "📄"
                if file.endswith(".xlsx"):
                    file_icon = "📊"
                elif file.endswith(".pdf"):
                    file_icon = "📑"
                elif file.endswith(".pptx"):
                    file_icon = "📽️"

                # Create a unique key for this file
                file_key = f"{folder}_{file}".replace(" ", "_").replace(".", "_")

                # Create a row layout for the file display
                cols = st.columns([12, 3, 5])

                with cols[0]:
                    # File name and icon
                    st.markdown(f"""
                    <div style="display: flex; align-items: center;">
                        <span class="file-icon">{file_icon}</span> 
                        <span>{file}</span>
                    </div>
                    """, unsafe_allow_html=True)

                with cols[1]:
                    # Date
                    st.markdown(f"""
                    <div style="color: #777; font-size: 12px; text-align: right;">
                        {date}
                    </div>
                    """, unsafe_allow_html=True)

                with cols[2]:
                    # AI Summary button
                    ai_button = st.button("AI Summary", key=f"ai_{file_key}",
                                          help="Generate AI summary of this document")

                # Custom state for each file to track if summary is showing
                if f"show_{file_key}" not in st.session_state:
                    st.session_state[f"show_{file_key}"] = False

                # Toggle state when button is clicked
                if ai_button:
                    st.session_state[f"show_{file_key}"] = not st.session_state[f"show_{file_key}"]

                # If state is True, display the summary properly
                if st.session_state[f"show_{file_key}"]:
                    # Get the summary content
                    summary_content = generate_ai_summary(file, folder, project)

                    # Create a container with a unique key for this file
                    with st.container():
                        # Add a unique identifier div
                        st.markdown(f'<div id="summary-{file_key}" class="summary-marker"></div>',
                                    unsafe_allow_html=True)

                        # Display the content
                        st.markdown(summary_content)

                    # Add styling that targets only this specific summary using the unique ID
                    st.markdown(f"""
                    <style>
                    /* Style only the container with this specific file's summary */
                    .element-container:has(#summary-{file_key}) + .element-container {{
                        background-color: white;
                        border-left: 4px solid #3f8cff;
                        margin: 15px 0 25px 35px;
                        padding: 18px 20px;
                        border-radius: 6px;
                        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
                    }}

                    /* Fix any black div bars */
                    .element-container:has(#summary-{file_key}) + .element-container div {{
                        background-color: transparent !important;
                        border: none !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)

        # Close file explorer div
        st.markdown("</div>", unsafe_allow_html=True)

        # Upload new document
        if upload_btn:
            uploaded_file = st.file_uploader("Select files to upload", accept_multiple_files=True,
                                             key="vault_project_upload")
            if uploaded_file:
                for file in uploaded_file:
                    file_details = {
                        "name": file.name,
                        "type": file.type,
                        "size": file.size,
                        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }

                    # Add to session state if project exists there
                    if project in st.session_state.projects:
                        st.session_state.projects[project]["files"].append(file_details)

                    st.success(f"Uploaded: {file.name}")

elif selected == "Workflows":
    st.title("Workflows")
    st.header("Recommended for You")

    col1, col2 = st.columns(2)

    with col1:
        # Loan Agreement Card
        st.markdown("""
        <div class="workflow-card">
            <h3>Loan Agreement Generator</h3>
            <p>Generate a customized loan agreement based on your inputs.</p>
            <div class="workflow-meta">Output • 2 steps</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶ Start Loan Generator", key="start_loan_gen"):
            st.session_state.current_workflow = "loan_generator"

        # Bond Analysis Card
        st.markdown("""
        <div class="workflow-card" style="margin-top: 2rem;">
            <h3>Bond Data Analysis</h3>
            <p>Upload & analyze bond data, focusing on interactive baseline plots.</p>
            <div class="workflow-meta">📊 Data & Charts • interactive steps</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶ Start Bond Analysis", key="start_bond_analysis"):
            st.session_state.current_workflow = "bond_analysis"

    with col2:
        # RCF Calculator Card
        st.markdown("""
        <div class="workflow-card">
            <h3>RCF-CLN Calculator</h3>
            <p>Calculate and analyze Revolving Credit Facility metrics.</p>
            <div class="workflow-meta">🔢 Calculation • 1 step</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶ Start RCF Calculator", key="start_rcf"):
            st.session_state.current_workflow = "rcf_calculator"

    # Display selected workflow with a clear button
    if st.session_state.current_workflow:
        st.markdown("---")
        col_clear, col_space = st.columns([1, 4])
        with col_clear:
            if st.button("← Back to Workflows", key="back_to_workflows"):
                st.session_state.current_workflow = None
                st.rerun()

        # Loan Generator
        if st.session_state.current_workflow == "loan_generator":
            st.subheader("Loan Agreement / Transaction Capture Form")
            
            # Get project names from the session state
            project_names = list(st.session_state.projects.keys()) if hasattr(st.session_state, 'projects') and st.session_state.projects else []
            
            # Add projects if they don't exist in session state
            if not project_names:
                project_names = ["Athens", "Sparta", "Hades", "Olympus", "Troy", "Apollo"]
            
            project_names.insert(0, "None / No Project")
            
            # Define hard-coded project data (that AI would generate in the real implementation)
            project_data = {
                "Athens": {
                    "transaction_name": "Athens Renewable Energy Financing",
                    "borrower": "Athens Green Power Ltd.",
                    "borrower_type": "Corporate",
                    "transaction_type": "Term Loan",
                    "currency": "EUR",
                    "amount": "350,000,000",
                    "term": "7 years",
                    "purpose": "Financing construction of solar power facilities in southern Greece",
                    "facility_agent": "RMB Bank",
                    "security_package": "First ranking security over project assets and shares",
                    "guarantors": "Athens Holdings and all material subsidiaries",
                    "governing_law": "English Law",
                    "interest_rate": "EURIBOR + 2.75%",
                    "interest_period": "3 months",
                    "upfront_fee": "1.25%",
                    "commitment_fee": "35% of applicable margin",
                    "financial_covenants": "Leverage ratio ≤4.0x, Interest cover ≥3.0x",
                },
                "Sparta": {
                    "transaction_name": "Sparta Infrastructure Development",
                    "borrower": "Sparta Holdings S.A.",
                    "borrower_type": "Public Entity",
                    "transaction_type": "Syndicated Loan",
                    "currency": "USD",
                    "amount": "720,000,000",
                    "term": "10 years",
                    "purpose": "Infrastructure development including highways and port facilities",
                    "facility_agent": "GBM International",
                    "security_package": "Government guarantees and project revenue assignment",
                    "guarantors": "Ministry of Finance and Regional Development Authority",
                    "governing_law": "New York Law",
                    "interest_rate": "SOFR + 3.15%",
                    "interest_period": "6 months",
                    "upfront_fee": "1.75%",
                    "commitment_fee": "40% of applicable margin",
                    "financial_covenants": "Debt Service Coverage Ratio ≥1.2x, Loan Life Coverage Ratio ≥1.3x",
                },
                "Hades": {
                    "transaction_name": "Hades Mining Expansion Facility",
                    "borrower": "Hades Natural Resources Corp.",
                    "borrower_type": "Corporate",
                    "transaction_type": "Revolving Credit Facility",
                    "currency": "USD",
                    "amount": "250,000,000",
                    "term": "5 years",
                    "purpose": "Expansion of copper and rare earth mining operations",
                    "facility_agent": "First Merchant Bank",
                    "security_package": "Mining concessions and fixed assets",
                    "guarantors": "Parent company and operating subsidiaries",
                    "governing_law": "English Law",
                    "interest_rate": "SOFR + 3.50%",
                    "interest_period": "1 month",
                    "upfront_fee": "1.50%",
                    "commitment_fee": "35% of applicable margin",
                    "financial_covenants": "Net Debt/EBITDA ≤3.5x, Interest Cover ≥2.5x",
                },
                "Troy": {
                    "transaction_name": "Troy Maritime Development", 
                    "borrower": "Troy Port Authority",
                    "borrower_type": "Public-Private Partnership",
                    "transaction_type": "Project Finance",
                    "currency": "USD",
                    "amount": "825,000,000",
                    "term": "15 years",
                    "purpose": "Development of deep-water port facilities and logistics hub",
                    "facility_agent": "Maritime Finance Partners",
                    "security_package": "Port assets, concession rights, and revenue accounts",
                    "guarantors": "Troy Development Corp. and Regional Government",
                    "governing_law": "English Law",
                    "interest_rate": "SOFR + 2.95%",
                    "interest_period": "6 months",
                    "upfront_fee": "2.00%",
                    "commitment_fee": "40% of applicable margin",
                    "financial_covenants": "DSCR ≥1.35x, Loan Life Coverage Ratio ≥1.4x",
                },
                "Apollo": {
                    "transaction_name": "Apollo Healthcare Expansion",
                    "borrower": "Apollo Healthcare Group",
                    "borrower_type": "Corporate",
                    "transaction_type": "Term Loan & RCF",
                    "currency": "EUR",
                    "amount": "280,000,000",
                    "term": "7 years",
                    "purpose": "Hospital network expansion and medical technology upgrades",
                    "facility_agent": "Healthcare Finance SA",
                    "security_package": "Healthcare assets, real estate, and receivables",
                    "guarantors": "Parent entity and operating subsidiaries",
                    "governing_law": "German Law",
                    "interest_rate": "EURIBOR + 2.45%",
                    "interest_period": "3 months",
                    "upfront_fee": "1.35%",
                    "commitment_fee": "30% of applicable margin",
                    "financial_covenants": "Leverage ratio ≤3.75x, Interest cover ≥3.25x",
                },
            }
            
            # Project selection with auto-populate functionality (outside form)
            selected_project = st.selectbox("Select a Project", project_names, index=0)
            
            # Information message and auto-populate button (outside form)
            if selected_project != "None / No Project":
                st.info(f"Using project: {selected_project}")
                auto_populate = st.checkbox("Auto-populate form based on project data", value=True)
            else:
                auto_populate = False
            
            # Get values for pre-population (outside form)
            project_values = project_data.get(selected_project, {}) if auto_populate else {}
            
            # Create the form - all fields must be inside this block
            form_submitted = False
            with st.form("loan_form", clear_on_submit=False):
                # Basic Transaction Information
                st.subheader("1. Basic Transaction Information")
                cols = st.columns(2)
                
                with cols[0]:
                    tx_id = st.text_input("Transaction ID", value="TX-" + datetime.now().strftime("%y%m%d-") + str(random.randint(1000, 9999)))
                    tx_name = st.text_input("Transaction Name", value=project_values.get("transaction_name", ""))
                    borrower = st.text_input("Borrower", value=project_values.get("borrower", ""))
                    borrower_type = st.selectbox("Borrower Type", 
                                     ["Corporate", "SPV", "Public Entity", "Public-Private Partnership", "Individual", "Other"],
                                     index=["Corporate", "SPV", "Public Entity", "Public-Private Partnership", "Individual", "Other"].index(project_values.get("borrower_type", "Corporate")) if project_values.get("borrower_type") in ["Corporate", "SPV", "Public Entity", "Public-Private Partnership", "Individual", "Other"] else 0)
                
                with cols[1]:
                    tx_type = st.selectbox("Transaction Type", 
                                 ["Term Loan", "Revolving Credit Facility", "Syndicated Loan", "Project Finance", "Acquisition Financing", "Bridge Loan", "Other"],
                                 index=["Term Loan", "Revolving Credit Facility", "Syndicated Loan", "Project Finance", "Acquisition Financing", "Bridge Loan", "Other"].index(project_values.get("transaction_type", "Term Loan")) if project_values.get("transaction_type") in ["Term Loan", "Revolving Credit Facility", "Syndicated Loan", "Project Finance", "Acquisition Financing", "Bridge Loan", "Other"] else 0)
                    currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "CHF", "ZAR", "Other"],
                                 index=["USD", "EUR", "GBP", "JPY", "CHF", "ZAR", "Other"].index(project_values.get("currency", "USD")) if project_values.get("currency") in ["USD", "EUR", "GBP", "JPY", "CHF", "ZAR", "Other"] else 0)
                    amount = st.text_input("Amount", value=project_values.get("amount", ""))
                    term = st.text_input("Term", value=project_values.get("term", ""))
                
                purpose = st.text_area("Purpose", value=project_values.get("purpose", ""), height=100)
                
                # Key Parties
                st.subheader("2. Key Parties")
                cols = st.columns(2)
                with cols[0]:
                    facility_agent = st.text_input("Facility Agent", value=project_values.get("facility_agent", ""))
                with cols[1]:
                    security_package = st.text_area("Security Package", value=project_values.get("security_package", ""), height=100)
                
                guarantors = st.text_area("Guarantors", value=project_values.get("guarantors", ""), height=100)
                governing_law = st.text_input("Governing Law", value=project_values.get("governing_law", ""))
                
                # Financial Terms
                st.subheader("3. Financial Terms")
                cols = st.columns(2)
                with cols[0]:
                    interest_rate = st.text_input("Interest Rate", value=project_values.get("interest_rate", ""))
                    interest_period = st.text_input("Interest Period", value=project_values.get("interest_period", ""))
                with cols[1]:
                    upfront_fee = st.text_input("Upfront Fee", value=project_values.get("upfront_fee", ""))
                    commitment_fee = st.text_input("Commitment Fee", value=project_values.get("commitment_fee", ""))
                
                financial_covenants = st.text_area("Financial Covenants", value=project_values.get("financial_covenants", ""), height=100)
                
                # Add these missing form fields above the submit button in the form

                # Add a new section for status and classification before the submit button
                st.subheader("4. Status and Classification")
                cols = st.columns(2)
                with cols[0]:
                    form_capturer = st.text_input("Who captured the form?", value=project_values.get("form_captured_by", ""))
                    rating_lgd = st.text_input("Rating and LGD", value=project_values.get("rating_lgd", ""))
                    dealmakers = st.text_input("Name of Dealmakers responsible", value=project_values.get("dealmakers", ""))
                
                with cols[1]:
                    is_distressed = st.selectbox("Is the loan currently in distress?", ["No", "Yes", "Watch List"], 
                              index=["No", "Yes", "Watch List"].index(project_values.get("is_distressed", "No")) if project_values.get("is_distressed") in ["No", "Yes", "Watch List"] else 0)
                    in_apm_portfolio = st.selectbox("Is the loan in the APM portfolio?", ["Yes", "No"], 
                                 index=["Yes", "No"].index(project_values.get("in_apm_portfolio", "Yes")) if project_values.get("in_apm_portfolio") in ["Yes", "No"] else 0)
                    selldown_reasons = st.text_input("Reasons for distribution/sell-down", value=project_values.get("selldown_reasons", ""))
                    business_unit = st.selectbox("Which Business Unit originated the loan?", 
                              ["DFS", "REIB", "Infrastructure", "Resources", "LevFin", "FOGS", "Principal Investments"],
                              index=["DFS", "REIB", "Infrastructure", "Resources", "LevFin", "FOGS", "Principal Investments"].index(project_values.get("business_unit", "Infrastructure")) if project_values.get("business_unit") in ["DFS", "REIB", "Infrastructure", "Resources", "LevFin", "FOGS", "Principal Investments"] else 0)
                    tx_mgmt_team = st.text_input("Which Transaction Management Team?", value=project_values.get("transaction_management_team", ""))
                    initial_lender = st.text_input("Name of Initial Lender", value=project_values.get("initial_lender", ""))

                # Replace the current styling block with this enhanced version

                # Add custom styling for the submit button with stronger selectors
                st.markdown("""
                <style>
                /* More specific selectors to target the form submit button */
                button[kind="formSubmit"],
                button[data-testid="stFormSubmitButton"],
                div[data-testid="stForm"] button,
                .stButton button[kind="formSubmit"] {
                    background-color: #000000 !important;
                    color: #ffffff !important;
                    font-weight: 800 !important;  /* Extra bold */
                    border: none !important;
                    padding: 10px 20px !important;
                    border-radius: 5px !important;
                    cursor: pointer !important;
                    width: 100% !important;
                    margin-top: 20px !important;
                    height: 46px !important;
                    font-size: 18px !important;  /* Larger font */
                    text-transform: uppercase !important;
                    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1) !important;
                    transition: all 0.3s ease !important;
                    letter-spacing: 1px !important;  /* Spacing between letters */
                    text-shadow: 0px 1px 2px rgba(0,0,0,0.3) !important;  /* Text shadow */
                }

                /* Enhanced text visibility for the button text */
                div[data-testid="stForm"] button span,
                button[kind="formSubmit"] span,
                button[data-testid="stFormSubmitButton"] span {
                    color: #ffffff !important;
                    font-weight: 800 !important;
                    text-shadow: 0px 1px 2px rgba(0,0,0,0.3) !important;
                }

                /* Hover state with even more contrast */
                button[kind="formSubmit"]:hover,
                button[data-testid="stFormSubmitButton"]:hover,
                div[data-testid="stForm"] button:hover,
                .stButton button[kind="formSubmit"]:hover {
                    background-color: #222222 !important;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2) !important;
                    color: #ffffff !important;
                    text-shadow: 0px 2px 3px rgba(0,0,0,0.4) !important;
                }

                /* Ensure no other styles interfere with our button */
                div.stButton > button[kind="formSubmit"],
                div.stButton > button[kind="formSubmit"] span {
                    background-color: #000000 !important;
                    color: #ffffff !important;
                }
                </style>
                """, unsafe_allow_html=True)

                # Submit button - MUST be inside the form
                form_submitted = st.form_submit_button("Generate Agreement Summary")
            
            # Handle form submission outside the form
            if form_submitted:
                # Generate the summary based on form inputs
                summary = f"""# LOAN AGREEMENT SUMMARY

## TRANSACTION DETAILS
* **Transaction ID:** {tx_id}
* **Transaction Name:** {tx_name}
* **Borrower:** {borrower}
* **Borrower Type:** {borrower_type}
* **Transaction Type:** {tx_type}
* **Currency:** {currency}
* **Amount:** {amount}
* **Term:** {term}
* **Purpose:** {purpose}

## PARTIES & LEGAL
* **Facility Agent:** {facility_agent}
* **Guarantors:** {guarantors}
* **Security Package:** {security_package}
* **Governing Law:** {governing_law}

## FINANCIAL TERMS
* **Interest Rate:** {interest_rate}
* **Interest Period:** {interest_period}
* **Upfront Fee:** {upfront_fee}
* **Commitment Fee:** {commitment_fee}
* **Financial Covenants:** {financial_covenants}

## PROJECT REFERENCE
Project: {selected_project if selected_project != "None / No Project" else "No project assigned"}
Document generated: {datetime.now().strftime('%d %B %Y, %H:%M')}
Status: {is_distressed}
APM Portfolio: {in_apm_portfolio}
Selldown Reasons: {selldown_reasons}
"""

                st.success("Agreement summary generated successfully!")
                st.markdown(summary)

                # Add download button
                st.download_button(
                    "Download Summary",
                    data=summary,
                    file_name=f"Loan_Agreement_Summary_{tx_name.replace(' ', '_') if tx_name else 'Unnamed'}.md",
                    mime="text/markdown"
                )

                # Save to project if applicable
                if selected_project != "None / No Project":
                    if "projects" not in st.session_state:
                        st.session_state.projects = {}
                    if selected_project not in st.session_state.projects:
                        st.session_state.projects[selected_project] = {}
                    if "loan_summaries" not in st.session_state.projects[selected_project]:
                        st.session_state.projects[selected_project]["loan_summaries"] = []
                    
                    st.session_state.projects[selected_project]["loan_summaries"].append({
                        "name": tx_name,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "content": summary,
                        "dealmakers": dealmakers,
                        "amount": project_values.get("amount", ""),
                        "currency": currency,
                        "business_unit": business_unit,
                        "is_distressed": is_distressed,
                    })
                    st.info(f"This summary has been saved to project: {selected_project}")
                    
                    # Add a view details button for the newly created summary
                    if st.button("View Saved Summary Details"):
                        st.subheader(f"Project: {selected_project} - Summary Details")
                        
                        # Get the latest summary
                        latest_summary = st.session_state.projects[selected_project]["loan_summaries"][-1]
                        
                        # Display key details
                        st.markdown(f"**Transaction Name:** {latest_summary['name']}")
                        st.markdown(f"**Created:** {latest_summary['date']}")
                        st.markdown(f"**Dealmakers:** {latest_summary['dealmakers']}")
                        st.markdown(f"**Amount:** {latest_summary['currency']} {latest_summary['amount']}")
                        st.markdown(f"**Business Unit:** {latest_summary['business_unit']}")
                        st.markdown(f"**Status:** {latest_summary['is_distressed']}")
                        
                        # Collapsible for full content
                        with st.expander("View Full Summary"):
                            st.markdown(latest_summary["content"])

        # Bond Analysis - THIS WAS MISSING
        elif st.session_state.current_workflow == "bond_analysis":
            show_bond_analysis_workflow()

        # RCF Calculator
        elif st.session_state.current_workflow == "rcf_calculator":
            st.subheader("RCF-CLN Calculator")

            company = st.text_input("Company Name", value="Zeus Holdings")
            facility_size = st.number_input("Facility Size (ZAR)", min_value=1000000.0, value=2000000000.0,
                                            format="%0.2f")
            drawn_pct = st.slider("Drawn Percentage", 0.0, 1.0, 0.35, 0.05)

            drawn = facility_size * drawn_pct
            undrawn = facility_size - drawn

            st.markdown(f"**Drawn: ZAR {drawn:,.2f}**")
            st.markdown(f"**Undrawn: ZAR {undrawn:,.2f}**")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Drawn Portion")
                margin_bps = st.number_input("Margin (bps)", value=250)
                funding_bps = st.number_input("Funding (bps)", value=-114)

            with col2:
                st.subheader("Undrawn Portion")
                commitment_fee = st.number_input("Commitment Fee (bps)", value=75)
                commitment_fee_funding = st.number_input("Commitment Fee Funding (bps)", value=-13)

            col1, col2 = st.columns(2)
            with col1:
                credit_bps = st.number_input("Credit (bps)", value=-29)
                capital_bps = st.number_input("Capital (bps)", value=-115)
            with col2:
                commitment_fee_credit = st.number_input("Commitment Fee Credit (bps)", value=-12)
                commitment_fee_capital = st.number_input("Commitment Fee Capital (bps)", value=-50)

            include_cln = st.checkbox("Include CLN")
            if include_cln:
                cln_size = st.number_input("CLN Size (ZAR)", min_value=0.0, value=300000000.0, format="%0.2f")
                cln_cost_bps = st.number_input("CLN Cost (bps)", value=-70)
                cln_percentage = cln_size / facility_size
            else:
                cln_size = 0.0
                cln_cost_bps = 0
                cln_percentage = 0

            if st.button("Calculate", key="calculate_rcf"):
                margin_zar = drawn * (margin_bps / 10000)
                funding_zar = drawn * (funding_bps / 10000)
                credit_zar = drawn * (credit_bps / 10000)
                capital_zar = drawn * (capital_bps / 10000)

                total_cost_bps = funding_bps + credit_bps + capital_bps
                total_cost_zar = funding_zar + credit_zar + capital_zar

                net_spread_zar = margin_zar + total_cost_zar
                net_spread_bps = margin_bps + total_cost_bps

                commitment_fee_zar = undrawn * (commitment_fee / 10000)
                comm_fee_funding_zar = undrawn * (commitment_fee_funding / 10000)
                comm_fee_credit_zar = undrawn * (commitment_fee_credit / 10000)
                comm_fee_capital_zar = undrawn * (commitment_fee_capital / 10000)

                net_commit_bps = commitment_fee + commitment_fee_funding + commitment_fee_credit + commitment_fee_capital
                net_commit_fees_zar = commitment_fee_zar + comm_fee_funding_zar + comm_fee_credit_zar + comm_fee_capital_zar

                blended_margin_zar = margin_zar + commitment_fee_zar
                blended_funding_zar = funding_zar + comm_fee_funding_zar
                blended_credit_zar = credit_zar + comm_fee_credit_zar
                blended_capital_zar = capital_zar + comm_fee_capital_zar

                if include_cln:
                    cln_cost_zar = cln_size * (cln_cost_bps / 10000)
                    adjusted_credit_zar = credit_zar * (1 - cln_percentage)
                    adjusted_capital_zar = capital_zar * (1 - cln_percentage)
                    total_with_cln_zar = blended_margin_zar + blended_funding_zar + cln_cost_zar + adjusted_credit_zar + adjusted_capital_zar

                    st.subheader("CLN Impact")
                    cln_results = pd.DataFrame({
                        "Item": ["CLN Size", "CLN Cost", "Adjusted Credit", "Adjusted Capital", "Total with CLN"],
                        "Amount (ZAR)": [cln_size, cln_cost_zar, adjusted_credit_zar, adjusted_capital_zar,
                                         total_with_cln_zar]
                    })
                    st.dataframe(cln_results.style.format({"Amount (ZAR)": "{:,.2f}"}))

                total_income = net_spread_zar + net_commit_fees_zar
                if include_cln:
                    total_income += cln_cost_zar
                    total_income += (adjusted_credit_zar - credit_zar)
                    total_income += (adjusted_capital_zar - capital_zar)

                st.success("Calculation complete!")
                st.subheader(f"Results for {company}")

                results = pd.DataFrame({
                    "Category": [
                        "Drawn Margin", "Funding Cost", "Credit Cost", "Capital Cost", "Net Spread (Drawn)",
                        "Commitment Fee", "CF Funding", "CF Credit", "CF Capital", "Net Spread (Undrawn)",
                        "Total Income"
                    ],
                    "Amount (ZAR)": [
                        margin_zar, funding_zar, credit_zar, capital_zar, net_spread_zar,
                        commitment_fee_zar, comm_fee_funding_zar, comm_fee_credit_zar,
                        comm_fee_capital_zar, net_commit_fees_zar, total_income
                    ]
                })
                st.dataframe(results.style.format({"Amount (ZAR)": "{:,.2f}"}))

                st.markdown(f"""
                ### Summary
                - **Total Facility**: ZAR {facility_size:,.2f}
                - **Drawn**: ZAR {drawn:,.2f} ({drawn_pct:.0%})
                - **Undrawn**: ZAR {undrawn:,.2f} ({1 - drawn_pct:.0%})
                - **Total Income**: ZAR {total_income:,.2f}
                """)

                if include_cln:
                    st.markdown(f"**CLN Impact**: Using ZAR {cln_size:,.2f} ({cln_percentage:.0%} of facility)")
                    if adjusted_capital_zar != 0:
                        roc = (margin_zar + funding_zar + cln_cost_zar + adjusted_credit_zar) / (
                            -adjusted_capital_zar) * 100
                        st.markdown(f"**Return on Capital**: {roc:.2f}%")

# At the top of your file, add this CSS reset for the multiselect elements
st.markdown("""
<style>
/* Reset for multiselect components - extremely aggressive targeting */
div[data-testid="stMultiSelect"],
div[data-testid="stMultiSelect"] *,
div[data-baseweb="select"],
div[data-baseweb="select"] *,
div[role="listbox"],
div[role="listbox"] *,
div[data-baseweb="popover"],
div[data-baseweb="popover"] * {
    background-color: white !important;
    color: #333 !important;
}

/* Force the dropdown items to have white background */
div[data-baseweb="popover"] div[role="option"] {
    background-color: white !important;
}

/* Force the dropdown items to have proper hover effect */
div[data-baseweb="popover"] div[role="option"]:hover {
    background-color: #f0f0f0 !important;
}

/* Style the selected tags */
div[data-baseweb="tag"] {
    background-color: #f5f5f5 !important;
    border: 1px solid #ddd !important;
}

/* Override Streamlit's dark mode style specifically for these elements */
[data-testid="stAppViewContainer"] [data-testid="stMultiSelect"] div {
    background-color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Add this CSS to create polished selection boxes for the Assistant tab
st.markdown("""
<style>
/* Primary container styling */
.selection-container {
    background-color: white;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.kb-border {
    border-left: 3px solid #ff4b8b;
}

.projects-border {
    border-left: 3px solid #3f8cff;
}

/* Header styling */
.selection-header {
    font-size: 15px;
    font-weight: 600;
    color: #333;
    margin-bottom: 12px;
}

/* Refined multiselect styling */
div[data-baseweb="select"] {
    background-color: white !important;
    border: 1px solid #e6e6e6 !important;
    border-radius: 6px !important;
}

/* Pill-style chips for selected items */
div[data-baseweb="tag"] {
    background-color: #f5f5f5 !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 12px !important;
    margin: 2px 4px 2px 0 !important;
    padding: 2px 8px !important;
}

/* Icon styling in chips */
div[data-baseweb="tag"] svg {
    color: #888 !important;
    height: 14px !important;
    width: 14px !important;
}

/* Hover effects */
div[data-baseweb="tag"]:hover {
    background-color: #eaeaea !important;
    border-color: #d0d0d0 !important;
}

/* Dropdown menu styling */
div[role="listbox"] {
    border-radius: 6px !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.12) !important;
    border: 1px solid #e0e0e0 !important;
}

/* Option items in dropdown */
div[role="option"] {
    padding: 8px 12px !important;
    font-size: 14px !important;
}

div[role="option"]:hover {
    background-color: #f5f5f5 !important;
}

/* Label text */
.stMultiSelect label {
    font-size: 13px !important;
    color: #666 !important;
    margin-bottom: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# Add this CSS at the end of your file to create more polished selection pills and dropdowns
st.markdown("""
<style>
/* Refined container styling */
.kb-container, .projects-container {
    background-color: white;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

/* Polished multiselect container */
div[data-baseweb="select"] {
    background-color: #f9f9f9 !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="select"]:hover {
    border-color: #ccc !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
}

/* Beautiful pill-style chips for selected items */
div[data-baseweb="tag"] {
    background-color: white !important;
    border: 1px solid #e6e6e6 !important;
    border-radius: 16px !important; /* More rounded pills */
    margin: 3px 5px 3px 0 !important;
    padding: 3px 10px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    transition: all 0.15s ease !important;
}

/* Improved hover effects on pills */
div[data-baseweb="tag"]:hover {
    background-color: #f0f0f0 !important;
    border-color: #ccc !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}

/* Cleaner X icon in pills */
div[data-baseweb="tag"] svg {
    color: #999 !important;
    height: 12px !important;
    width: 12px !important;
    margin-left: 4px !important;
    transition: all 0.15s ease !important;
}

div[data-baseweb="tag"] svg:hover {
    color: #555 !important;
}

/* More polished dropdown menu */
div[role="listbox"] {
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    border: 1px solid #ddd !important;
    padding: 4px !important;
}

/* Nicer option items in dropdown */
div[role="option"] {
    border-radius: 6px !important;
    padding: 8px 12px !important;
    margin: 2px 0 !important;
    transition: background-color 0.15s ease !important;
}

div[role="option"]:hover {
    background-color: #f0f6ff !important;
}

/* Improved label text */
.stMultiSelect label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #555 !important;
    margin-bottom: 5px !important;
    letter-spacing: 0.01em !important;
}

/* Dropdown arrow */
div[data-baseweb="select"] [role="button"] svg {
    color: #888 !important;
    transition: transform 0.2s ease !important;
}

div[data-baseweb="select"]:hover [role="button"] svg {
    color: #555 !important;
}
</style>
""", unsafe_allow_html=True)

# Replace the existing multiselect styling CSS block with this improved version
st.markdown('''
<style>
/* Base styling for multiselect components */
div[data-testid="stMultiSelect"] div,
div[data-baseweb="select"] div,
div[data-baseweb="select"] span {
    background-color: white !important;
    color: #333 !important;
}

/* Selection box container */
div[data-baseweb="select"] {
    background-color: #f9f9f9 !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="select"]:hover {
    border-color: #ccc !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
}

/* Pill-style tags for selected items */
div[data-baseweb="tag"] {
    background-color: white !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 16px !important;
    margin: 3px 5px 3px 0 !important;
    padding: 3px 10px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    transition: all 0.15s ease !important;
}

/* Hover effects for pills */
div[data-baseweb="tag"]:hover {
    background-color: #f0f0f0 !important;
    border-color: #ccc !important;
}

/* Improved X icon in pills */
div[data-baseweb="tag"] svg {
    color: #999 !important;
    height: 12px !important;
    width: 12px !important;
    margin-left: 4px !important;
}

/* Dropdown menu styling */
div[role="listbox"],
div[data-baseweb="menu"],
div[data-baseweb="popover"] {
    background-color: white !important;
    border: 1px solid #ddd !important;
    border-radius: 6px !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.1) !important;
}

/* Option items in dropdown */
div[role="option"] {
    padding: 8px 12px !important;
    border-radius: 4px !important;
    margin: 2px 4px !important;
}

div[role="option"]:hover {
    background-color: #f0f6ff !important;
}

/* Container styles for the sections */
.kb-container, .projects-container {
    background-color: white !important;
    border-radius: 8px !important;
    padding: 15px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}
</style>
''', unsafe_allow_html=True)
