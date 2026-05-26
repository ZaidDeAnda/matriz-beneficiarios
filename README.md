# Matriz de Beneficiarios

Aplicación desarrollada en **Streamlit** para visualizar, consultar y descargar información de beneficiarios por vía de atención, así como analizar la complementariedad entre programas sociales.

## Descripción

Este proyecto contiene una aplicación web para analizar beneficiarios asociados a distintas vías de atención institucional, como educación, salud, vivienda, alimentación e ingreso y trabajo.

La aplicación permite iniciar sesión según la vía correspondiente, visualizar una matriz de complementariedad entre vías, consultar beneficiarios por vía y buscar CURPs de forma individual o grupal.

La información se obtiene principalmente desde una base de datos **PostgreSQL** y se complementa con un archivo local de beneficiarios de programas sociales.

## Funcionalidades principales

- Inicio de sesión con usuario y contraseña.
- Acceso diferenciado por vía de atención.
- Visualización de matriz de complementariedad entre vías.
- Conteo de usuarios únicos por vía.
- Consulta de beneficiarios por vía.
- Búsqueda individual por CURP.
- Búsqueda grupal por lista de CURPs.
- Carga de archivo `.txt` con CURPs.
- Descarga de bases filtradas en CSV.
- Conexión configurable mediante archivo `config.yml`.

## Archivos principales

```text
.
├── README.md
├── app.py
├── requirements.txt
├── .gitignore
├── data
│   └── beneficiarios_ps.csv
├── utils
│   ├── authentication.py
│   ├── config.py
│   ├── data.py
│   └── database.py
└── vistas
    ├── vista.py
    ├── individual.py
    ├── buscador.py
    └── mapa.py
```

## Archivos principales del proyecto

### `app.py`

Aplicación principal de Streamlit.

Configura la página en modo amplio, valida el acceso mediante usuario y contraseña, y define la navegación entre vistas:

- `Vista matriz`
- `Vista por vía`
- `Buscador de curps`

### `vistas/vista.py`

Vista principal de análisis agregado.

Muestra:

- Matriz de complementariedad entre vías.
- Conteo acumulado de usuarios únicos por vía.

Esta vista utiliza funciones de `utils/data.py` para construir una matriz simétrica donde se contabilizan coincidencias entre categorías de atención.

### `vistas/individual.py`

Vista de usuarios por vía.

Permite consultar beneficiarios relacionados con la vía correspondiente al usuario autenticado.

Por ejemplo:

- `via-educacion` consulta beneficiarios de Educación.
- `via-salud` consulta beneficiarios de Salud.
- `via-vivienda` consulta beneficiarios de Vivienda.
- `via-alimentacion` consulta beneficiarios de Alimentación.
- `via-trabajo` consulta beneficiarios de Ingreso y Trabajo.

También permite descargar la base filtrada.

### `vistas/buscador.py`

Vista para búsqueda de CURPs.

Permite buscar beneficiarios mediante:

- Búsqueda individual.
- Búsqueda grupal con CURPs separados por coma.
- Búsqueda grupal mediante archivo `.txt`.

Después de realizar la búsqueda, muestra los resultados en tabla y permite descargar la información filtrada.

### `vistas/mapa.py`

Vista auxiliar para mostrar recursos externos embebidos.

Incluye:

- Un reporte de Power BI.
- Un mapa de ArcGIS.

### `utils/authentication.py`

Contiene la lógica de autenticación.

Actualmente define los usuarios y contraseñas directamente en el código:

```python
user_dict = {
    "via-educacion": "40qQ1",
    "via-salud": "Hp941",
    "via-trabajo": "dX803",
    "via-vivienda": "29Q3r",
    "via-alimentacion": "zN436"
}
```

También contiene la función `select_via(user)`, que convierte el usuario autenticado en la vía correspondiente.

### `utils/config.py`

Contiene la clase `Config`, encargada de leer el archivo de configuración:

```text
config.yml
```

Este archivo debe ubicarse en la raíz del repositorio.

### `utils/database.py`

Contiene funciones para conectarse a bases de datos.

Incluye conexión a:

- PostgreSQL mediante `psycopg2`.
- SQL Server mediante SQLAlchemy.

La aplicación principal usa la conexión PostgreSQL para consultar información de beneficiarios.

### `utils/data.py`

Contiene la lógica principal de carga, transformación, consulta y descarga de datos.

Incluye funciones para:

- Cargar datos desde PostgreSQL.
- Leer archivo local `data/beneficiarios_ps.csv`.
- Unificar bases de beneficiarios.
- Mapear programas sociales a vías de atención.
- Generar variables dummy por vía.
- Construir matriz de complementariedad.
- Calcular conteos acumulados por número de vías.
- Buscar beneficiarios por CURP.
- Descargar resultados en CSV.
- Calcular edad a partir de fecha de nacimiento.

## Requisitos

Para ejecutar el proyecto se recomienda contar con Python 3.8 o superior.

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye:

```text
streamlit==1.36
sqlalchemy
pandas
pyyaml
pyodbc
psycopg2
```

En algunos sistemas puede ser más sencillo instalar `psycopg2-binary`:

```bash
pip install psycopg2-binary
```

## Configuración requerida

Para que el proyecto funcione correctamente, es necesario crear un archivo llamado:

```text
config.yml
```

en la raíz del repositorio.

