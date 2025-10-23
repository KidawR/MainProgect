from sqlalchemy import create_engine, text
from datetime import datetime
from decimal import Decimal
from app.crud_mongo import log_action  # твоя функция логирования

# ===== Настройки подключения =====
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_DB = "cafe_db"

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}")

# ===== ВСПОМОГАТЕЛЬНЫЕ =====
def safe_log(user_id, action, details=None):
    """
    Логирование с конверсией Decimal -> float
    """
    def convert(value):
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, dict):
            return {k: convert(v) for k, v in value.items()}
        if isinstance(value, list):
            return [convert(v) for v in value]
        return value

    safe_details = convert(details or {})
    log_action(user_id=user_id, action=action, details=safe_details)


# ===================================================
# ===============  КЛИЕНТЫ  ========================
# ===================================================

def get_customers():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Customer"))
        return [dict(r._mapping) for r in result]

def add_customer(name, phone, email):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO Customer (name, phone, email, registration_date)
                VALUES (:name, :phone, :email, NOW())
                RETURNING customer_id
            """),
            {"name": name, "phone": phone, "email": email}
        )
        customer_id = result.scalar()
    safe_log(customer_id, "add_customer", {"name": name, "phone": phone, "email": email})
    return customer_id

def update_customer(customer_id, **kwargs):
    fields = ', '.join([f"{k} = :{k}" for k in kwargs])
    kwargs["customer_id"] = customer_id
    with engine.begin() as conn:
        conn.execute(text(f"UPDATE Customer SET {fields} WHERE customer_id=:customer_id"), kwargs)
    safe_log(customer_id, "update_customer", kwargs)

def delete_customer(customer_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM Customer WHERE customer_id=:id"), {"id": customer_id})
    safe_log(customer_id, "delete_customer")


# ===================================================
# ===============  СОТРУДНИКИ  ======================
# ===================================================

def add_employee(name, position, hire_date, salary, email, is_active=True):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO Employee (name, position, hire_date, salary, email, is_active)
                VALUES (:name, :position, :hire_date, :salary, :email, :is_active)
                RETURNING employee_id
            """),
            {"name": name, "position": position, "hire_date": hire_date,
             "salary": salary, "email": email, "is_active": is_active}
        )
        employee_id = result.scalar()
    safe_log(employee_id, "add_employee", {"name": name, "position": position, "salary": salary})
    return employee_id

def assign_employee_to_branch(employee_id, branch_id):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO EmployeeBranch (employee_id, branch_id, assigned_date)
                VALUES (:employee_id, :branch_id, CURRENT_DATE)
                ON CONFLICT DO NOTHING
            """),
            {"employee_id": employee_id, "branch_id": branch_id}
        )
    safe_log(employee_id, "assign_employee_to_branch", {"branch_id": branch_id})

def get_employees(branch_id=None):
    query = """
        SELECT e.*, eb.branch_id 
        FROM Employee e
        LEFT JOIN EmployeeBranch eb ON e.employee_id = eb.employee_id
    """
    params = {}
    if branch_id:
        query += " WHERE eb.branch_id=:branch_id"
        params["branch_id"] = branch_id
    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        employees = [dict(r._mapping) for r in result]
    safe_log(0, "get_employees", {"branch_id": branch_id})
    return employees

def update_employee(employee_id, **kwargs):
    fields = ', '.join([f"{k} = :{k}" for k in kwargs])
    kwargs["employee_id"] = employee_id
    with engine.begin() as conn:
        conn.execute(text(f"UPDATE Employee SET {fields} WHERE employee_id=:employee_id"), kwargs)
    safe_log(employee_id, "update_employee", kwargs)

def remove_employee(employee_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM Employee WHERE employee_id=:id"), {"id": employee_id})
    safe_log(employee_id, "remove_employee")


# ===================================================
# ===============  МЕНЮ =============================
# ===================================================

def add_menu_category(name, description=None):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO MenuCategory (name, description) VALUES (:name, :description)"),
            {"name": name, "description": description}
        )
    safe_log(0, "add_menu_category", {"name": name, "description": description})

def get_menu_categories():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM MenuCategory"))
        categories = [dict(r._mapping) for r in result]
    safe_log(0, "get_menu_categories")
    return categories

def add_menu_item(name, description, price, calories, is_available=True, image_url=None):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO MenuItem (name, description, price, calories, is_available, image_url)
                VALUES (:name, :description, :price, :calories, :is_available, :image_url)
            """),
            {"name": name, "description": description, "price": price,
             "calories": calories, "is_available": is_available, "image_url": image_url}
        )
    safe_log(0, "add_menu_item", {"name": name, "price": price})

def assign_item_to_category(item_id, category_id):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO MenuCategoryItem (category_id, item_id)
                VALUES (:category_id, :item_id)
                ON CONFLICT DO NOTHING
            """),
            {"category_id": category_id, "item_id": item_id}
        )
    safe_log(0, "assign_item_to_category", {"item_id": item_id, "category_id": category_id})

def get_menu():
    query = """
        SELECT mi.item_id, mi.name, mi.price, mi.is_available, mc.name AS category
        FROM MenuItem mi
        LEFT JOIN MenuCategoryItem mci ON mi.item_id = mci.item_id
        LEFT JOIN MenuCategory mc ON mci.category_id = mc.category_id
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        menu = [dict(r._mapping) for r in result]
    safe_log(0, "get_menu")
    return menu

