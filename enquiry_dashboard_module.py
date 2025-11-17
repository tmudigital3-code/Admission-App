import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, date
import warnings
warnings.filterwarnings('ignore')

def render_enquiry_dashboard(uploaded_files=None):
    """Render the enquiry dashboard content"""
    
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
        /* Section Header */
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
        .sidebar-header {
            background-color: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            text-align: center;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Enhanced Header with gradient styling
    st.markdown("""
    <div class="section-header">
        📞 Enquiry Data Analysis Dashboard
    </div>
    """, unsafe_allow_html=True)

    # Function to load data from uploaded file or default data
    @st.cache_data
    def load_data_from_file(uploaded_files):
        """Load data from single or multiple uploaded files or default data"""
        dataframes = []
        
        # If no files were uploaded, try to load default data
        if uploaded_files is None or len(uploaded_files) == 0:
            try:
                df = pd.read_csv('enquiry_data.csv')
                dataframes.append(df)
            except FileNotFoundError:
                return pd.DataFrame()  # Return empty DataFrame if no default file
        else:
            # Handle multiple uploaded files
            for uploaded_file in uploaded_files:
                try:
                    # Read the uploaded CSV file
                    df = pd.read_csv(uploaded_file)
                    dataframes.append(df)
                except Exception as e:
                    st.warning(f"Error loading file {uploaded_file.name}: {str(e)}")
                    continue
    
        # Combine all dataframes if we have any
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)
            
            # Remove duplicate entries (entries with same Enquiry No. and different times)
            if 'Enquiry No.' in combined_df.columns:
                df_unique = combined_df.drop_duplicates(subset=['Enquiry No.'], keep='first')
            else:
                df_unique = combined_df
            
            # Convert Enquiry Date to datetime with error handling
            # Try multiple date formats including those with AM/PM
            date_formats = [
                '%d-%b-%Y %I:%M %p',  # Format like "20-Feb-2025 2:40 PM"
                '%d-%b-%Y %H:%M',     # Format like "20-Feb-2025 14:40"
                '%d-%m-%Y %H:%M',     # Format like "20-02-2025 14:40"
                '%m-%d-%Y %H:%M'      # Format like "02-20-2025 14:40"
            ]
            
            # Store the original date strings
            if df_unique is not None and 'Enquiry Date' in df_unique.columns:
                date_strings = df_unique['Enquiry Date'].copy()
            else:
                date_strings = pd.Series()
            
            # Initialize parsed_dates as None
            parsed_dates = None
            
            # Try each format until we successfully parse some dates
            for fmt in date_formats:
                try:
                    # Try to parse with the current format using the original date strings
                    parsed_dates = pd.to_datetime(date_strings, format=fmt, errors='coerce')
                    # If we successfully parsed some dates, use them
                    if hasattr(parsed_dates, 'notna') and parsed_dates.notna().sum() > 0:
                        if df_unique is not None:
                            df_unique['Enquiry Date'] = parsed_dates
                        break
                except Exception as e:
                    continue
            
            # If that didn't work, try without format specification
            try:
                if parsed_dates is None:
                    if df_unique is not None:
                        df_unique['Enquiry Date'] = pd.to_datetime(date_strings, errors='coerce')
                else:
                    # Check if all values are NaN using pandas methods
                    isna_check = pd.isna(parsed_dates).sum()
                    total_count = len(parsed_dates) if hasattr(parsed_dates, '__len__') else 0
                    if isna_check == total_count and total_count > 0:
                        if df_unique is not None:
                            df_unique['Enquiry Date'] = pd.to_datetime(date_strings, errors='coerce')
            except Exception:
                if df_unique is not None:
                    df_unique['Enquiry Date'] = pd.to_datetime(date_strings, errors='coerce')
            
            # Remove rows with invalid dates
            if df_unique is not None and 'Enquiry Date' in df_unique.columns:
                df_unique = df_unique.dropna(subset=['Enquiry Date'])
            
            # Extract date components for analysis
            if df_unique is not None and 'Enquiry Date' in df_unique.columns:
                df_unique['Year'] = df_unique['Enquiry Date'].dt.year
                df_unique['Month'] = df_unique['Enquiry Date'].dt.month
                df_unique['Day'] = df_unique['Enquiry Date'].dt.day
                df_unique['Hour'] = df_unique['Enquiry Date'].dt.hour
            
            return df_unique if df_unique is not None else pd.DataFrame()
        else:
            return pd.DataFrame()

    # Check if files were uploaded from master dashboard
    if uploaded_files is not None and len(uploaded_files) > 0:
        df = load_data_from_file(uploaded_files)
        for uploaded_file in uploaded_files:
            st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
    else:
        # If no files were uploaded from master dashboard, load default data silently
        df = load_data_from_file(None)
    
    # Check if we have valid data
    if df is None or df.empty:
        st.info("Please upload a CSV file to begin analysis.")
        st.markdown("""
        <div class="info-box">
            <h4>💡 Tips for Using This Dashboard:</h4>
            <ul>
                <li>Upload a CSV file containing enquiry data</li>
                <li>Ensure your data includes columns like: Enquiry No., Enquiry Date, College, Specialization, Enquiry Type, Allotment Status, Gender</li>
                <li>Use the filters in the sidebar to analyze specific segments</li>
                <li>View visualizations to understand enquiry patterns and trends</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return

    # Initialize filtered_df with the full dataset
    filtered_df = df.copy()

    # Sidebar filters
    st.sidebar.markdown('<div class="sidebar-header">🔍 Filters</div>', unsafe_allow_html=True)

    # College filter
    colleges = ['All Colleges'] + list(df['College'].unique())
    selected_college = st.sidebar.selectbox("Select College", colleges, key="enquiry_college")

    # Specialization filter
    specializations = ['All Specializations'] + list(df['Specialization'].unique())
    selected_specialization = st.sidebar.selectbox("Select Specialization", specializations, key="enquiry_specialization")

    # Enquiry Type filter
    enquiry_types = ['All Types'] + list(df['Enquiry Type'].unique())
    selected_enquiry_type = st.sidebar.selectbox("Select Enquiry Type", enquiry_types, key="enquiry_type")

    # Date range filter - with proper error handling
    try:
        # Fix date attribute access issues by using pandas functions
        min_date_raw = df['Enquiry Date'].min()
        max_date_raw = df['Enquiry Date'].max()
        
        # Safely extract date components using pandas methods
        try:
            min_date_series = pd.Series([min_date_raw])
            max_date_series = pd.Series([max_date_raw])
            
            # Convert to datetime and extract date
            min_date_dt = pd.to_datetime(min_date_series, errors='coerce')
            max_date_dt = pd.to_datetime(max_date_series, errors='coerce')
            
            if not min_date_dt.isna().any() and not max_date_dt.isna().any():
                min_date = min_date_dt.dt.date.iloc[0]
                max_date = max_date_dt.dt.date.iloc[0]
                
                # Ensure we have valid dates
                start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date, key="enquiry_start_date")
                end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date, key="enquiry_end_date")
            else:
                start_date = date.today()
                end_date = date.today()
        except Exception:
            start_date = date.today()
            end_date = date.today()
    except Exception as e:
        st.sidebar.warning("Error processing dates. Using default date range.")
        start_date = date.today()
        end_date = date.today()

    # Apply filters to the data
    if selected_college != 'All Colleges':
        filtered_df = filtered_df[filtered_df['College'] == selected_college]

    if selected_specialization != 'All Specializations':
        filtered_df = filtered_df[filtered_df['Specialization'] == selected_specialization]

    if selected_enquiry_type != 'All Types':
        filtered_df = filtered_df[filtered_df['Enquiry Type'] == selected_enquiry_type]

    # Convert dates for filtering with error handling
    try:
        # Fix date combination issues by checking the type of start_date and end_date
        if isinstance(start_date, tuple):
            start_date = start_date[0] if start_date else date.today()
        if isinstance(end_date, tuple):
            end_date = end_date[0] if end_date else date.today()
            
        # Ensure we have valid dates
        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = date.today()
            
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        filtered_df = filtered_df[(filtered_df['Enquiry Date'] >= start_datetime) & 
                                  (filtered_df['Enquiry Date'] <= end_datetime)]
    except Exception as e:
        st.warning("Error filtering by date. Showing all data.")
        pass
            
    # Calculate metrics
    total_enquiries = len(filtered_df)
    allotted_enquiries = len(filtered_df[filtered_df['Allotment Status'] == 'Allotted'])
    admission_enquiries = len(filtered_df[filtered_df['Allotment Status'] == 'Admission'])
        
    # Fix nunique issue by using pandas functions explicitly
    try:
        unique_specializations_series = pd.Series(filtered_df['Specialization']).nunique()
        unique_specializations = int(unique_specializations_series) if not pd.isna(unique_specializations_series) else 0
    except Exception:
        unique_specializations = 0

    # Additional metrics
    walkin_enquiries = len(filtered_df[filtered_df['Enquiry Type'] == 'Walk-in'])
    online_enquiries = len(filtered_df[filtered_df['Enquiry Type'] == 'Online'])
    male_enquiries = len(filtered_df[filtered_df['Gender'] == 'Male'])
    female_enquiries = len(filtered_df[filtered_df['Gender'] == 'Female'])

    # Display key metrics
    st.markdown("""
    <div class="metrics-container">
        <div class="metrics-title">📊 Key Metrics</div>
    </div>
    """, unsafe_allow_html=True)
        
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Enquiries", total_enquiries)
    col2.metric("Allotted Enquiries", allotted_enquiries)
    col3.metric("Admission Enquiries", admission_enquiries)
    col4.metric("Unique Specializations", unique_specializations)

    # Additional metrics row
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Walk-in Enquiries", walkin_enquiries)
    col6.metric("Online Enquiries", online_enquiries)
    col7.metric("Male Enquiries", male_enquiries)
    col8.metric("Female Enquiries", female_enquiries)

    # Create charts
    st.markdown('<div class="section-header">📈 Data Visualizations</div>', unsafe_allow_html=True)

    # Row 1
    col1, col2 = st.columns(2)

    # Enquiries by date (line chart)
    with col1:
        # Fix groupby and dt issues by using pandas functions explicitly
        try:
            enquiry_date_series = pd.Series(filtered_df['Enquiry Date'])
            date_groups = enquiry_date_series.groupby(enquiry_date_series.dt.date)
            daily_counts_series = date_groups.size()
            # Fix reset_index issue
            daily_counts = pd.DataFrame({
                'Enquiry Date': daily_counts_series.index,
                'Count': daily_counts_series.values
            })
            if not daily_counts.empty:
                fig1 = px.line(daily_counts, x='Enquiry Date', y='Count', 
                               title='Enquiries Over Time')
                fig1.update_layout(xaxis_title='Date', yaxis_title='Number of Enquiries')
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No data available for this selection")
        except Exception as e:
            st.info("No data available for this selection")

    # Enquiries by college (bar chart)
    with col2:
        # Fix value_counts issues by using pandas functions explicitly
        try:
            college_value_counts = pd.Series(filtered_df['College']).value_counts()
            college_counts = college_value_counts.reset_index()
            college_counts.columns = ['College', 'Count']
            if not college_counts.empty:
                fig2 = px.bar(college_counts, x='College', y='Count', 
                              title='Enquiries by College')
                fig2.update_layout(xaxis_title='College', yaxis_title='Number of Enquiries')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No data available for this selection")
        except Exception as e:
            st.info("No data available for this selection")

    # Row 2
    col1, col2 = st.columns(2)

    # Enquiries by specialization (bar chart)
    with col1:
        # Fix value_counts issues by using pandas functions explicitly
        try:
            specialization_counts = pd.Series(filtered_df['Specialization']).value_counts().head(10)
            if not specialization_counts.empty:
                fig3 = px.bar(x=specialization_counts.values, y=specialization_counts.index,
                              orientation='h', title='Top 10 Specializations by Enquiries')
                fig3.update_layout(xaxis_title='Number of Enquiries', yaxis_title='Specialization')
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No data available for this selection")
        except Exception as e:
            st.info("No data available for this selection")

    # Enquiries by type (pie chart)
    with col2:
        # Fix value_counts issues by using pandas functions explicitly
        try:
            enquiry_type_counts = pd.Series(filtered_df['Enquiry Type']).value_counts()
            if not enquiry_type_counts.empty:
                fig4 = px.pie(values=enquiry_type_counts.values, names=enquiry_type_counts.index,
                              title='Enquiries by Type')
                fig4.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#2c3e50")
                )
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("No data available for this selection")
        except Exception as e:
            st.info("No data available for this selection")

    # Row 3
    col1, col2 = st.columns(2)

    # Enquiries by status (bar chart)
    with col1:
        # Fix value_counts issues by using pandas functions explicitly
        try:
            status_counts = pd.Series(filtered_df['Allotment Status']).value_counts()
            if not status_counts.empty:
                fig5 = px.bar(x=status_counts.index, y=status_counts.values,
                              title='Enquiries by Status')
                fig5.update_layout(xaxis_title='Status', yaxis_title='Number of Enquiries')
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.info("No data available for this selection")
        except Exception as e:
            st.info("No data available for this selection")

    # Enquiries by gender (pie chart)
    with col2:
        # Fix value_counts issues by using pandas functions explicitly
        try:
            gender_counts = pd.Series(filtered_df['Gender']).value_counts()
            if not gender_counts.empty:
                fig6 = px.pie(values=gender_counts.values, names=gender_counts.index,
                              title='Enquiries by Gender')
                fig6.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#2c3e50")
                )
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.info("No data available for this selection")
        except Exception as e:
            st.info("No data available for this selection")
        
    # Row 4 - Additional Charts
    st.markdown('<div class="section-header">📈 Advanced Analytics</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Monthly trend analysis
    st.write("### Monthly Trend Analysis")
    try:
        # Fix dt and groupby issues by using pandas functions explicitly
        enquiry_date_series = pd.Series(filtered_df['Enquiry Date'])
        monthly_data = pd.DataFrame({
            'Enquiry Date': enquiry_date_series
        })
        # Extract year and month using pandas functions
        monthly_data['Year'] = pd.to_datetime(monthly_data['Enquiry Date']).dt.year
        monthly_data['Month'] = pd.to_datetime(monthly_data['Enquiry Date']).dt.month
            
        # Group by year and month
        monthly_groups = monthly_data.groupby(['Year', 'Month'])
        monthly_counts_series = monthly_groups.size()
            
        # Fix reset_index issue
        monthly_counts = pd.DataFrame({
            'Year': monthly_counts_series.index.get_level_values(0),
            'Month': monthly_counts_series.index.get_level_values(1),
            'Count': monthly_counts_series.values
        })
            
        if not monthly_counts.empty:
            # Create a date column for plotting
            monthly_counts['Date'] = pd.to_datetime(monthly_counts[['Year', 'Month']].assign(day=1))
            fig7 = px.line(monthly_counts, x='Date', y='Count', title='Monthly Enquiry Trends')
            fig7.update_layout(xaxis_title='Month', yaxis_title='Number of Enquiries')
            st.plotly_chart(fig7, use_container_width=True)
        else:
            st.info("No data available for monthly trend analysis")
    except Exception as e:
        st.info("No data available for monthly trend analysis")

    # Hourly Distribution Analysis
    with col2:
        st.write("### Hourly Distribution")
        try:
            # Fix dt issues by using pandas functions explicitly
            enquiry_date_series = pd.Series(filtered_df['Enquiry Date'])
            hour_series = pd.to_datetime(enquiry_date_series).dt.hour
            hourly_counts = pd.Series(hour_series).value_counts().sort_index()
                
            if not hourly_counts.empty:
                fig8 = px.bar(x=hourly_counts.index, y=hourly_counts.values,
                              title='Enquiries by Hour of Day')
                fig8.update_layout(xaxis_title='Hour of Day', yaxis_title='Number of Enquiries')
                st.plotly_chart(fig8, use_container_width=True)
            else:
                st.info("No data available for hourly distribution")
        except Exception as e:
            st.info("No data available for hourly distribution")

    # College-Specialization Heatmap
    st.write("### College-Specialization Analysis")
    try:
        # Fix groupby issues by using pandas functions explicitly
        college_series = pd.Series(filtered_df['College'])
        specialization_series = pd.Series(filtered_df['Specialization'])
            
        # Create a DataFrame for groupby operation
        college_spec_data = pd.DataFrame({
            'College': college_series,
            'Specialization': specialization_series
        })
            
        college_spec_groups = college_spec_data.groupby(['College', 'Specialization'])
        college_spec_counts_series = college_spec_groups.size()
            
        # Fix reset_index issue
        college_spec_counts = pd.DataFrame({
            'College': college_spec_counts_series.index.get_level_values(0),
            'Specialization': college_spec_counts_series.index.get_level_values(1),
            'Count': college_spec_counts_series.values
        })
            
        if not college_spec_counts.empty:
            # Create pivot table for heatmap
            pivot_table = college_spec_counts.pivot_table(
                index='College', 
                columns='Specialization', 
                values='Count', 
                fill_value=0
            )
                
            fig9 = px.imshow(
                pivot_table,
                title='College-Specialization Distribution Heatmap',
                color_continuous_scale=px.colors.sequential.Viridis
            )
            fig9.update_layout(
                xaxis_title='Specialization',
                yaxis_title='College'
            )
            st.plotly_chart(fig9, use_container_width=True)
        else:
            st.info("No data available for college-specialization analysis")
    except Exception as e:
        st.info("No data available for college-specialization analysis")

    # College Performance Analysis
    st.write("### College Performance")
    try:
        # Fix value_counts issues by using pandas functions explicitly
        college_counts = pd.Series(filtered_df['College']).value_counts()
            
        if not college_counts.empty:
            fig10 = px.bar(x=college_counts.index, y=college_counts.values,
                           title='Enquiries by College')
            fig10.update_layout(xaxis_title='College', yaxis_title='Number of Enquiries')
            st.plotly_chart(fig10, use_container_width=True)
        else:
            st.info("No data available for college performance analysis")
    except Exception as e:
        st.info("No data available for college performance analysis")
        
    # Enhanced Analysis Section
    st.subheader("Enhanced Analysis")
        
    # Additional Charts and Analysis Parameters
    enh_col1, enh_col2, enh_col3 = st.columns(3)
        
    with enh_col1:
        # Enquiry Type Analysis
        if 'Enquiry Type' in filtered_df.columns:
            try:
                enquiry_type_counts = pd.Series(filtered_df['Enquiry Type']).value_counts()
                if not enquiry_type_counts.empty:
                    fig_enq_type = px.pie(values=enquiry_type_counts.values, names=enquiry_type_counts.index,
                                             title='Enquiry Type Distribution')
                    st.plotly_chart(fig_enq_type, use_container_width=True)
            except Exception as e:
                st.info("Unable to create enquiry type analysis")
        
        with enh_col2:
            # Gender Distribution Analysis
            if 'Gender' in filtered_df.columns:
                try:
                    gender_counts = pd.Series(filtered_df['Gender']).value_counts()
                    if not gender_counts.empty:
                        fig_gender = px.bar(x=gender_counts.index, y=gender_counts.values,
                                           title='Gender Distribution',
                                           color_discrete_sequence=['#FF6699'])
                        st.plotly_chart(fig_gender, use_container_width=True)
                except Exception as e:
                    st.info("Unable to create gender distribution analysis")
        
        with enh_col3:
            # Allotment Status Analysis
            if 'Allotment Status' in filtered_df.columns:
                try:
                    allotment_counts = pd.Series(filtered_df['Allotment Status']).value_counts()
                    if not allotment_counts.empty:
                        fig_allotment = px.pie(values=allotment_counts.values, names=allotment_counts.index,
                                              title='Allotment Status Distribution')
                        st.plotly_chart(fig_allotment, use_container_width=True)
                except Exception as e:
                    st.info("Unable to create allotment status analysis")
        
        # Advanced Visualizations
        st.subheader("Advanced Visualizations")
        adv_col1, adv_col2 = st.columns(2)
        
        with adv_col1:
            # Time Series Analysis
            if 'Enquiry Date' in filtered_df.columns:
                try:
                    # Create daily enquiry counts
                    daily_counts = filtered_df.groupby(filtered_df['Enquiry Date'].dt.date).size()
                    if not daily_counts.empty:
                        fig_time_series = px.line(x=daily_counts.index, y=daily_counts.values,
                                                 title='Daily Enquiry Trends')
                        fig_time_series.update_layout(xaxis_title='Date', yaxis_title='Number of Enquiries')
                        st.plotly_chart(fig_time_series, use_container_width=True)
                except Exception as e:
                    st.info("Unable to create time series analysis")
        
        with adv_col2:
            # Hourly Analysis
            if 'Hour' in filtered_df.columns:
                try:
                    hourly_counts = filtered_df['Hour'].value_counts().sort_index()
                    if not hourly_counts.empty:
                        fig_hourly = px.bar(x=hourly_counts.index, y=hourly_counts.values,
                                           title='Enquiries by Hour of Day')
                        fig_hourly.update_layout(xaxis_title='Hour', yaxis_title='Number of Enquiries')
                        st.plotly_chart(fig_hourly, use_container_width=True)
                except Exception as e:
                    st.info("Unable to create hourly analysis")
        
        # Multi-dimensional Analysis
        st.subheader("Multi-dimensional Analysis")
        
        # Heatmap for College vs Specialization
        if 'College' in filtered_df.columns and 'Specialization' in filtered_df.columns:
            try:
                # Create a pivot table for heatmap
                pivot_data = filtered_df.groupby(['College', 'Specialization']).size().reset_index(name='Count')
                if not pivot_data.empty:
                    pivot_table = pivot_data.pivot_table(index='College', columns='Specialization', values='Count', fill_value=0)
                    fig_heatmap = px.imshow(pivot_table, 
                                           title='College vs Specialization Heatmap',
                                           color_continuous_scale='Viridis')
                    st.plotly_chart(fig_heatmap, use_container_width=True)
            except Exception as e:
                st.info("Unable to create college-specialization heatmap")
        
        # Scatter Plot Analysis
        if 'Year' in filtered_df.columns and 'Month' in filtered_df.columns:
            try:
                # Create a scatter plot of enquiries by year and month
                yearly_monthly = filtered_df.groupby(['Year', 'Month']).size().reset_index(name='Count')
                if not yearly_monthly.empty:
                    fig_scatter = px.scatter(yearly_monthly, x='Month', y='Year', size='Count', color='Count',
                                            title='Enquiries by Year and Month',
                                            color_continuous_scale='Plasma')
                    st.plotly_chart(fig_scatter, use_container_width=True)
            except Exception as e:
                st.info("Unable to create year-month scatter analysis")

        # Additional information
        st.markdown("""
        <div class="info-box">
            <h4>🔗 Integration Information:</h4>
            <p>This dashboard is part of the Admission Analytics Suite, which includes:</p>
            <ul>
                <li>📞 Enquiry Dashboard (current)</li>
                <li>🎓 Applicant Dashboard</li>
                <li>🏫 Admission Dashboard</li>
            </ul>
            <p>Run the master dashboard to access all modules from a single interface.</p>
        </div>
        """, unsafe_allow_html=True)

