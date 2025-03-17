import streamlit as st

# Set Page Config
st.set_page_config(page_title="Michael's Honorary Page", layout="wide")

# Custom Background
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://stsci-opo.org/STScI-01HMA7E9Q34VN3RAXGQE7E5GVV.png");
        background-size: cover;
    }

    /* Video styling - positioning it at the bottom-right corner */
    .video-frame {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 25%;  /* Reduce size by 20% */
        height: 30%; /* Adjust height to maintain aspect ratio */;

    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Meow meow meow meow, meow meow meow meow.")

# Display the smaller cat image
st.image("assets/asmodeus2.jpg", caption="Asmodeus, the Data Science Cosmonaut", use_container_width=False)

# Embed YouTube Video (No autoplay, user will initiate)
st.markdown(
    """
    <iframe class="video-frame" src="https://www.youtube.com/embed/gc5t68ogB84" 
    frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    """,
    unsafe_allow_html=True
)

# Disclaimer
st.markdown(
    """
    **Disclaimer:**  
    This video is embedded for entertainment purposes only.  
    We do not own the rights to this content. All rights belong to their respective owners.
    """,
    unsafe_allow_html=True
)
