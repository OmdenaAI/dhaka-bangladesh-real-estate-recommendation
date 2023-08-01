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
    ('Badda', 'Banani', 'Bashundhara R/A', 'Chattogram City',
       'Dakshin Khan', 'Demra', 'Dhaka Cantonment', 'Dhanmondi',
       'Gulshan', 'Hatirpool', 'Hazaribagh', 'Jatrabari', 'Keraniganj',
       'Khilgaon', 'Khilkhet', 'Kurmitola', 'Mirpur', 'Mohakhali',
       'Mohammadpur', 'Motijheel', 'Mugdapara', 'New Market', 'Old Dhaka',
       'Ramna', 'Savar', 'Shabujbag', 'Sher-E-Bangla Nagar', 'Shyamoli',
       'Sub-district of Bandarban', 'Sub-district of Barguna',
       'Sub-district of Bogura', 'Sub-district of Chandpur',
       'Sub-district of Chattogram', 'Sub-district of Cumilla',
       'Sub-district of Dhaka', 'Sub-district of Gazipur',
       'Sub-district of Habiganj', 'Sub-district of Jessore',
       'Sub-district of Khulna', 'Sub-district of Kishoreganj',
       'Sub-district of Manikganj', 'Sub-district of Narayanganj',
       'Sub-district of Narsingdi', 'Sub-district of Rajshahi',
       'Sub-district of Rangpur', 'Sub-district of Satkhira',
       'Sub-district of Sherpur', 'Sub-district of Sirajganj', 'Sutrapur',
       'Sylhet City', 'Tejgaon', 'Turag', 'Uttara'))
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

