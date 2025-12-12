import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on the smoothie will be:", name_on_order)

# Snowflake connection
conn = st.connection("snowflake")
session = conn.session()

# Load fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).to_pandas()
fruit_list = my_dataframe["FRUIT_NAME"].tolist()

# Fruit multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Process selected fruits
if ingredients_list:

    ingredients_string = " ".join(ingredients_list)

    for fruit_chosen in ingredients_list:
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # FIXED URL
        api_url = f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}"
        response = requests.get(api_url)

        if response.status_code == 200:
            st.dataframe(response.json(), use_container_width=True)
        else:
            st.error(f"Could not load nutrition data for {fruit_chosen}")

    # Insert order into Snowflake
    if st.button("Submit Order"):
        session.table("smoothies.public.orders").insert(
            {"ingredients": ingredients_string, "name_on_order": name_on_order}
        )
        st.success("Your Smoothie is ordered!", icon="✅")
