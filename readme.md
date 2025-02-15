# DrugSculptor
This app allows you to predict the bioactivity towards inhibting the Acetylcholinesterase enzyme. Acetylcholinesterase is a drug target for Alzheimer's disease.
Higher pIC50 means low dose of the same drug is required, indicating it's efficacy. 

## Environment Setup

```sh
     python -m venv venv
     venv\Scripts\activate
```

## Install Dependencies
```sh
     pip install -r requirements.txt
```

## Run Streamlit app
```sh
     streamlit run app.py
```
click on `predict`