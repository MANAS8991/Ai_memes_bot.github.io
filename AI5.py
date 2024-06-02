import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

API_URL_Semantics = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
API_URL_Caption = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

headers = {"Authorization": "Bearer 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"}

def generate_semantics(file):
    response = requests.post(API_URL_Semantics, headers=headers, data=file)
    return response.json()[0]["generated_text"]

def generated_caption(payload):
    response = requests.post(API_URL_Caption, headers=headers, json=payload)
    return response.json()[0]["generated_text"]

def draw_text_on_image(image, text, position, text_color, text_size, bold, font_style):
    # Resize image to make it larger
    width, height = image.size
    new_width = int(width * 1.5)
    new_height = int(height * 1.5)
    image = image.resize((new_width, new_height), Image.LANCZOS)

    draw = ImageDraw.Draw(image)

    # Set font size and style
    font_size = text_size
    try:
        if font_style == "Arial":
            font = ImageFont.truetype("arial.ttf", font_size)
        elif font_style == "Times New Roman":
            font = ImageFont.truetype("times.ttf", font_size)
        elif font_style == "Courier New":
            font = ImageFont.truetype("courier.ttf", font_size)
        else:
            font = ImageFont.load_default()
    except IOError:
        font = ImageFont.load_default()

    # Wrap text to fit within image width
    wrapped_text = textwrap.fill(text, width=int(new_width // (font_size / 2)))

    # Calculate text size
    lines = wrapped_text.split('\n')
    total_text_height = 0
    for line in lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        total_text_height += bottom - top
    line_height = total_text_height / len(lines)

    # Calculate y position based on the selected option
    if position == 'top':
        y = 20
    elif position == 'middle':
        y = (new_height - total_text_height) / 2
    else:  # bottom
        y = new_height - total_text_height - 20

    # Draw text
    for line in lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        x = (new_width - text_width) / 2

        if bold:
            # Draw bold text with outline
            draw.text((x-1, y-1), line, font=font, fill=text_color)
            draw.text((x+1, y-1), line, font=font, fill=text_color)
            draw.text((x-1, y+1), line, font=font, fill=text_color)
            draw.text((x+1, y+1), line, font=font, fill=text_color)
            draw.text((x, y), line, font=font, fill=text_color)
        else:
            draw.text((x, y), line, font=font, fill=text_color)

        y += line_height

    return image

# Load banner image
banner_image = Image.open("AI1.png")

st.image(banner_image, use_column_width=True)

st.title("Image Meme Generator")

file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
position = st.radio("Select text position", ('top', 'middle', 'bottom'))
text_input = st.text_area("Enter text for the meme")
text_color = st.color_picker("Select text color", "#FFFFFF")
text_size = st.slider("Select text size", 10, 200, 30)
bold_text = st.checkbox("Make text bold")
font_style = st.selectbox("Select font style", ["Arial", "Times New Roman", "Courier New", "Default"])

if file:
    col1, col2 = st.columns(2)
    with col1:
        st.image(file, use_column_width=True)
    with col2:
        with st.spinner("Generating Semantics..."):
            semantics = generate_semantics(file.getvalue())

        with st.spinner("Generating Meme..."):
            if not text_input:
                prompt_dic = {
                    "inputs": f"Assistant's main purpose is to create funny and sassy meme captions from the images User provides. "
                              f"Assistant should be humorous and cheeky, but avoid toxic, offensive, or demeaning language. "
                              f"Based on the following image semantics: '{semantics}', generate a short, funny meme caption in a similar style to the image. Caption: "
                }
                caption_raw = generated_caption(prompt_dic)
                meme_text = caption_raw.split("Caption: ")[1]
            else:
                meme_text = text_input

            st.subheader("Meme")

            image = Image.open(file)
            image_with_text = draw_text_on_image(image, meme_text, position, text_color, text_size, bold_text, font_style)

            # Save to a bytes buffer
            img_buffer = io.BytesIO()
            image_with_text.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            st.image(img_buffer, use_column_width=True)
            st.download_button("Download Meme Image", img_buffer, file_name="meme.png")
