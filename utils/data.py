import pandas as pd
import numpy as np
import streamlit as st

via_dict = {'HAMBRE CERO ESCUELA TIEMPO COMPLETO': 'Alimentación',
            'COSEA': 'Educación',
            'EDUCACIÓN PARA LOS ADULTOS': 'Educación',
            'PROYECTOS PRODUCTIVOS': 'Ingreso y Trabajo',
            'FISE': 'Vivienda',
            'CUIDAR TÚ SALUD': 'Salud',
            'CANCER INFANTIL': 'Salud',
            'CANCER DE MAMA':'Salud',
            'HAMBRE CERO': 'Alimentación',
            'IMPULSO A CUIDADORAS': 'Ingreso y Trabajo',
            'INCLUIR PARA SER IGUALES PERSONAS CON DISCAPACIDAD':'Ingreso y Trabajo',
            'BECAS NIÑOS Y NIÑAS PRIMERA INFANCIA': 'Ingreso y Trabajo',
            'GESTORIA':'NA',
            'PROGRAMA DE INCLUSIÓN PARA MUJERES JEFAS DE FAMILIA EN CONDICIÓN DE VULNERABILIDAD': 'Ingreso y Trabajo',
            'CENTROS COMUNITARIOS DE DESARROLLO SOCIAL':'NA',
            'La NUEVA RUTA':'NA',
            'BANCO DE ALIMENTOS':'Alimentación',
            'BENEFICIARIOS':'Vivienda',
            'DESAYUNO ESCOLAR':'Alimentación',
            '100 DÍAS':'Alimentación',
            'ASAPAP': 'Alimentación',
            'Becas para capacitacion':'Educación',
            'Becas para la capacitacion':'Educación',
            'Prevención embarazo adolescente':'Salud',
            'Cultura mediación para la primera infancia': 'Educación',
            'Asistimos con amor': 'Salud',
            '463 - Cuestionario Socioeconomico, CHECS 2023 JAVASCRIPT': 'NA'

            }

@st.cache_data
def load_generic_data():

    df = pd.read_csv("data-040324.csv")

    df['via'] = df['programa'].map(via_dict)
    df.drop(["programa"], inplace=True, axis=1)
    df.drop(["persona_id"], inplace=True, axis=1)
    dummy_df = pd.get_dummies(df.loc[df["via"] != 'NA'], columns=["via"], prefix="", prefix_sep="").groupby(["CURP",'sexo']).sum()
    dummy_df[dummy_df > 1] = 1
    categorias = dummy_df.columns
    n = len(categorias)

    return dummy_df, categorias, n

@st.cache_data
def load_symmetric_data(dummy_df, _categorias, _n):

    symmetric_matrix = np.zeros((_n, _n), dtype=int)

    for i in range(_n):
        for j in range(_n):
            if i == j:
                # Contar ocurrencias de una sola categoría
                symmetric_matrix[i, j] = (dummy_df[_categorias[i]] == 1)
            else:
                # Contar combinaciones de dos categorías
                symmetric_matrix[i, j] = ((dummy_df[_categorias[i]] == 1) & (dummy_df[_categorias[j]] == 1)).sum()

    # Convertir la matriz simétrica a un DataFrame para mejor visualización
    symmetric_df = pd.DataFrame(symmetric_matrix, index=_categorias, columns=_categorias)

    return symmetric_df

@st.cache_data
def load_accumulative_data(dummy_df, _categorias):

    accumulative = {via : {
        x : 0 for x in range(1,6)
    } for via in _categorias}

    for _, row in dummy_df.iterrows():
        interes = row.loc[row > 0]
        total = len(interes)
        vias = interes.index
        for via in vias:
            accumulative[via][total] += 1

    accumulative_df = pd.DataFrame.from_dict(accumulative).T
    accumulative_df['Total'] = accumulative_df.sum(axis=1)
    return accumulative_df