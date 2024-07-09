import streamlit as st
from io import StringIO
import pandas as pd

from utils.data import read_data, download_df, load_generic_data_non_dummy
from utils.authentication import get_user, select_via

st.subheader("Registro de tarjetas Programas sociales")

user = select_via(get_user())

total_df = load_generic_data_non_dummy()

vw_programas = read_data("ps", total_df, user, "partial")
st.dataframe(vw_programas)
with st.form("my_form", clear_on_submit=False):
    submit = st.form_submit_button("Descargar BD", on_click=download_df, kwargs={"table" : "ps", "total_df":total_df, "user":user})
# try:
# except:
#     st.warning("Lo sentimos, la base de datos está presentando algunos fallos, estamos trabajando en ello ⚙ 👷‍♂️")

st.markdown('-----')

st.subheader("Registro de tarjetas Jefas de Familia")

# try:
#     vw_jefas = read_data("jf", total_df, "partial")
#     st.dataframe(vw_jefas)
#     with st.form("my_form2", clear_on_submit=False):
#         submit = st.form_submit_button("Descargar BD", on_click=download_df, kwargs={"table" : "jf", "total_df":total_df})
# except:
#     st.warning("Lo sentimos, la base de datos está presentando algunos fallos, estamos trabajando en ello ⚙ 👷‍♂️")
