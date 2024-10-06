# Import necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from the Gemini model
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    if input_prompt:
        response = model.generate_content([input_prompt, image])
    else:
        response = model.generate_content(image)
    return response.text

# Initialize the Streamlit app
st.set_page_config(page_title="Nutritional Insights with Gemini", layout="wide")

# Add a title and description
st.title("🥗 Nutritional Insights Application")
st.write("Upload an image of your meal and provide some context to receive personalized nutritional advice.")

# Create a sidebar for additional user inputs
st.sidebar.header("Enjoy your meal today!")

# Meal type selection
meal_type = st.sidebar.selectbox("Select Meal Type:", ["Breakfast", "Lunch", "Dinner", "Snack"])

# Ingredient selection
common_ingredients = [
    "Chicken", "Beef", "Fish", "Rice", "Pasta", "Vegetables", 
    "Fruits", "Eggs", "Tofu", "Beans", "Nuts", "Bread"
]
selected_ingredients = st.sidebar.multiselect("Select Ingredients:", common_ingredients)

# Cooking method selection
cooking_method = st.sidebar.selectbox("Cooking Method:", ["Grilled", "Fried", "Baked", "Steamed", "Raw"])

# Recipe suggestion based on meal type
if meal_type == "Breakfast":
    st.sidebar.write("### Suggested Breakfast Options:")
    st.sidebar.write("- Oatmeal with fruits")
    st.sidebar.write("- Smoothie bowl")
    st.sidebar.write("- Avocado toast")

elif meal_type == "Lunch":
    st.sidebar.write("### Suggested Lunch Options:")
    st.sidebar.write("- Grilled chicken salad")
    st.sidebar.write("- Quinoa bowl")
    st.sidebar.write("- Vegetable stir-fry")

elif meal_type == "Dinner":
    st.sidebar.write("### Suggested Dinner Options:")
    st.sidebar.write("- Baked salmon with veggies")
    st.sidebar.write("- Pasta primavera")
    st.sidebar.write("- Stir-fried tofu with rice")

elif meal_type == "Snack":
    st.sidebar.write("### Suggested Snack Options:")
    st.sidebar.write("- Greek yogurt with honey")
    st.sidebar.write("- Mixed nuts")
    st.sidebar.write("- Veggie sticks with hummus")

# File uploader for meal image
uploaded_file = st.file_uploader("Choose an image of your meal...", type=["jpg", "jpeg", "png"])
image = None

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Meal Image", use_column_width=True)

# Input prompt for additional user context
input_prompt = st.text_input("Add any specific questions or requests for nutritional advice:")

# Submit button to get insights
if st.button("Get Nutritional Insights"):
    if image is not None:
        # Collecting all the user inputs for context
        ingredients_str = ", ".join(selected_ingredients) if selected_ingredients else "No specific ingredients provided"
        full_prompt = (
            f"You are a nutritionist. This is a {meal_type} meal with ingredients: {ingredients_str}. "
            f"It was prepared by {cooking_method}. Please provide insights for this meal. {input_prompt}"
        )
        response = get_gemini_response(full_prompt, image)
        
        # Display the response in a structured format
        st.subheader("Nutritional Insights:")
        st.write(response)
    else:
        st.warning("Please upload an image of your meal before submitting.")

# Add footer for credits or additional links
st.markdown("---")
st.write("Made with ❤️ NutriLens, Enjoy your nutri-Meals with nutri-Lens!")
st.write("Feel free to give feedback on this application!")
