import streamlit as st
from PIL import Image
from PIL.ImageFile import ImageFile
import io

Image.MAX_IMAGE_PIXELS = 933120000

def make_collage(images: list[ImageFile], rows: int, cols: int) -> Image.Image:
    # Resize images to be the same size
    resized_images: list[Image.Image] = []
    max_height = max([img.size[1] for img in images])
    max_width = max([img.size[0] for img in images])
    for img in images:
        resized_images.append(img.resize((max_width, max_height), Image.Resampling.LANCZOS))

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

def download_collage_png(collage: Image.Image):
    buf = io.BytesIO()
    collage.save(buf, format='PNG', compress_level=7)
    buf.seek(0)
    return buf

def download_collage_jpeg(collage: Image.Image):
    buf = io.BytesIO()
    collage.save(buf, format='JPEG', quality=100)
    buf.seek(0)
    return buf

def main():
    st.set_page_config(page_title='Photo Collage Maker')
    st.title("Photo Collage Maker")
    st.markdown(
            """
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

    rows = st.selectbox("Number of rows", options=range(1, 100))
    cols = st.selectbox("Number of columns", options=range(1, 100))
    format = st.selectbox("Format", options=["JPEG", "PNG"])

    if uploaded_files:
        images = [Image.open(file) for file in uploaded_files]
        st.write(f"Selected {len(images)} images")

        if len(images) >= rows * cols:
            if st.button('Create Collage'):
                st.write("Creating your photo collage...")
                collage = make_collage(images, rows, cols)

                # Display the collage
                st.image(collage, width='content')

                if format == "PNG":
                    st.write("Generating PNG...")
                    data = download_collage_png(collage)
                    st.download_button(
                        label="Download PNG",
                        data=data,
                        file_name="collage.png",
                        mime="image/png",
                    )
                elif format == "JPEG":
                    st.write("Generating JPEG...")
                    data = download_collage_jpeg(collage)
                    st.download_button(
                        label="Download JPEG",
                        data=data,
                        file_name="collage.jpeg",
                        mime="image/jpeg",
                    )

                st.success("Photo collage created successfully!")
        else:
            st.warning(f"Please select at least {rows*cols} images for a {rows}x{cols} collage")

if __name__ == "__main__":
    main()
