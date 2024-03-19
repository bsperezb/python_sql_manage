import os
import logging
from db.database import Database
from excel.excel_handler import ExcelHandler
from utils.general import find_matching_tuple, clean_string
from utils.graph import plot_histogram_and_std, calcular_intervalo_confianza, bootstrap_ci
from dotenv import load_dotenv

# Configuración básica del registro (logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def main():
    # Definir Variables
    excel_data = "usuarios a inactivar en prod.xls"
    # excel_data = "test_db.xlsx"

    # Configurar la conexión a la base de datos
    db = Database(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    # Registrar la conexión exitosa a la base de datos
    logger.info("Conexión a la base de datos establecida exitosamente.")

    # Preguntar antes de leer el archivo Excel
    user_input = input("¿Deseas leer el archivo Excel? (y/n): ")
    if user_input.lower() == 'y':
        # Leer datos desde el archivo Excel
        excel_handler = ExcelHandler(excel_data)
        data_excel = excel_handler.read_excel()
        count = 0
        excel_data_error = []
        db_data_error = []
        delete_data_error_user = []
        for item_excel in data_excel:
            # iterate data Excel
            excel_id = item_excel['ID usuario']
            excel_email = item_excel['Correo']
            if not excel_id: 
                # Not id  in excel
                excel_data_error.append(item_excel)
                continue
            
            # Data user database
            user = db.get_user_by_id(excel_id)

            # check database
            if user is None:
                # Not id in User DB
                logger.error(f'Error, no user in db: {excel_id}')
                db_data_error.append(item_excel)
            
            client_id = user[0][3]
            user_email = user[0][2]
            # check if mail correspond to the same user
            if user_email.strip() != excel_email.strip():
                logger.error(f'Error, is not the same mail {excel_id}')
                logger.error(user_email.strip())
                logger.error(excel_email.strip())
                db_data_error.append(item_excel)
                continue

            # Delete user -----
            delete_user = db.delet_user_by_id(excel_id)

            if not delete_user:
                delete_data_error_user = item_excel
                logger.error(f'Error, id User not delete: {excel_id}')
                continue

            if not client_id:
                continue

            delete_client = db.delet_client_by_id(user_clientId)
            if not delete_user:
                logger.error(f'Error, id Client not delete: {user_clientId}')

            count = count + 1
            print('count: ', count) 

        # Generate excel
        excel_handler.generate_csv('excel_data_error', excel_data_error)
        excel_handler.generate_csv('db_data_error', db_data_error)
        excel_handler.generate_csv('delete_data_error_user', delete_data_error_user)
        logger.info("Excels generados")
        logger.info("OPERACION TERMINADA")
            

if __name__ == "__main__":
    main()
