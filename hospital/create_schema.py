from sqlalchemy import create_engine

"""Notas
    - employee: juntamos physician y nurse en una sola dimension
                y agregamos role que dice si es physician o nurse
"""


if __name__ == '__main__':
    
    # connect to server
    # cambiar root:root por tu usuario:password y 3310 por el puerto que asignaste a tu base de datos
    engine = create_engine('mysql+pymysql://root:root@localhost:3310')

    engine.execute("CREATE DATABASE IF NOT EXISTS dw_hospital")
    engine.execute("USE dw_hospital")
    engine.execute("SET FOREIGN_KEY_CHECKS = 0;")  # para que nos permita eliminar filas con referencias de FK si queremos reconstruir el esquema

    # Dimension empleado
    engine.execute("DROP TABLE IF EXISTS bt_employee;")
    engine.execute("""
        CREATE TABLE bt_employee(
            id INT NOT NULL,
            ssn INT NOT NULL,
            name VARCHAR(50) NOT NULL,
            position VARCHAR(50),
            role VARCHAR(50),
            registered_nurse TINYINT,
            PRIMARY KEY(id)
        );
    """)

    # Dimension procedimiento
    engine.execute("DROP TABLE IF EXISTS bt_procedure;")
    engine.execute("""
        CREATE TABLE bt_procedure(
            code INT NOT NULL,
            name VARCHAR(100),
            cost FLOAT,
            PRIMARY KEY(code)
        );""")

    # Dimension paciente
    engine.execute("DROP TABLE IF EXISTS bt_patient;")
    engine.execute("""
        CREATE TABLE bt_patient(
            ssn INT NOT NULL,
            name VARCHAR(50),
            address VARCHAR(50),
            phone VARCHAR(50),
            insurance_id INT,
            pcp INT,
            PRIMARY KEY(ssn)
        );""")

    # Dimension estadia
    engine.execute("DROP TABLE IF EXISTS bt_stay;")
    engine.execute("""
        CREATE TABLE bt_stay(
            id INT NOT NULL,
            patient_ssn INT NOT NULL,
            room INT NOT NULL,
            start DATETIME,
            end DATETIME,
            PRIMARY KEY(id)
        );""")

    # Fact procedimiento
    engine.execute("DROP TABLE IF EXISTS ft_procedure;")
    engine.execute("""
        CREATE TABLE ft_procedure(
            id INT NOT NULL AUTO_INCREMENT,
            patient_ssn INT NOT NULL,
            procedure_code INT NOT NULL,
            stay_id INT NOT NULL,
            date DATETIME NOT NULL,
            physician_id INT NOT NULL,
            nurse_id INT,
            PRIMARY KEY(id),
            FOREIGN KEY(patient_ssn) REFERENCES bt_patient(ssn),
            FOREIGN KEY(procedure_code) REFERENCES bt_procedure(code),
            FOREIGN KEY(stay_id) REFERENCES bt_stay(id),
            FOREIGN KEY(physician_id) REFERENCES bt_employee(id),
            FOREIGN KEY(nurse_id) REFERENCES bt_employee(id)
        );""")

    engine.execute("SET FOREIGN_KEY_CHECKS = 1;")
