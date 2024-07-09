import streamlit as st

from utils.authentication import check_password, get_user

st.set_page_config(layout="wide")

if check_password():

    user = get_user()
    pages = {
        "Mapa" : [
            st.Page("vistas/mapa.py", title="Mapa")
        ],
        "Vistas" : [
            st.Page("vistas/vista.py", title="Vista matriz"),
            st.Page("vistas/buscador.py", title="Buscador de curps")
        ]
    }

    pg = st.navigation(pages)
    pg.run()
