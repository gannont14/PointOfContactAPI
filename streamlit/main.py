import streamlit as st
product_name = st.text_input("Product Name", "")
repository_name = st.text_input("Repository Name", "")
if st.button("Search", "primary"):
  st.write("The current product name is", product_name)
  st.write("The current repository name is", repository_name)