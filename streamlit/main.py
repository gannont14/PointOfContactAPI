import streamlit as st
import requests
from streamlit_searchbox import st_searchbox

FLASK_BASE_URL = 'http://127.0.0.1:5000/'

st.set_page_config(
    page_title="Point of Contact",
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    .stAppDeployButton {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

def search_autocomplete_products(search_query):
    """Search products from the API."""
    if not search_query:
        return []
    url = f"{FLASK_BASE_URL}contact/search/products"
    try:
        response = requests.get(url, params={'search_query': search_query})
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        st.error("Failed to connect to the search API")
    return []

def search_autocomplete_repos(search_query):
    """Search repositories from the API."""
    if not search_query:
        return []
    url = f"{FLASK_BASE_URL}contact/search/repos"
    try:
        response = requests.get(url, params={'search_query': search_query})
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        st.error("Failed to connect to the search API")
    return []

def fetch_product_data(product_name):
    """Fetch contact data for a specific product."""
    url = f"{FLASK_BASE_URL}contact/products"
    try:
        response = requests.get(url, params={'search_query': product_name})
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
            st.write("No contacts found for this product")
    except requests.exceptions.RequestException as e:
        st.write(f"An error occurred: {e}")
    return None

def fetch_repo_data(repo_name):
    """Fetch contact data for a specific repository."""
    url = f"{FLASK_BASE_URL}contact/repos"
    try:
        response = requests.get(url, params={'search_query': repo_name})
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
            st.write("No contacts found for this repository")
    except requests.exceptions.RequestException as e:
        st.write(f"An error occurred: {e}")
    return None

def render_product_item(item):
    """Render a product contact item."""
    with st.container(border=True):
        st.markdown(
            f"""
            <h4 style="margin: 0; padding: 0;">{item['first name']} {item['last name']}</h4>
            <small style="color: gray; font-size: 0.9em;">{item['role']}</small><br>
            <p style="margin: 5px 0;">
                <strong>Email:</strong> <a href="mailto:{item['email']}">{item['email']}</a><br>
                <strong>Chat Username:</strong> {item['chat username']}<br>
                <strong>Location:</strong> {item['location']}<br>
                <strong>Product Name:</strong> {item['product name']}
            </p>
            """,
            unsafe_allow_html=True
        )

def render_repo_item(item):
    """Render a repository contact item."""
    with st.container(border=True):
        st.markdown(
            f"""
            <h4 style="margin: 0; padding: 0;">{item['first name']} {item['last name']}</h4>
            <small style="color: gray; font-size: 0.9em;">{item['role']}</small><br>
            <p style="margin: 5px 0;">
                <strong>Email:</strong> <a href="mailto:{item['email']}">{item['email']}</a><br>
                <strong>Chat Username:</strong> {item['chat username']}<br>
                <strong>Location:</strong> {item['location']}<br>
                <strong>Product Name:</strong> {item['product name']}<br>
                <strong>Repository Name:</strong> {item['repo name']}
            </p>
            """,
            unsafe_allow_html=True
        )

search_type = st.radio(
    "Select search type:",
    ("Product Name", "Repository Name"),
    horizontal=True
)

if search_type == "Product Name":
    selected_item = st_searchbox(
        search_autocomplete_products,
        key="product_searchbox",
        placeholder="Search for a product...",
        default_options=[],
        clear_on_submit=False,
        debounce=300,
    )
    if selected_item:
        data = fetch_product_data(selected_item)
        if data:
            st.subheader("Results")
            for item in data:
                render_product_item(item)
else:
    selected_item = st_searchbox(
        search_autocomplete_repos,
        key="repo_searchbox",
        placeholder="Search for a repository...",
        default_options=[],
        clear_on_submit=False,
        debounce=300,
    )
    if selected_item:
        data = fetch_repo_data(selected_item)
        if data:
            st.subheader("Results")
            for item in data:
                render_repo_item(item)