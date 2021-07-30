-- Cantidad de procedimientos por medico(physician)
SELECT e.id, e.name, COUNT(*)
FROM ft_procedure f
LEFT JOIN bt_employee e ON f.physician_id = e.id
GROUP BY e.id, e.name
ORDER BY COUNT(*) DESC;