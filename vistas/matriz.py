import streamlit as st
from utils.data import load_generic_data, load_symmetric_data, load_accumulative_data
from utils.authentication import get_user
import time

user = get_user()

inicio = time.time()
print(f"inicia obtención de datos {inicio - time.time()}")
dummy_df, categories, n = load_generic_data(user=user)
print(f"termina obtención de datos {inicio - time.time()}")

symmetric_df = load_symmetric_data(dummy_df, categories, n)
print(f"terminan datos simétricos {inicio - time.time()}")

accumulative_df = load_accumulative_data(dummy_df, categories)
print(f"terminan datos acumulativos {inicio - time.time()}")

if user != "proteccionsocial":
    st.header("Complementariedad Usuarios Únicos nueva ruta")
    st.dataframe(symmetric_df, width=1400)

    st.header("Usuarios Únicos Nueva Ruta")

else:
    st.header("Complementariedad de Beneficios de programas sociales de la SII")
    cols = ['Hambre Cero', 'PROYECTOS PRODUCTIVOS', 'IMPULSO A CUIDADORAS', 'PERSONAS CON DISCAPACIDAD', 'APOYO PARA PERSONAS EN EMERGENCIA POR FENÓMENO SOCIAL O NATURAL DEL EJERCICIO FISCAL 2024', 'APOYO PARA LA ADQUISICIÓN DE MATERIAL PARA MEJORAMIENTO DE LA VIVIENDA']
    filtered_dummy = dummy_df[cols]
    print(f"empiezan datos simetricos dos {inicio - time.time()}")
    symmetric_df_filtered = load_symmetric_data(filtered_dummy, cols, len(cols))
    print(f"terminan datos simetricos dos {inicio - time.time()}")
    st.dataframe(symmetric_df_filtered)
    accumulative_df = accumulative_df[accumulative_df.index.isin(cols)]
    accumulative_df = accumulative_df[[1,2,3,4,5,6,7]]
    st.header("Complementariedad de beneficios gabinete de igualdad para todas las personas")

st.dataframe(accumulative_df, width=1400)

