import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("ВелоПрокат — Учёт заказов")
root.geometry("800x500")

# Данные: цены велосипедов и коэффициенты тарифов
bikes = {"Горный": 350, "Городской": 300, "Шоссейный": 450, "Электро": 600, "Детский": 200}
tariffs = {"1 час": 1, "3 часа": 2.5, "Весь день": 4}
statuses = ["Забронирован", "В прокате", "Завершён"]

# Начальный список заказов
orders = [
    [1, "Горный", "3 часа", 1, 875, "В прокате"],
    [2, "Городской", "1 час", 2, 600, "Завершён"],
    [4, "Электро", "Весь день", 2, 4800, "Забронирован"],
    [5, "Шоссейный", "1 час", 1, 450, "Забронирован"],
    [6, "Детский", "3 часа", 1, 500, "Забронирован"],
]
next_id = 7
edit_id = None  # Хранит номер заказа, если мы его редактируем


# --- ФУНКЦИИ ---
def calc_total(*args):
    qty = int(qty_var.get()) if qty_var.get().isdigit() else 0
    total = int(bikes[bike_var.get()] * tariffs[tariff_var.get()] * qty)
    total_lbl.config(text=f"Итого: {total} ₽")
    return total


def update_table(*args):
    tree.delete(*tree.get_children())
    q = search_var.get().lower()
    st = status_var.get()

    for o in orders:
        if (st == "Все" or o == st) and (q in str(o) or q in o.lower()):
            tree.insert("", "end", values=o)


def add_order():
    global next_id
    total = calc_total()
    if total > 0:
        orders.append([next_id, bike_var.get(), tariff_var.get(), int(qty_var.get()), total, "Забронирован"])
        next_id += 1
        clear_form()
        update_table()


def select_row(event):
    global edit_id
    sel = tree.selection()
    if sel:
        vals = tree.item(sel, "values")
        edit_id = int(vals)
        bike_var.set(vals)
        tariff_var.set(vals)
        qty_var.set(vals)
        mode_lbl.config(text=f"Режим: редактирование (№{edit_id})")


def save_order():
    total = calc_total()
    if edit_id and total > 0:
        for o in orders:
            if o == edit_id:
                o[1:5] = [bike_var.get(), tariff_var.get(), int(qty_var.get()), total]
        clear_form()
        update_table()


def next_status():
    sel = tree.selection()
    if sel:
        oid = int(tree.item(sel, "values"))
        for o in orders:
            if o == oid:
                o = statuses[(statuses.index(o) + 1) % 3]
        update_table()


def delete_order():
    sel = tree.selection()
    if sel:
        oid = int(tree.item(sel, "values"))
        orders[:] = [o for o in orders if o != oid]
        clear_form()
        update_table()


def clear_form():
    global edit_id
    edit_id = None
    bike_var.set("Горный")
    tariff_var.set("1 час")
    qty_var.set("1")
    mode_lbl.config(text="Режим: новый заказ")
    tree.selection_remove(tree.selection())
    calc_total()


def reset_filter():
    search_var.set("")
    status_var.set("Все")


# --- ИНТЕРФЕЙС ---
# 1. Форма заказа
f_form = ttk.LabelFrame(root, text="Форма заказа", padding=10)
f_form.pack(fill="x", padx=15, pady=5)

r1 = ttk.Frame(f_form)
r1.pack(fill="x", pady=5)

bike_var = tk.StringVar(value="Горный")
tariff_var = tk.StringVar(value="1 час")
qty_var = tk.StringVar(value="1")

ttk.Label(r1, text="Велосипед:").pack(side="left")
cb1 = ttk.Combobox(r1, textvariable=bike_var, values=list(bikes), state="readonly", width=16)
cb1.pack(side="left", padx=10)

ttk.Label(r1, text="Тариф:").pack(side="left")
cb2 = ttk.Combobox(r1, textvariable=tariff_var, values=list(tariffs), state="readonly", width=15)
cb2.pack(side="left", padx=10)

ttk.Label(r1, text="Количество:").pack(side="left")
ttk.Entry(r1, textvariable=qty_var, width=8).pack(side="left", padx=10)

# Автопересчёт суммы
cb1.bind("<<ComboboxSelected>>", calc_total)
cb2.bind("<<ComboboxSelected>>", calc_total)
qty_var.trace_add("write", calc_total)

r2 = ttk.Frame(f_form)
r2.pack(fill="x", pady=5)
total_lbl = ttk.Label(r2, text="Итого: 350 ₽", font=("Arial", 10, "bold"))
total_lbl.pack(side="left")
mode_lbl = ttk.Label(r2, text="Режим: новый заказ", foreground="gray")
mode_lbl.pack(side="right", padx=150)

r3 = ttk.Frame(f_form)
r3.pack(fill="x", pady=5)
ttk.Button(r3, text="Добавить заказ", command=add_order).pack(side="left", padx=3)
ttk.Button(r3, text="Сохранить изменения", command=save_order).pack(side="left", padx=3)
ttk.Button(r3, text="Следующий статус", command=next_status).pack(side="left", padx=3)
ttk.Button(r3, text="Удалить заказ", command=delete_order).pack(side="left", padx=3)
ttk.Button(r3, text="Очистить форму", command=clear_form).pack(side="left", padx=3)

# 2. Поиск и фильтрация
f_filt = ttk.LabelFrame(root, text="Поиск и фильтрация", padding=10)
f_filt.pack(fill="x", padx=15, pady=5)

search_var = tk.StringVar()
status_var = tk.StringVar(value="Все")

ttk.Label(f_filt, text="Поиск (№ или велосипед):").pack(side="left")
ttk.Entry(f_filt, textvariable=search_var, width=22).pack(side="left", padx=10)

ttk.Label(f_filt, text="Статус:").pack(side="left")
cb_st = ttk.Combobox(f_filt, textvariable=status_var, values=["Все"] + statuses, state="readonly", width=15)
cb_st.pack(side="left", padx=10)

ttk.Button(f_filt, text="Сбросить фильтр", command=reset_filter).pack(side="left", padx=10)

search_var.trace_add("write", update_table)
cb_st.bind("<<ComboboxSelected>>", update_table)

# 3. Список заказов (Таблица)
f_list = ttk.LabelFrame(root, text="Список заказов", padding=10)
f_list.pack(fill="both", expand=True, padx=15, pady=5)

cols = ("№", "Велосипед", "Тариф", "Кол-во", "Сумма (₽)", "Статус")
tree = ttk.Treeview(f_list, columns=cols, show="headings")

for c, w, a in zip(cols, [50, 200, 150, 80, 110, 130], ["center", "w", "center", "center", "e", "center"]):
    tree.heading(c, text=c)
    tree.column(c, width=w, anchor=a)

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", select_row)

update_table()
root.mainloop()
