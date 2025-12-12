# Import packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# App title
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
if name_on_order:
    st.write("The name on the smoothie will be:", name_on_order)

# Snowflake connection
conn = st.connection("snowflake")   # Must match your secrets.toml
session = conn.session()

# Load fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options") \
                      .select(col("FRUIT_NAME")) \
                      .to_pandas()
fruit_list = my_dataframe["FRUIT_NAME"].tolist()

# Fruit selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# If fruits are selected
if ingredients_list:

    # Combine ingredients into a single string
    ingredients_string = " ".join(ingredients_list)

    # Display nutrition info for each selected fruit
    for fruit_chosen in ingredients_list:
        st.subheader(f"{fruit_chosen} Nutrition Information")
        api_url = f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}"
        response = requests.get(api_url)

        if response.status_code == 200:
            st.dataframe(response.json(), use_container_width=True)
        else:
            st.error(f"Could not load nutrition data for {fruit_chosen}")

    # Button to submit the order
    if st.button("Submit Order"):

        # ✅ Insert order into Snowflake using SQL (safe and simple)
        insert_stmt = f"""
        INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER, ORDER_FILLED)
        VALUES ('{ingredients_string}', '{name_on_order}', FALSE)
        """
        session.sql(insert_stmt).collect()

        st.success("Your Smoothie is ordered!", icon="✅")
