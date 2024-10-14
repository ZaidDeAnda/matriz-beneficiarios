import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import base64
from datetime import datetime

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
def load_generic_data_non_dummy(user="", limit="", curp_list=""):
    config = Config()

    if limit:
        limit_keyword = " LIMIT "+str(limit)
    elif curp_list:
        curp_str = '(\'' + '\',\''.join(curp_list) + '\')'
        limit_keyword = f' AND p."CURP" IN {curp_str}'
    else:
        print("Sin limite")
        limit_keyword = ""
    if user == "proteccion":
        user = "pp.nombre = ANY (ARRAY['Hambre Cero', 'FISE', 'IMPULSO A CUIDADORAS', 'PERSONAS CON DISCAPACIDAD', 'Modelo de Acompañamiento'])"
    elif user:
        user = f"pp.via = '{user}'"
        print(user)

    query = f"""
    WITH IdentificacionesGeograficas AS (
    SELECT *, 
           ROW_NUMBER() OVER (PARTITION BY persona_id ORDER BY identificacion_geografica_id DESC) AS rn
    FROM "PersonasOnIdentificacionesGeograficas"
    )
    SELECT 
        p."CURP", 
        p.id AS persona_id, 
        p.sexo AS sexo, 
        p.fecha_nacimiento AS fecha_nacimiento, 
        pp.id AS idprograma, 
        pp.nombre AS nombre_programa, 
        ig.municipio_label AS municipio, 
        CAST(pp.via AS VARCHAR) AS via
    FROM 
        "Persona" p
    LEFT JOIN 
        "PersonasOnTramites" pt ON p.id = pt.persona_id
    LEFT JOIN 
        "Tramite" t ON t.id = pt.tramite_id
    LEFT JOIN 
        "ProcesoPrograma" pp ON pp.id = t.proceso_id
    LEFT JOIN 
        "IdentificacionGeografica" ig ON ig.tramite_id = pt.tramite_id
    WHERE 
        pp.id = ANY (ARRAY[1,2,3,5,6,7,8,9,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,37])
    AND 
        {user}

    UNION

    SELECT 
        b."CURP", 
        p.id AS persona_id, 
        p.sexo AS sexo, 
        p.fecha_nacimiento AS fecha_nacimiento, 
        pp.id AS idprograma, 
        CAST(pp.nombre AS VARCHAR) AS nombre_programa,
        ig.municipio_label AS municipio, 
        CAST(pp.via AS VARCHAR) AS via
    FROM 
        "Beneficiario" b
    LEFT JOIN 
        "ProcesoPrograma" pp ON pp.id = b.programa_id
    LEFT JOIN 
        "Persona" p ON p."CURP" = b."CURP"
    LEFT JOIN 
        IdentificacionesGeograficas pi ON pi.persona_id = p.id AND pi.rn = 1
    LEFT JOIN 
        "IdentificacionGeografica" ig ON ig.tramite_id = pi.identificacion_geografica_id
    WHERE
        {user}
    {limit_keyword}
    """

    secrets = config.get_config()['vias']

    connection = connect_post(secrets)

    total_df = pd.read_sql(query, connection)

    total_df['edad'] = total_df['fecha_nacimiento'].apply(calcular_edad)
    total_df.drop('fecha_nacimiento', inplace=True, axis=1)

    return total_df

@st.cache_data
def load_generic_null_data(user="", limit="", curp_list=""):
    config = Config()

    if limit:
        limit_keyword = " LIMIT "+str(limit)
    elif curp_list:
        curp_str = '(\'' + '\',\''.join(curp_list) + '\')'
        limit_keyword = f' AND p."CURP" IN {curp_str}'
    else:
        print("Sin limite")
        limit_keyword = ""
    if user == "proteccion":
        user = "pp.nombre = ANY (ARRAY['Hambre Cero', 'FISE', 'IMPULSO A CUIDADORAS', 'PERSONAS CON DISCAPACIDAD', 'Modelo de Acompañamiento'])"
    elif user:
        user = f"pp.via = '{user}'"
        print(user)
    

    query = f"""WITH IdentificacionesGeograficas AS (
        SELECT *, 
            ROW_NUMBER() OVER (PARTITION BY persona_id ORDER BY identificacion_geografica_id DESC) AS rn
        FROM "PersonasOnIdentificacionesGeograficas"
    )
    SELECT 
        p."CURP", 
        p.id AS persona_id, 
        p.sexo AS sexo, 
        p.fecha_nacimiento AS fecha_nacimiento, 
        pp.id AS idprograma, 
        pp.nombre AS nombre_programa, 
        ig.municipio_label AS municipio, 
        CAST(pp.via AS VARCHAR) AS via
    FROM 
        "Persona" p
    LEFT JOIN 
        "PersonasOnTramites" pt ON p.id = pt.persona_id
    LEFT JOIN 
        "Tramite" t ON t.id = pt.tramite_id
    LEFT JOIN 
        "ProcesoPrograma" pp ON pp.id = t.proceso_id
    LEFT JOIN 
        "IdentificacionGeografica" ig ON ig.tramite_id = pt.tramite_id
    WHERE 
        pp.id = ANY (ARRAY[1,2,3,5,6,7,8,9,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,37])
        AND (
            p."CURP" IS NULL OR
            p.sexo IS NULL OR
            p.fecha_nacimiento IS NULL OR
            pp.nombre IS NULL OR
            ig.municipio_label IS NULL OR
            pp.via IS NULL
        )
        AND {user}

    UNION

    SELECT 
        b."CURP", 
        p.id AS persona_id, 
        p.sexo AS sexo, 
        p.fecha_nacimiento AS fecha_nacimiento, 
        pp.id AS idprograma, 
        CAST(pp.nombre AS VARCHAR) AS nombre_programa,
        ig.municipio_label AS municipio, 
        CAST(pp.via AS VARCHAR) AS via
    FROM 
        "Beneficiario" b
    LEFT JOIN 
        "ProcesoPrograma" pp ON pp.id = b.programa_id
    LEFT JOIN 
        "Persona" p ON p."CURP" = b."CURP"
    LEFT JOIN 
        IdentificacionesGeograficas pi ON pi.persona_id = p.id AND pi.rn = 1
    LEFT JOIN 
        "IdentificacionGeografica" ig ON ig.tramite_id = pi.identificacion_geografica_id
    WHERE
        (
            b."CURP" IS NULL OR
            p.sexo IS NULL OR
            p.fecha_nacimiento IS NULL OR
            pp.nombre IS NULL OR
            ig.municipio_label IS NULL OR
            pp.via IS NULL
        )
    AND {user}
    {limit_keyword}
    """

    secrets = config.get_config()['vias']

    connection = connect_post(secrets)

    total_df = pd.read_sql(query, connection)

    total_df['edad'] = total_df['fecha_nacimiento'].apply(calcular_edad)
    total_df.drop('fecha_nacimiento', inplace=True, axis=1)

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


def download_df(user="",curp_list=""):
    df = load_generic_data_non_dummy(user=user, curp_list=curp_list)
    csv = df.to_csv().encode('utf-8')
    components.html(
        download_button(csv, f"beneficiarios_{user}.csv"),
        height=0,)
    
def calcular_edad(fecha_nacimiento):
    hoy = datetime.today()
    try:
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    except:
        edad = "No encontrada"
    return edad
