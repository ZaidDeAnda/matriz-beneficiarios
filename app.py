import streamlit as st

from utils.authentication import check_password, get_user

st.set_page_config(layout="wide")

if check_password():

    user = get_user()
    if user:
        pages = {
            "Vistas" : [
                st.Page("vistas/vista.py", title="Vista matriz"),
                st.Page("vistas/buscador.py", title="Vista por vía")
            ]
        }

        pg = st.navigation(pages)
        pg.run()
