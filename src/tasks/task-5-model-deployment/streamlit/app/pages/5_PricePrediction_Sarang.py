import sys
import os
import streamlit as st
import subprocess

parent_folder = parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

from artifactory import model_sarang

st.subheader("Predict price of any Property")

building_nature = st.selectbox(
    'Select the nature of building (Residential/Commercial)',
    ('Residential', 'Commercial')
)

area = st.number_input('Area in Sq. ft.', min_value = 10)

num_bath_rooms = st.number_input('Number of bathrooms')

num_bed_rooms = st.number_input('Number of bedrooms')

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

purpose = st.selectbox(
    'Sale or rent?',
    ('rent','sale'))

building_type = st.selectbox(
    'Select type of property',
    ('Apartment', 'Residential Plot', 'Building', 'Shop', 'Office', 'Floor')
)


prediction = model_sarang.make_prediction({
    'division': divison,
    'building_type': building_type,
    'building_nature': building_nature,
    'purpose': purpose,
    'zone': zone,
    'num_bed_rooms': num_bed_rooms,
    'num_bath_rooms': num_bath_rooms,
    'area': area
})

st.write(f"Predicted price is  {prediction}")