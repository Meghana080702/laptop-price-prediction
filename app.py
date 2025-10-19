import streamlit as st
import pandas as pd
import pickle

# --- Load trained model and columns ---
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model_columns.pkl', 'rb') as f:
    model_columns = pickle.load(f)

st.title("💻 Laptop Price Prediction — SmartTech Co.")
st.write("Enter the laptop specifications below:")

# --- User Inputs ---
company_list = [col.replace('Company_', '') for col in model_columns if col.startswith('Company_')]
typename_list = [col.replace('TypeName_', '') for col in model_columns if col.startswith('TypeName_')]
resolution_list = [col.replace('ScreenResolution_', '') for col in model_columns if col.startswith('ScreenResolution_')]
cpu_list = [col.replace('Cpu_', '') for col in model_columns if col.startswith('Cpu_')]
gpu_list = [col.replace('Gpu_', '') for col in model_columns if col.startswith('Gpu_')]
opsys_list = [col.replace('OpSys_', '') for col in model_columns if col.startswith('OpSys_')]

company = st.selectbox("Company", company_list)
typename = st.selectbox("Type", typename_list)
inches = st.slider("Screen Size (inches)", 10.0, 18.0, 13.3)
resolution = st.selectbox("Screen Resolution", resolution_list)
cpu = st.selectbox("Processor", cpu_list)
ram = st.slider("RAM (GB)", 2, 64, 8)
ssd = st.selectbox("SSD Storage", [0, 1])
hdd = st.selectbox("HDD Storage", [0, 1])
gpu = st.selectbox("GPU", gpu_list)
opsys = st.selectbox("Operating System", opsys_list)
weight = st.slider("Weight (kg)", 0.5, 5.0, 1.5)

# --- Prepare input DataFrame ---
input_dict = {
    'Inches': inches,
    'Ram': ram,
    'Weight': weight,
    'SSD': ssd,
    'HDD': hdd
}

# Add one-hot encoded categorical features safely
for col in model_columns:
    if col.startswith('Company_'):
        input_dict[col] = 1 if col == 'Company_' + company else 0
    elif col.startswith('TypeName_'):
        input_dict[col] = 1 if col == 'TypeName_' + typename else 0
    elif col.startswith('ScreenResolution_'):
        input_dict[col] = 1 if col == 'ScreenResolution_' + resolution else 0
    elif col.startswith('Cpu_'):
        input_dict[col] = 1 if col == 'Cpu_' + cpu else 0
    elif col.startswith('Gpu_'):
        input_dict[col] = 1 if col == 'Gpu_' + gpu else 0
    elif col.startswith('OpSys_'):
        input_dict[col] = 1 if col == 'OpSys_' + opsys else 0

input_df = pd.DataFrame([input_dict])
input_df = input_df[model_columns]  # Ensure correct column order

# --- Prediction ---
if st.button("Predict Price"):
    prediction = model.predict(input_df)[0]
    st.success(f"💰 Estimated Laptop Price: ₹{prediction:,.2f}")
