import pandas as pd
import streamlit as st

def check_password():
    user_dict = {
        "proteccionsocial" : "123456789",
        "sistemas" : "planeacion"
    }
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (st.session_state["username"] in user_dict.keys()
                and st.session_state["password"]
                == user_dict[st.session_state["username"]]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    sb1 = st.sidebar.empty()
    sb2 = st.sidebar.empty()
    sb3 = st.sidebar.empty()


    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        sb1.text_input("Usuario", key="username")
        sb2.text_input("Contraseña",
                    type="password",
                    on_change=password_entered,
                    key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        sb1.text_input("Usuario", key="username")
        sb2.text_input("Contraseña",
                    type="password",
                    on_change=password_entered,
                    key="password")
        sb3.error("😕 Usuario desconocido o contraseña errónea")
        return False
    else:
        # Password correct.
        sb3.success("Datos ingresados correctamente")
        return True



def get_user():
    st.session_state["username"] = st.session_state["username"]
    return st.session_state["username"]