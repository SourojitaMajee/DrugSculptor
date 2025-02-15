import streamlit as st
import pandas as pd
from PIL import Image
import subprocess
import os
import base64
import pickle

# Molecular descriptor calculator
def desc_calc():
    # For Windows, use full path to padel.bat or modify command
    if os.name == 'nt':  # Windows
        padel_path = os.path.join('PaDEL-Descriptor', 'padel.bat')
        command = f'{padel_path} -removesalt -standardizenitro -fingerprints -descriptortypes PubchemFingerprinter.xml -dir molecule.smi -file descriptors_output.csv'
        # Use shell=True for Windows when running .bat files
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:  # Linux/Mac
        bashCommand = f"java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes PubchemFingerprinter.xml -dir molecule.smi -file descriptors_output.csv"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    
    output, error = process.communicate()
    os.remove('molecule.smi')

# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Model building
def build_model(input_data):
    # Reads in saved regression model
    load_model = pickle.load(open('acetylcholinesterase_model.pkl', 'rb'))
    # Apply model to make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='pIC50')
    molecule_name = pd.Series(load_data[1], name='molecule_name')
    df = pd.concat([molecule_name, prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)

# Logo image
image = Image.open('logo.png')

st.image(image, use_container_width=True)

# Page title
st.markdown("""
# DrugSculptor (Acetylcholinesterase)

This app allows you to predict the bioactivity towards inhibting the `Acetylcholinesterase` enzyme. `Acetylcholinesterase` is a drug target for Alzheimer's disease.

""")

# Sidebar
with st.sidebar.header('1. Upload your CSV data'):
    # Replace file uploader with a direct path
    input_file_path = "example_acetylcholinesterase.txt"  # Default input file
    st.sidebar.markdown("""
Using default input file from the local directory: `example_acetylcholinesterase.txt`
""")

if st.sidebar.button('Predict'):
    # Modified to use direct file path instead of uploaded_file
    load_data = pd.read_table(input_file_path, sep=' ', header=None)
    load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False)

    st.header('**Original input data**')
    st.write(load_data)

    with st.spinner("Calculating descriptors..."):
        desc_calc()

    # Read in calculated descriptors and display the dataframe
    st.header('**Calculated molecular descriptors**')
    desc = pd.read_csv('descriptors_output.csv')
    st.write(desc)
    st.write(desc.shape)

    # Read descriptor list used in previously built model
    st.header('**Subset of descriptors from previously built models**')
    Xlist = list(pd.read_csv('descriptor_list.csv').columns)
    desc_subset = desc[Xlist]
    st.write(desc_subset)
    st.write(desc_subset.shape)

    # Apply trained model to make prediction on query compounds
    build_model(desc_subset)
else:
    st.info('Upload input data in the sidebar to start!')
