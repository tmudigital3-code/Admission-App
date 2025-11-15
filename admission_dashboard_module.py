"""
Admission Data Analysis Dashboard - Streamlit Version
Interactive dashboard for comprehensive admission data analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, date
import warnings
warnings.filterwarnings('ignore')

def render_admission_dashboard():
    """Render the admission dashboard as a module"""
    
    # Enhanced Custom CSS with professional styling
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        /* KPI Card Styles */
        .kpi-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            margin: 10px 0;
        }
        .kpi-icon {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 15px;
            font-size: 32px;
        }
        .kpi-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .kpi-subtitle {
            font-size: 14px;
            color: #666;
        }
        /* Orange Section Header */
        .section-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        /* Tab Buttons */
        .tab-buttons {
            display: flex;
            gap: 5px;
            margin: 20px 0;
        }
        .tab-button {
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: 600;
            cursor: pointer;
            border: none;
        }
        .tab-button.active {
            background-color: #f7931e;
            color: white;
        }
        .tab-button.inactive {
            background-color: #5a6c7d;
            color: white;
        }
        /* Data Table */
        .dataframe {
            font-size: 14px;
        }
        .dataframe thead tr th {
            background-color: #5a6c7d !important;
            color: white !important;
            font-weight: bold;
        }
        .dataframe tbody tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        .info-box {
            background-color: #e3f2fd;
            border-left: 5px solid #2196f3;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .warning-box {
            background-color: #fff3e0;
            border-left: 5px solid #ff9800;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .success-box {
            background-color: #e8f5e9;
            border-left: 5px solid #4caf50;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .metrics-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metrics-title {
            font-size: 1.5em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Enhanced Header with gradient styling
    st.markdown("""
    <div class="section-header">
        🎓 Admission Data Analysis Dashboard 2025
    </div>
    """, unsafe_allow_html=True)

    # Load data with caching
    @st.cache_data
    def load_data(uploaded_file=None):
        """Load and preprocess data"""
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            try:
                df = pd.read_csv('2025 admissions  - primary only (1).csv')
            except FileNotFoundError:
                return None
        
        # Data preprocessing with more flexible date parsing
        df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce')
        df['enquiry date'] = pd.to_datetime(df['enquiry date'], errors='coerce')
        df['Date of Birth'] = pd.to_datetime(df['Date of Birth'], errors='coerce')
        df['Family Annual Income'] = pd.to_numeric(df['Family Annual Income'], errors='coerce')
        df['Prequalification Percentage'] = pd.to_numeric(df['Prequalification Percentage'], errors='coerce')
        df['Age'] = 2025 - df['Date of Birth'].dt.year
        df['Month'] = df['Date of Admission'].dt.to_period('M').astype(str)
        df['Days_to_Admission'] = (df['Date of Admission'] - df['enquiry date']).dt.days
        
        return df

    # File Upload Section
    st.sidebar.header("📁 Data Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Admission Data Upload",
        type=['csv'],
        accept_multiple_files=False,
        help="Upload your admission data CSV file"
    )

    if uploaded_file is not None:
        st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
        df = load_data(uploaded_file)
    else:
        st.sidebar.info("Using default data file")
        df = load_data()

    # Check if data is loaded
    if df is None:
        st.error("❌ No data file found! Please upload a CSV file using the sidebar.")
        st.info("""📋 **Required CSV Columns:**
        - Date of Admission
        - enquiry date
        - Date of Birth
        - Gender
        - Category
        - Religion
        - Programme Name
        - Program Level
        - Student Status
        - And other relevant fields...
        """)
        st.markdown("""
        <div class="info-box">
            <h4>💡 Tips for Using This Dashboard:</h4>
            <ul>
                <li>Upload a CSV file containing admission data</li>
                <li>Ensure your data includes the required columns listed above</li>
                <li>Use the filters in the sidebar to analyze specific date ranges and categories</li>
                <li>Switch between tabs to view different types of analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return

    # Check if dataframe is empty
    if df is not None and df.empty:
        st.info("No data found. Please upload a CSV file using the uploader in the sidebar.")
        st.markdown("""
        <div class="info-box">
            <h4>💡 Tips for Using This Dashboard:</h4>
            <ul>
                <li>Upload a CSV file containing admission data</li>
                <li>Ensure your data includes the required columns listed above</li>
                <li>Use the filters in the sidebar to analyze specific date ranges and categories</li>
                <li>Switch between tabs to view different types of analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return

    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filters")

    # Initialize variables with default values
    gender_options = ['All']
    program_levels = ['All']
    states = ['All']
    categories = ['All']
    religions = ['All']
    sources = ['All']
    status_options = ['All']
    min_income = 0
    max_income = 1000000
    min_score = 0.0
    max_score = 100.0

    # Only process filters if we have valid data
    if df is not None and not df.empty:
        # Gender filter
        gender_options = ['All'] + list(df['Gender'].dropna().unique())
        
        # Program Level filter
        program_levels = ['All'] + list(df['Program Level'].dropna().unique())
        
        # State filter
        states = ['All'] + list(df['erp20may_State'].dropna().unique())

    # State filter
    selected_state = st.sidebar.multiselect(
        "State",
        options=states,
        default=['All']
    )

    # Additional Filters
    st.sidebar.markdown("---")
    st.sidebar.subheader("📌 Advanced Filters")

    # Category filter
    selected_category = st.sidebar.multiselect(
        "Category",
        options=categories,
        default=['All']
    )

    # Religion filter
    selected_religion = st.sidebar.multiselect(
        "Religion",
        options=religions,
        default=['All']
    )

    # Source filter
    if df is not None and not df.empty and 'Source' in df.columns:
        sources = ['All'] + list(df['Source'].dropna().unique())
    else:
        sources = ['All']
    selected_source = st.sidebar.multiselect(
        "Admission Source",
        options=sources,
        default=['All']
    )

    # Student Status filter
    if df is not None and not df.empty and 'Student Status' in df.columns:
        status_options = ['All'] + list(df['Student Status'].dropna().unique())
    else:
        status_options = ['All']
    selected_status = st.sidebar.multiselect(
        "Student Status",
        options=status_options,
        default=['All']
    )

    # Income Range filter
    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Income Filter")
    if df is not None and not df.empty and 'Family Annual Income' in df.columns:
        min_income_val = df['Family Annual Income'].min()
        max_income_val = df['Family Annual Income'].max()
        # Safely convert to numeric values
        min_income_val = pd.to_numeric(min_income_val, errors='coerce')
        max_income_val = pd.to_numeric(max_income_val, errors='coerce')
        min_income = int(min_income_val) if pd.notna(min_income_val) else 0
        max_income = int(max_income_val) if pd.notna(max_income_val) else 1000000
    else:
        min_income = 0
        max_income = 1000000
        
    income_range = st.sidebar.slider(
        "Family Annual Income (₹)",
        min_value=min_income,
        max_value=max_income,
        value=(min_income, max_income),
        step=50000,
        format="₹%d"
    )

    # Score Range filter
    st.sidebar.subheader("📊 Score Filter")
    if df is not None and not df.empty and 'Prequalification Percentage' in df.columns:
        min_score_val = df['Prequalification Percentage'].min()
        max_score_val = df['Prequalification Percentage'].max()
        # Safely convert to numeric values
        min_score_val = pd.to_numeric(min_score_val, errors='coerce')
        max_score_val = pd.to_numeric(max_score_val, errors='coerce')
        min_score = float(min_score_val) if pd.notna(min_score_val) else 0.0
        max_score = float(max_score_val) if pd.notna(max_score_val) else 100.0
    else:
        min_score = 0.0
        max_score = 100.0
        
    score_range = st.sidebar.slider(
        "Prequalification Score (%)",
        min_value=min_score,
        max_value=max_score,
        value=(min_score, max_score),
        step=1.0
    )

    # Date range filter with error handling
    # Initialize filtered_df
    filtered_df = df.copy() if df is not None else pd.DataFrame()
    
    try:
        if df is not None and not df.empty:
            # Safely get min and max dates using a simple approach
            try:
                min_date_raw = df['Date of Admission'].min()
                max_date_raw = df['Date of Admission'].max()
                
                # Convert to datetime using pd.Series to ensure it's array-like
                min_date_dt = pd.to_datetime(pd.Series([min_date_raw]), errors='coerce').iloc[0]
                max_date_dt = pd.to_datetime(pd.Series([max_date_raw]), errors='coerce').iloc[0]
                
                # Use today's date as fallback if min/max dates are invalid
                today = date.today()
                min_date = min_date_dt.date() if pd.notna(min_date_dt) else today
                max_date = max_date_dt.date() if pd.notna(max_date_dt) else today
                
                date_range = st.sidebar.date_input(
                    "Select Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
                
                # Apply date range filter
                # Check if date_range is a tuple (which is what we expect)
                if isinstance(date_range, tuple) and len(date_range) == 2:
                    start_date, end_date = date_range
                    filtered_df = filtered_df[
                        (filtered_df['Date of Admission'] >= pd.Timestamp(start_date)) &
                        (filtered_df['Date of Admission'] <= pd.Timestamp(end_date))
                    ]
            except Exception as e:
                # If we can't process dates, use default range
                today = date.today()
                date_range = st.sidebar.date_input(
                    "Select Date Range",
                    value=(today, today),
                    min_value=today,
                    max_value=today
                )
    except Exception as e:
        st.warning(f"Date filter error: {str(e)}")
        filtered_df = df.copy() if df is not None else pd.DataFrame()

    # Apply all filters
    try:
        # Make sure filtered_df is a DataFrame
        if not isinstance(filtered_df, pd.DataFrame):
            filtered_df = pd.DataFrame()
        
        # State filter
        if 'All' not in selected_state and selected_state and len(selected_state) > 0 and 'erp20may_State' in filtered_df.columns:
            # Ensure filtered_df is not empty and has the column
            if not filtered_df.empty:
                filtered_df = filtered_df[filtered_df['erp20may_State'].isin(selected_state)]
        
        # Category filter
        if 'All' not in selected_category and selected_category and len(selected_category) > 0 and 'Category' in filtered_df.columns:
            # Ensure filtered_df is not empty
            if not filtered_df.empty:
                filtered_df = filtered_df[filtered_df['Category'].isin(selected_category)]
        
        # Religion filter
        if 'All' not in selected_religion and selected_religion and len(selected_religion) > 0 and 'Religion' in filtered_df.columns:
            # Ensure filtered_df is not empty
            if not filtered_df.empty:
                filtered_df = filtered_df[filtered_df['Religion'].isin(selected_religion)]
        
        # Source filter
        if 'All' not in selected_source and selected_source and len(selected_source) > 0 and 'Source' in filtered_df.columns:
            # Ensure filtered_df is not empty
            if not filtered_df.empty:
                filtered_df = filtered_df[filtered_df['Source'].isin(selected_source)]
        
        # Student Status filter
        if 'All' not in selected_status and selected_status and len(selected_status) > 0 and 'Student Status' in filtered_df.columns:
            # Ensure filtered_df is not empty
            if not filtered_df.empty:
                filtered_df = filtered_df[filtered_df['Student Status'].isin(selected_status)]
        
        # Income filter
        if 'Family Annual Income' in filtered_df.columns and len(income_range) == 2:
            # Ensure filtered_df is not empty
            if not filtered_df.empty:
                filtered_df = filtered_df[
                    (filtered_df['Family Annual Income'] >= income_range[0]) &
                    (filtered_df['Family Annual Income'] <= income_range[1])
                ]
        
        # Score filter
        if 'Prequalification Percentage' in filtered_df.columns and len(score_range) == 2:
            # Ensure filtered_df is not empty
            if not filtered_df.empty:
                filtered_df = filtered_df[
                    (filtered_df['Prequalification Percentage'] >= score_range[0]) &
                    (filtered_df['Prequalification Percentage'] <= score_range[1])
                ]
    except Exception as e:
        st.warning(f"Filter application error: {str(e)}")
        # Reset to original data if filters fail
        filtered_df = df.copy() if df is not None else pd.DataFrame()

    # Main dashboard content
    try:
        # Create tabs for different analysis sections
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📈 Overview", 
            "📊 KPIs", 
            "👥 Demographics", 
            "🎓 Programs", 
            "📈 Trends", 
            "🌍 Geography", 
            "💰 Financial"
        ])

        with tab1:
            st.header("Overview")
            
            # Display key metrics in cards
            if not filtered_df.empty:
                total_admissions = len(filtered_df)
                avg_income = filtered_df['Family Annual Income'].mean() if 'Family Annual Income' in filtered_df.columns else 0
                avg_score = filtered_df['Prequalification Percentage'].mean() if 'Prequalification Percentage' in filtered_df.columns else 0
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-icon" style="background-color: #4e73df;">
                            📈
                        </div>
                        <div class="kpi-title">Total Admissions</div>
                        <div class="kpi-value">{total_admissions:,}</div>
                        <div class="kpi-subtitle">Students admitted</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-icon" style="background-color: #1cc88a;">
                            💰
                        </div>
                        <div class="kpi-title">Avg. Family Income</div>
                        <div class="kpi-value">₹{avg_income:,.0f}</div>
                        <div class="kpi-subtitle">Annual income</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-icon" style="background-color: #36b9cc;">
                            📊
                        </div>
                        <div class="kpi-title">Avg. Score</div>
                        <div class="kpi-value">{avg_score:.1f}%</div>
                        <div class="kpi-subtitle">Prequalification</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display filtered data
                st.subheader("Filtered Data")
                st.dataframe(filtered_df)
            else:
                st.info("No data available with current filters.")

        with tab2:
            st.header("Key Performance Indicators")
            if not filtered_df.empty:
                # Create KPI metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_students = len(filtered_df)
                    st.metric("Total Students", total_students)
                
                with col2:
                    if 'Family Annual Income' in filtered_df.columns:
                        avg_income = filtered_df['Family Annual Income'].mean()
                        st.metric("Avg. Family Income", f"₹{avg_income:,.0f}")
                    else:
                        st.metric("Avg. Family Income", "N/A")
                
                with col3:
                    if 'Prequalification Percentage' in filtered_df.columns:
                        avg_score = filtered_df['Prequalification Percentage'].mean()
                        st.metric("Avg. Score", f"{avg_score:.1f}%")
                    else:
                        st.metric("Avg. Score", "N/A")
                
                with col4:
                    if 'Gender' in filtered_df.columns:
                        male_count = len(filtered_df[filtered_df['Gender'] == 'Male'])
                        female_count = len(filtered_df[filtered_df['Gender'] == 'Female'])
                        st.metric("Gender Ratio (M:F)", f"{male_count}:{female_count}")
                    else:
                        st.metric("Gender Ratio", "N/A")
                
                # Additional KPIs
                st.subheader("Advanced KPIs")
                kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
                
                with kpi_col1:
                    if 'Days_to_Admission' in filtered_df.columns:
                        avg_days = filtered_df['Days_to_Admission'].mean()
                        st.metric("Avg. Days to Admission", f"{avg_days:.1f}")
                    else:
                        st.metric("Avg. Days to Admission", "N/A")
                
                with kpi_col2:
                    if 'Age' in filtered_df.columns:
                        avg_age = filtered_df['Age'].mean()
                        st.metric("Avg. Age", f"{avg_age:.1f}")
                    else:
                        st.metric("Avg. Age", "N/A")
                
                with kpi_col3:
                    if 'Student Status' in filtered_df.columns:
                        active_count = len(filtered_df[filtered_df['Student Status'] == 'Active'])
                        active_pct = (active_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
                        st.metric("Active Students", f"{active_pct:.1f}%")
                    else:
                        st.metric("Active Students", "N/A")
                
                # KPI Charts
                st.subheader("KPI Visualizations")
                chart_col1, chart_col2, chart_col3 = st.columns(3)
                
                with chart_col1:
                    # Program Level Distribution
                    if 'Program Level' in filtered_df.columns:
                        program_counts = filtered_df['Program Level'].value_counts()
                        fig1 = px.pie(values=program_counts.values, names=program_counts.index, 
                                     title="Distribution by Program Level")
                        st.plotly_chart(fig1, use_container_width=True)
                
                with chart_col2:
                    # Gender Distribution
                    if 'Gender' in filtered_df.columns:
                        gender_counts = filtered_df['Gender'].value_counts()
                        fig2 = px.bar(x=gender_counts.index, y=gender_counts.values,
                                     labels={'x': 'Gender', 'y': 'Count'},
                                     title="Gender Distribution")
                        st.plotly_chart(fig2, use_container_width=True)
                
                with chart_col3:
                    # Student Status Distribution
                    if 'Student Status' in filtered_df.columns:
                        status_counts = filtered_df['Student Status'].value_counts()
                        fig3 = px.pie(values=status_counts.values, names=status_counts.index,
                                     title="Student Status Distribution")
                        st.plotly_chart(fig3, use_container_width=True)
                
                # Additional Charts
                st.subheader("Advanced Visualizations")
                adv_col1, adv_col2 = st.columns(2)
                
                with adv_col1:
                    # Age Distribution Histogram
                    if 'Age' in filtered_df.columns:
                        fig4 = px.histogram(filtered_df, x='Age', nbins=20,
                                          title="Age Distribution",
                                          color_discrete_sequence=['#636EFA'])
                        st.plotly_chart(fig4, use_container_width=True)
                
                with adv_col2:
                    # Income vs Score Scatter Plot
                    if 'Family Annual Income' in filtered_df.columns and 'Prequalification Percentage' in filtered_df.columns:
                        fig5 = px.scatter(filtered_df, x='Family Annual Income', y='Prequalification Percentage',
                                         title="Income vs. Prequalification Score",
                                         color_discrete_sequence=['#EF553B'])
                        st.plotly_chart(fig5, use_container_width=True)

            else:
                st.info("No data available for KPI analysis.")

        with tab3:
            st.header("Demographics Analysis")
            if not filtered_df.empty:
                # Age Distribution
                if 'Age' in filtered_df.columns:
                    st.subheader("Age Distribution")
                    fig_age = px.histogram(filtered_df, x='Age', nbins=20,
                                          title="Distribution of Student Ages")
                    st.plotly_chart(fig_age, use_container_width=True)
                
                # Category Distribution
                if 'Category' in filtered_df.columns:
                    st.subheader("Category Distribution")
                    category_counts = filtered_df['Category'].value_counts()
                    fig_cat = px.bar(x=category_counts.index, y=category_counts.values,
                                    labels={'x': 'Category', 'y': 'Count'},
                                    title="Student Distribution by Category")
                    st.plotly_chart(fig_cat, use_container_width=True)
                
                # Religion Distribution
                if 'Religion' in filtered_df.columns:
                    st.subheader("Religion Distribution")
                    religion_counts = filtered_df['Religion'].value_counts()
                    fig_rel = px.pie(values=religion_counts.values, names=religion_counts.index,
                                    title="Student Distribution by Religion")
                    st.plotly_chart(fig_rel, use_container_width=True)
            else:
                st.info("No data available for demographics analysis.")

        with tab4:
            st.header("Programs Analysis")
            if not filtered_df.empty:
                # Programmes Analysis
                if 'Programme Name' in filtered_df.columns:
                    st.subheader("Programme Distribution")
                    prog_counts = filtered_df['Programme Name'].value_counts().head(10)
                    fig_prog = px.bar(x=prog_counts.index, y=prog_counts.values,
                                     labels={'x': 'Programme', 'y': 'Count'},
                                     title="Top 10 Programmes")
                    fig_prog.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig_prog, use_container_width=True)
                
                # Program Level Analysis
                if 'Program Level' in filtered_df.columns:
                    st.subheader("Program Level Analysis")
                    level_counts = filtered_df['Program Level'].value_counts()
                    fig_level = px.bar(x=level_counts.index, y=level_counts.values,
                                      labels={'x': 'Program Level', 'y': 'Count'},
                                      title="Distribution by Program Level")
                    st.plotly_chart(fig_level, use_container_width=True)
            else:
                st.info("No data available for programs analysis.")

        with tab5:
            st.header("Trends Analysis")
            if not filtered_df.empty:
                # Admission Trends over Time
                if 'Date of Admission' in filtered_df.columns:
                    st.subheader("Admission Trends Over Time")
                    # Create monthly admission counts
                    filtered_df['Admission_Month'] = filtered_df['Date of Admission'].dt.to_period('M').astype(str)
                    monthly_counts = filtered_df['Admission_Month'].value_counts().sort_index()
                    
                    fig_trend = px.line(x=monthly_counts.index, y=monthly_counts.values,
                                       labels={'x': 'Month', 'y': 'Number of Admissions'},
                                       title="Monthly Admission Trends")
                    st.plotly_chart(fig_trend, use_container_width=True)
                
                # Score Trends
                if 'Prequalification Percentage' in filtered_df.columns and 'Date of Admission' in filtered_df.columns:
                    st.subheader("Average Score Trends")
                    # Group by month and calculate average scores
                    monthly_scores = filtered_df.groupby('Admission_Month')['Prequalification Percentage'].mean()
                    
                    fig_score_trend = px.line(x=monthly_scores.index, y=monthly_scores.values,
                                             labels={'x': 'Month', 'y': 'Average Score'},
                                             title="Average Prequalification Score Trends")
                    st.plotly_chart(fig_score_trend, use_container_width=True)
            else:
                st.info("No data available for trends analysis.")

        with tab6:
            st.header("Geographic Analysis")
            if not filtered_df.empty:
                # State-wise Analysis
                if 'erp20may_State' in filtered_df.columns:
                    st.subheader("State-wise Admission Distribution")
                    state_counts = filtered_df['erp20may_State'].value_counts().head(10)
                    fig_state = px.bar(x=state_counts.index, y=state_counts.values,
                                      labels={'x': 'State', 'y': 'Number of Admissions'},
                                      title="Top 10 States by Admissions")
                    fig_state.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig_state, use_container_width=True)
                
                # State-wise Average Income
                if 'erp20may_State' in filtered_df.columns and 'Family Annual Income' in filtered_df.columns:
                    st.subheader("Average Family Income by State")
                    state_income = filtered_df.groupby('erp20may_State')['Family Annual Income'].mean().sort_values(ascending=False).head(10)
                    fig_income = px.bar(x=state_income.index, y=state_income.values,
                                       labels={'x': 'State', 'y': 'Average Income (₹)'},
                                       title="Top 10 States by Average Family Income")
                    fig_income.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig_income, use_container_width=True)
            else:
                st.info("No data available for geographic analysis.")

        with tab7:
            st.header("Financial Analysis")
            if not filtered_df.empty:
                # Income Distribution
                if 'Family Annual Income' in filtered_df.columns:
                    st.subheader("Family Annual Income Distribution")
                    fig_income_dist = px.histogram(filtered_df, x='Family Annual Income', nbins=30,
                                                  title="Distribution of Family Annual Income")
                    st.plotly_chart(fig_income_dist, use_container_width=True)
                
                # Income vs Score Correlation
                if 'Family Annual Income' in filtered_df.columns and 'Prequalification Percentage' in filtered_df.columns:
                    st.subheader("Income vs. Prequalification Score")
                    fig_corr = px.scatter(filtered_df, x='Family Annual Income', y='Prequalification Percentage',
                                         title="Correlation between Family Income and Prequalification Score",
                                         labels={'Family Annual Income': 'Family Annual Income (₹)',
                                                'Prequalification Percentage': 'Prequalification Score (%)'})
                    st.plotly_chart(fig_corr, use_container_width=True)
                
                # Income by Category
                if 'Family Annual Income' in filtered_df.columns and 'Category' in filtered_df.columns:
                    st.subheader("Average Income by Category")
                    category_income = filtered_df.groupby('Category')['Family Annual Income'].mean().sort_values(ascending=False)
                    fig_cat_income = px.bar(x=category_income.index, y=category_income.values,
                                           labels={'x': 'Category', 'y': 'Average Income (₹)'},
                                           title="Average Family Income by Category")
                    st.plotly_chart(fig_cat_income, use_container_width=True)
            else:
                st.info("No data available for financial analysis.")

    except Exception as e:
        st.error(f"Error displaying dashboard content: {str(e)}")

# Allow direct execution for testing
if __name__ == "__main__":
    render_admission_dashboard()