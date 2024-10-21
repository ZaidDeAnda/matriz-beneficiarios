import streamlit as st
from utils.data import load_generic_data, load_symmetric_data, load_accumulative_data
from utils.authentication import get_user

user = get_user()

st.write(user)

dummy_df, categories, n = load_generic_data(user=user)

symmetric_df = load_symmetric_data(dummy_df, categories, n)

accumulative_df = load_accumulative_data(dummy_df, categories)

if user != "proteccionsocial":
    st.header("Complementariedad Usuarios Únicos nueva ruta")
    st.dataframe(symmetric_df, width=1400)

    st.header("Usuarios Únicos Nueva Ruta")

st.dataframe(accumulative_df, width=1400)

