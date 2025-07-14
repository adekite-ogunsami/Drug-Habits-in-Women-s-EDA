import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

from data_loader import load_data, AGE_MAP, EDU_MAP, MARITAL_MAP, WORK_MAP, INCOME_MAP, YES_NO_MAP, POVERTY_MAP
from utils import get_readable_feature_name

def show_predictive_page():
    """
    Displays the predictive analysis page, allowing users to interact with a trained ML model.
    """
    if st.button("← Back to Home", key="back_to_home_pred_page"):
        st.session_state.page = 'home'
        st.rerun()

    st.title("🔮 Predictive Analysis: Substance Use Likelihood")
    st.markdown("This section allows you to interact with the trained machine learning model.")

    df = load_data()

    st.markdown("### Select Substance for Prediction")
    selected_substance = st.radio(
        "Which substance use would you like to predict?",
        ('Marijuana Use', 'Alcohol Use'),
        key='substance_selection'
    )

    if selected_substance == 'Marijuana Use':
        target_variable = 'mjever'
        substance_label = 'marijuana'
    else: # Alcohol Use
        target_variable = 'alcever'
        substance_label = 'alcohol'

    st.write(f"Predicting the likelihood of **{substance_label}** use based on various factors.")


    features = [
        'age2', 'eduhighcat', 'irmaritstat', 'irwrkstat', 'income',
        'imother', 'ifather', 'frdmjmon', 'irhhsiz2', 'poverty3'
    ]

    df_model = df[features + [target_variable]].dropna()

    if df_model.empty:
        st.warning("Not enough data after dropping missing values for predictive analysis. Please check your dataset.")
        return

    categorical_features = ['eduhighcat', 'irmaritstat', 'irwrkstat', 'imother', 'ifather', 'poverty3', 'income']
    numerical_features = ['age2', 'frdmjmon', 'irhhsiz2']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', 'passthrough', numerical_features)
        ],
        remainder='passthrough'
    )


    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                     ('classifier', LogisticRegression(solver='liblinear', random_state=42))])

    # Prepare X and y
    X = df_model[features]
    y = df_model[target_variable]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


    with st.spinner(f"Training model for {substance_label} use prediction..."):
        try:
            model_pipeline.fit(X_train, y_train)
            st.success(f"Model for {substance_label} use trained successfully!")
        except Exception as e:
            st.error(f"Error training model for {substance_label} use: {e}")
            return

    st.markdown(f"### Make a Prediction for {substance_label.capitalize()} Use")
    st.write(f"Enter the characteristics below to predict the likelihood of {substance_label} use.")


    input_data = {}
    col1, col2, col3 = st.columns(3)

    with col1:
        input_data['age2'] = st.selectbox("Current Age Group:", options=sorted(df['age2'].dropna().unique()), format_func=lambda x: AGE_MAP.get(x, str(x)), key=f'age2_{substance_label}')
        input_data['eduhighcat'] = st.selectbox("Education Level:", options=sorted(df['eduhighcat'].dropna().unique()), format_func=lambda x: EDU_MAP.get(x, str(x)), key=f'eduhighcat_{substance_label}')
        input_data['irmaritstat'] = st.selectbox("Marital Status:", options=sorted(df['irmaritstat'].dropna().unique()), format_func=lambda x: MARITAL_MAP.get(x, str(x)), key=f'irmaritstat_{substance_label}')
    with col2:
        input_data['irwrkstat'] = st.selectbox("Employment Status:", options=sorted(df['irwrkstat'].dropna().unique()), format_func=lambda x: WORK_MAP.get(x, str(x)), key=f'irwrkstat_{substance_label}')
        input_data['income'] = st.selectbox("Income Category:", options=sorted(df['income'].dropna().unique()), format_func=lambda x: INCOME_MAP.get(x, str(x)), key=f'income_{substance_label}')
        input_data['imother'] = st.selectbox("Mother Present in Household:", options=[1, 2], format_func=lambda x: YES_NO_MAP.get(x, str(x)), key=f'imother_{substance_label}')
    with col3:
        input_data['ifather'] = st.selectbox("Father Present in Household:", options=[1, 2], format_func=lambda x: YES_NO_MAP.get(x, str(x)), key=f'ifather_{substance_label}')
        input_data['frdmjmon'] = st.number_input("Friends' Marijuana Use (0-10+):", min_value=0, max_value=int(df['frdmjmon'].max()), value=int(df['frdmjmon'].median()), key=f'frdmjmon_{substance_label}')
        input_data['irhhsiz2'] = st.number_input("Household Size:", min_value=1, max_value=int(df['irhhsiz2'].max()), value=int(df['irhhsiz2'].median()), key=f'irhhsiz2_{substance_label}')
        input_data['poverty3'] = st.selectbox("Income-to-Poverty Ratio:", options=sorted(df['poverty3'].dropna().unique()), format_func=lambda x: POVERTY_MAP.get(x, str(x)), key=f'poverty3_{substance_label}')


    if st.button(f"Predict {substance_label.capitalize()} Likelihood"):
        input_df = pd.DataFrame([input_data])
        input_df = input_df[features]

        with st.spinner(f"Predicting {substance_label} likelihood..."):
            try:
                prediction_proba = model_pipeline.predict_proba(input_df)[0][1]
                prediction_class = model_pipeline.predict(input_df)[0]

                st.markdown(f"### Prediction Result for {substance_label.capitalize()} Use:")
                st.info(f"Based on the provided inputs, the likelihood of {substance_label} use is: **{prediction_proba:.2f}**")
                if prediction_class == 1:
                    st.warning(f"This individual is predicted to likely use {substance_label}.")
                else:
                    st.success(f"This individual is predicted to likely NOT use {substance_label}.")
            except Exception as e:
                st.error(f"Error during prediction: {e}")

    st.markdown(f"### Identified Risk Factors (Model Coefficients) for {substance_label.capitalize()} Use")
    st.write(f"The coefficients below indicate the influence of each factor on the likelihood of {substance_label} use. A positive coefficient suggests an increased likelihood, while a negative coefficient suggests a decreased likelihood. The absolute value (magnitude) of the coefficient indicates the strength of that factor's influence; larger absolute values mean a stronger impact.")


    ohe_feature_names = model_pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)
    final_feature_names = list(ohe_feature_names) + numerical_features

    coefficients = model_pipeline.named_steps['classifier'].coef_[0]

    coef_df = pd.DataFrame({
        'Feature': [get_readable_feature_name(f, categorical_features) for f in final_feature_names],
        'Coefficient': coefficients
    }).sort_values(by='Coefficient', ascending=False)

    st.dataframe(coef_df, use_container_width=True)
