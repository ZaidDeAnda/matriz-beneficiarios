import streamlit as st
from io import StringIO
import pandas as pd

from utils.data import download_df, load_generic_data_non_dummy
from utils.authentication import get_user, select_via

st.subheader("Vista de usuarios por via")

user = select_via(get_user())

total_df = load_generic_data_non_dummy(user, limit=2000)

st.dataframe(total_df)
with st.form("my_form", clear_on_submit=False):
    submit = st.form_submit_button("Descargar BD", on_click=download_df, kwargs={"table" : user})
# try:
# except:
#     st.warning("Lo sentimos, la base de datos está presentando algunos fallos, estamos trabajando en ello ⚙ 👷‍♂️")
