import sys
import os
import streamlit as st
import subprocess
import imp

model_path = 'app/artifactory/model_sarang.py'
model = imp.load_source('model_sarang', model_path)

st.subheader("Predict price of any Property")

building_type = st.selectbox(
    'What are you looking for',
    ('Apartment', 'Plot', 'Full Residential Building', 'Shop', 'Office', 'Floor')
)

if building_type == 'Full Residential Building':
    building_type = 'Building'

if building_type == 'Plot':
    building_type = 'Residential Plot'

building_nature = st.selectbox(
    'Residential or Commercial',
    ('Residential', 'Commercial')
)

purpose = st.selectbox(
    'Sale or rent?',
    ('Rent','Sale'))

area = st.number_input('Area in Sq. ft.', min_value = 10)

num_bath_rooms = st.number_input('Number of bathrooms',value=0, step=1, format="%d")

num_bed_rooms = st.number_input('Number of Rooms/Bedrooms',value=0, step=1, format="%d")

divison = st.selectbox(
    'Select division',
    ('Dhaka','Chattogram','Barisal'))

zone = st.selectbox(
    'Select Zone',
    ('Mohammadpur', 'Bashundhara R/A', 'Uttara', 'Mirpur', 'Gulshan',
       'Chattogram City', 'Hazaribagh', 'Sub-district of Chattogram',
       'Dhanmondi', 'Hatirpool', 'Dhaka Cantonment', 'Khilgaon',
       'Khilkhet', 'Ramna', 'Banani', 'Badda', 'Shyamoli', 'Mohakhali',
       'Sher-E-Bangla Nagar', 'Old Dhaka', 'Dakshin Khan', 'Tejgaon',
       'Motijheel', 'Sutrapur', 'New Market', 'Turag', 'Kurmitola',
       'Shabujbag', 'Jatrabari', 'Mugdapara', 'Keraniganj',
       'Sub-district of Gazipur', 'Savar', 'Demra',
       'Sub-district of Barishal', 'Purbachal',
       'Sub-district of Narayanganj', 'Sub-district of Dhaka', 'Golapbag',
       'Sub-district of Sirajganj'))



prediction = model.make_prediction({
    'division': divison,
    'building_type': building_type,
    'building_nature': building_nature,
    'purpose': purpose,
    'zone': zone,
    'num_bed_rooms': num_bed_rooms,
    'num_bath_rooms': num_bath_rooms,
    'area': area
})

def convert_to_bdt_price(value):
    formatted_value = "{:,.2f}".format(value) 
    bdt_price = "৳" + formatted_value
    
    return bdt_price

bdt_price = convert_to_bdt_price(prediction)
print(bdt_price)

st.write(f"Predicted price: {bdt_price}")

"note: For relavent residential properties, '0' Rooms/Bedrooms may not be considered when predicting price"