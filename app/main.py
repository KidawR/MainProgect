from crud_postgres import *  # PostgreSQL функции для заказов, меню, сотрудников и т.д.
from crud_mongo import *     # MongoDB функции для отзывов и логов

# ====== Действия клиента ======
def customer_actions():
    print("=== Customer Actions ===")
    # Добавление клиента
    print("\n👤 Добавление клиента...")
    cust_id = add_customer("Пётр Петров", "89991234568", "petr@example.com")
    print(f"✅ Добавлен клиент (id={cust_id})")

    # Обновление клиента
    update_customer(customer_id=cust_id, phone="89997654321", email="petr_new@example.com")
    print("\nОбновлённые клиенты:")
    for c in get_customers():
        print(f"{c['customer_id']}: {c['name']} - {c['phone']} - {c['email']}")

    # Удаление клиента
    delete_customer(customer_id=cust_id)
    print("\nПосле удаления клиента:")
    for c in get_customers():
        print(f"{c['customer_id']}: {c['name']} - {c['phone']} - {c['email']}")
    # Просмотр меню
    print("\n📋 Меню:")
    for item in get_menu_items():
        print(f"- {item['name']} ({item['price']}₽) — {item['description']}")

    # Просмотр филиалов
    print("\n🏠 Филиалы:")
    for branch in get_branches():
        print(f"- {branch['name']} ({branch['city']}) — {branch['address']}")

    print("\n🛒 Создание заказа...")
    order_id = create_order(customer_id=1, branch_id=1, employee_id=1, total_amount=0)

    # Добавление позиций в заказ
    add_order_item(order_id=order_id, item_id=1, quantity=2)
    add_order_item(order_id=order_id, item_id=2, quantity=1)
    update_order_total(order_id)

    # Получаем и выводим заказ с его позициями
    print("✅ Заказ создан:", get_order(order_id))

    # Просмотр заказов клиента
    print("\n📦 Мои заказы:")
    for order in get_orders_by_customer(customer_id=1):
        print(order)

    # Добавление отзыва через MongoDB
    print("\n⭐ Добавление отзыва...")
    add_review(customer_id=1, branch_id=1, rating=5, comment="Очень вкусно!", sentiment=5)
    print("Отзывы о филиале:", get_reviews(branch_id=1))

# ====== Действия сотрудника ======
def employee_actions():
    print("\n=== Employee Actions ===")

    # Получение списка клиентов
    customers = get_customers()
    print("\n📋 Список клиентов:")
    for c in customers:
        print(f"{c['customer_id']}: {c['name']} - {c['phone']} - {c['email']}")

    # Обновление статуса заказа
    update_order_status(order_id=7, status="completed")
    print("📦 Заказ обновлён:", get_order(7))

    # Создание заявки на поставку
    print("\n📦 Создание заявки на поставку...")
    supply_id = create_supply_order(supplier_id=1, branch_id=1)
    add_item_to_supply(supply_order_id=supply_id, item_id=1, quantity=10)
    add_item_to_supply(supply_order_id=supply_id, item_id=2, quantity=5)
    print("Заявка создана:", get_supply_order(supply_id))

    # Просмотр текущих поставок
    print("\n🚚 Активные поставки:")
    for s in get_supply_orders():
        print(s)

    # Управление складом
    print("\n🏭 Обновление склада...")
    create_inventory(branch_id=1, item_name="Молоко", quantity=20, unit="л")
    update_inventory(branch_id=1, item_name="Молоко", quantity_delta=-5)
    print("Склад:", get_inventory(branch_id=1))

# ====== Действия администратора ======
def admin_actions():
    print("\n=== Admin Actions ===")

    # === Admin Actions ===
    print("\n👤 Добавление сотрудника...")
    emp_id = add_employee("Иван Иванов", "Бариста", "2025-10-23", 1200, "ivan@example.com")
    print(f"✅ Добавлен сотрудник (id={emp_id})")

    # Получаем список всех сотрудников
    employees = get_employees()
    print("\n📋 Список сотрудников:")
    for e in employees:
        print(f"{e['employee_id']}: {e['name']} - {e['position']} - {e['email']}")

    # Обновление данных сотрудника
    update_employee(employee_id=emp_id, salary=35000, position="Старший бариста")
    print("Обновлённые сотрудники:", get_employees())

    # Удаление сотрудника
    remove_employee(employee_id=emp_id)
    print("После удаления:", get_employees())

    # Удаление заказа
    delete_order(order_id=1)
    print("После удаления заказа:", get_orders())

    #####################################################################
    # Логирование действий через MongoDB
    log_action(user_id=1, action="delete_order", details={"order_id": 1})
    ######################################################################

def print_all_relationships():
    # ===================================================
    # 1️⃣ Категории ↔ Пункты меню
    # ===================================================
    print("\n=== Категории ↔ Пункты меню ===")
    for cat in get_menu_categories():
        print(f"\nКатегория: {cat['name']} ({cat.get('description','')})")
        items = get_items_by_category(cat['category_id'])
        if items:
            for item in items:
                print(f" - {item['name']} ({item['price']}₽): {item.get('description','')}")
        else:
            print(" - Пункты меню отсутствуют")

    # ===================================================
    # 2️⃣ Поставщики ↔ Товары
    # ===================================================
    print("\n=== Поставщики ↔ Товары ===")
    for sup in get_suppliers():
        print(f"\nПоставщик: {sup['name']} (тел: {sup.get('phone','')}, email: {sup.get('email','')})")
        items = get_items_by_supplier(sup['supplier_id'])
        if items:
            for item in items:
                print(f" - {item['name']} ({item['price']}₽), цена поставки: {item['supply_price']}₽")
        else:
            print(" - Товары отсутствуют")

    # ===================================================
    # 3️⃣ Сотрудники ↔ Филиалы
    # ===================================================
    print("\n=== Сотрудники ↔ Филиалы ===")
    for emp in get_employees():
        print(f"\nСотрудник: {emp['name']} ({emp['position']}), email: {emp.get('email','')}")
        branches = get_branches_by_employee(emp['employee_id'])
        if branches:
            for b in branches:
                print(f" - Филиал: {b['name']} ({b['city']}), адрес: {b['address']}")
        else:
            print(" - Филиалы отсутствуют")

    # ===================================================
    # 4️⃣ Пункты меню ↔ Поставщики
    # ===================================================
    print("\n=== Пункты меню ↔ Поставщики ===")
    for item in get_menu_items():
        print(f"\nПункт меню: {item['name']} ({item['price']}₽)")
        suppliers = get_suppliers_by_item(item['item_id'])
        if suppliers:
            for s in suppliers:
                print(f" - Поставщик: {s['name']} (тел: {s.get('phone','')}, email: {s.get('email','')})")
        else:
            print(" - Поставщики отсутствуют")
# ====== Точка входа ======
if __name__ == "__main__":
    customer_actions()
    employee_actions()
    admin_actions()
    print_all_relationships()

## docker system prune -a --volumes
