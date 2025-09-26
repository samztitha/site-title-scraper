import streamlit as st
import requests
from bs4 import BeautifulSoup

# simple streamlit webscraping app
st.title("Website Title Finder")

# input box for url
website = st.text_input("Enter website URL", "https://example.com")

if st.button("Get Title"):
    try:
        # fetch html page
        r = requests.get(website)
        # parse html
        soup = BeautifulSoup(r.text, "html.parser")
        # get title
        if soup.title:
            st.write("Website Title is:", soup.title.string)
        else:
            st.write("No title found in this website")
    except:
        st.write("Error: could not fetch the website")
