import streamlit as st

st.set_page_config(
    page_title="Recommendation System App",
    page_icon="👋",
)

st.title("Home Page")
st.image("Propertyai.jpeg", caption='', use_column_width=True)

st.header("The Problem")
st.write("""
Bangladesh's property market is important for the country's money matters, but it has problems with sharing information and being open. This makes it hard for people to make smart choices. The lack of good data encourages dishonest behavior and makes people lose trust. To solve this, we need a computer system that can show easy-to-understand, correct property data. Current websites give basic services, but they don't have advanced data analysis or complete data, so they can't serve people's needs fully.
""")

st.header("Want to know more?")
st.markdown("* [Omdena Page](https://omdena.com/chapter-challenges/propertyai-a-one-stop-solution-for-real-estate-data-powered-by-ai/)")

st.sidebar.success("Select a page above.")
