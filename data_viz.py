import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_data, apply_display_mappings, AGE_MAP, EDU_MAP, WORK_MAP, MARITAL_MAP, INCOME_MAP, POVERTY_MAP, YES_NO_MAP, ALCPDANG_MAP


def show_data_visualization():
    """
    Displays the interactive data visualization dashboard.
    Loads data, applies filters, and generates various plots.
    """
    df = load_data()
    df_display = apply_display_mappings(df)


    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 1rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem;
        }
        .insight-box {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #1f77b4;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    
    st.markdown('<h1 class="main-header">📊 Descriptive Analysis of the Dataset</h1>', unsafe_allow_html=True)

    
    st.sidebar.markdown("---") 
    if st.sidebar.button("← Back to Home", key="back_to_home_sidebar"):
        st.session_state.page = 'home'
        st.rerun()
    st.sidebar.markdown("---")

    st.sidebar.markdown("### 🔍 Filter Options")

    age_options = sorted(df["age2"].dropna().unique())
    selected_age_codes = st.sidebar.multiselect(
        "Select Age Group(s):",
        options=age_options,
        default=age_options,
        format_func=lambda x: AGE_MAP.get(x, str(x)),
        help="Filter by age groups"
    )

    # Education level filter - Use format_func for display
    edu_options = sorted(df["eduhighcat"].dropna().unique())
    selected_edu_codes = st.sidebar.multiselect(
        "Select Education Level(s):",
        options=edu_options,
        default=edu_options,
        format_func=lambda x: EDU_MAP.get(x, str(x)),
        help="Filter by education level"
    )

    # Employment status filter - Use format_func for display
    work_options = sorted(df["irwrkstat"].dropna().unique())
    selected_work_codes = st.sidebar.multiselect(
        "Select Employment Status:",
        options=work_options,
        default=work_options,
        format_func=lambda x: WORK_MAP.get(x, str(x)),
        help="Filter by employment status"
    )

    # Marital status filter - Use format_func for display
    marital_options = sorted(df["irmaritstat"].dropna().unique())
    selected_marital_codes = st.sidebar.multiselect(
        "Select Marital Status:",
        options=marital_options,
        default=marital_options,
        format_func=lambda x: MARITAL_MAP.get(x, str(x)),
        help="Filter by marital status"
    )

    # Apply filters using original numerical values
    filtered_df = df.copy()
    if selected_age_codes:
        filtered_df = filtered_df[filtered_df["age2"].isin(selected_age_codes)]
    if selected_edu_codes:
        filtered_df = filtered_df[filtered_df["eduhighcat"].isin(selected_edu_codes)]
    if selected_work_codes:
        filtered_df = filtered_df[filtered_df["irwrkstat"].isin(selected_work_codes)]
    if selected_marital_codes:
        filtered_df = filtered_df[filtered_df["irmaritstat"].isin(selected_marital_codes)]

    # Apply display mappings to the filtered DataFrame for plotting
    filtered_df_display = apply_display_mappings(filtered_df)


    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Dataset Info")
    st.sidebar.info(f"**Total Records:** {len(df):,}")
    st.sidebar.info(f"**Filtered Records:** {len(filtered_df):,}")
    st.sidebar.info(f"**Variables:** {len(df.columns)}")

    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview",
        "🌿 Marijuana Analysis",
        "🍷 Alcohol Analysis",
        "👥 Social Factors",
        "💰 Socioeconomic Impact",
        "🏥 Treatment & Risk"
    ])

    # Tab 1: Overview
    with tab1:
        st.markdown('<h2 class="sub-header">📊 Dataset Overview</h2>', unsafe_allow_html=True)
        st.markdown("This section provides a high-level summary of the dataset and key demographic distributions.")

        # Dataset Description and Image
        desc_col, img_col = st.columns([2, 2]) # Adjust column ratio as needed

        with desc_col:
            st.markdown(f"""
            Drug abuse among women is a complex issue influenced by both parental involvement and social environments. Research has shown that the absence of parental support,
            supervision, or open communication can increase vulnerability to substance use. Additionally, peer pressure and social acceptance of drugs—especially in close circles—can further encourage risky behavior.
            Understanding how these two forces interact is critical to developing targeted prevention and treatment strategies for women at risk.
            The dataset used in this research is derived from the **[National Survey on Drug Use and Health (NSDUH)](https://www.kaggle.com/datasets/bgallamoza/national-survey-of-drug-use-and-health-20152019)**,
            covering the years 2015 to 2019. 
            """)
        with img_col:
            # IMPORTANT: Update this image path if your image is not in the specified location
            st.image(r"C:\Users\zanny\Desktop\School\NCAIR Cohort\Data Science Beginners\Project\National Survey of Drug Use and Health\womens-picture2.jpg", use_container_width=True)

        st.markdown('<h2 class="sub-header">Key Metrics</h2>', unsafe_allow_html=True)
        st.write("These cards display essential summary statistics for the entire dataset and the filtered data, giving you an immediate sense of the scale and prevalence of substance use within the surveyed population.")

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Respondents", f"{len(filtered_df_display):,}")
        with col2:
            marijuana_users = len(filtered_df_display[filtered_df_display["mjever"] == 1])
            st.metric("Marijuana Users", f"{marijuana_users:,}",
                     f"{marijuana_users/len(filtered_df_display)*100:.1f}%")
        with col3:
            alcohol_users = len(filtered_df_display[filtered_df_display["alcever"] == 1])
            st.metric("Alcohol Users", f"{alcohol_users:,}",
                     f"{alcohol_users/len(filtered_df_display)*100:.1f}%")
        with col4:
            # Average age group might still be numerical, or we can map it to a representative label
            avg_age_code = filtered_df_display["age2"].mean()
            # Find the closest age group label for display
            closest_age_label = "N/A"
            if not pd.isna(avg_age_code):
                closest_age_code = min(AGE_MAP.keys(), key=lambda k: abs(k - avg_age_code))
                closest_age_label = AGE_MAP.get(closest_age_code, str(round(avg_age_code, 1)))
            st.metric("Average Age Group", closest_age_label)


        # Demographics overview
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Age Group Distribution")
            st.write("This bar chart shows the number of respondents falling into each defined age category. It helps you understand the age demographics of the survey participants.")
            # Age distribution - Use age2_label for x-axis
            age_dist = filtered_df_display["age2_label"].value_counts().reindex([AGE_MAP[k] for k in sorted(AGE_MAP.keys())], fill_value=0)
            fig_age = px.bar(
                x=age_dist.index,
                y=age_dist.values,
                title="Age Group Distribution",
                labels={"x": "Age Group", "y": "Count"},
                color=age_dist.values,
                color_continuous_scale="viridis",
                category_orders={"x": [AGE_MAP[k] for k in sorted(AGE_MAP.keys())]} # Ensure correct order
            )
            fig_age.update_layout(showlegend=False)
            st.plotly_chart(fig_age, use_container_width=True)

        with col2:
            st.markdown("### Education Level Distribution")
            st.write("This pie chart illustrates the proportion of respondents across different education levels, providing insight into the educational background of the surveyed women.")
            # Education distribution - Use eduhighcat_label for names
            edu_dist = filtered_df_display["eduhighcat_label"].value_counts().reindex([EDU_MAP[k] for k in sorted(EDU_MAP.keys())], fill_value=0)
            fig_edu = px.pie(
                values=edu_dist.values,
                names=edu_dist.index,
                title="Education Level Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3,
                category_orders={"names": [EDU_MAP[k] for k in sorted(EDU_MAP.keys())]} # Ensure correct order
            )
            st.plotly_chart(fig_edu, use_container_width=True)

        # Correlation heatmap
        st.markdown("### 🔥 Substance Use Correlation")
        st.write("This heatmap visualizes the statistical relationships between various substance use-related variables. Red colors (towards -1) indicate a strong negative correlation (as one variable increases, the other tends to decrease). Blue colors (towards +1) indicate a strong positive correlation (as one variable increases, the other also tends to increase). Colors near white/gray (near 0) indicate a weak or no linear correlation.")
        substance_cols = ["mjever", "alcever", "mjday30a", "alcydays", "mjage"]
        available_cols = [col for col in filtered_df_display.columns if col in substance_cols] # Ensure column exists

        if len(available_cols) > 1:
            corr_matrix = filtered_df_display[available_cols].corr(numeric_only=True) # Added numeric_only=True
            fig_corr = px.imshow(
                corr_matrix,
                color_continuous_scale="RdBu",
                title="Substance Use Correlation Matrix",
                aspect="auto"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Not enough numerical substance use columns available to compute correlation in the filtered data.")

    # Tab 2: Marijuana Analysis
    with tab2:
        st.markdown('<h2 class="sub-header">🌿 Marijuana Use Analysis</h2>', unsafe_allow_html=True)
        st.markdown("This tab focuses specifically on patterns and characteristics related to marijuana use.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Marijuana Use Rate by Age Group")
            st.write("This chart shows the percentage of women in each age group who have reported using marijuana. It helps identify which age demographics have higher or lower rates of marijuana use.")
            # Marijuana use by age group - Use age2_label for x-axis
            mj_age_data = filtered_df_display.groupby("age2_label")["mjever"].agg(["count", "sum"]).reset_index()
            mj_age_data["percentage"] = (mj_age_data["sum"] / mj_age_data["count"]) * 100

            fig_mj_age = px.bar(
                mj_age_data,
                x="age2_label",
                y="percentage",
                title="Marijuana Use Rate by Age Group",
                labels={"age2_label": "Age Group", "percentage": "Usage Rate (%)"},
                color="percentage",
                color_continuous_scale="greens",
                category_orders={"age2_label": [AGE_MAP[k] for k in sorted(AGE_MAP.keys())]} # Ensure correct order
            )
            st.plotly_chart(fig_mj_age, use_container_width=True)

        with col2:
            st.markdown("### Age at First Marijuana Use")
            st.write("This histogram displays the distribution of ages at which individuals first used marijuana. Peaks in the histogram indicate common ages for initiation.")
            # Age at first use (mjage is numerical, no mapping needed here)
            mj_first_use = filtered_df_display[filtered_df_display["mjage"] > 0]["mjage"]
            if len(mj_first_use) > 0:
                fig_mj_first = px.histogram(
                    mj_first_use,
                    nbins=20,
                    title="Age at First Marijuana Use",
                    labels={"value": "Age at First Use", "count": "Number of Users"},
                    color_discrete_sequence=["#2E8B57"]
                )
                st.plotly_chart(fig_mj_first, use_container_width=True)
            else:
                st.info("No data for Age at First Marijuana Use in the filtered selection.")


        # Usage frequency analysis
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Marijuana Use Frequency (Past 30 Days)")
            st.write("This chart illustrates how many days in the past 30 days respondents reported using marijuana. It gives insight into the intensity of recent use among users.")
            # Days used in past 30 days (mjday30a is numerical)
            mj_30_days = filtered_df_display[filtered_df_display["mjday30a"] > 0]["mjday30a"]
            if len(mj_30_days) > 0:
                fig_mj_30 = px.histogram(
                    mj_30_days,
                    nbins=15,
                    title="Marijuana Use Frequency (Past 30 Days)",
                    labels={"value": "Days Used", "count": "Number of Users"},
                    color_discrete_sequence=["#228B22"]
                )
                st.plotly_chart(fig_mj_30, use_container_width=True)
            else:
                st.info("No data for Marijuana Use Frequency (Past 30 Days) in the filtered selection.")

        with col2:
            st.markdown("### Marijuana Use Rate by Education Level")
            st.write("Similar to the age group analysis, this bar chart shows the percentage of women at different education levels who have used marijuana, revealing potential links between education and use.")
            # Marijuana use by education level - Use eduhighcat_label for x-axis
            mj_edu_data = filtered_df_display.groupby("eduhighcat_label")["mjever"].agg(["count", "sum"]).reset_index()
            mj_edu_data["percentage"] = (mj_edu_data["sum"] / mj_edu_data["count"]) * 100

            fig_mj_edu = px.bar(
                mj_edu_data,
                x="eduhighcat_label",
                y="percentage",
                title="Marijuana Use Rate by Education Level",
                labels={"eduhighcat_label": "Education Level", "percentage": "Usage Rate (%)"},
                color="percentage",
                color_continuous_scale="greens",
                category_orders={"eduhighcat_label": [EDU_MAP[k] for k in sorted(EDU_MAP.keys())]} # Ensure correct order
            )
            st.plotly_chart(fig_mj_edu, use_container_width=True)

 # Tab 3: Alcohol Analysis
    with tab3:
        st.markdown('<h2 class="sub-header">🍷 Alcohol Use Analysis</h2>', unsafe_allow_html=True)
        st.markdown("This section delves into various aspects of alcohol consumption and related behaviors.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Alcohol Use Days in Past Year")
            st.write("This histogram shows the distribution of the number of days respondents reported using alcohol in the past year, indicating frequency of consumption.")
            # Alcohol use days in past year (alcydays is numerical)
            alc_days = filtered_df_display[filtered_df_display["alcydays"] > 0]["alcydays"]
            if len(alc_days) > 0:
                fig_alc_days = px.histogram(
                    alc_days,
                    nbins=30,
                    title="Alcohol Use Days in Past Year",
                    labels={"value": "Days Used", "count": "Number of Users"},
                    color_discrete_sequence=["#8B0000"]
                )
                st.plotly_chart(fig_alc_days, use_container_width=True)
            else:
                st.info("No data for Alcohol Use Days in Past Year in the filtered selection.")

        with col2:
            st.markdown("### Binge Drinking Rate by Age Group")
            st.write("This chart displays the percentage of women in each age group who reported engaging in binge drinking in the past 30 days. It highlights age groups with higher rates of heavy episodic drinking.")
            # Binge drinking by age group - Use age2_label for x-axis
            binge_data = filtered_df_display.groupby("age2_label")["alcbng30d"].agg(["count", "sum"]).reset_index()
            binge_data["percentage"] = (binge_data["sum"] / binge_data["count"]) * 100

            fig_binge = px.bar(
                binge_data,
                x="age2_label",
                y="percentage",
                title="Binge Drinking Rate by Age Group",
                labels={"age2_label": "Age Group", "percentage": "Binge Drinking Rate (%)"},
                color="percentage",
                color_continuous_scale="reds",
                category_orders={"age2_label": [AGE_MAP[k] for k in sorted(AGE_MAP.keys())]} # Ensure correct order
            )
            st.plotly_chart(fig_binge, use_container_width=True)

        # Alcohol-related risks
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Drove Under Influence of Alcohol")
            st.write("This pie chart shows the proportion of respondents who reported driving under the influence of alcohol.")
            # Driving under influence - Use drvinalco_label for names
            dui_data = filtered_df_display["drvinalco_label"].value_counts().reindex(["No", "Yes"], fill_value=0)
            fig_dui = px.pie(
                values=dui_data.values,
                names=dui_data.index, # Use index which now contains "No", "Yes"
                title="Drove Under Influence of Alcohol",
                color_discrete_sequence=["#90EE90", "#FF6B6B"]
            )
            st.plotly_chart(fig_dui, use_container_width=True)

        with col2:
            st.markdown("### Alcohol Caused Dangerous Situations")
            st.write("This pie chart indicates the percentage of individuals who reported experiencing dangerous situations as a result of their alcohol use.")
            # Alcohol-related dangerous situations - Use alcpdang_label for names
            if "alcpdang_label" in filtered_df_display.columns:
                danger_data = filtered_df_display["alcpdang_label"].value_counts().reindex([ALCPDANG_MAP[k] for k in sorted(ALCPDANG_MAP.keys())], fill_value=0)
                if not danger_data.empty and danger_data.sum() > 0:
                    fig_danger = px.pie(
                        values=danger_data.values,
                        names=danger_data.index, # Use index which now contains labels
                        title="Alcohol Caused Dangerous Situations",
                        color_discrete_sequence=["#98FB98", "#FF4500"],
                        category_orders={"names": [ALCPDANG_MAP[k] for k in sorted(ALCPDANG_MAP.keys())]}
                    )
                    st.plotly_chart(fig_danger, use_container_width=True)
                else:
                    st.info("No data for Alcohol Caused Dangerous Situations in the filtered selection.")
            else:
                st.info("Column 'alcpdang_label' not found in the filtered dataset.")


    # Tab 4: Social Factors
    with tab4:
        st.markdown('<h2 class="sub-header">👥 Social Factors Analysis</h2>', unsafe_allow_html=True)
        st.markdown("This tab explores how social environments and relationships influence substance use.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Marijuana Use by Parental Presence")
            st.write("This chart compares marijuana use rates based on whether the mother and/or father were present in the household. It helps assess the impact of parental presence.")
            # Parental influence on marijuana use - Use imother_label and ifather_label
            # Create a combined label for parental status
            parent_data_display = filtered_df_display.copy()
            if 'imother_label' in parent_data_display.columns and 'ifather_label' in parent_data_display.columns:
                parent_data_display['parent_status_label'] = parent_data_display.apply(
                    lambda row: f"Mother: {row['imother_label']}, Father: {row['ifather_label']}", axis=1
                )
                parent_agg = parent_data_display.groupby("parent_status_label")["mjever"].agg(["count", "sum"]).reset_index()
                parent_agg["percentage"] = (parent_agg["sum"] / parent_agg["count"]) * 100

                # Define a custom order for parental status for better visualization
                parent_order = [
                    "Mother: Yes, Father: Yes",
                    "Mother: Yes, Father: No",
                    "Mother: No, Father: Yes",
                    "Mother: No, Father: No"
                ]
                # Reindex to ensure all categories are present, even if empty
                parent_agg_reindexed = parent_agg.set_index('parent_status_label').reindex(parent_order, fill_value=0).reset_index()
                parent_agg_reindexed['percentage'] = parent_agg_reindexed['percentage'].fillna(0) # Fill NaN percentages with 0

                fig_parent = px.bar(
                    parent_agg_reindexed,
                    x="parent_status_label",
                    y="percentage",
                    title="Marijuana Use by Parental Presence",
                    labels={"parent_status_label": "Parental Presence", "percentage": "Usage Rate (%)"},
                    color="percentage",
                    color_continuous_scale="blues",
                    category_orders={"parent_status_label": parent_order}
                )
                fig_parent.update_xaxes(tickangle=45)
                st.plotly_chart(fig_parent, use_container_width=True)
            else:
                st.info("Parental presence data (imother, ifather) not available in the filtered dataset.")


        with col2:
            st.markdown("### Marijuana Use by Friends' Marijuana Use (Past 30 Days)")
            st.write("This bar chart shows the percentage of marijuana users based on the number of close friends who also use marijuana. It illustrates the influence of peer behavior.")
            # Friend influence on marijuana use (frdmjmon is numerical)
            if "frdmjmon" in filtered_df_display.columns:
                friend_data = filtered_df_display.groupby("frdmjmon")["mjever"].agg(["count", "sum"]).reset_index()
                friend_data["percentage"] = (friend_data["sum"] / friend_data["count"]) * 100

                if not friend_data.empty:
                    fig_friend = px.bar(
                        friend_data,
                        x="frdmjmon",
                        y="percentage",
                        title="Marijuana Use by Friends' Marijuana Use (Past 30 Days)",
                        labels={"frdmjmon": "Number of Friends Using Marijuana (Past 30 Days)", "percentage": "Usage Rate (%)"},
                        color="percentage",
                        color_continuous_scale="purples"
                    )
                    st.plotly_chart(fig_friend, use_container_width=True)
                else:
                    st.info("No data for Friends' Marijuana Use in the filtered selection.")
            else:
                st.info("Column 'frdmjmon' not found in the filtered dataset.")

        # Household characteristics
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Substance Use by Household Size")
            st.write("This line chart plots the marijuana and alcohol use rates against the number of people in the household, revealing how household size might correlate with substance use.")
            # Household size vs substance use (irhhsiz2 is numerical)
            if "irhhsiz2" in filtered_df_display.columns:
                household_data = filtered_df_display.groupby("irhhsiz2")[["mjever", "alcever"]].mean().reset_index()
                household_data["mjever"] *= 100
                household_data["alcever"] *= 100

                if not household_data.empty:
                    fig_household = go.Figure()
                    fig_household.add_trace(go.Scatter(
                        x=household_data["irhhsiz2"],
                        y=household_data["mjever"],
                        mode="lines+markers",
                        name="Marijuana Use",
                        line=dict(color="green")
                    ))
                    fig_household.add_trace(go.Scatter(
                        x=household_data["irhhsiz2"],
                        y=household_data["alcever"],
                        mode="lines+markers",
                        name="Alcohol Use",
                        line=dict(color="red")
                    ))
                    fig_household.update_layout(
                        title="Substance Use by Household Size",
                        xaxis_title="Household Size",
                        yaxis_title="Usage Rate (%)"
                    )
                    st.plotly_chart(fig_household, use_container_width=True)
                else:
                    st.info("No data for Household Size in the filtered selection.")
            else:
                st.info("Column 'irhhsiz2' not found in the filtered dataset.")


        with col2:
            st.markdown("### Substance Use by Marital Status")
            st.write("This chart compares marijuana and alcohol use rates across different marital statuses, indicating potential associations between relationship status and substance use.")
            # Marital status vs substance use - Use irmaritstat_label for x-axis
            if "irmaritstat_label" in filtered_df_display.columns:
                marital_data = filtered_df_display.groupby("irmaritstat_label")[["mjever", "alcever"]].agg(["count", "sum"])
                marital_mj = (marital_data["mjever"]["sum"] / marital_data["mjever"]["count"]) * 100
                marital_alc = (marital_data["alcever"]["sum"] / marital_data["alcever"]["count"]) * 100

                # Reindex to ensure all categories are present, even if empty
                marital_order = [MARITAL_MAP[k] for k in sorted(MARITAL_MAP.keys())]
                marital_mj_reindexed = marital_mj.reindex(marital_order, fill_value=0).fillna(0)
                marital_alc_reindexed = marital_alc.reindex(marital_order, fill_value=0).fillna(0)

                if not marital_mj_reindexed.empty or not marital_alc_reindexed.empty:
                    fig_marital = go.Figure()
                    fig_marital.add_trace(go.Bar(
                        x=marital_mj_reindexed.index,
                        y=marital_mj_reindexed.values,
                        name="Marijuana Use",
                        marker_color="lightgreen"
                    ))
                    fig_marital.add_trace(go.Bar(
                        x=marital_alc_reindexed.index,
                        y=marital_alc_reindexed.values,
                        name="Alcohol Use",
                        marker_color="lightcoral"
                    ))
                    fig_marital.update_layout(
                        title="Substance Use by Marital Status",
                        xaxis_title="Marital Status",
                        yaxis_title="Usage Rate (%)",
                        barmode="group",
                        xaxis=dict(categoryorder='array', categoryarray=marital_order) # Ensure order
                    )
                    st.plotly_chart(fig_marital, use_container_width=True)
                else:
                    st.info("No data for Marital Status vs Substance Use in the filtered selection.")
            else:
                st.info("Column 'irmaritstat_label' not found in the filtered dataset.")

    # Tab 5: Socioeconomic Impact
    with tab5:
        st.markdown('<h2 class="sub-header">💰 Socioeconomic Impact Analysis</h2>', unsafe_allow_html=True)
        st.markdown("This section examines the connection between socioeconomic factors and substance use.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Substance Use by Income Level")
            st.write("This line chart displays the trends in marijuana and alcohol use rates across different annual family income categories.")
            # Income vs substance use - Use income_label for x-axis
            if "income_label" in filtered_df_display.columns:
                income_data = filtered_df_display.groupby("income_label")[["mjever", "alcever"]].agg(["count", "sum"]).reset_index()
                income_data[("mjever", "percentage")] = (income_data["mjever"]["sum"] / income_data["mjever"]["count"]) * 100
                income_data[("alcever", "percentage")] = (income_data["alcever"]["sum"] / income_data["alcever"]["count"]) * 100

                # Reindex to ensure all categories are present, even if empty
                income_order = [INCOME_MAP[k] for k in sorted(INCOME_MAP.keys())]
                income_data_reindexed = income_data.set_index('income_label').reindex(income_order, fill_value=0).reset_index()
                income_data_reindexed[("mjever", "percentage")] = income_data_reindexed[("mjever", "percentage")].fillna(0)
                income_data_reindexed[("alcever", "percentage")] = income_data_reindexed[("alcever", "percentage")].fillna(0)

                if not income_data_reindexed.empty:
                    fig_income = go.Figure()
                    fig_income.add_trace(go.Scatter(
                        x=income_data_reindexed["income_label"],
                        y=income_data_reindexed[("mjever", "percentage")],
                        mode="lines+markers",
                        name="Marijuana Use",
                        line=dict(color="green")
                    ))
                    fig_income.add_trace(go.Scatter(
                        x=income_data_reindexed["income_label"],
                        y=income_data_reindexed[("alcever", "percentage")],
                        mode="lines+markers",
                        name="Alcohol Use",
                        line=dict(color="red")
                    ))
                    fig_income.update_layout(
                        title="Substance Use by Income Level",
                        xaxis_title="Income Category",
                        yaxis_title="Usage Rate (%)",
                        xaxis=dict(categoryorder='array', categoryarray=income_order) # Ensure order
                    )
                    st.plotly_chart(fig_income, use_container_width=True)
                else:
                    st.info("No data for Income Level vs Substance Use in the filtered selection.")
            else:
                st.info("Column 'income_label' not found in the filtered dataset.")

        with col2:
            st.markdown("### Marijuana Use vs Poverty Level")
            st.write("This scatter plot shows the relationship between marijuana use rate and poverty level, with the size of the points potentially indicating the alcohol use rate for that group.")
            # Poverty level vs substance use - Use poverty3_label for x-axis
            if "poverty3_label" in filtered_df_display.columns:
                poverty_data = filtered_df_display.groupby("poverty3_label")[["mjever", "alcever"]].mean().reset_index()
                poverty_data["mjever"] *= 100
                poverty_data["alcever"] *= 100

                # Reindex to ensure all categories are present, even if empty
                poverty_order = [POVERTY_MAP[k] for k in sorted(POVERTY_MAP.keys())]
                poverty_data_reindexed = poverty_data.set_index('poverty3_label').reindex(poverty_order, fill_value=0).reset_index()
                poverty_data_reindexed["mjever"] = poverty_data_reindexed["mjever"].fillna(0)
                poverty_data_reindexed["alcever"] = poverty_data_reindexed["alcever"].fillna(0)

                if not poverty_data_reindexed.empty:
                    fig_poverty = px.scatter(
                        poverty_data_reindexed,
                        x="poverty3_label",
                        y="mjever",
                        size="alcever",
                        title="Marijuana Use vs Poverty Level",
                        labels={"poverty3_label": "Poverty Level", "mjever": "Marijuana Use Rate (%)", "alcever": "Alcohol Use Rate (%)"},
                        color="alcever",
                        color_continuous_scale="viridis",
                        category_orders={"poverty3_label": poverty_order}
                    )
                    st.plotly_chart(fig_poverty, use_container_width=True)
                else:
                    st.info("No data for Poverty Level vs Substance Use in the filtered selection.")
            else:
                st.info("Column 'poverty3_label' not found in the filtered dataset.")

        # Employment status analysis
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Substance Use by Employment Status")
            st.write("This chart illustrates marijuana and alcohol use rates based on employment status (employed, unemployed, not in labor force).")
            # Employment status vs substance use - Use irwrkstat_label for x-axis
            if "irwrkstat_label" in filtered_df_display.columns:
                work_data = filtered_df_display.groupby("irwrkstat_label")[["mjever", "alcever"]].agg(["count", "sum"])
                work_mj = (work_data["mjever"]["sum"] / work_data["mjever"]["count"]) * 100
                work_alc = (work_data["alcever"]["sum"] / work_data["alcever"]["count"]) * 100

                # Reindex to ensure all categories are present, even if empty
                work_order = [WORK_MAP[k] for k in sorted(WORK_MAP.keys())]
                work_mj_reindexed = work_mj.reindex(work_order, fill_value=0).fillna(0)
                work_alc_reindexed = work_alc.reindex(work_order, fill_value=0).fillna(0)

                if not work_mj_reindexed.empty or not work_alc_reindexed.empty:
                    fig_work = go.Figure()
                    fig_work.add_trace(go.Bar(
                        x=work_mj_reindexed.index,
                        y=work_mj_reindexed.values,
                        name="Marijuana Use",
                        marker_color="lightgreen"
                    ))
                    fig_work.add_trace(go.Bar(
                        x=work_alc_reindexed.index,
                        y=work_alc_reindexed.values,
                        name="Alcohol Use",
                        marker_color="lightcoral"
                    ))
                    fig_work.update_layout(
                        title="Substance Use by Employment Status",
                        xaxis_title="Employment Status",
                        yaxis_title="Usage Rate (%)",
                        barmode="group",
                        xaxis=dict(categoryorder='array', categoryarray=work_order) # Ensure order
                    )
                    st.plotly_chart(fig_work, use_container_width=True)
                else:
                    st.info("No data for Employment Status vs Substance Use in the filtered selection.")
            else:
                st.info("Column 'irwrkstat_label' not found in the filtered dataset.")

        with col2:
            st.markdown("### Substance Use by Government Assistance")
            st.write("This chart compares substance use rates between individuals who receive government assistance and those who do not.")
            # Government assistance vs substance use - Use YES_NO_MAP for x-axis
            if "govtprog" in filtered_df_display.columns:
                # FIX: Added extra brackets to ensure column selection is a list
                govt_data = filtered_df_display.groupby("govtprog")[["mjever", "alcever"]].agg(["count", "sum"])
                govt_mj = (govt_data["mjever"]["sum"] / govt_data["mjever"]["count"]) * 100
                govt_alc = (govt_data["alcever"]["sum"] / govt_data["alcever"]["count"]) * 100

                # Reindex to ensure all categories (1 and 2) are present, even if empty
                govt_order_codes = [1, 2] # 1: Yes, 2: No
                govt_mj_reindexed = govt_mj.reindex(govt_order_codes, fill_value=0).fillna(0)
                govt_alc_reindexed = govt_alc.reindex(govt_order_codes, fill_value=0).fillna(0)

                # Map the indices to display labels for plotting
                govt_labels = [YES_NO_MAP.get(idx, str(idx)) for idx in govt_mj_reindexed.index]

                if not govt_mj_reindexed.empty or not govt_alc_reindexed.empty:
                    fig_govt = go.Figure()
                    fig_govt.add_trace(go.Bar(
                        x=govt_labels,
                        y=govt_mj_reindexed.values,
                        name="Marijuana Use",
                        marker_color="lightgreen"
                    ))
                    fig_govt.add_trace(go.Bar(
                        x=govt_labels,
                        y=govt_alc_reindexed.values,
                        name="Alcohol Use",
                        marker_color="lightcoral"
                    ))
                    fig_govt.update_layout(
                        title="Substance Use by Government Assistance",
                        xaxis_title="Government Assistance Status",
                        yaxis_title="Usage Rate (%)",
                        barmode="group",
                        xaxis=dict(categoryorder='array', categoryarray=govt_labels) # Ensure order
                    )
                    st.plotly_chart(fig_govt, use_container_width=True)
                else:
                    st.info("No data for Government Assistance vs Substance Use in the filtered selection.")
            else:
                st.info("Column 'govtprog' not found in the filtered dataset.")

    # Tab 6: Treatment & Risk
    with tab6:
        st.markdown('<h2 class="sub-header">🏥 Treatment & Risk Analysis</h2>', unsafe_allow_html=True)
        st.markdown("This tab focuses on treatment-seeking behaviors and other risk factors.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Alcohol Treatment Seeking Behavior")
            st.write("This pie chart shows the proportion of respondents who have sought treatment for alcohol use in the past year.")
            # Treatment seeking behavior - Use txyralc_label for names
            if "txyralc_label" in filtered_df_display.columns:
                treatment_data = filtered_df_display["txyralc_label"].value_counts().reindex(["No", "Yes"], fill_value=0)
                if not treatment_data.empty and treatment_data.sum() > 0:
                    fig_treatment = px.pie(
                        values=treatment_data.values,
                        names=treatment_data.index,
                        title="Alcohol Treatment Seeking Behavior",
                        color_discrete_sequence=["#FFB6C1", "#FF69B4"]
                    )
                    st.plotly_chart(fig_treatment, use_container_width=True)
                else:
                    st.info("No data for Alcohol Treatment Seeking Behavior in the filtered selection.")
            else:
                st.info("Column 'txyralc_label' not found in the filtered dataset.")


        with col2:
            st.markdown("### Risk Behaviors and Consequences (Count of 'Yes')")
            st.write("This bar chart displays the total count of individuals who reported engaging in specific risk behaviors related to substance use, such as driving under influence or experiencing dangerous situations.")
            # Risk behaviors (drvinalco_label, alcpdang_label, alclimit_label)
            risk_behaviors = []
            risk_labels = []

            # Sum 'Yes' (1) occurrences for each risk behavior
            if "drvinalco" in filtered_df_display.columns:
                risk_behaviors.append(filtered_df_display[filtered_df_display["drvinalco"] == 1].shape[0])
                risk_labels.append("Drove Under Influence")

            if "alcpdang" in filtered_df_display.columns:
                # Assuming 'alcpdang' 1-4, where 1 is most dangerous.
                # Let's count those who perceive it as dangerous (1 or 2)
                # Or, if it's a binary 'Yes/No' like the PDF implies for the example, use that.
                # The PDF example for alcpdang is "1=At parties, 2=Alone..." which is confusing.
                # If it's a binary "Yes/No" for "alcohol caused dangerous situations",
                # it should be mapped like other Yes/No. Assuming it's a binary flag (1=Yes, 2=No)
                # based on the previous pie chart.
                risk_behaviors.append(filtered_df_display[filtered_df_display["alcpdang"] == 1].shape[0])
                risk_labels.append("Alcohol Caused Danger")


            if "alclimit" in filtered_df_display.columns:
                risk_behaviors.append(filtered_df_display[filtered_df_display["alclimit"] == 1].shape[0])
                risk_labels.append("Tried to Limit Alcohol")

            if risk_behaviors:
                fig_risk = px.bar(
                    x=risk_labels,
                    y=risk_behaviors,
                    title="Risk Behaviors and Consequences (Count of 'Yes')",
                    labels={"x": "Risk Behavior", "y": "Number of Cases"},
                    color=risk_behaviors,
                    color_continuous_scale="reds"
                )
                fig_risk.update_xaxes(tickangle=45)
                st.plotly_chart(fig_risk, use_container_width=True)
            else:
                st.info("No risk behavior data available in the filtered selection.")


        # Age at first use analysis
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Age at First Marijuana Use vs Current Age Group")
            st.write("This scatter plot visualizes the relationship between the age at which an individual first used marijuana and their current age group. The diagonal red line serves as a reference where first use age equals current age.")
            # Age at first marijuana use vs current age (mjage is numerical)
            if "mjage" in filtered_df_display.columns:
                age_comparison = filtered_df_display[filtered_df_display["mjage"] > 0][["age2_label", "mjage"]]
                if len(age_comparison) > 0:
                    fig_age_comp = px.scatter(
                        age_comparison,
                        x="mjage",
                        y="age2_label", # Use label for y-axis
                        title="Age at First Marijuana Use vs Current Age Group",
                        labels={"mjage": "Age at First Use", "age2_label": "Current Age Group"},
                        opacity=0.6,
                        category_orders={"age2_label": [AGE_MAP[k] for k in sorted(AGE_MAP.keys())]} # Ensure order
                    )
                    # Add diagonal reference line
                    fig_age_comp.add_shape(
                        type="line",
                        x0=age_comparison["mjage"].min(),
                        y0=age_comparison["mjage"].min(),
                        x1=age_comparison["mjage"].max(),
                        y1=age_comparison["mjage"].max(),
                        line=dict(color="red", dash="dash")
                    )
                    st.plotly_chart(fig_age_comp, use_container_width=True)
                else:
                    st.info("No data for Age at First Marijuana Use vs Current Age Group in the filtered selection.")
            else:
                st.info("Column 'mjage' not found in the filtered dataset.")

        with col2:
            st.markdown("### Type of Treatment Received (Alcohol Only)")
            st.write("This pie chart breaks down the types of treatment received, specifically for alcohol-only treatment versus mixed substance treatment.")
            # Treatment type analysis - Use txalconly_label for names
            if "txalconly_label" in filtered_df_display.columns:
                tx_type_data = filtered_df_display["txalconly_label"].value_counts().reindex(["No", "Yes"], fill_value=0)
                if not tx_type_data.empty and tx_type_data.sum() > 0:
                    fig_tx_type = px.pie(
                        values=tx_type_data.values,
                        names=tx_type_data.index,
                        title="Type of Treatment Received (Alcohol Only)",
                        color_discrete_sequence=["#87CEEB", "#4682B4"]
                    )
                    st.plotly_chart(fig_tx_type, use_container_width=True)
                else:
                    st.info("No data for Type of Treatment Received (Alcohol Only) in the filtered selection.")
            else:
                st.info("Column 'txalconly_label' not found in the filtered dataset.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>📊 NSDUH Women Drug Use Analysis Dashboard | Data visualization for research purposes</p>
        <p>Built with Streamlit & Plotly | Filter and explore the data using the sidebar controls</p>
    </div>
    """, unsafe_allow_html=True)
