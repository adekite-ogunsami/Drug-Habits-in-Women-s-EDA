from data_loader import AGE_MAP, EDU_MAP, MARITAL_MAP, WORK_MAP, YES_NO_MAP, INCOME_MAP, POVERTY_MAP


def get_readable_feature_name(ohe_feature_name, categorical_features_list):
    """
    Converts a one-hot encoded feature name (e.g., 'age2_1.0') back to a readable label
    (e.g., 'Age Group: 12-17') using predefined mappings.

    Args:
        ohe_feature_name (str): The name of the one-hot encoded feature.
        categorical_features_list (list): A list of original categorical feature names.

    Returns:
        str: The human-readable feature name.
    """
    combined_cat_map = {
        'age2': AGE_MAP,
        'eduhighcat': EDU_MAP,
        'irmaritstat': MARITAL_MAP,
        'irwrkstat': WORK_MAP,
        'imother': YES_NO_MAP,
        'ifather': YES_NO_MAP,
        'frdmjmon': {},
        'poverty3': POVERTY_MAP,
        'income': INCOME_MAP
    }

    for original_col in categorical_features_list:
        if original_col in combined_cat_map:
            try:
                code_str = ohe_feature_name.split('_')[-1]
                code = int(float(code_str))
            except ValueError:

                continue


            if f"{original_col}_{code_str}" == ohe_feature_name:

                return f"{original_col.replace('cat', ' Category').replace('stat', ' Status').replace('2', ' Group').replace('3', ' Level').title().replace('_', ' ')}: {combined_cat_map[original_col].get(code, str(code))}"

        if ohe_feature_name.startswith(f"{original_col}_"):
            try:
                code_str = ohe_feature_name.split('_')[-1]
                code = int(float(code_str))
            except ValueError:
                code = ohe_feature_name.split('_')[-1]


            if original_col == 'frdmjmon':
                return f"Friends Marijuana Use: {code}"
            elif original_col == 'income':
                 return f"Income: {INCOME_MAP.get(code, code_str)}"
            elif original_col == 'poverty3':
                 return f"Poverty Level: {POVERTY_MAP.get(code, code_str)}"



    return ohe_feature_name.replace('2', ' Group').replace('3', ' Level').title().replace('_', ' ')

