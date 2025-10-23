-- ==============================
--  Тестовые данные
-- ==============================

-- Филиалы
INSERT INTO CafeBranch (name, address, city, phone, open_time, close_time) VALUES
('Downtown Coffee', '123 Main St', 'Amsterdam', '+31-612-345-678', '07:00', '22:00'),
('Utrecht Central', '45 Stationweg', 'Utrecht', '+31-612-999-555', '08:00', '21:00'),
('Rotterdam Harbor', '88 Havenstraat', 'Rotterdam', '+31-611-111-222', '07:30', '23:00');

-- Сотрудники
INSERT INTO Employee (name, position, hire_date, salary, email) VALUES
('Anna de Vries', 'Barista', '2022-05-01', 2500.00, 'anna@coffee.com'),
('Pieter Janssen', 'Manager', '2021-10-12', 3800.00, 'pieter@coffee.com'),
('Laura Smits', 'Cashier', '2023-01-10', 2100.00, 'laura@coffee.com'),
('Tom Bakker', 'Barista', '2022-07-07', 2400.00, 'tom@coffee.com');

-- Привязка сотрудников к филиалам
INSERT INTO EmployeeBranch (employee_id, branch_id) VALUES
(1, 1), (2, 1), (3, 2), (4, 3);

-- Клиенты
INSERT INTO Customer (name, phone, email, loyalty_points) VALUES
('Sophie van Dijk', '+31-620-111-333', 'sophie@gmail.com', 120),
('Lucas Vermeer', '+31-620-222-444', 'lucas@gmail.com', 50),
('Emma Jansen', '+31-620-333-555', 'emma@gmail.com', 30);

-- Категории меню
INSERT INTO MenuCategory (name, description) VALUES
('Coffee', 'Freshly brewed coffee drinks'),
('Tea', 'A variety of hot and iced teas'),
('Desserts', 'Homemade sweets and pastries'),
('Snacks', 'Light bites and sandwiches');

-- Пункты меню
INSERT INTO MenuItem (name, description, price, calories, image_url) VALUES
('Espresso', 'Strong and aromatic espresso shot', 2.50, 10, 'images/espresso.jpg'),
('Cappuccino', 'Espresso with steamed milk and foam', 3.20, 120, 'images/cappuccino.jpg'),
('Latte', 'Smooth espresso with steamed milk', 3.50, 150, 'images/latte.jpg'),
('Green Tea', 'Fresh green tea leaves brew', 2.00, 5, 'images/greentea.jpg'),
('Cheesecake', 'Classic creamy cheesecake', 4.50, 350, 'images/cheesecake.jpg'),
('Club Sandwich', 'Chicken, lettuce, tomato, and mayo sandwich', 5.50, 420, 'images/clubsandwich.jpg');

-- Связь категорий и пунктов меню
INSERT INTO MenuCategoryItem (category_id, item_id) VALUES
(1,1), (1,2), (1,3),
(2,4),
(3,5),
(4,6);

-- Заказы
INSERT INTO "Order" (customer_id, branch_id, employee_id, status, total_amount) VALUES
(1, 1, 1, 'completed', 6.00),
(2, 2, 3, 'completed', 9.00),
(3, 1, 2, 'created', 3.50);

-- Позиции заказов
INSERT INTO OrderItem (order_id, item_id, quantity, price) VALUES
(1, 1, 1, 2.50),
(1, 5, 1, 3.50),
(2, 3, 1, 3.50),
(2, 6, 1, 5.50),
(3, 2, 1, 3.20);

-- Платежи
INSERT INTO Payment (order_id, method, amount, status) VALUES
(1, 'card', 6.00, 'success'),
(2, 'cash', 9.00, 'success'),
(3, 'card', 3.50, 'pending');

-- Поставщики
INSERT INTO Supplier (name, phone, email, address) VALUES
('CoffeeCo', '+31-650-111-999', 'sales@coffeeco.nl', 'Beanslaan 12, Amsterdam'),
('SweetFactory', '+31-650-222-888', 'info@sweetfactory.nl', 'Bakeryweg 5, Rotterdam'),
('FreshFoods', '+31-650-333-777', 'orders@freshfoods.nl', 'Farmstraat 7, Utrecht');

-- Связь поставщиков и меню
INSERT INTO SupplierMenuItem (supplier_id, item_id, supply_price) VALUES
(1, 1, 1.50),
(1, 2, 1.80),
(2, 5, 3.00),
(3, 6, 3.20);

-- Заказы поставки
INSERT INTO SupplyOrder (supplier_id, branch_id, status) VALUES
(1, 1, 'delivered'),
(2, 3, 'in_progress'),
(3, 2, 'pending');

-- Склад
INSERT INTO Inventory (branch_id, item_name, quantity, unit) VALUES
(1, 'Coffee Beans', 50, 'kg'),
(1, 'Milk', 30, 'L'),
(2, 'Tea Leaves', 20, 'kg'),
(3, 'Cheesecake Slices', 40, 'pcs'),
(3, 'Bread Loaves', 25, 'pcs');

-- Связь склад ↔ меню (ингредиенты)
INSERT INTO InventoryMenuItem (inventory_id, item_id, quantity_used) VALUES
(1, 1, 0.02),
(1, 2, 0.03),
(1, 3, 0.04),
(2, 4, 0.01),
(3, 5, 1.00),
(3, 6, 0.50);