def update_menu_item(item_id, **kwargs):
    fields = ', '.join([f"{k} = :{k}" for k in kwargs])
    kwargs["item_id"] = item_id
    with engine.begin() as conn:
        conn.execute(text(f"UPDATE MenuItem SET {fields} WHERE item_id=:item_id"), kwargs)
    safe_log(item_id, "update_menu_item", kwargs)

def remove_menu_item(item_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM MenuItem WHERE item_id=:item_id"), {"item_id": item_id})
    safe_log(item_id, "remove_menu_item")


# ===================================================
# ===============  ЗАКАЗЫ ===========================
# ===================================================

def create_order(customer_id, branch_id, employee_id, total_amount):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO "Order" (customer_id, branch_id, employee_id, total_amount, status)
                VALUES (:customer_id, :branch_id, :employee_id, :total_amount, 'created')
                RETURNING order_id
            """),
            {"customer_id": customer_id, "branch_id": branch_id,
             "employee_id": employee_id, "total_amount": total_amount}
        )
        order_id = result.scalar()
    safe_log(customer_id, "create_order", {"order_id": order_id, "total_amount": total_amount})
    return order_id

def get_orders():
    with engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM "Order"'))
        orders = [dict(r._mapping) for r in result]
    safe_log(0, "get_orders")
    return orders

def update_order_status(order_id, status):
    with engine.begin() as conn:
        conn.execute(text('UPDATE "Order" SET status=:status WHERE order_id=:id'),
                     {"status": status, "id": order_id})
    safe_log(0, "update_order_status", {"order_id": order_id, "status": status})

def delete_order(order_id):
    with engine.begin() as conn:
        conn.execute(text('DELETE FROM "Order" WHERE order_id=:id'), {"id": order_id})
    safe_log(0, "delete_order", {"order_id": order_id})

def get_order(order_id):
    with engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM "Order" WHERE order_id=:id'), {"id": order_id}).fetchone()
        order = dict(result._mapping) if result else None
    safe_log(0, "get_order", {"order_id": order_id})
    return order

def get_orders_by_customer(customer_id):
    with engine.connect() as conn:
        result = conn.execute(
            text('SELECT * FROM "Order" WHERE customer_id=:cid ORDER BY order_time DESC'),
            {"cid": customer_id}
        )
        orders = [dict(r._mapping) for r in result]
    safe_log(customer_id, "get_orders_by_customer")
    return orders

def add_order_item(order_id, item_id, quantity):
    with engine.begin() as conn:
        price = conn.execute(text("SELECT price FROM MenuItem WHERE item_id=:id"), {"id": item_id}).scalar()
        conn.execute(
            text("""
                INSERT INTO OrderItem (order_id, item_id, quantity, price)
                VALUES (:order_id, :item_id, :quantity, :price)
            """),
            {"order_id": order_id, "item_id": item_id, "quantity": quantity, "price": price}
        )
    safe_log(0, "add_order_item", {"order_id": order_id, "item_id": item_id, "quantity": quantity, "price": price})

def update_order_total(order_id):
    with engine.begin() as conn:
        total = conn.execute(
            text("SELECT SUM(quantity * price) FROM OrderItem WHERE order_id=:id"),
            {"id": order_id}
        ).scalar()
        conn.execute(text('UPDATE "Order" SET total_amount=:t WHERE order_id=:id'),
                     {"t": total or 0, "id": order_id})
    safe_log(0, "update_order_total", {"order_id": order_id, "total_amount": total or 0})


# ===================================================
# ===============  СКЛАД ============================
# ===================================================

def create_inventory(branch_id, item_name, quantity, unit):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO Inventory (branch_id, item_name, quantity, unit)
                VALUES (:branch_id, :item_name, :quantity, :unit)
            """),
            {"branch_id": branch_id, "item_name": item_name, "quantity": quantity, "unit": unit}
        )
    safe_log(0, "create_inventory", {"branch_id": branch_id, "item_name": item_name, "quantity": quantity})

def get_inventory(branch_id=None):
    query = "SELECT * FROM Inventory"
    params = {}
    if branch_id:
        query += " WHERE branch_id=:branch_id"
        params["branch_id"] = branch_id
    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        inventory = [dict(r._mapping) for r in result]
    safe_log(0, "get_inventory", {"branch_id": branch_id})
    return inventory

