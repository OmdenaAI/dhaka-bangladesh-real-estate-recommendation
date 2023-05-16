import streamlit as st
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity
from sentence_transformers import SentenceTransformer


st.header("Recommendations")

@st.cache_data
def dataframe_data():

    return pd.read_csv('app/artifactory/bl_property_processed.csv')

@st.cache_data
def dataframe_data_transformer():
    return pd.read_csv('app/artifactory/bl_property_processed.csv')

def sbert_recommendation(query):

        embeddings_file = 'app/artifactory/property_recommend.npy'
        model = SentenceTransformer('paraphrase-distilroberta-base-v1')
        query_embedding = model.encode([query])

        description_embeddings = np.load(embeddings_file)

        similarities = cosine_similarity(query_embedding, description_embeddings)

        top_n = 10
        top_n_indices = similarities[0].argsort()[-top_n:][::-1]

        df = dataframe_data_transformer()
        if len(top_n_indices) == 0:
            st.write("NO PROPERTIES FOUND")
        else:
            st.subheader("Top Matching PROPERTIES using SBERT")
            for index in top_n_indices:
                building_type = df.iloc[index]['building_type']
                building_nature = df.iloc[index]['building_nature']

                city = df.iloc[index]['city']
                zone = df.iloc[index]['zone']
                price = df.iloc[index]['price']
                property_description = df.iloc[index]['property_description']
                image_url = df.iloc[index]['image_url']
                property_url = df.iloc[index]['property_url']

                st.image(image_url, caption="Property Image", width=100)
                st.markdown(f"**Property Type:** {building_type}")
                st.markdown(f"**Buiding Nature:** {building_nature}")
                st.markdown(f"**Zone:** {zone} **City: {city} ")
                st.markdown(f"**Price:** {price}")
                st.markdown(f"**Property Page:** [Link]({property_url})", unsafe_allow_html=True)
                st.markdown(f"**Description:** {property_description}")
                st.write("---")

@st.cache_data
def buildingModel():
    tf_idf = TfidfVectorizer(ngram_range=(2, 2), stop_words="english")
    df = dataframe_data()

    tfidf_matrix = tf_idf.fit_transform(df['recommend_text'])

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    return cosine_sim


def recommend(id):

    idx = dataframe_data()[dataframe_data()['id'] == id].index[0]

    cosine_sim = buildingModel()
    # Get the pairwise similarity scores between the input Property and all the properties
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the properties based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Select the top three similarity scores
    sim_scores = sim_scores[1:10]

    # Get the property variety indices
    property_idx_list = [i[0] for i in sim_scores]

    df = dataframe_data()
    if len(property_idx_list) == 0:
        st.write("NO PROPERTIES FOUND")
    else:
        st.subheader("Top Matching PROPERTIES using TDIDF")
        for index in property_idx_list:
            building_type = df.iloc[index]['building_type']
            building_nature = df.iloc[index]['building_nature']

            city = df.iloc[index]['city']
            zone = df.iloc[index]['zone']
            price = df.iloc[index]['price']
            property_description = df.iloc[index]['property_description']
            image_url = df.iloc[index]['image_url']
            property_url = df.iloc[index]['property_url']

            st.image(image_url, caption="Property Image", width=100)
            st.markdown(f"**Property Type:** {building_type}")
            st.markdown(f"**Buiding Nature:** {building_nature}")
            st.markdown(f"**Zone:** {zone} **City: {city} ")
            st.markdown(f"**Price:** {price}")
            st.markdown(f"**Property Page:** [Link]({property_url})", unsafe_allow_html=True)
            st.markdown(f"**Description:** {property_description}")
            st.write("---")


