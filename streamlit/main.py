import streamlit as st
import requests

FLASK_BASE_URL = 'http://127.0.0.1:5000/'


def fetch_data(endpoint, search_query):
    """Fetch data from the API."""
    url = f"{FLASK_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params={'search_query': search_query})
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
            else:
                st.write("No results found")
        else:
            st.write(f"Failed to retrieve data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.write(f"An error occurred: {e}")
    return None


def render_item(item, include_repo=False):
    """Render a single item with optional repository details."""
    with st.container(border=True):
        st.markdown(
            f"""
            <h4 style="margin: 0; padding: 0;">{item['first name']} {item['last name']}</h4>
            <small style="color: gray; font-size: 0.9em;">{item['role']}</small><br>
            <p style="margin: 5px 0;">
                <strong>Email:</strong> <a href="mailto:{item['email']}">{item['email']}</a><br>
                <strong>Chat Username:</strong> {item['chat username']}<br>
                <strong>Location:</strong> {item['location']}<br>
                <strong>Product Name:</strong> 
                <span title="Product Description:">{item['product name']}</span>
                {"<br><strong>Repository Name:</strong> " + item['repo name'] if include_repo else ""}
            </p>
            """,
            unsafe_allow_html=True
        )


# Search input and type
search_query = st.text_input("Enter search term:")
search_type = st.radio(
    "Select search type:",
    ("Product Name", "Repository Name"),
    horizontal=True
)

# Handle Search
if st.button("Search") or search_query:
    endpoint = '/contact/products' if search_type == "Product Name" else '/contact/repos'
    data = fetch_data(endpoint, search_query)

    if data:
        st.subheader("Results")
        for item in data:
            render_item(item, include_repo=(search_type == "Repository Name"))

        st.subheader("Suggestions ✨")