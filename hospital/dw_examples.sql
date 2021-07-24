-- Crear FT entrenamientos

CREATE TABLE ft_trained_in(
    training_id INT NOT NULL AUTO_INCREMENT,
    physician_id INT NOT NULL,
    treatment_code INT NOT NULL,
    CertificationDate DATETIME,
    CertificationExpires DATETIME
    PRIMARY KEY(training_id),
    FOREIGN KEY(physician_id) REFERENCES physician(EmployeeID),
    FOREIGN KEY(treatment_code) REFERENCES procedures(Code)
    metrica1
    metrica2
);

-- Crear DT de medicos

CREATE TABLE bt_physician(
    EmployeeID INT NOT NULL,
    Name VARCHAR(50) NOT NULL,
    Position VARCHAR(50),
    SSN INT NOT NULL,
    PRIMARY KEY(EmployeeID)
);

-- Insertar datos en FT entrenamientos

INSERT INTO ft_trained_in(
    physician_id,
    treatment_code,
    CertificationDate,
    CertificationExpires
)
SELECT
    Physician,
    Treatment,
    CertificationDate,
    CertificationExpires
FROM Trained_In;

