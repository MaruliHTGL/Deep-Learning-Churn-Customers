# import ml package
import joblib
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
import keras

gen = {'Female': 0, 'Male': 1}
credit = {'No Credit Card': 0, 'Has Credit Card': 1}
active = {'Inactive Member': 0, 'Active Member': 1}

def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value
        
def load_scaler(scaler_file):
    loaded_scaler = joblib.load(open(os.path.join(scaler_file), 'rb'))
    return loaded_scaler
        
def load_model(model_file):
    return tf.keras.models.load_model(model_file)

def run_ml_app():
    st.markdown("<h2 style = 'text-align: center;'> Input Your Customer Data </h2>", unsafe_allow_html=True)

    credit_score = st.number_input("Credit Score", 0, 1000, value=500)
    geography = st.selectbox("Geography", ['France', 'Germany', 'Spain'])
    gender = st.radio('Gender', ['Male','Female'])
    age = st.number_input("Age", 18, 100, value=25)
    tenure = st.number_input("Tenure (Months)", 0, 100, value=5)
    balance = st.number_input("Balance (USD)", 0, 999999, value=50000)
    num_of_products = st.number_input("Number of Products", 1, 10, value=5)
    has_cr_card = st.radio('Has Credit Card', ['Has Credit Card','No Credit Card'])
    is_active_member = st.radio('Is Active Member', ['Active Member','Inactive Member'])
    estimated_salary = st.number_input("Estimated Salary (USD)", 1, 999999, value=50000)

    result = {
            'credit_score': credit_score,
            'gender': gender,
            'age': age,
            'tenure': tenure,
            'balance': balance,
            'num_of_products': num_of_products,
            'has_cr_card': has_cr_card,
            'is_active_member': is_active_member,
            'estimated_salary': estimated_salary,
            'geography': geography
    }

    # Map geography to one-hot encoding
    geography_dict = {'France': [0, 0], 'Germany': [1, 0], 'Spain': [0, 1]}
    
    # Create DataFrame with one-hot encoded Geography
    df = pd.DataFrame(
        {
            'Credit Score': [credit_score],
            'Geography': [geography],
            'Gender': [gender],
            'Age': [age],
            'Tenure': [tenure],
            'Balance (USD)': [balance],
            'Number Of Products': [num_of_products],
            'Has Credit Card': [has_cr_card],
            'Is Active Member': [is_active_member],
            'Estimated Salary (USD)': [estimated_salary],
        }
    )
    
    st.markdown("<h2 style = 'text-align: center;'>Your Customer Data </h2>", unsafe_allow_html=True)

    st.dataframe(df, height=50)

    encoded_result = []

    for i in result.values():
        if type(i) == int:
            encoded_result.append(i)
        elif i in ['Male', 'Female']:
            res = get_value(i, gen)
            encoded_result.append(res)
        elif i in ['Has Credit Card', 'No Credit Card']:
            res = get_value(i, credit)
            encoded_result.append(res)
        elif i in ['Active Member', 'Inactive Member']:
            res = get_value(i, active)
            encoded_result.append(res)
        elif i in ['France', 'Germany', 'Spain']:
            encoded_result.extend(geography_dict[i])

    single_array = np.array(encoded_result).reshape(1, -1)


    st.markdown("<h2 style = 'text-align: center;'> Prediction Result </h2>", unsafe_allow_html=True)

    scaling = load_scaler("scaler.pkl")    
    scaling_array = scaling.transform(single_array)

    model = load_model("model_ann.keras")  
    prediction = model.predict(scaling_array)

    if prediction > 0.5:
        st.warning("Churn Customer")
        st.write("Customers will stop using credit cards. Take immediate action against this customer!")
    else:
        st.success("Retained Customers")
        st.write("Customers will continue to use credit cards. Retain this customer!")

    st.markdown('''<br><p style='text-align: justfy;'> <strong>Caution:</strong> It is better to predict <strong>“Churn Customers”</strong> but in fact they are <strong>“Retained Customers”</strong> because we can continue to provide treatment to them. Otherwise, if we predict and assume they are <strong>“Retained Customers”</strong> and ignore them even though they will stop using credit cards.</p>''', unsafe_allow_html=True)
