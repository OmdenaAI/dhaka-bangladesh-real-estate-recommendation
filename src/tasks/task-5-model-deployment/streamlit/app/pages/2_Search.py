import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st

def show_header():
   st.sidebar.markdown('## Search')
   st.header("Property Search")

@st.cache_data
def dataframe_data():
    return pd.read_csv('app/artifactory/bl_property_processed.csv')

def show_search_query():
    query = st.text_input('Search query')

    if query:
        embeddings_file = 'app/artifactory/property_recommend.npy'
        model = SentenceTransformer('paraphrase-distilroberta-base-v1')
        query_embedding = model.encode([query])

        description_embeddings = np.load(embeddings_file)

        similarities = cosine_similarity(query_embedding, description_embeddings)

        top_n = 10
        top_n_indices = similarities[0].argsort()[-top_n:][::-1]

        df = dataframe_data()
        if len(top_n_indices) == 0:
            st.write("NO PROPERTIES FOUND")
        else:
            st.subheader("Top Matching PROPERTIES")
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
                st.markdown(f"**zone:** {zone} **City: {city} ")
                st.markdown(f"**Price:** {price}")
                st.markdown(f"**Property Page:** [Link]({property_url})", unsafe_allow_html=True)
                st.markdown(f"**Description:** {property_description}")
                st.write("---")


def main():
    show_header()
    show_search_query()

main()
