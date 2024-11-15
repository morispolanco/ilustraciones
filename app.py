import streamlit as st
import requests  # Import for making API requests

# Streamlit Secrets Management (hide TOGETHER_API_KEY)
st.set_page_config(page_title="Children's Story Illustration Generator", page_icon="")
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]  # Retrieve API key from Streamlit Secrets

def generate_illustration(prompt):
    """Generates a children's story illustration using the Together.xyz API.

    Args:
        prompt (str): Textual description of the scene to illustrate.

    Returns:
        str (base64 encoded JSON): The generated image in base64-encoded JSON format.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the API request.
    """

    url = "https://api.together.xyz/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "black-forest-labs/FLUX.1-schnell-Free",
        "prompt": prompt,
        "width": 544,
        "height": 544,
        "steps": 4,  # Adjust for desired image quality (higher = better, slower)
        "n": 1,
        "response_format": "b64_json",
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        return response.json()["generated_images"][0]  # Extract the generated image
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating illustration: {e}")
        return None

st.title("Children's Story Illustration Generator")
st.write("Describe the scene you want illustrated, and we'll use Together.xyz's FLUX model to create a free children's story style image!")

prompt = st.text_input("Scene Description:")

if st.button("Generate Illustration"):
    if prompt:
        try:
            image_data = generate_illustration(prompt)
            if image_data:
                st.image(image_data, use_column_width=True)  # Display image full width
            else:
                st.write("An error occurred while generating the image. Please try again.")
        except KeyError:
            st.error("The API response is missing the generated image data. Please contact Together.xyz support.")
    else:
        st.write("Please enter a description of the scene you want illustrated.")

# Streamlit Secrets Configuration (optional)
if st.sidebar.header("Configure Together.xyz API Key"):
    st.sidebar.write(
        """
        To use the Together.xyz API, you'll need a free API key. You can obtain one by signing up on their website: https://together.xyz/

        Once you have your API key, create a secret named `TOGETHER_API_KEY` in Streamlit Secrets using the following steps:

        1. Click on the "..." menu in the top right corner of the Streamlit app.
        2. Select "Manage app" -> "Edit configuration".
        3. In the "Secrets" section, create a new secret named `TOGETHER_API_KEY` and paste your API key into the value field.
        4. Save the changes.

        **Important:** Never share your API key publicly, as it could be used to generate images on your behalf and incur costs.
        """
    )
