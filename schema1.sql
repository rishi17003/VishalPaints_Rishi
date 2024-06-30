create database vishalpaints;
use vishalpaints;
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    yield int,
    total_rate DECIMAL(10, 2) NOT NULL
    
);
drop table products;
CREATE TABLE raw_materials (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    mat_type VARCHAR(255) NOT NULL
);
drop table raw_materials;
INSERT INTO raw_materials (name, price, mat_type) VALUES
    ('P1', 227.00, 'Pigment'),
    ('P11', 109.00, 'Pigment'),
    ('P6', 170.00, 'Pigment'),
    ('P3', 560.00, 'Pigment'),
    ('P4', 158.00, 'Pigment'),
    ('P5', 109.00, 'Pigment'),
    ('P60', 59.00, 'Pigment'),
    ('P7', 115.00, 'Pigment'),
    ('P100', 35.00, 'Pigment'),
    ('P50', 125.00, 'Pigment'),
    ('P70', 130.00, 'Pigment'),
    ('Redoxide Powder', 15.00, 'Pigment'),
    ('White Whiting', 25.00, 'Pigment'),
    ('Talc', 104.00, 'Pigment'),
    ('A1', 162.00, 'Additive'),
    ('A2', 150.00, 'Additive'),
    ('HCO', 150.00, 'Additive'),
    ('ACE', 600.00, 'Additive'),
    ('PINCOIL', 150.00, 'Additive'),
    ('BRIGHT', 600.00, 'Additive'),
    ('CATALYST MATT', 225.00, 'Additive'),
    ('ICLAY', 308.00, 'Additive'),
    ('ICLAY JELLY 10%', 250.00, 'Additive'),
    ('LEAK 10%', 108.00, 'Additive'),
    ('OMEGA', 55.00, 'Additive'),
    ('DH', 134.00, 'Additive'),
    ('M1 50%', 125.00, 'Resin'),
    ('M1 70%', 124.00, 'Resin'),
    ('M6', 206.00, 'Resin'),
    ('Mo 70%', 220.00, 'Resin'),
    ('MD', 129.00, 'Resin'),
    ('MD 60%', 125.00, 'Resin'),
    ('R 920', 160.00, 'Resin'),
    ('DBTL', 40.00, 'Resin'),
    ('927', 109.00, 'Resin'),
    ('1030', 135.00, 'Resin'),
    ('S1', 100.00, 'Thinner'),
    ('C1', 1.00, 'Thinner'),
    ('S6', 128.50, 'Thinner'),
    ('S20', 47.50, 'Thinner'),
    ('BA (Kg)', 135.00, 'Thinner'),
    ('BA (Lit)', 116.50, 'Thinner'),
    ('ETHYLE', 230.00, 'Thinner');


DESCRIBE raw_materials;

DROP TABLE IF EXISTS product_raw_materials;

CREATE TABLE product_raw_materials (
    product_id INT,
    material_id INT,
    quantity DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (material_id) REFERENCES raw_materials(id)
);


select * from raw_materials;

describe products;

select* from products;

ALTER TABLE products MODIFY total_rate DECIMAL(15,2);

ALTER TABLE products
ADD COLUMN viscosity DECIMAL(10, 2) NOT NULL,
ADD COLUMN weight_lit DECIMAL(10, 2) NOT NULL,
ADD COLUMN container_cost DECIMAL(10, 2) NOT NULL,
ADD COLUMN transport_cost DECIMAL(10, 2) NOT NULL,
ADD COLUMN sales_cost DECIMAL(10, 2) NOT NULL,
ADD COLUMN misc_cost DECIMAL(10, 2) NOT NULL;