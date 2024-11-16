import streamlit as st
import requests


FLASK_BASE_URL = 'http://127.0.0.1:5000/'  

search_query = st.text_input("Enter search term:")

search_type = st.radio(
    "Select search type:",
    ("Product Name", "Repository Name"),
    horizontal=True
)

# Search button
if st.button("Search") or search_query:

    if search_type == "Product Name":
        endpoint = '/contact/products'
    else:
        st.write("Repository Name search is not implemented yet.")
        st.stop()

    url = f"{FLASK_BASE_URL}{endpoint}"

    try:
        response = requests.get(url, params={'search_query': search_query})

        if response.status_code == 200:
            st.write(f"{response.text}")
        else:
            st.write(f"Failed to retrieve data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.write(f"An error occurred: {e}")