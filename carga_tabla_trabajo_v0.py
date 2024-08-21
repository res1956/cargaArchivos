import pandas as pd
import pyodbc
from datetime import datetime

# Configuración de la conexión a SQL Server
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-H0ADGQ8\MSSQLSERVER_DEV;"
    "DATABASE=seguros;"
    "UID=enaccion;"
    "PWD=enaccion;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Cargar el archivo CSV en un DataFrame
csv_file = "z:\\2020\\FALABELLA-SEGUROS\\desarrollo PYTHON\\archivosCSV\\cargaArchivos-main\\excel.csv"
df = pd.read_csv(csv_file)  # Lee el CSV, asumiendo que la primera fila tiene los nombres de columnas

# Nombre de la tabla de trabajo
work_table = 'EAC_FASECOLDA_WK'

# Verificar la cantidad de columnas en la tabla existente
def get_table_columns(table_name):
    query = f"""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{table_name}';
    """
    print(query)
    cursor.execute(query)
    columns = [row.COLUMN_NAME for row in cursor.fetchall()]
    print ( "devuelve columns" , columns)
    return columns

existing_columns = get_table_columns(work_table)

if len(existing_columns) != len(df.columns):
    # Si no coinciden las columnas, renombrar la tabla existente
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    rename_table_query = f"EXEC sp_rename '{work_table}', '{work_table}_{timestamp}';"
    cursor.execute(rename_table_query)

    # Crear la nueva tabla con todas las columnas como VARCHAR
    column_definitions = ', '.join([f'[{col}] VARCHAR(255)' for col in df.columns])
    create_table_query = f"CREATE TABLE {work_table} ({column_definitions});"
    print ("create_table_query ", create_table_query)
    cursor.execute(create_table_query)

# Truncar la tabla de trabajo antes de cargar los nuevos datos
cursor.execute(f"TRUNCATE TABLE {work_table};")

# Insertar los datos del CSV en la tabla de trabajo
for index, row in df.iterrows():
    # Generar el INSERT con los nombres de columnas y valores
    columns = ', '.join([f'[{col}]' for col in df.columns])
    values = ', '.join([f"'{str(value)}'" for value in row])
    insert_query = f"INSERT INTO {work_table} ({columns}) VALUES ({values});"
    cursor.execute(insert_query)

# Confirmar los cambios en la base de datos
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()
