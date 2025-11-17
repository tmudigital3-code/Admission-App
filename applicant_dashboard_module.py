import streamlit as st
import pandas as pd
import os
import glob
import plotly.express as px
import plotly.graph_objects as go

def render_applicant_dashboard(uploaded_files=None):
    """Render the applicant dashboard content"""
    
    # Enhanced Professional header with custom styling
    st.markdown("""
    <style>
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .title {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.2em;
        opacity: 0.9;
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
    <div class="header">
        <div class="title">🎓 Applicant Analytics Dashboard</div>
        <div class="subtitle">Comprehensive insights into applicant data</div>
    </div>
    """, unsafe_allow_html=True)

    # Add a horizontal line for separation
    st.markdown("---")

    # Professional sidebar styling
    st.sidebar.markdown('<div class="sidebar-header">🔍 Filters</div>', unsafe_allow_html=True)

    # Function to load and clean data
    @st.cache_data
    def load_data(uploaded_files=None):
        if uploaded_files and len(uploaded_files) > 0:
            # Load uploaded files
            dataframes = []
            for uploaded_file in uploaded_files:
                try:
                    df = pd.read_csv(uploaded_file)
                    # Clean column names - remove extra quotes and equal signs
                    df.columns = df.columns.str.replace('="', '').str.replace('""', '').str.replace('"', '')
                    # Clean data - remove extra quotes from string columns
                    for col in df.columns:
                        if df[col].dtype == 'object':
                            df[col] = df[col].astype(str).str.replace('="', '').str.replace('""', '').str.replace('"', '').str.replace('=', '')
                    dataframes.append(df)
                except Exception as e:
                    st.warning(f"Error loading file {uploaded_file.name}: {str(e)}")
                    continue
            
            # Combine all dataframes
            if dataframes:
                combined_df = pd.concat(dataframes, ignore_index=True)
                # Further clean data values to remove any remaining quotes
                for col in combined_df.columns:
                    if combined_df[col].dtype == 'object':
                        combined_df[col] = combined_df[col].astype(str).str.replace('=', '').str.replace('"', '').str.replace('""', '')
                return combined_df
            else:
                return pd.DataFrame()
        else:
            # Get all CSV files in the applicant data directory
            csv_files = glob.glob("applicant data/*.csv")
            
            # Load all CSV files and combine them
            dataframes = []
            for file in csv_files:
                try:
                    df = pd.read_csv(file)
                    # Clean column names - remove extra quotes and equal signs
                    df.columns = df.columns.str.replace('="', '').str.replace('""', '').str.replace('"', '')
                    # Clean data - remove extra quotes from string columns
                    for col in df.columns:
                        if df[col].dtype == 'object':
                            df[col] = df[col].astype(str).str.replace('="', '').str.replace('""', '').str.replace('"', '').str.replace('=', '')
                    dataframes.append(df)
                except Exception as e:
                    st.warning(f"Error loading file {file}: {str(e)}")
                    continue
            
            # Combine all dataframes
            if dataframes:
                combined_df = pd.concat(dataframes, ignore_index=True)
                # Further clean data values to remove any remaining quotes
                for col in combined_df.columns:
                    if combined_df[col].dtype == 'object':
                        combined_df[col] = combined_df[col].astype(str).str.replace('=', '').str.replace('"', '').str.replace('""', '')
                return combined_df
            else:
                return pd.DataFrame()

    # Check if files were uploaded from master dashboard
    if uploaded_files is not None and len(uploaded_files) > 0:
        df = load_data(uploaded_files)
        for uploaded_file in uploaded_files:
            st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
    else:
        # If no files were uploaded from master dashboard, load default data silently
        df = load_data()
    
    if df.empty:
        st.info("No data found. Please upload CSV files using the uploader in the sidebar, or check the 'applicant data' directory for existing files.")
        st.markdown("""
        <div class="info-box">
            <h4>💡 Tips for Using This Dashboard:</h4>
            <ul>
                <li>Upload CSV files containing applicant data</li>
                <li>Ensure your data includes columns like: Allotment Status, Level, Discipline, College</li>
                <li>Use the filters in the sidebar to analyze specific segments</li>
                <li>Download filtered data using the download button in the Data tab</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display column names for debugging
        # st.write("Column names:", df.columns.tolist())
        
        # Check if required columns exist
        required_columns = ['Allotment Status', 'Level', 'Discipline', 'College']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {missing_columns}")
            st.write("Available columns:", df.columns.tolist())
        else:
            # Sidebar filters
            st.sidebar.header("Filters")
            
            # Filter by Allotment Status
            allotment_status = st.sidebar.multiselect(
                "Select Allotment Status:",
                options=df["Allotment Status"].unique(),
                default=df["Allotment Status"].unique(),
                key="applicant_allotment_status"
            )
            
            # Filter by Level
            level = st.sidebar.multiselect(
                "Select Level:",
                options=df["Level"].unique(),
                default=df["Level"].unique(),
                key="applicant_level"
            )
            
            # Filter by Discipline
            discipline = st.sidebar.multiselect(
                "Select Discipline:",
                options=df["Discipline"].unique(),
                default=df["Discipline"].unique(),
                key="applicant_discipline"
            )
            
            # Filter by College
            college = st.sidebar.multiselect(
                "Select College:",
                options=df["College"].unique(),
                default=df["College"].unique(),
                key="applicant_college"
            )
            
            # Apply filters
            filtered_df = df[
                (df["Allotment Status"].isin(allotment_status)) &
                (df["Level"].isin(level)) &
                (df["Discipline"].isin(discipline)) &
                (df["College"].isin(college))
            ]
            
            # Main dashboard with professional styling
            st.markdown("""
            <div class="metrics-container">
                <div class="metrics-title">📊 Key Metrics</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Key metrics with improved styling
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Applicants", len(filtered_df), delta_color="normal")
            
            with col2:
                allotted_count = len(filtered_df[filtered_df["Allotment Status"] == "Allotted"])
                st.metric("Allotted Applicants", allotted_count, delta=allotted_count - len(filtered_df) // 2, delta_color="normal")
            
            with col3:
                not_allotted_count = len(filtered_df[filtered_df["Allotment Status"] == "Not Allotted"])
                st.metric("Not Allotted", not_allotted_count, delta=not_allotted_count - len(filtered_df) // 2, delta_color="inverse")
            
            with col4:
                # Fix type checking issue for nunique by using pandas functions explicitly
                if "Program" in filtered_df.columns:
                    try:
                        unique_programs = pd.Series(filtered_df["Program"]).nunique()
                    except Exception:
                        unique_programs = 0
                else:
                    unique_programs = 0
                st.metric("Programs Applied", int(unique_programs), delta_color="normal")
            
            # Professional tabs styling
            st.markdown("""
            <style>
            .tabs-container {
                margin-top: 20px;
            }
            </style>
            <div class="tabs-container">
            </div>
            """, unsafe_allow_html=True)
            
            # Tabs for different views
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Charts", "🔍 Advanced Analysis", "📋 Data", "ℹ️ About"])
            
            with tab1:
                st.subheader("Applicant Distribution")
                
                # Allotment Status Distribution
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("### By Allotment Status")
                    # Fix type checking issue by using pandas functions explicitly
                    try:
                        allotment_counts = pd.Series(filtered_df["Allotment Status"]).value_counts()
                    except Exception:
                        allotment_counts = pd.Series()
                    fig_allotment = px.pie(
                        values=allotment_counts.values,
                        names=allotment_counts.index,
                        title="Applicant Distribution by Allotment Status",
                        color_discrete_sequence=px.colors.sequential.Viridis
                    )
                    fig_allotment.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="#2c3e50"),
                        title=dict(font=dict(size=16))
                    )
                    st.plotly_chart(fig_allotment, use_container_width=True)
                
                with col2:
                    st.write("### By Level")
                    # Fix type checking issue by using pandas functions explicitly
                    try:
                        level_counts = pd.Series(filtered_df["Level"]).value_counts()
                    except Exception:
                        level_counts = pd.Series()
                    fig_level = px.bar(
                        x=level_counts.index,
                        y=level_counts.values,
                        title="Applicant Distribution by Level",
                        labels={"x": "Level", "y": "Number of Applicants"},
                        color_discrete_sequence=px.colors.sequential.Plasma
                    )
                    fig_level.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="#2c3e50"),
                        title=dict(font=dict(size=16))
                    )
                    st.plotly_chart(fig_level, use_container_width=True)
            
            with tab2:
                st.subheader("Detailed Analysis")
                
                # Discipline Distribution
                st.write("### By Discipline")
                # Fix type checking issue by using pandas functions explicitly
                try:
                    discipline_counts = pd.Series(filtered_df["Discipline"]).value_counts().head(10)
                except Exception:
                    discipline_counts = pd.Series()
                fig_discipline = px.bar(
                    x=discipline_counts.values,
                    y=discipline_counts.index,
                    orientation='h',
                    title="Top 10 Disciplines by Number of Applicants",
                    labels={"x": "Number of Applicants", "y": "Discipline"},
                    color_discrete_sequence=px.colors.sequential.Inferno
                )
                fig_discipline.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#2c3e50"),
                    title=dict(font=dict(size=16))
                )
                st.plotly_chart(fig_discipline, use_container_width=True)
                
                # College Distribution
                st.write("### By College")
                # Fix type checking issue by using pandas functions explicitly
                try:
                    college_counts = pd.Series(filtered_df["College"]).value_counts()
                except Exception:
                    college_counts = pd.Series()
                fig_college = px.bar(
                    x=college_counts.index,
                    y=college_counts.values,
                    title="Applicant Distribution by College",
                    labels={"x": "College", "y": "Number of Applicants"},
                    color_discrete_sequence=px.colors.sequential.Magma
                )
                fig_college.update_layout(
                    xaxis_tickangle=-45,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#2c3e50"),
                    title=dict(font=dict(size=16))
                )
                st.plotly_chart(fig_college, use_container_width=True)
                
                # Allotment Status by Level
                st.write("### Allotment Status by Level")
                allotment_by_level = pd.crosstab(filtered_df["Level"], filtered_df["Allotment Status"])
                fig_allotment_level = px.bar(
                    allotment_by_level,
                    title="Allotment Status Distribution by Level",
                    labels={"value": "Number of Applicants"},
                    color_discrete_sequence=px.colors.sequential.Cividis
                )
                fig_allotment_level.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#2c3e50"),
                    title=dict(font=dict(size=16))
                )
                st.plotly_chart(fig_allotment_level, use_container_width=True)
            
            with tab3:
                st.subheader("Advanced Analysis")
                
                # Create tabs for different advanced analysis sections
                analysis_tab1, analysis_tab2, analysis_tab3 = st.tabs(["📈 Rate Analysis", "📊 Correlation Analysis", "🔮 Predictive Insights"])
                
                with analysis_tab1:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Allotment Rate by Discipline
                        st.write("### Allotment Rate by Discipline")
                        discipline_allotment = pd.crosstab(filtered_df["Discipline"], filtered_df["Allotment Status"], margins=True)
                        if 'Allotted' in discipline_allotment.columns and 'Not Allotted' in discipline_allotment.columns:
                            discipline_allotment['Allotment Rate'] = discipline_allotment['Allotted'] / discipline_allotment['All'] * 100
                            discipline_rate = discipline_allotment.sort_values('Allotment Rate', ascending=False)['Allotment Rate'].head(10)
                            fig_discipline_rate = px.bar(
                                x=discipline_rate.values,
                                y=discipline_rate.index,
                                orientation='h',
                                title="Top 10 Disciplines by Allotment Rate",
                                labels={"x": "Allotment Rate (%)", "y": "Discipline"},
                                color_discrete_sequence=px.colors.sequential.Inferno
                            )
                            fig_discipline_rate.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color="#2c3e50"),
                                title=dict(font=dict(size=16))
                            )
                            st.plotly_chart(fig_discipline_rate, use_container_width=True)
                    
                    with col2:
                        # Allotment Rate by College
                        st.write("### Allotment Rate by College")
                        college_allotment = pd.crosstab(filtered_df["College"], filtered_df["Allotment Status"], margins=True)
                        if 'Allotted' in college_allotment.columns and 'Not Allotted' in college_allotment.columns:
                            college_allotment['Allotment Rate'] = college_allotment['Allotted'] / college_allotment['All'] * 100
                            college_rate = college_allotment.sort_values('Allotment Rate', ascending=False)['Allotment Rate'].head(10)
                            fig_college_rate = px.bar(
                                x=college_rate.values,
                                y=college_rate.index,
                                orientation='h',
                                title="Top 10 Colleges by Allotment Rate",
                                labels={"x": "Allotment Rate (%)", "y": "College"},
                                color_discrete_sequence=px.colors.sequential.Magma
                            )
                            fig_college_rate.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color="#2c3e50"),
                                title=dict(font=dict(size=16))
                            )
                            st.plotly_chart(fig_college_rate, use_container_width=True)
                    
                    # Program Popularity Analysis
                    if "Program" in filtered_df.columns:
                        st.write("### Program Popularity Analysis")
                        # Fix type checking issue by using pandas functions explicitly
                        try:
                            program_counts = pd.Series(filtered_df["Program"]).value_counts().head(10)
                        except Exception:
                            program_counts = pd.Series()
                        fig_programs = px.bar(
                            x=program_counts.values,
                            y=program_counts.index,
                            orientation='h',
                            title="Top 10 Most Popular Programs",
                            labels={"x": "Number of Applicants", "y": "Program"},
                            color_discrete_sequence=px.colors.sequential.Viridis
                        )
                        fig_programs.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="#2c3e50"),
                            title=dict(font=dict(size=16))
                        )
                        st.plotly_chart(fig_programs, use_container_width=True)
                
                with analysis_tab2:
                    # Level vs Discipline Heatmap and Correlation Analysis
                    st.write("### Level vs Discipline Analysis")
                    
                    # Create a copy of the filtered data for correlation analysis
                    corr_df = filtered_df.copy()
                    
                    # Convert categorical variables to numerical for correlation analysis
                    if 'Allotment Status' in corr_df.columns:
                        # Fix map issue by using pandas functions explicitly
                        try:
                            allotment_mapping = {'Allotted': 1, 'Not Allotted': 0}
                            corr_df['Allotment_Status_Num'] = pd.Series(corr_df['Allotment Status']).map(allotment_mapping)
                        except Exception:
                            corr_df['Allotment_Status_Num'] = pd.Series([0] * len(corr_df))
                    
                    if 'Level' in corr_df.columns:
                        # Fix unique and map issues by using pandas functions explicitly
                        try:
                            level_series = pd.Series(corr_df['Level'])
                            level_mapping = {level: idx for idx, level in enumerate(level_series.unique())}
                            corr_df['Level_Num'] = level_series.map(level_mapping)
                        except Exception:
                            corr_df['Level_Num'] = pd.Series([0] * len(corr_df))
                    
                    # Select only numerical columns for correlation analysis
                    numerical_cols = corr_df.select_dtypes(include=['number']).columns.tolist()
                    
                    if len(numerical_cols) > 1:
                        try:
                            # Fix corr issue by ensuring we're working with a DataFrame
                            correlation_matrix = pd.DataFrame(corr_df[numerical_cols]).corr()
                            fig_corr = px.imshow(
                                correlation_matrix,
                                title="Correlation Matrix of Numerical Variables",
                                color_continuous_scale=px.colors.sequential.Viridis
                            )
                            fig_corr.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color="#2c3e50"),
                                title=dict(font=dict(size=16))
                            )
                            st.plotly_chart(fig_corr, use_container_width=True)
                        except Exception as e:
                            st.warning("Unable to compute correlation matrix.")
                    else:
                        st.info("Not enough numerical variables for correlation analysis.")
                
                with analysis_tab3:
                    # Predictive Insights and Recommendations
                    st.write("### Predictive Insights")
                    
                    # Discipline Success Rate Analysis
                    st.write("### Discipline Success Rate")
                    # Fix crosstab normalize parameter issue
                    try:
                        discipline_success = pd.crosstab(
                            pd.Series(filtered_df['Discipline']), 
                            pd.Series(filtered_df['Allotment Status']), 
                            normalize=True
                        )
                        if 'Allotted' in discipline_success.columns:
                            discipline_success_rate = discipline_success['Allotted'] * 100
                            discipline_success_df = pd.DataFrame({
                                'Discipline': discipline_success_rate.index,
                                'Success Rate (%)': discipline_success_rate.values
                            }).sort_values('Success Rate (%)', ascending=False).head(10)
                            
                            fig_discipline_success = px.bar(
                                discipline_success_df,
                                x='Success Rate (%)',
                                y='Discipline',
                                orientation='h',
                                title="Top 10 Disciplines by Success Rate",
                                labels={"Success Rate (%)": "Success Rate (%)"},
                                color='Success Rate (%)',
                                color_continuous_scale=px.colors.sequential.Viridis
                            )
                            fig_discipline_success.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color="#2c3e50"),
                                title=dict(font=dict(size=16))
                            )
                            st.plotly_chart(fig_discipline_success, use_container_width=True)
                    except Exception as e:
                        st.warning("Unable to compute discipline success rate analysis.")
                    
                    # Calculate success factors
                    if 'Allotment Status' in filtered_df.columns and 'Discipline' in filtered_df.columns:
                        # Discipline success rate
                        try:
                            # Fix crosstab normalize parameter issue
                            discipline_crosstab = pd.crosstab(
                                pd.Series(filtered_df['Discipline']), 
                                pd.Series(filtered_df['Allotment Status'])
                            )
                            # Normalize manually
                            discipline_success = discipline_crosstab.div(discipline_crosstab.sum(axis=1), axis=0)
                            
                            if 'Allotted' in discipline_success.columns:
                                top_disciplines = discipline_success['Allotted'].sort_values(ascending=False).head(5)
                                st.write("**Top 5 Disciplines by Allotment Rate:**")
                                for discipline, rate in top_disciplines.items():
                                    st.write(f"- {discipline}: {rate:.2%}")
                        except Exception as e:
                            pass
                    
                    if 'Allotment Status' in filtered_df.columns and 'College' in filtered_df.columns:
                        # College success rate
                        try:
                            # Fix crosstab normalize parameter issue
                            college_crosstab = pd.crosstab(
                                pd.Series(filtered_df['College']), 
                                pd.Series(filtered_df['Allotment Status'])
                            )
                            # Normalize manually
                            college_success = college_crosstab.div(college_crosstab.sum(axis=1), axis=0)
                             
                            if 'Allotted' in college_success.columns:
                                top_colleges = college_success['Allotted'].sort_values(ascending=False).head(5)
                                st.write("**Top 5 Colleges by Allotment Rate:**")
                                for college, rate in top_colleges.items():
                                    st.write(f"- {college}: {rate:.2%}")
                        except Exception as e:
                            pass
                     
                    # Program diversity analysis
                    if 'Program' in filtered_df.columns:
                        try:
                            # Fix nunique issue by using pandas functions explicitly
                            unique_programs = pd.Series(filtered_df['Program']).nunique()
                            total_applicants = len(filtered_df)
                            diversity_ratio = unique_programs / total_applicants if total_applicants > 0 else 0
                            
                            st.write("**Program Diversity Metrics:**")
                            st.write(f"- Unique Programs: {unique_programs}")
                            st.write(f"- Diversity Ratio: {diversity_ratio:.2%}")
                        except Exception as e:
                            pass

                    # Data Insights Section
                    st.subheader("Data Insights")
                    
                    # Add more analysis parameters
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Level distribution analysis
                        if 'Level' in filtered_df.columns:
                            level_dist = filtered_df['Level'].value_counts()
                            fig_level = px.bar(x=level_dist.index, y=level_dist.values,
                                              title="Applicant Distribution by Level",
                                              color_discrete_sequence=['#00CC96'])
                            st.plotly_chart(fig_level, use_container_width=True)
                    
                    with col2:
                        # Discipline distribution analysis
                        if 'Discipline' in filtered_df.columns:
                            discipline_dist = filtered_df['Discipline'].value_counts().head(10)
                            fig_discipline = px.bar(x=discipline_dist.index, y=discipline_dist.values,
                                                   title="Top 10 Disciplines",
                                                   color_discrete_sequence=['#AB63FA'])
                            fig_discipline.update_layout(xaxis_tickangle=-45)
                            st.plotly_chart(fig_discipline, use_container_width=True)
                    
                    with col3:
                        # College distribution analysis
                        if 'College' in filtered_df.columns:
                            college_dist = filtered_df['College'].value_counts().head(10)
                            fig_college = px.bar(x=college_dist.index, y=college_dist.values,
                                                title="Top 10 Colleges",
                                                color_discrete_sequence=['#FFA15A'])
                            fig_college.update_layout(xaxis_tickangle=-45)
                            st.plotly_chart(fig_college, use_container_width=True)
                    
                    # Advanced Visualizations
                    st.subheader("Advanced Analysis")
                    adv_col1, adv_col2 = st.columns(2)
                    
                    with adv_col1:
                        # Allotment Status Analysis with Multiple Chart Types
                        if 'Allotment Status' in filtered_df.columns:
                            status_counts = filtered_df['Allotment Status'].value_counts()
                            
                            # Bar Chart
                            fig_status_bar = px.bar(x=status_counts.index, y=status_counts.values,
                                                   title="Allotment Status Distribution (Bar)",
                                                   color_discrete_sequence=['#636EFA'])
                            st.plotly_chart(fig_status_bar, use_container_width=True)
                            
                            # Pie Chart
                            fig_status_pie = px.pie(values=status_counts.values, names=status_counts.index,
                                                   title="Allotment Status Distribution (Pie)")
                            st.plotly_chart(fig_status_pie, use_container_width=True)
                    
                    with adv_col2:
                        # Heatmap Analysis
                        if 'Level' in filtered_df.columns and 'Allotment Status' in filtered_df.columns:
                            try:
                                # Create a crosstab for heatmap
                                crosstab = pd.crosstab(filtered_df['Level'], filtered_df['Allotment Status'])
                                fig_heatmap = px.imshow(crosstab, 
                                                       title="Level vs Allotment Status Heatmap",
                                                       color_continuous_scale='RdBu')
                                st.plotly_chart(fig_heatmap, use_container_width=True)
                            except Exception as e:
                                st.info("Unable to create heatmap analysis.")
                        
                        # Box Plot for Numerical Analysis
                        if 'Level' in filtered_df.columns:
                            fig_box = px.box(filtered_df, x='Level', y=filtered_df.index,
                                            title="Distribution of Applications by Level",
                                            color_discrete_sequence=['#FECB52'])
                            st.plotly_chart(fig_box, use_container_width=True)
