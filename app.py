import streamlit as st
from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = 933120000

def make_collage(images, rows, cols):
    # Resize images to be the same size
    resized_images = []
    max_height = max([img.size[1] for img in images])
    max_width = max([img.size[0] for img in images])
    for img in images:
        resized_images.append(img.resize((max_width, max_height)))

    # Create the blank canvas
    collage_width = max_width * cols
    collage_height = max_height * rows
    collage = Image.new('RGB', (collage_width, collage_height))

    # Paste the images onto the canvas
    for i in range(rows):
        for j in range(cols):
            img_index = i * cols + j
            if img_index < len(resized_images):
                collage.paste(resized_images[img_index], (j * max_width, i * max_height))

    return collage
st.set_page_config(page_title='Photo Collage Maker')
st.title("Photo Collage Maker")
st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://4kwallpapers.com/images/wallpapers/macos-monterey-wwdc-21-stock-dark-mode-5k-4480x2520-5585.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
st.write("Upload your images and select the number of rows and columns for your collage")

uploaded_files = st.file_uploader("Choose images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

rows = st.selectbox("Number of rows", options=[1, 2, 3, 4, 5])
cols = st.selectbox("Number of columns", options=[1, 2, 3, 4, 5])

if uploaded_files:
    images = [Image.open(file) for file in uploaded_files]
    st.write(f"Selected {len(images)} images")

    if len(images) >= rows * cols:
        if st.button('Create Collage'):
            st.write("Creating your photo collage...")
            collage = make_collage(images, rows, cols)
            st.image(np.array(collage))
    else:
        st.warning(f"Please select at least {rows*cols} images for a {rows}x{cols} collage")
