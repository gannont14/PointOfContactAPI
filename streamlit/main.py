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
        print(len(response.json()))

        if response.status_code == 200 and response.json():
            data = response.json()
            
            st.subheader(f"Results")
          
            for item in data:
                with st.container(border=True):  
                    st.markdown(
                        f"""
                          <h4 style="margin: 0; padding: 0;">{item['first_name']} {item['last_name']}</h4>
                          <small style="color: gray; font-size: 0.9em;">{item['role']}</small><br>
                          <p style="margin: 5px 0;">
                              <strong>Email:</strong> <a href="mailto:{item['email']}">{item['email']}</a><br>
                              <strong>Chat Username:</strong> {item['chat username']}<br>
                              <strong>Location:</strong> {item['location']}<br>
                              <strong>Product Name:</strong> 
                              <span title="Product Description:">{item['product name']}</span>
                          </p>
                          """,
                        unsafe_allow_html=True
                    )
            st.subheader("Suggestions")  
        else:
            if response.status_code != 200: st.write(f"Failed to retrieve data. Status code: {response.status_code}")
            else: st.write("No results found")
    except requests.exceptions.RequestException as e:
        st.write(f"An error occurred: {e}")
