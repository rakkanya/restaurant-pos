import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "pos_data.json"


def load_data():
    empty = {
                "menus": [
            {"id": 1, "name": "ข้าวหน้าเนื้อ", "price": 89.0, "available": True},
            {"id": 2, "name": "ข้าวหน้าเนื้อไข่ลวก", "price": 99.0, "available": True},
            {"id": 3, "name": "เนื้อย่างจิ้มแจ่ว", "price": 129.0, "available": True}
        ],
        "orders": [],
    }
    try:
        if not DATA_FILE.exists():
            save_data(empty)
            return empty
        text = DATA_FILE.read_text(encoding="utf-8")
        data = json.loads(text)
        if not isinstance(data, dict):
            return empty
        data.setdefault("menus", [])
        data.setdefault("orders", [])
        return data
    except (OSError, json.JSONDecodeError):
        print("อ่านไฟล์ไม่สำเร็จ ใช้ข้อมูลว่างแทน")
        return empty


def save_data(data):
    try:
        DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except OSError:
        print("บันทึกไฟล์ไม่สำเร็จ")
        return False


def to_int(text):
    try:
        return True, int(str(text).strip())
    except (TypeError, ValueError):
        return False, 0


def to_float(text):
    try:
        return True, float(str(text).strip())
    except (TypeError, ValueError):
        return False, 0.0


def find_menu(menus, menu_id):
    for item in menus:
        if item.get("id") == menu_id:
            return item
    return None


def add_menu(data, name, price, available):
    menus = data["menus"]
    new_id = 1
    if menus:
        new_id = max(item["id"] for item in menus) + 1
    menus.append({
        "id": new_id,
        "name": name,
        "price": price,
        "available": available,
    })
    save_data(data)
    return new_id


def create_order(data, table_no, menu_id, qty):
    item = find_menu(data["menus"], menu_id)
    if item is None:
        return False, "ไม่พบเมนู"
    if not item.get("available"):
        return False, "เมนูหมด"
    if qty < 1:
        return False, "จำนวนต้องมากกว่า 0"
    total = round(item["price"] * qty, 2)
    order = {
        "table": table_no,
        "menu": item["name"],
        "qty": qty,
        "total": total,
    }
    data["orders"].append(order)
    save_data(data)
    return True, order


def calc_bill(orders, table_no, service_rate, tax_rate, discount):
    selected = [row for row in orders if row.get("table") == table_no]
    subtotal = 0.0
    for row in selected:
        subtotal += float(row["total"])
    service = round(subtotal * service_rate, 2)
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + service + tax - discount, 2)
    if total < 0:
        total = 0.0
    return {
        "count": len(selected),
        "subtotal": subtotal,
        "service": service,
        "tax": tax,
        "discount": discount,
        "total": total,
    }


def sold_names(orders):
    names = set()
    for row in orders:
        names.add(row.get("menu", ""))
    return names