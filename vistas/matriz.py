import streamlit as st
from utils.data import load_generic_data, load_symmetric_data, load_accumulative_data

st.header("Complementariedad Usuarios Únicos nueva ruta")

dummy_df, categories, n = load_generic_data()

symmetric_df = load_symmetric_data(dummy_df, categories, n)

st.dataframe(symmetric_df, width=1400)

st.header("Usuarios Únicos Nueva Ruta")

accumulative_df = load_accumulative_data(dummy_df, categories)

st.dataframe(accumulative_df, width=1400)