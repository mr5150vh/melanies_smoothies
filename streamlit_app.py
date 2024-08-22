# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """:mango: Choose the fruits you want in your custom Smoothie :watermelon:
    """)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will is', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect ( 'Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
            
    my_insert_stmt = "INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES ('"+ ingredients_string +"','" + name_on_order +"')"

    time_to_insert = st.button( 'Submit Order')

    if time_to_insert: 
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {name_on_order}', icon="✅")
        

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.json(fruityvice_response.json())
#fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fruityvice_data = fruityvice_response.json()

# Convert the JSON data into a pandas DataFrame
fv_df = pd.json_normalize(fruityvice_data)

# Display the DataFrame
st.dataframe(data=fv_df, use_container_width=True)
