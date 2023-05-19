import streamlit as st
import subprocess
import csv

st.subheader("Predict price for an apartment")

area = st.number_input('Area in Sq. ft.', min_value = 10)
# st.write('Area: ', area)

num_bath_rooms = st.number_input('Number of bathrooms')
# st.write('Bathrooms: ', num_bath_rooms)

num_bed_rooms = st.number_input('Number of bedrooms')
# st.write('Bedrooms: ', num_bed_rooms)

zone = st.selectbox(
    'Which zone would you prefer?',
    ('Mirpur', 'Chattogram City', 'Bashundhara R/A', 'Khilgaon', 'Mohammadpur', 'Uttara', 
     'Badda', 'Dakshin Khan', 'Sub-district of Chattogram', 'Dhaka Cantonment'))
# st.write('You selected:', zone)

purpose = st.selectbox(
    'Sale or rent?',
    ('sale', 'rent'))
# st.write('You selected:', purpose)

f = open('./app/artifactory/input.csv', 'w') #write mode 
writer = csv.writer(f, delimiter=',', quotechar='"')
writer.writerow(["area","num_bath_rooms","num_bed_rooms","zone","purpose"])
writer.writerow([area, num_bath_rooms, num_bed_rooms, zone, purpose])
f.close()

# Sent the input to the R function
process = subprocess.Popen(["Rscript", "./app/artifactory/predict_property_price.R"], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Read, format and print the prediction
result = process.communicate()
# st.write(result)

predicted_price = list(result)[0].split(' ')[2]
st.write(f'Price prediction: {predicted_price} BDT for the {purpose} of {area} Sq. ft apartment in {zone}')

