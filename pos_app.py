from pos_logic import (
    add_menu,
    calc_bill,
    create_order,
    load_data,
    sold_names,
    to_float,
    to_int,
)


def input_int(message):
    raw = input(message)
    ok, value = to_int(raw)
    if not ok:
        print("กรุณาใส่เป็นจำนวนเต็ม")
        return None
    return value


def input_float(message):
    raw = input(message)
    ok, value = to_float(raw)
    if not ok:
        print("กรุณาใส่เป็นตัวเลข")
        return None
    return value


def show_menus(data):
    print("----- เมนู -----")
    for item in data["menus"]:
        status = "พร้อมขาย" if item["available"] else "หมด"
        print(item["id"], item["name"], item["price"], "บาท", status)


def menu_add(data):
    name = input("ชื่อเมนู: ").strip()
    if not name:
        print("ชื่อเมนูห้ามว่าง")
        return
    price = input_float("ราคา: ")
    if price is None or price < 0:
        print("ราคาไม่ถูกต้อง")
        return
    raw = input("พร้อมขายหรือไม่ (y/n): ").strip().lower()
    available = raw == "y" or raw == "yes"
    new_id = add_menu(data, name, price, available)
    print("เพิ่มเมนูรหัส", new_id, "แล้ว")


def menu_order(data):
    show_menus(data)
    table_no = input_int("หมายเลขโต๊ะ: ")
    menu_id = input_int("รหัสเมนู: ")
    qty = input_int("จำนวน: ")
    if table_no is None or menu_id is None or qty is None:
        return
    if table_no < 1 or table_no > 20:
        print("โต๊ะต้องอยู่ระหว่าง 1 ถึง 20")
        return
    ok, result = create_order(data, table_no, menu_id, qty)
    if ok:
        print("รับออเดอร์แล้ว ยอด", result["total"], "บาท")
    else:
        print(result)


def menu_bill(data):
    table_no = input_int("เช็คบิลโต๊ะไหน: ")
    if table_no is None:
        return
    discount = input_float("ส่วนลด: ")
    if discount is None or discount < 0:
        print("ส่วนลดไม่ถูกต้อง")
        return
    bill = calc_bill(data["orders"], table_no, 0.10, 0.07, discount)
    if bill["count"] == 0:
        print("โต๊ะนี้ยังไม่มีออเดอร์")
        return
    print("ยอดก่อนคิด", bill["subtotal"])
    print("ค่าบริการ", bill["service"])
    print("ภาษี", bill["tax"])
    print("ส่วนลด", bill["discount"])
    print("ยอดสุทธิ", bill["total"])


def menu_report(data):
    names = sold_names(data["orders"])
    print("จำนวนออเดอร์", len(data["orders"]))
    if names:
        print("เมนูที่มีการสั่ง:", ", ".join(names))
    else:
        print("ยังไม่มีออเดอร์")


def run():
    data = load_data()
    running = True
    while running:
        print("===== ระบบร้านอาหาร =====")
        print("1. แสดงเมนู")
        print("2. เพิ่มเมนู")
        print("3. รับออเดอร์")
        print("4. เช็คบิล")
        print("5. รายงาน")
        print("0. ออกจากโปรแกรม")
        choice = input("เลือกเมนู: ").strip()
        if choice == "1":
            show_menus(data)
        elif choice == "2":
            menu_add(data)
        elif choice == "3":
            menu_order(data)
        elif choice == "4":
            menu_bill(data)
        elif choice == "5":
            menu_report(data)
        elif choice == "0":
            print("บันทึกข้อมูลแล้ว ปิดโปรแกรม")
            running = False
        else:
            print("กรุณาเลือก 0 ถึง 5 เท่านั้น")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nปิดโปรแกรม")