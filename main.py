import sqlite3
import pandas as pd

conn = sqlite3.connect("data.sqlite")

# 1
q1 = pd.read_sql("""
SELECT firstName, lastName, jobTitle
FROM employees
JOIN offices
ON employees.officeCode = offices.officeCode
WHERE offices.city = 'Boston';
""", conn)
print(q1)

# 2
q2 = pd.read_sql("""
SELECT offices.officeCode, offices.city
FROM offices
LEFT JOIN employees
ON offices.officeCode = employees.officeCode
WHERE employees.employeeNumber IS NULL;
""", conn)
print(q2)

# 3
q3 = pd.read_sql("""
SELECT employees.firstName, employees.lastName, offices.city, offices.state
FROM employees
LEFT JOIN offices
ON employees.officeCode = offices.officeCode
ORDER BY employees.firstName, employees.lastName;
""", conn)
print(q3)

# 4
q4 = pd.read_sql("""
SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
FROM customers
WHERE customerNumber NOT IN (
SELECT customerNumber
FROM orders
)
ORDER BY contactLastName;
""", conn)
print(q4)

# 5
q5 = pd.read_sql("""
SELECT customers.contactFirstName,
customers.contactLastName,
payments.amount,
payments.paymentDate
FROM customers
JOIN payments
ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(payments.amount AS REAL) DESC;
""", conn)
print(q5)

# 6
q6 = pd.read_sql("""
SELECT employees.employeeNumber,
employees.firstName,
employees.lastName,
COUNT(customers.customerNumber) AS numberOfCustomers
FROM employees
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employees.employeeNumber, employees.firstName, employees.lastName
HAVING AVG(customers.creditLimit) > 90000
ORDER BY numberOfCustomers DESC;
""", conn)
print(q6)

# 7
q7 = pd.read_sql("""
SELECT products.productName,
COUNT(orderdetails.orderNumber) AS numorders,
SUM(orderdetails.quantityOrdered) AS totalunits
FROM products
JOIN orderdetails
ON products.productCode = orderdetails.productCode
GROUP BY products.productName
ORDER BY totalunits DESC;
""", conn)
print(q7)

# 8
q8 = pd.read_sql("""
SELECT products.productName,
products.productCode,
COUNT(DISTINCT orders.customerNumber) AS numpurchasers
FROM products
JOIN orderdetails
ON products.productCode = orderdetails.productCode
JOIN orders
ON orderdetails.orderNumber = orders.orderNumber
GROUP BY products.productName, products.productCode
ORDER BY numpurchasers DESC;
""", conn)
print(q8)

# 9
q9 = pd.read_sql("""
SELECT offices.officeCode,
offices.city,
COUNT(customers.customerNumber) AS n_customers
FROM offices
JOIN employees
ON offices.officeCode = employees.officeCode
LEFT JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY offices.officeCode, offices.city;
""", conn)
print(q9)

# 10
q10 = pd.read_sql("""
SELECT DISTINCT employees.employeeNumber,
employees.firstName,
employees.lastName,
offices.city,
offices.officeCode
FROM employees
JOIN offices
ON employees.officeCode = offices.officeCode
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
JOIN orders
ON customers.customerNumber = orders.customerNumber
JOIN orderdetails
ON orders.orderNumber = orderdetails.orderNumber
WHERE orderdetails.productCode IN (
SELECT orderdetails.productCode
FROM orderdetails
JOIN orders
ON orderdetails.orderNumber = orders.orderNumber
GROUP BY orderdetails.productCode
HAVING COUNT(DISTINCT orders.customerNumber) < 20
);
""", conn)
print(q10)

conn.close()
