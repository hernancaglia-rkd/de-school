from sqlalchemy import create_engine


def extract(engine):
    engine.execute("CREATE DATABASE IF NOT EXISTS staging")  # creamos DB staging para guardar la data tal cual como viene
    engine.execute("USE staging")

    engine.execute("DROP TABLE IF EXISTS raw_physician;")
    engine.execute("""
        CREATE TABLE raw_physician AS
        SELECT * FROM hospital.physician
        ;""")

    engine.execute("DROP TABLE IF EXISTS raw_nurse;")
    engine.execute("""
        CREATE TABLE raw_nurse AS
        SELECT * FROM hospital.nurse
        ;""")

    engine.execute("DROP TABLE IF EXISTS raw_procedures;")
    engine.execute("""
        CREATE TABLE raw_procedures AS
        SELECT * FROM hospital.procedures
        ;""")

    engine.execute("DROP TABLE IF EXISTS raw_patient;")
    engine.execute("""
        CREATE TABLE raw_patient AS
        SELECT * FROM hospital.patient
        ;""")

    engine.execute("DROP TABLE IF EXISTS raw_stay;")
    engine.execute("""
        CREATE TABLE raw_stay AS
        SELECT * FROM hospital.stay
        ;""")

    engine.execute("DROP TABLE IF EXISTS raw_undergoes;")
    engine.execute("""
        CREATE TABLE raw_undergoes AS
        SELECT * FROM hospital.undergoes
        ;""")


def transform(engine):
    engine.execute("USE staging")

    engine.execute("DROP TABLE IF EXISTS stg_bt_employee;")
    engine.execute("""
        CREATE TABLE stg_bt_employee AS
            SELECT
                EmployeeID AS id,
                ssn,
                name,
                position,
                'Physician' AS role,
                NULL AS registered_nurse
            FROM raw_physician
            UNION
            SELECT
                EmployeeID AS id,
                ssn,
                name,
                position,
                'Nurse' AS role,
                registered AS registered_nurse
            FROM raw_nurse
        ;""")

    engine.execute("DROP TABLE IF EXISTS stg_bt_procedure;")
    engine.execute("""
        CREATE TABLE stg_bt_procedure AS
            SELECT
                code,
                name,
                cost
            FROM raw_procedures
        ;""")

    engine.execute("DROP TABLE IF EXISTS stg_bt_patient;")
    engine.execute("""
        CREATE TABLE stg_bt_patient AS
            SELECT
                ssn,
                name,
                address,
                phone,
                InsuranceID AS insurance_id,
                pcp
            FROM raw_patient
        ;""")

    engine.execute("DROP TABLE IF EXISTS stg_bt_stay;")
    engine.execute("""
        CREATE TABLE stg_bt_stay AS
            SELECT
                StayID AS id,
                patient AS patient_ssn,
                room,
                StayStart AS start,
                StayEnd AS end
            FROM raw_stay
        ;""")

    engine.execute("DROP TABLE IF EXISTS stg_ft_procedure;")
    engine.execute("""
        CREATE TABLE stg_ft_procedure AS
            SELECT
                patient AS patient_ssn,
                Procedures AS procedure_code,
                stay AS stay_id,
                DateUndergoes AS date,
                physician AS physician_id,
                AssistingNurse AS nurse_id
            FROM raw_undergoes
        ;""")


def load(engine):
    engine.execute("USE dw_hospital")

    engine.execute("""
        INSERT INTO bt_employee(
            id,
            ssn,
            name,
            position,
            role,
            registered_nurse
        )
        SELECT
            id,
            ssn,
            name,
            position,
            role,
            registered_nurse
        FROM staging.stg_bt_employee
        ;""")

    engine.execute("""
        INSERT INTO bt_procedure(
            code,
            name,
            cost
        )
        SELECT
            code,
            name,
            cost
        FROM staging.stg_bt_procedure
        ;""")

    engine.execute("""
        INSERT INTO bt_patient(
            ssn,
            name,
            address,
            phone,
            insurance_id,
            pcp
        )
        SELECT
            ssn,
            name,
            address,
            phone,
            insurance_id,
            pcp
        FROM staging.stg_bt_patient
        ;""")

    engine.execute("""
        INSERT INTO bt_stay(
            id,
            patient_ssn,
            room,
            start,
            end
        )
        SELECT
            id,
            patient_ssn,
            room,
            start,
            end
        FROM staging.stg_bt_stay
        ;""")

    engine.execute("""
        INSERT INTO ft_procedure(
            patient_ssn,
            procedure_code,
            stay_id,
            date,
            physician_id,
            nurse_id
        )
        SELECT
            patient_ssn,
            procedure_code,
            stay_id,
            date,
            physician_id,
            nurse_id
        FROM staging.stg_ft_procedure
        ;""")


if __name__ == '__main__':
    
    # connect to server
    # cambiar root:root por tu usuario:password y 3310 por el puerto que asignaste a tu base de datos
    engine = create_engine('mysql+pymysql://root:root@localhost:3310')
    
    # extraemos los datos de la fuente y los guardamos en un area staging para usar
    extract(engine)
    
    # adecuamos los datos a la estructura de nuestro esquema y los guardamos en staging
    transform(engine)

    # agregamos los nuevos datos a nuestro data warehouse
    load(engine)
