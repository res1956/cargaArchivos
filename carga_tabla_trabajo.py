import pandas as pd
import pyodbc
from datetime import datetime

# Configuración de la conexión a SQL Server
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-H0ADGQ8\\MSSQLSERVER_DEV;"
    "DATABASE=seguros;"
    "UID=enaccion;"
    "PWD=enaccion;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Cargar el archivo CSV en un DataFrame, especificando el delimitador adecuado
csv_file = "z:\\2020\\FALABELLA-SEGUROS\\desarrollo PYTHON\\archivosCSV\\cargaArchivos-main\\excel.csv"
df = pd.read_csv(csv_file, delimiter=';')

# Nombre de la tabla de trabajo
work_table = 'EAC_FASECOLDA_WK'

# Verificar si la tabla ya existe
def table_exists(table_name):
    query = f"""
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME = '{table_name}';
    """
    cursor.execute(query)
    return cursor.fetchone()[0] > 0

# Si la tabla no existe, crearla
if not table_exists(work_table):
    # Crear la nueva tabla con todas las columnas como VARCHAR
    column_definitions = ', '.join([f'[{col}] VARCHAR(255)' for col in df.columns])
    create_table_query = f"CREATE TABLE {work_table} ({column_definitions});"
    cursor.execute(create_table_query)
else:
    # Verificar la cantidad de columnas en la tabla existente
    def get_table_columns(table_name):
        query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}';
        """
        cursor.execute(query)
        columns = [row.COLUMN_NAME for row in cursor.fetchall()]
        return columns

    existing_columns = get_table_columns(work_table)

    # Si no coinciden las columnas, renombrar la tabla existente y crear una nueva
    if len(existing_columns) != len(df.columns):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        rename_table_query = f"EXEC sp_rename '{work_table}', '{work_table}_{timestamp}';"
        cursor.execute(rename_table_query)

        # Crear la nueva tabla con las columnas correctas
        column_definitions = ', '.join([f'[{col}] VARCHAR(255)' for col in df.columns])
        create_table_query = f"CREATE TABLE {work_table} ({column_definitions});"
        cursor.execute(create_table_query)

# Truncar la tabla de trabajo antes de cargar los nuevos datos
cursor.execute(f"TRUNCATE TABLE {work_table};")

# Insertar los datos del CSV en la tabla de trabajo
for index, row in df.iterrows():
    # Generar el INSERT con los nombres de columnas y parámetros
    columns = ', '.join([f'[{col}]' for col in df.columns])
    placeholders = ', '.join(['?' for _ in df.columns])
    insert_query = f"INSERT INTO {work_table} ({columns}) VALUES ({placeholders});"
    
    # Convertir todos los valores a cadenas y manejar nulos
    values = tuple(str(value) if pd.notna(value) else None for value in row)
    
    try:
        cursor.execute(insert_query, values)
    except pyodbc.Error as e:
        print(f"Error al insertar en la fila {index}: {e}")
        continue  # Continuar con la siguiente fila en caso de error

# Confirmar los cambios en la base de datos
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()
