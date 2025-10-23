-- ==============================
--  INIT DATABASE: cafe_db
-- ==============================
-- Проверяем, существует ли база, если нет — создаём
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'cafe_db'
   ) THEN
      PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE cafe_db');
   END IF;
END
$do$;

-- Подключаемся к базе (используй psql -f init.sql для исполнения)
\connect cafe_db
-- ===== Филиалы =====
CREATE TABLE CafeBranch (
    branch_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(50),
    phone VARCHAR(20),
    open_time TIME,
    close_time TIME
);

-- ===== Сотрудники =====
CREATE TABLE Employee (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(50),
    hire_date DATE,
    salary NUMERIC(10,2),
    email VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
);

-- ===== Клиенты =====
CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(100),
    loyalty_points INT DEFAULT 0,
    registration_date TIMESTAMP DEFAULT NOW()
);

-- ===== Категории меню =====
CREATE TABLE MenuCategory (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    description TEXT
);

-- ===== Пункты меню =====
CREATE TABLE MenuItem (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price NUMERIC(10,2),
    calories INT,
    is_available BOOLEAN DEFAULT TRUE,
    image_url TEXT
);

-- ===== Заказы =====
CREATE TABLE "Order" (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES Customer(customer_id) ON DELETE SET NULL,
    branch_id INT REFERENCES CafeBranch(branch_id) ON DELETE SET NULL,
    employee_id INT REFERENCES Employee(employee_id) ON DELETE SET NULL,
    order_time TIMESTAMP DEFAULT NOW(),
    status VARCHAR(30) DEFAULT 'created',
    total_amount NUMERIC(10,2) DEFAULT 0
);

-- ===== Позиции заказа =====
CREATE TABLE OrderItem (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES "Order"(order_id) ON DELETE CASCADE,
    item_id INT REFERENCES MenuItem(item_id) ON DELETE SET NULL,
    quantity INT CHECK (quantity > 0),
    price NUMERIC(10,2)
);

-- ===== Платежи =====
CREATE TABLE Payment (
    payment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES "Order"(order_id) ON DELETE CASCADE,
    method VARCHAR(30),
    amount NUMERIC(10,2),
    payment_time TIMESTAMP DEFAULT NOW(),
    status VARCHAR(30) DEFAULT 'success'
);

-- ===== Поставщики =====
CREATE TABLE Supplier (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT
);

-- ===== Заказы поставки =====
CREATE TABLE SupplyOrder (
    supply_order_id SERIAL PRIMARY KEY,
    supplier_id INT REFERENCES Supplier(supplier_id) ON DELETE CASCADE,
    branch_id INT REFERENCES CafeBranch(branch_id) ON DELETE CASCADE,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(30) DEFAULT 'in_progress'
);

-- ===== Склад =====
CREATE TABLE Inventory (
    inventory_id SERIAL PRIMARY KEY,
    branch_id INT REFERENCES CafeBranch(branch_id) ON DELETE CASCADE,
    item_name VARCHAR(100),
    quantity NUMERIC(10,2),
    unit VARCHAR(10),
    last_updated TIMESTAMP DEFAULT NOW()
);

-- ==============================
--  M:N Связи
-- ==============================

-- Сотрудники ↔ Филиалы
CREATE TABLE EmployeeBranch (
    employee_id INT REFERENCES Employee(employee_id) ON DELETE CASCADE,
    branch_id INT REFERENCES CafeBranch(branch_id) ON DELETE CASCADE,
    assigned_date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (employee_id, branch_id)
);

-- Поставщики ↔ Товары
CREATE TABLE SupplierMenuItem (
    supplier_id INT REFERENCES Supplier(supplier_id) ON DELETE CASCADE,
    item_id INT REFERENCES MenuItem(item_id) ON DELETE CASCADE,
    supply_price NUMERIC(10,2),
    PRIMARY KEY (supplier_id, item_id)
);

-- Категории ↔ Пункты меню
CREATE TABLE MenuCategoryItem (
    category_id INT REFERENCES MenuCategory(category_id) ON DELETE CASCADE,
    item_id INT REFERENCES MenuItem(item_id) ON DELETE CASCADE,
    PRIMARY KEY (category_id, item_id)
);

-- Склад ↔ Пункты меню (ингредиенты для блюд)
CREATE TABLE InventoryMenuItem (
    inventory_id INT REFERENCES Inventory(inventory_id) ON DELETE CASCADE,
    item_id INT REFERENCES MenuItem(item_id) ON DELETE CASCADE,
    quantity_used NUMERIC(10,2),
    PRIMARY KEY (inventory_id, item_id)
);

-- ==============================
--  Дополнительные таблицы
-- ==============================


-- Элементы заказа поставки
CREATE TABLE SupplyOrderItem (
    supply_order_item_id SERIAL PRIMARY KEY,
    supply_order_id INT REFERENCES SupplyOrder(supply_order_id) ON DELETE CASCADE,
    item_id INT REFERENCES MenuItem(item_id),
    quantity INT CHECK (quantity > 0)
);
