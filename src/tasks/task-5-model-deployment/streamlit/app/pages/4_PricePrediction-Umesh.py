import streamlit as st
import subprocess

st.subheader("Generate property price")

process = subprocess.Popen(["Rscript", "predict_property_price.R"], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

result = process.communicate()
st.write(result)
