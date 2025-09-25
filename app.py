import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

st.set_page_config(page_title="Site Explorer", page_icon="🕸️")

st.title("🕸️ Site Explorer - Page Titles")

# Input field
url = st.text_input("Enter a website link:", "https://example.com")

if st.button("Fetch Titles"):
    try:
        # Get main page
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        main_title = soup.title.string.strip() if soup.title else "No title available"

        st.subheader("📌 Homepage Title")
        st.success(main_title)

        # Collect internal links
        found_links = set()
        base_domain = urlparse(url).netloc

        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            if urlparse(full_url).netloc == base_domain:  # keep same domain
                found_links.add(full_url)

        st.subheader("📑 Subpage Titles")
        if not found_links:
            st.warning("No subpages were detected.")
        else:
            for i, link in enumerate(list(found_links)[:10], start=1):  # show max 10
                try:
                    sub_res = requests.get(link, timeout=10)
                    sub_soup = BeautifulSoup(sub_res.text, "html.parser")
                    sub_title = sub_soup.title.string.strip() if sub_soup.title else "No title available"
                    st.write(f"{i}. **{sub_title}**  👉  [Open Link]({link})")
                except Exception:
                    st.write(f"{i}. Could not fetch {link}")

    except Exception as e:
        st.error(f"⚠️ Failed to fetch: {e}")
