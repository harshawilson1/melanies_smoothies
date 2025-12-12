# -------------------------
# Import python packages
# -------------------------
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# -------------------------
# Streamlit Page Layout
# -------------------------
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your smoothie!")


# -------------------------
# Get the Order Name
# -------------------------
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on the smoothie will be:", name_on_order)


# -------------------------
# Snowflake Connection
# -------------------------
cnx = st.connection("snowflake")   # must match secrets.toml
session = cnx.session()            # THIS is the correct session for Streamlit apps


# -------------------------
# Load Fruit Options
# -------------------------
fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).to_pandas()

# Multiselect requires a list or pandas series, not Snowpark DF
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_df["FRUIT_NAME"].tolist(),
    max_selections=5
)


# -------------------------
# Insert Order
# -------------------------
if ingredients_list:

    ingredients_string = " ".join(ingredients_list)

    insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    submit = st.button("Submit Order")

    if submit:
        session.sql(insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
