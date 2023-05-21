import streamlit as st
import numpy as np
import pandas as pd
import pickle
import bz2file as bz2

# load model from file
#model = pickle.load(open("app/artifactory/models_sunitha/Randomforest.pkl", "rb"))
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

model = decompress_pickle('app/artifactory/models_sunitha/RandomForest.pbz2')

#Load StandardScalar
scaler = pickle.load(open("app/artifactory/models_sunitha/StandardScaler.pkl", "rb"))

@st.cache_data
def load_data():
    data = pd.read_csv('app/artifactory/models_sunitha/no_outlier_df.csv', low_memory=False)
    cols = ['area', 'building_type', 'building_nature',
            'num_bath_rooms', 'num_bed_rooms', 'price',
            'purpose', 'city', 'locality',
            'relaxation_amenity_count', 'security_amenity_count',
            'maintenance_or_cleaning_amenity_count', 'social_amenity_count',
            'expendable_amenity_count', 'service_staff_amenity_count',
            'unclassify_amenity_count', 'division', 'zone']
    housing_df = data[cols]
    return housing_df

def getDataList(df,col):
    if col=='city':
        cities = []
        city_counts = df.city.value_counts()
        for city, count in city_counts.items():
            if count > 10:
                cities.append(city)
        # Setting the cities for counts<10 as Remaining
        for index, row in df.iterrows():
            if row['city'] not in cities:
                df.at[index, 'city'] = 'Remaining'
    col_list=df[col].unique().tolist()

    return col_list

housing_df=load_data()
zone_list=getDataList(housing_df,'zone')
division_list=getDataList(housing_df,'division')
city_list=getDataList(housing_df,'city')
locality_list=getDataList(housing_df,'locality')
building_type_list=getDataList(housing_df,'building_type')
building_nature_list=getDataList(housing_df,'building_nature')
purpose_list=getDataList(housing_df,'purpose')

#Load the encoders
building_type_enc = pickle.load(open('app/artifactory/models_sunitha/Building_Type.pkl', "rb"))
building_nature_enc = pickle.load(open('app/artifactory/models_sunitha/Building_Nature.pkl', "rb"))
purpose_enc = pickle.load(open('app/artifactory/models_sunitha/Purpose.pkl', "rb"))
city_enc = pickle.load(open('app/artifactory/models_sunitha/City.pkl', "rb"))
division_enc = pickle.load(open('app/artifactory/models_sunitha/Division.pkl', "rb"))
locality_enc = pickle.load(open('app/artifactory/models_sunitha/Locality.pkl', "rb"))
zone_enc = pickle.load(open('app/artifactory/models_sunitha/Zone.pkl', "rb"))

#Setting Title of App
st.title("Price Prediction")
st.markdown("Enter the data to predict the price")

#Input the required data for price prediction
col1, col2, col3 = st.columns(3)
with col1:
    zone = st.selectbox('Zone', zone_list)
    division = st.selectbox('Division', division_list)
    city = st.selectbox('City', city_list)
    locality = st.selectbox('Locality', locality_list)
    submit = st.button('Predict')
with col2:
    area = st.number_input('Area', min_value=90)
    no_bed = st.number_input('Bedrooms', min_value=0)
    no_bath = st.number_input('Bathrooms', min_value=0)


with col3:
    building_nature = st.selectbox('Building Nature', building_nature_list)
    building_type = st.selectbox('Building Type', building_type_list)
    purpos = st.selectbox('Purpose', purpose_list)

#On predict button click
if submit:
    # Encoding the Categorical data
    building_type = pd.DataFrame(building_type_enc.transform([[building_type]]).toarray())
    building_nature = pd.DataFrame(building_nature_enc.transform([[building_nature]]).toarray())
    purpose = pd.DataFrame(purpose_enc.transform([[purpos]]).toarray())
    city = pd.DataFrame(city_enc.transform([[city]]).toarray())
    locality = int(locality_enc.transform([[locality]]))
    division = int(division_enc.transform([[division]]))
    zone = int(zone_enc.transform([[zone]]))
    input_data=pd.DataFrame([[area,no_bath,no_bed,locality,0,2,2,0,2,0,3,division,zone]])
    input_data=pd.concat([input_data,building_type,building_nature,purpose,city],axis=1,ignore_index=True)
    input_data.columns=['area', 'num_bath_rooms', 'num_bed_rooms', 'locality', 'relaxation_amenity_count',
                        'security_amenity_count', 'maintenance_or_cleaning_amenity_count', 'social_amenity_count',
                        'expendable_amenity_count', 'service_staff_amenity_count', 'unclassify_amenity_count',
                        'division', 'zone','building_type_0', 'building_type_1', 'building_type_2', 'building_type_3',
                        'building_type_4', 'building_type_5', 'building_type_6', 'building_type_7', 'building_type_8',
                        'building_type_9', 'building_type_10', 'building_nature_0', 'purpose_0', 'city_0', 'city_1',
                        'city_2', 'city_3', 'city_4', 'city_5', 'city_6', 'city_7', 'city_8', 'city_9', 'city_10']

    cols = input_data.columns
    input_data[cols] = scaler.transform(input_data[cols])
    price =model.predict(input_data)
    price=int(price[0])
    st.header("Predicted "+purpos+" for the property is BDT"+str(price))

