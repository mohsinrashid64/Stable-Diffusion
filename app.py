import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# Function to call the API and generate the image
def generate_image(prompt, steps, width, height):
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    payload = {
        "prompt": prompt,
        "steps": steps,
        "width": width,
        "height": height
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None

# Function to decode base64 image and display it
def display_image(base64_str):
    try:
        # Decode base64
        image_data = base64.b64decode(base64_str)
        # Convert to image
        image = Image.open(BytesIO(image_data))
        # Display the image
        st.image(image, caption="Generated Image", use_column_width=True)
    except Exception as e:
        st.error(f"Failed to process image: {e}")

# Streamlit App Layout
st.title("Stable Diffusion Image Generator")

# Input fields
prompt = st.text_input("Enter your prompt:", "a futuristic city at sunset")
steps = st.slider("Number of steps:", min_value=10, max_value=50, value=20)
width = st.slider("Image width:", min_value=256, max_value=1024, value=512, step=64)
height = st.slider("Image height:", min_value=256, max_value=1024, value=512, step=64)

# Generate button
if st.button("Generate Image"):
    with st.spinner("Generating image..."):
        # Call the API
        result = generate_image(prompt, steps, width, height)
        if result:
            # Extract the base64 image from the response
            base64_str = result.get("images", [None])[0]
            if base64_str:
                # Display the image
                display_image(base64_str)
            else:
                st.error("No image data found in the response.")