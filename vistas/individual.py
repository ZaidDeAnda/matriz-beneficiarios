import streamlit as st
from io import StringIO
import pandas as pd

from utils.data import download_df, load_generic_data_non_dummy
from utils.authentication import get_user, select_via

st.header("Vista de usuarios por via")

user = select_via(get_user())

st.subheader("Muestra de la base de datos")

total_df = load_generic_data_non_dummy(user=user)

st.dataframe(total_df, width=1400)

with st.form("my_form", clear_on_submit=False):
    submit = st.form_submit_button("Descargar BD completa", on_click=download_df, kwargs={"user" : user})

st.warning(f"Un total de {total_df.isnull().any(axis=1).sum()} registros cuentan con al menos un dato faltante")
st.download_button("Descargar datos incompletos ", data = total_df.isnull().any(axis=1).to_csv().encode("utf-8"), file_name="datos_incompletos.csv")
