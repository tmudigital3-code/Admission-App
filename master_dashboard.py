import streamlit as st
import sys
import os

# Add the dashboard directories to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "admission dashboard"))
sys.path.append(os.path.join(os.path.dirname(__file__), "applicant dashboard"))
sys.path.append(os.path.join(os.path.dirname(__file__), "enquiry dashboard"))

# Import the module functions
MODULES_AVAILABLE = True
# Define stub functions in case imports fail
def stub_dashboard():
    st.info("This dashboard module is not available.")
    st.markdown("""<div class="info-box"><h4>💡 Tips:</h4><ul><li>Ensure all required dependencies are installed</li><li>Check that the dashboard module files are accessible</li></ul></div>""", unsafe_allow_html=True)

def stub_admission_dashboard():
    st.info("The Admission Dashboard module is not available.")
    st.markdown("""<div class="info-box"><h4>💡 Tips:</h4><ul><li>The admission dashboard module needs to be properly configured</li><li>Ensure all required dependencies are installed</li><li>Check that the admission_dashboard_module.py file has the proper render function</li></ul></div>""", unsafe_allow_html=True)

def stub_applicant_dashboard():
    st.info("The Applicant Dashboard module is not available.")
    st.markdown("""<div class="info-box"><h4>💡 Tips:</h4><ul><li>The applicant dashboard module needs to be properly configured</li><li>Ensure all required dependencies are installed</li><li>Check that the applicant_dashboard_module.py file is accessible</li></ul></div>""", unsafe_allow_html=True)

def stub_enquiry_dashboard():
    st.info("The Enquiry Dashboard module is not available.")
    st.markdown("""<div class="info-box"><h4>💡 Tips:</h4><ul><li>The enquiry dashboard module needs to be properly configured</li><li>Ensure all required dependencies are installed</li><li>Check that the enquiry_dashboard_module.py file is accessible</li></ul></div>""", unsafe_allow_html=True)

# Try to import all dashboard modules, but handle gracefully if any fail
APPLICANT_MODULE_AVAILABLE = False
ENQUIRY_MODULE_AVAILABLE = False
ADMISSION_MODULE_AVAILABLE = False

try:
    from applicant_dashboard_module import render_applicant_dashboard
    APPLICANT_MODULE_AVAILABLE = True
except ImportError as e:
    st.error(f"Error importing applicant dashboard module: {str(e)}")
    render_applicant_dashboard = stub_applicant_dashboard

try:
    from enquiry_dashboard_module import render_enquiry_dashboard
    ENQUIRY_MODULE_AVAILABLE = True
except ImportError as e:
    st.error(f"Error importing enquiry dashboard module: {str(e)}")
    render_enquiry_dashboard = stub_enquiry_dashboard

try:
    from admission_dashboard_module import render_admission_dashboard
    ADMISSION_MODULE_AVAILABLE = True
except ImportError as e:
    st.warning(f"Warning: Admission dashboard module not available: {str(e)}")
    render_admission_dashboard = stub_admission_dashboard

# Set MODULES_AVAILABLE based on whether we have at least one working module
MODULES_AVAILABLE = APPLICANT_MODULE_AVAILABLE or ENQUIRY_MODULE_AVAILABLE or ADMISSION_MODULE_AVAILABLE