property_dist = { 'bproperty-4910':'This 875.0 square feet Area of the Sale Apartment is a residential property with 2.0 bedrooms and 2.0 baths and priced at BDT 3700000.0 in Mohammadpur and zone in Mohammadpur', 'bproperty-815':'This 1365.0 square feet Area of the Sale Apartment is a residential property with 3.0 bedrooms and 3.0 baths and priced at BDT 9000000.0 in Tejgaon and zone in Tejgaon', 'bproperty-10970':'This 5600.0 Sq ft area of the Rent Apartment in a commercial property and priced at BDT 448000.00000000006 in Dhanmondi zone in Dhanmondi' ,'bproperty-983':'This 1290.0 square feet Area of the Sale Apartment is a residential property with 3.0 bedrooms and 3.0 baths and priced at BDT 7795000.0 in Mirpur and zone in Mirpur', 'bproperty-16944':'This 2700.0 square feet Area of the Rent Apartment is a residential property with 4.0 bedrooms and 4.0 baths and priced at BDT 100000.0 in Uttara and zone in Uttara', 'bproperty-6851':'This 1445.0 square feet Area of the Sale Apartment is a residential property with 3.0 bedrooms and 3.0 baths and priced at BDT 6936000.0 in Kachukhet and zone in Mirpur', 'bproperty-12551':'This 1835.0 Sq ft area of the Rent Office in a commercial property and priced at BDT 100000.0 in Paribagh zone in Ramna', 'bproperty-14977':'This 2200.0 square feet Area of the Rent Apartment is a residential property with 4.0 bedrooms and 3.0 baths and priced at BDT 45000.0 in Uttara and zone in Uttara', 'bproperty-8646':'This 950.0 square feet Area of the Sale Apartment is a residential property with 2.0 bedrooms and 2.0 baths and priced at BDT 4500000.0 in Mirpur and zone in Mirpur', 'bproperty-13573':'This 12000.0 Sq ft area of the Rent Floor in a commercial property and priced at BDT 300000.0 in Uttara zone in Uttara', 'bproperty-11375':'This 4000.0 Sq ft area of the Rent Office in a commercial property and priced at BDT 720000.0 in Tejgaon zone in Tejgaon', 'bproperty-4034':'This 1440.0 square feet Area of the Sale Apartment is a residential property with 3.0 bedrooms and 3.0 baths and priced at BDT 6500000.0 in Bayazid and zone in Chattogram City', 'bproperty-11802':'This 850.0 Sq ft area of the Rent Office in a commercial property and priced at BDT 10000.0 in Bayazid zone in Chattogram City', 'bproperty-16888':'This 1100.0 square feet Area of the Rent Apartment is a residential property with 3.0 bedrooms and 2.0 baths and priced at BDT 22000.0 in Aftab Nagar and zone in Khilgaon', 'bproperty-14657':'This 1676.0 square feet Area of the Rent Apartment is a residential property with 3.0 bedrooms and 3.0 baths and priced at BDT 35000.0 in Uttara and zone in Uttara', 'bproperty-12947':'This 3000.0 Sq ft area of the Rent Office in a commercial property and priced at BDT 160000.0 in Uttara zone in Uttara', 'bproperty-13462':'This 1600.0 Sq ft area of the Rent Office in a commercial property and priced at BDT 109000.0 in Motijheel zone in Motijheel', 'bproperty-10701':'This 1247.0 Sq ft area of the Sale Office in a commercial property and priced at BDT 11800000.0 in Motijheel zone in Motijheel', 'bproperty-12463':'This 5000.0 Sq ft area of the Rent Office in a commercial property and priced at BDT 300000.0 in Double Mooring zone in Chattogram City', 'bproperty-1037':'This 1300.0 square feet Area of the Sale Apartment is a residential property with 3.0 bedrooms and 3.0 baths and priced at BDT 6500000.0 in 7 No. West Sholoshohor Ward and zone in Chattogram City'}

r_type = st.radio("Select Recommendation Type",   ( 'SBERT','TFIDF'))

option = st.selectbox("What\'s your favorite property",list(property_dist.keys()))

if option and r_type:

    if r_type == 'TFIDF':
        recommend(option)
    else:
        sbert_recommendation(property_dist[option])

