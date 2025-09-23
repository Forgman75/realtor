import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from decimal import Decimal

class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Риэлторское агентство")
        
        # Создание базы данных
        self.create_database()
        
        # Создание элементов интерфейса
        self.create_widgets()
        
        # Обновление таблицы при запуске
        self.update_table()
        
    def create_database(self):
        conn = sqlite3.connect('realtor.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS deals
                    (deal_id INTEGER PRIMARY KEY,
                     price REAL,
                     commission_percent REAL)''')
        conn.commit()
        conn.close()
        
    def create_widgets(self):
        # Форма ввода
        input_frame = ttk.LabelFrame(self.root, text="Ввод данных", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        ttk.Label(input_frame, text="№ сделки:").grid(row=0, column=0, sticky="w")
        self.deal_id_entry = ttk.Entry(input_frame)
        self.deal_id_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Стоимость квартиры:").grid(row=1, column=0, sticky="w")
        self.price_entry = ttk.Entry(input_frame)
        self.price_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(input_frame, text="Процент комиссии:").grid(row=2, column=0, sticky="w")
        self.commission_entry = ttk.Entry(input_frame)
        self.commission_entry.grid(row=2, column=1, padx=5)
        
        ttk.Button(input_frame, text="Добавить", command=self.add_deal).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Таблица сделок
        table_frame = ttk.LabelFrame(self.root, text="Сделки", padding=10)
        table_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        columns = ("№ сделки", "Стоимость квартиры", "Процент комиссии", "Сумма комиссии")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
            
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Полосы прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
    def add_deal(self):
        try:
            deal_id = int(self.deal_id_entry.get())
            price = Decimal(self.price_entry.get())
            commission_percent = Decimal(self.commission_entry.get())
            
            conn = sqlite3.connect('realtor.db')
            c = conn.cursor()
            c.execute("INSERT INTO deals (deal_id, price, commission_percent) VALUES (?, ?, ?)",
                     (deal_id, float(price), float(commission_percent)))
            conn.commit()
            conn.close()
            
            self.clear_entries()
            self.update_table()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения")
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Сделка с таким номером уже существует")
            
    def clear_entries(self):
        self.deal_id_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.commission_entry.delete(0, tk.END)
        
    def update_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Получение данных из БД
        conn = sqlite3.connect('realtor.db')
        c = conn.cursor()
        c.execute("SELECT * FROM deals")
        deals = c.fetchall()
        conn.close()
        
        # Заполнение таблицы
        for deal in deals:
            deal_id, price, commission_percent = deal


            commission = price * commission_percent / 100
            self.tree.insert("", tk.END, values=(deal_id, price, commission_percent, commission))

if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()