def update_inventory(branch_id, item_name, quantity_delta):
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE Inventory
                SET quantity = quantity + :delta, last_updated = NOW()
                WHERE branch_id=:b AND item_name=:n
            """),
            {"delta": quantity_delta, "b": branch_id, "n": item_name}
        )
    safe_log(0, "update_inventory", {"branch_id": branch_id, "item_name": item_name, "delta": quantity_delta})


# ===================================================
# ===============  ПОСТАВКИ =========================
# ===================================================

def create_supply_order(supplier_id, branch_id, status="in_progress"):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO SupplyOrder (supplier_id, branch_id, status)
                VALUES (:supplier_id, :branch_id, :status)
                RETURNING supply_order_id
            """),
            {"supplier_id": supplier_id, "branch_id": branch_id, "status": status}
        )
        supply_order_id = result.scalar()
    safe_log(0, "create_supply_order", {"supply_order_id": supply_order_id})
    return supply_order_id

def get_supply_orders():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM SupplyOrder"))
        orders = [dict(r._mapping) for r in result]
    safe_log(0, "get_supply_orders")
    return orders

def get_supply_order(supply_order_id):
    with engine.connect() as conn:
        order = conn.execute(text("SELECT * FROM SupplyOrder WHERE supply_order_id=:id"),
                             {"id": supply_order_id}).fetchone()
        if not order:
            return None
        items = conn.execute(text("SELECT * FROM SupplyOrderItem WHERE supply_order_id=:id"),
                             {"id": supply_order_id})
        data = dict(order._mapping)
        data["items"] = [dict(r._mapping) for r in items]
    safe_log(0, "get_supply_order", {"supply_order_id": supply_order_id})
    return data

def add_item_to_supply(supply_order_id, item_id, quantity):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO SupplyOrderItem (supply_order_id, item_id, quantity)
                VALUES (:sid, :iid, :q)
            """),
            {"sid": supply_order_id, "iid": item_id, "q": quantity}
        )
    safe_log(0, "add_item_to_supply", {"supply_order_id": supply_order_id, "item_id": item_id, "quantity": quantity})


# ===================================================
# ===============  ПОСТАВЩИКИ =======================
# ===================================================

def add_supplier(name, phone, email, address):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO Supplier (name, phone, email, address)
                VALUES (:name, :phone, :email, :address)
            """),
            {"name": name, "phone": phone, "email": email, "address": address}
        )
    safe_log(0, "add_supplier", {"name": name, "phone": phone})

def link_supplier_item(supplier_id, item_id, supply_price):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO SupplierMenuItem (supplier_id, item_id, supply_price)
                VALUES (:supplier_id, :item_id, :supply_price)
                ON CONFLICT DO NOTHING
            """),
            {"supplier_id": supplier_id, "item_id": item_id, "supply_price": supply_price}
        )
    safe_log(0, "link_supplier_item", {"supplier_id": supplier_id, "item_id": item_id, "supply_price": supply_price})

def get_suppliers():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Supplier"))
        suppliers = [dict(r._mapping) for r in result]
    safe_log(0, "get_suppliers")
    return suppliers

def get_supplier_items(supplier_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT mi.name, smi.supply_price
                FROM SupplierMenuItem smi
                JOIN MenuItem mi ON smi.item_id = mi.item_id
                WHERE smi.supplier_id=:id
            """),
            {"id": supplier_id}
        )
        items = [dict(r._mapping) for r in result]
    safe_log(supplier_id, "get_supplier_items")
    return items


# ===================================================
# ===============  ВСПОМОГАТЕЛЬНЫЕ ==================
# ===================================================

def get_branches():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM CafeBranch"))
        branches = [dict(r._mapping) for r in result]
    safe_log(0, "get_branches")
    return branches

def get_menu_items():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM MenuItem ORDER BY item_id"))
        items = [dict(r._mapping) for r in result]
    safe_log(0, "get_menu_items")
    return items


# ===== NtoN функции =====

def get_items_by_category(category_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT mi.*
                FROM MenuItem mi
                JOIN MenuCategoryItem mci ON mi.item_id = mci.item_id
                WHERE mci.category_id=:cid
            """),
            {"cid": category_id}
        ).fetchall()
        items = [r._mapping for r in result]
    safe_log(0, "get_items_by_category", {"category_id": category_id})
    return items

def get_items_by_supplier(supplier_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT mi.*, smi.supply_price
                FROM MenuItem mi
                JOIN SupplierMenuItem smi ON mi.item_id = smi.item_id
                WHERE smi.supplier_id=:sid
            """),
            {"sid": supplier_id}
        ).fetchall()
        items = [r._mapping for r in result]
    safe_log(supplier_id, "get_items_by_supplier")
    return items

def get_suppliers_by_item(item_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT s.*
                FROM Supplier s
                JOIN SupplierMenuItem smi ON s.supplier_id = smi.supplier_id
                WHERE smi.item_id=:iid
            """),
            {"iid": item_id}
        ).fetchall()
        suppliers = [r._mapping for r in result]
    safe_log(0, "get_suppliers_by_item", {"item_id": item_id})
    return suppliers

def get_branches_by_employee(employee_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT cb.*
                FROM CafeBranch cb
                JOIN EmployeeBranch eb ON cb.branch_id = eb.branch_id
                WHERE eb.employee_id=:eid
            """),
            {"eid": employee_id}
        ).fetchall()
        branches = [r._mapping for r in result]
    safe_log(employee_id, "get_branches_by_employee")
    return branches