# Set page configuration
st.set_page_config(
    page_title="Admission Analytics Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS styling for a more professional look
st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #2c3e50 0%, #4a6491 100%);
        color: white;
        padding: 25px 40px;
        border-radius: 15px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .main-title {
        font-size: 2.8em;
        font-weight: 700;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }
    .main-subtitle {
        font-size: 1.3em;
        opacity: 0.9;
        font-weight: 300;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 25px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1em;
        background-color: #e9ecef;
        color: #495057;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #dee2e6;
        transform: translateY(-2px);
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0d6efd;
        color: white;
        box-shadow: 0 4px 8px rgba(13, 110, 253, 0.2);
    }
    
    /* Dashboard intro text */
    .dashboard-intro {
        background: #e7f1ff;
        border-left: 4px solid #0d6efd;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
        font-size: 1.1em;
        line-height: 1.6;
    }
    
    .dashboard-intro h2 {
        color: #0d6efd;
        margin-top: 0;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #6c757d;
        padding: 20px;
        margin-top: 30px;
        border-top: 1px solid #dee2e6;
        font-size: 0.9em;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .sidebar-title {
        font-size: 1.2em;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .sidebar-description {
        font-size: 0.9em;
        color: #6c757d;
        margin-bottom: 15px;
        line-height: 1.4;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.2em;
        }
        .main-subtitle {
            font-size: 1.1em;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 15px;
            font-size: 0.9em;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Main header with enhanced professional styling
st.markdown("""
<div class="main-header">
    <div class="main-title">📊 Admission Analytics Suite</div>
    <div class="main-subtitle">Comprehensive Dashboard for Admission, Applicant, and Enquiry Analytics</div>
</div>
""", unsafe_allow_html=True)

# Check if modules are available
if not MODULES_AVAILABLE:
    st.error("Dashboard modules are not available. Please check your installation.")
    st.stop()

# Enhanced sidebar with user-friendly labels
with st.sidebar:
    st.markdown('<div class="sidebar-section"><div class="sidebar-title">🏫 Admission Data Upload</div><div class="sidebar-description">Upload your admission CSV files here for immediate analysis</div></div>', unsafe_allow_html=True)
    admission_uploaded_file = st.sidebar.file_uploader("Choose Admission CSV File", type=['csv'], key="admission_upload", help="Upload CSV with columns: Date of Admission, enquiry date, Date of Birth, Gender, Category, Religion, Programme Name, Program Level, Student Status, erp20may_State, Source, Family Annual Income, Prequalification Percentage")
    
    st.markdown('<div class="sidebar-section"><div class="sidebar-title">🎓 Applicant Data Upload</div><div class="sidebar-description">Upload your applicant CSV files here for detailed profiling</div></div>', unsafe_allow_html=True)
    applicant_uploaded_files = st.sidebar.file_uploader("Choose Applicant CSV Files", type=['csv'], key="applicant_upload", accept_multiple_files=True, help="Upload CSV files with columns: Allotment Status, Level, Discipline, College")
    
    st.markdown('<div class="sidebar-section"><div class="sidebar-title">📞 Enquiry Data Upload</div><div class="sidebar-description">Upload your enquiry CSV files here for conversion analysis</div></div>', unsafe_allow_html=True)
    enquiry_uploaded_file = st.sidebar.file_uploader("Choose Enquiry CSV File", type=['csv'], key="enquiry_upload", help="Upload CSV with enquiry data including Enquiry No., Enquiry Date, and other relevant fields")
    
    st.markdown('<div class="sidebar-section"><div class="sidebar-title">💡 Quick Help</div><div class="sidebar-description">Switch between modules using the tabs above. Each tab will automatically use the data uploaded here.</div></div>', unsafe_allow_html=True)

# Create tabs for each dashboard with improved styling
admission_tab, applicant_tab, enquiry_tab = st.tabs([
    "🏫 Admission Dashboard", 
    "🎓 Applicant Dashboard", 
    "📞 Enquiry Dashboard"
])

# Admission Dashboard Tab
with admission_tab:
    st.markdown("""<div class="dashboard-intro"><h2>🏫 Admission Dashboard</h2><p>Analyze comprehensive admission data including KPIs, trends, demographics, and advanced analytics. The dashboard will automatically use the CSV file you uploaded in the sidebar.</p></div>""", unsafe_allow_html=True)
    
    # Render the admission dashboard with uploaded file
    try:
        # Pass the uploaded file to the dashboard function
        render_admission_dashboard(admission_uploaded_file)
    except Exception as e:
        st.error(f"Error rendering Admission dashboard: {str(e)}")

# Applicant Dashboard Tab
with applicant_tab:
    st.markdown("""
    <div class="dashboard-intro">
        <h2>🎓 Applicant Dashboard</h2>
        <p>Analyze applicant profiles, performance, and demographic insights. 
        The dashboard will automatically use the CSV files you uploaded in the sidebar.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render the applicant dashboard with uploaded files
    try:
        # Pass the uploaded files to the dashboard function
        render_applicant_dashboard(applicant_uploaded_files)
    except Exception as e:
        st.error(f"Error rendering Applicant dashboard: {str(e)}")

# Enquiry Dashboard Tab
with enquiry_tab:
    st.markdown("""
    <div class="dashboard-intro">
        <h2>📞 Enquiry Dashboard</h2>
        <p>Track enquiry data, conversion rates, and response times. 
        The dashboard will automatically use the CSV file you uploaded in the sidebar.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render the enquiry dashboard with uploaded file
    try:
        # Pass the uploaded file to the dashboard function
        render_enquiry_dashboard(enquiry_uploaded_file)
    except Exception as e:
        st.error(f"Error rendering Enquiry dashboard: {str(e)}")

# Enhanced Footer
st.markdown("""
<div class="footer">
    <p>📊 Admission Analytics Suite | Built with Streamlit</p>
    <p>Integrated dashboard providing access to all analytics modules in one professional interface</p>
</div>
""", unsafe_allow_html=True)