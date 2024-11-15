import streamlit as st
from utils.data import load_generic_data, load_symmetric_data, load_accumulative_data
from utils.authentication import get_user

user = get_user()

dummy_df, categories, n = load_generic_data(user=user)

symmetric_df = load_symmetric_data(dummy_df, categories, n)

accumulative_df = load_accumulative_data(dummy_df, categories)

if user != "proteccionsocial":
    st.header("Complementariedad Usuarios Únicos nueva ruta")
    st.dataframe(symmetric_df, width=1400)

    st.header("Usuarios Únicos Nueva Ruta")

else:
    st.header("Complementariedad de Beneficios de programas sociales de la SII")
    cols = ['Hambre Cero', 'PROYECTOS PRODUCTIVOS', 'IMPULSO A CUIDADORAS', 'PERSONAS CON DISCAPACIDAD', 'APOYO PARA PERSONAS EN EMERGENCIA POR FENÓMENO SOCIAL O NATURAL DEL EJERCICIO FISCAL 2024', 'APOYO PARA LA ADQUISICIÓN DE MATERIAL PARA MEJORAMIENTO DE LA VIVIENDA']
    filtered_dummy = dummy_df[cols]
    symmetric_df_filtered = load_symmetric_data(filtered_dummy, cols, len(cols))
    st.dataframe(symmetric_df_filtered)
    accumulative_df = accumulative_df[accumulative_df.index.isin(cols)]
    accumulative_df = accumulative_df[[1,2,3,4,5,6,7]]
    st.header("Complementariedad de beneficios gabinete de igualdad para todas las personas")

st.dataframe(accumulative_df, width=1400)

