from sqlalchemy import create_engine
import streamlit as st
import psycopg2

@st.cache_resource
def connect_post(secrets):
    connection = psycopg2.connect(**secrets)

    return connection


@st.cache_resource
def connect_sql(secrets):
    DATABASE_CONNECTION = f'mssql://{secrets["USERNAME"]}:{secrets["PASSWORD"]}@{secrets["SERVER"]}/{secrets["DATABASE"]}?driver={secrets["DRIVER"]}'

    engine = create_engine(DATABASE_CONNECTION)
    connection = engine.connect()

    return connection
