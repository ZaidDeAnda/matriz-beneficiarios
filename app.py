import streamlit as st

from utils.authentication import check_password
from utils.data import load_generic_data, load_symmetric_data, load_accumulative_data

if check_password():

    st.header("Complementariedad Usuarios Únicos nueva ruta")

    dummy_df, categories, n = load_generic_data()

    symmetric_df = load_symmetric_data(dummy_df, categories, n)

    st.dataframe(symmetric_df)

    st.header("Usuarios Únicos Nueva Ruta")

    accumulative_df = load_accumulative_data(dummy_df, categories)

    st.dataframe(accumulative_df)