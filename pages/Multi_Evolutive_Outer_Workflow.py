import streamlit as st

# Set Page Config
st.set_page_config(page_title="Michael's Honorary Page", layout="wide")

#  "logo"

st.sidebar.image("assets/logo_asmodeus.jpg", use_container_width=True)

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
        bottom: 20%;
        right: 25%;
        width: 40%;
        height: 45%; /* Adjust height to maintain aspect ratio */
    }

    /* GIFs styling - positioning them around the page */
     .gif2, .gif3, .gif4, .gif5 {
        position: fixed;
        width: 20%; /* Adjust width as needed */
        height: auto;
        z-index: 10; /* Ensures GIFs appear above other content */
    }

    /* Specific positioning for each GIF */
   

    .gif5 {
        top: 25%;
        right: 5%;
        
    }

    .gif3 {
        bottom: 3%;
        left: 20%;
        width: 13%;
        height: auto
    }

    .gif4 {
        bottom: 5%;
        right: 5%;
        width: 13%;
        height: auto;
        
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

# GIFs with direct links to GIF sources
st.markdown(
    """
    
    <img src="https://media.giphy.com/media/ArAgo5dU2z2xO/giphy.gif" class="gif3">
    <img src="https://media.giphy.com/media/gX2NAgKI2HeoM/giphy.gif" class="gif4">
    <img src="https://media.giphy.com/media/O0oQygeklvnX2/giphy.gif" class="gif5">
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