Este archivo debe contener las credenciales de conexión a PostgreSQL dentro de una sección llamada `vias`.

## Formato requerido de `config.yml`

```yaml
vias:
  host: "TU_HOST_POSTGRES"
  port: 5432
  database: "TU_BASE_DE_DATOS"
  user: "TU_USUARIO"
  password: "TU_PASSWORD"
```

## Ejemplo de `config.yml`

```yaml
vias:
  host: "localhost"
  port: 5432
  database: "padron_beneficiarios"
  user: "usuario_demo"
  password: "password_demo"
```

La conexión se construye internamente con:

```python
psycopg2.connect(**secrets)
```

donde `secrets` corresponde al contenido de la sección `vias`.

## Archivo local requerido

El proyecto también espera encontrar el archivo:

```text
data/beneficiarios_ps.csv
```

Este archivo se lee con:

```python
pd.read_csv("data/beneficiarios_ps.csv", encoding="latin", sep=";")
```

Por lo tanto, debe estar separado por punto y coma `;` y contener información compatible con las columnas utilizadas en el proyecto.

## Ejecución

Para ejecutar la aplicación localmente:

```bash
streamlit run app.py
```

Después de ejecutar el comando, Streamlit abrirá la aplicación en el navegador.

## Uso esperado

1. Crear el archivo `config.yml` con las credenciales de PostgreSQL.
2. Verificar que exista el archivo `data/beneficiarios_ps.csv`.
3. Instalar las dependencias del proyecto.
4. Ejecutar la aplicación con Streamlit.
5. Iniciar sesión con el usuario correspondiente a una vía.
6. Consultar la matriz de complementariedad.
7. Revisar beneficiarios por vía.
8. Buscar CURPs individuales o grupales.
9. Descargar resultados filtrados en CSV.

## Usuarios de acceso

Los usuarios definidos actualmente son:

```text
via-educacion
via-salud
via-trabajo
via-vivienda
via-alimentacion
```

Cada usuario se asocia a una vía mediante la función `select_via`.

## Vías de atención

El proyecto clasifica programas sociales en las siguientes vías:

```text
Educación
Salud
Ingreso y Trabajo
Vivienda
Alimentación
```

Algunos programas se clasifican como:

```text
NA
```

cuando no pertenecen a una vía específica dentro del análisis.

## Consulta a PostgreSQL

El proyecto consulta tablas relacionadas con personas, trámites y programas.

Tablas utilizadas:

```text
Persona
PersonasOnTramites
Tramite
ProcesoPrograma
IdentificacionGeografica
```

Campos principales consultados:

```text
CURP
persona_id
nombres
ap_paterno
ap_materno
municipio
sexo
fecha_nacimiento
idprograma
nombre_programa
```

## Matriz de complementariedad

La matriz de complementariedad cruza las vías de atención para identificar cuántos usuarios aparecen en una o más vías.

La diagonal representa el número de usuarios asociados a una vía específica.

Las celdas fuera de la diagonal representan coincidencias entre dos vías.

Ejemplo conceptual:

```text
                Educación   Salud   Vivienda
Educación            1000     120        80
Salud                 120     900        60
Vivienda               80      60       700
```

## Búsqueda de CURPs

La vista de búsqueda permite tres formas de consulta.

### Búsqueda individual

```text
ABCD010101HNLXXX09
```

### Búsqueda grupal con CURPs separados por coma

```text
ABCD010101HNLXXX09,EFGH020202MNLXXX01,IJKL030303HNLXXX02
```

### Búsqueda grupal con archivo `.txt`

El archivo debe contener un CURP por línea:

```text
ABCD010101HNLXXX09
EFGH020202MNLXXX01
IJKL030303HNLXXX02
```

## Descarga de resultados

La aplicación permite descargar resultados en formato CSV.

Los archivos se generan dinámicamente con nombres como:

```text
beneficiarios_Educación.csv
beneficiarios_Salud.csv
beneficiarios_Vivienda.csv
beneficiarios_Alimentación.csv
beneficiarios_Ingreso y Trabajo.csv
```

## Posibles mejoras

- Mover usuarios y contraseñas a MongoDB, PostgreSQL o variables de entorno.
- Agregar archivo `config.example.yml`.
- Agregar validación formal de CURP.
- Normalizar CURPs eliminando espacios y convirtiendo a mayúsculas.
- Mejorar el manejo de errores cuando falle la conexión PostgreSQL.
- Documentar la estructura esperada de `beneficiarios_ps.csv`.
- Agregar filtros por municipio, sexo, edad o programa.
- Agregar visualizaciones gráficas para la matriz de complementariedad.
- Agregar descarga en Excel.
- Parametrizar los IDs de programas usados en la consulta.
- Evitar construir consultas SQL con listas de CURPs interpoladas directamente.
- Separar consultas SQL en un archivo `.sql` o `.yaml`.

## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- NumPy
- PostgreSQL
- Psycopg2
- SQLAlchemy
- SQL Server
- PyODBC
- YAML

## Objetivo del proyecto

Facilitar el análisis de complementariedad entre vías de atención y la consulta de beneficiarios por programa o CURP, mediante una aplicación web conectada a fuentes institucionales de datos.

## Estado del proyecto

Proyecto en desarrollo para uso interno en actividades de análisis, consulta y seguimiento de beneficiarios.