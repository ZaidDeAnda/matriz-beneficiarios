import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import base64

from utils.database import connect_post, connect_sql
from utils.config import Config

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
            'BECAS PARA CAPACITACION':'Educación',
            'BECAS PARA LA CAPACITACION':'Educación',
            'PREVENCIÓN EMBARAZO ADOLESCENTE':'Salud',
            'CULTURA MEDIACIÓN PARA LA PRIMERA INFANCIA': 'Educación',
            'ASISTIMOS CON AMOR': 'Salud',
            '463 - Cuestionario Socioeconomico, CHECS 2023 JAVASCRIPT': 'NA',
            'PERSONAS CON DISCAPACIDAD' : 'Ingreso y Trabajo',
            'APOYO PARA LA ADQUISICIÓN DE MATERIAL PARA MEJORAMIENTO DE LA VIVIENDA' : 'Vivienda',
            'BANCO DE LECHE' : 'Salud',
            'COBERTURA UNIVERSAL C�NCER DE MAMA' : 'Salud',
            'IMPLANTE COCLEAR' : 'Salud',
            'APOYO PARA PERSONAS EN EMERGENCIA POR FENÓMENO SOCIAL O NATURAL DEL EJERCICIO FISCAL 2024' : 'NA',
            'C�NCER INFANTIL' : 'Salud',
            'COBERTURA UNIVERSAL PROGRAMA CANCER INFANTIL' : 'Salud'
            }


@st.cache_data
def load_generic_data():
    config = Config()

    query = """
    SELECT p."CURP",
        p.id AS persona_id,
        pp.id as idprograma,
        pp.nombre AS nombre_programa
    FROM "Persona" p
        LEFT JOIN "PersonasOnTramites" pt ON p.id = pt.persona_id
        LEFT JOIN "Tramite" t ON t.id = pt.tramite_id
        LEFT JOIN "ProcesoPrograma" pp ON pp.id = t.proceso_id
    WHERE pp.id = ANY (ARRAY[1,2,3,5,6,7,8,9,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,37]);
    """

    secrets = config.get_config()['vias']

    connection = connect_post(secrets)

    df1 = pd.read_sql(query, connection)
    df1.columns = ["CURP", "IDBeneficiario", "IdPrograma", "NombrePrograma"]

    df2 = pd.read_csv("data/beneficiarios_ps.csv", encoding="latin", sep=";")

    total_df = pd.concat([df1, df2], axis=0)

    total_df.drop('IdPrograma', inplace=True, axis=1)
    total_df.drop('IDBeneficiario', inplace=True, axis=1)

    total_df["NombrePrograma"] = total_df["NombrePrograma"].str.upper().replace(via_dict)
    
    dummy_df = pd.get_dummies(total_df.loc[total_df["NombrePrograma"] != 'NA'], columns=["NombrePrograma"], prefix="", prefix_sep="").groupby(["CURP"]).sum()
    dummy_df[dummy_df > 1] = 1
    categorias = dummy_df.columns
    n = len(categorias)

    return dummy_df, categorias, n

@st.cache_data
def load_generic_data_non_dummy():
    config = Config()

    query = """
    SELECT p."CURP",
        p.id AS persona_id,
        pp.id as idprograma,
        pp.nombre AS nombre_programa
    FROM "Persona" p
        LEFT JOIN "PersonasOnTramites" pt ON p.id = pt.persona_id
        LEFT JOIN "Tramite" t ON t.id = pt.tramite_id
        LEFT JOIN "ProcesoPrograma" pp ON pp.id = t.proceso_id
    WHERE pp.id = ANY (ARRAY[1,2,3,5,6,7,8,9,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,37]);
    """

    secrets = config.get_config()['vias']

    connection = connect_post(secrets)

    df1 = pd.read_sql(query, connection)
    df1.columns = ["CURP", "IDBeneficiario", "IdPrograma", "Via"]

    df2 = pd.read_csv("data/beneficiarios_ps.csv", encoding="latin", sep=";")

    total_df = pd.concat([df1, df2], axis=0)

    total_df.drop('IdPrograma', inplace=True, axis=1)
    total_df.drop('IDBeneficiario', inplace=True, axis=1)

    total_df["Via"] = total_df["Via"].str.upper().replace(via_dict)

    return total_df

@st.cache_data
def load_symmetric_data(dummy_df, _categorias, _n):

    symmetric_matrix = np.zeros((_n, _n), dtype=int)

    for i in range(_n):
        for j in range(_n):
            if i == j:
                # Contar ocurrencias de una sola categoría
                symmetric_matrix[i, j] = (dummy_df[_categorias[i]] == 1).sum()
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

def read_data_from_sql(table, selection):
    config = Config()

    secrets = config.get_config()[table]

    conn = connect_sql(secrets)

    if selection == "partial":
        limit = " TOP 500"
    else:
        limit = ""
    query = f'''Select{limit} * FROM vw_beneficariotarjetas'''
        
    data = pd.read_sql_query(query, conn)

    return data

def read_data(table,total_df, user, selection="complete"):
    if selection=="debug":
        data = pd.read_csv('data-integrator completo.csv')
    else:
        data = read_data_from_sql(table, selection)
    filtered_df = drop_missing(data)
    filtered_df['CURP'] = filtered_df['CURP'].astype({'CURP':'string'})
    total_df['CURP'] = total_df['CURP'].astype({'CURP':'string'})
    joined_df = filtered_df.merge(total_df, on="CURP")
    joined_df = joined_df[joined_df["Via"] == user]
    return joined_df
        

def drop_missing(df):
    filtered_df = df.loc[df['CURP'].notna()]
    return filtered_df

def download_button(object_to_download, download_filename):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    """

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    dl_link = f"""
    <html>
    <head>
    <title>Start Auto Download file</title>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $('<a href="data:text/csv;base64,{b64}" download="{download_filename}">')[0].click()
    </script>
    </head>
    </html>
    """
    return dl_link


def download_df(table, total_df, user):
    df = read_data(table, total_df, user)
    csv = df.to_csv().encode('utf-8')
    components.html(
        download_button(csv, f"beneficiarios_{table}.csv"),
        height=0,)