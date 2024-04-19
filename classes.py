import sqlite3
import datetime
from tkinter import *
import tkinter as tk
from tkinter import ttk
#import tkinter.ttk as ttk
import re

class main:
	def __init__(self,title="Учет сотрудников"):
		self.root = Tk()
		self.root.title(title)
		self.root.geometry("300x550")
		# создание соединения с базой данных и извлечение данных при открытии приложения
		self.connection = sqlite3.connect('database.db')
		self.cur = self.connection.cursor()
		self.query = """ CREATE TABLE IF NOT EXISTS employees(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL, date_of_exam) """
		self.cur.execute(self.query)
		self.cur.execute("SELECT * FROM employees")
		self.results =self.cur.fetchall()
		self.connection.commit()
		self.cur.close()
		self.connection.close()

		# root = Tk()
		# root.title("Учет сотрудников")
		# root.geometry("300x550")

		self.empl_name = StringVar()
		self.date_of_exam = StringVar()
		self.errmsg = StringVar()
		self.check = (self.root.register(self.is_valid), "%P")

		self.label = ttk.Label(text="Введите имя:")
		self.label.pack()

		self.entry = ttk.Entry(textvariable=self.empl_name)
		self.entry.pack(pady=15)

		self.label2 = ttk.Label(text="Введите дату проверки:")
		self.label2.pack()

		self.entry2 = ttk.Entry(textvariable=self.date_of_exam, validate="key", validatecommand=self.check)
		self.entry2.pack(pady=15)

		self.error_label = ttk.Label(foreground="red", textvariable=self.errmsg, wraplength=250)
		self.error_label.pack()

		self.display_button = tk.Button(text="Внести", command=self.save_to_db, bg="#0088cc", fg="white", width=10)
		self.display_button.pack(padx=5, pady=5)

		self.clear_button = tk.Button(text="Очистить", command=self.clear_input, bg="#0088cc", fg="white", width=10)
		self.clear_button.pack(padx=5, pady=5)

		# первая таблица со всеми сотрудниками
		self.frame_exam = Frame()
		self.frame_exam.pack(expand=tk.YES, fill=tk.BOTH)
		self.exam_table = ttk.Treeview(self.frame_exam, columns=('id', 'name', 'date'), show="headings", selectmode="browse", style="My.Treeview", height=5)
		self.exam_table.heading("id", text="айди")
		self.exam_table.heading("name", text="Имя")
		self.exam_table.heading("date", text="Дата")
		self.exam_table.column("#1", stretch=NO, width=40)
		self.exam_table.column("#2", stretch=NO, width=100)
		self.exam_table.column("#3", stretch=NO, width=100)
		self.exam_table.tag_configure('deadline', background='green')
		self.exam_table.tag_configure('allok', background='white')
		self.scroll2 = Scrollbar(self.frame_exam, orient=VERTICAL, command=self.exam_table.yview)
		self.exam_table.configure(yscrollcommand=self.scroll2.set)
		self.scroll2.pack(side=RIGHT, fill=Y)
		self.exam_table.pack()

		# вторая таблица с сотрудниками с истекающими сроками
		self.label_title = ttk.Label(text="Проверка через 60 дней или меньше:", font=("Arial", 12))
		self.label_title.pack(pady=15)
		self.frame = Frame()
		self.frame.pack(expand=tk.YES, fill=tk.BOTH)
		self.exam = ttk.Treeview(self.frame, columns=('id', 'name', 'date'), show="headings", selectmode="browse", height=5)
		self.exam.heading("id", text="айди")
		self.exam.heading("name", text="Имя")
		self.exam.heading("date", text="Дата")
		self.exam.column("#1", stretch=NO, width=40)
		self.exam.column("#2", stretch=NO, width=100)
		self.exam.column("#3", stretch=NO, width=100)
		self.exam.tag_configure('red', background='red')
		self.scroll3 = Scrollbar(self.frame, orient=VERTICAL, command=self.exam.yview)
		self.exam.configure(yscrollcommand=self.scroll3.set)
		self.scroll3.pack(side=RIGHT, fill=Y)
		self.exam.pack()
		# наполнение таблиц данными  и окрашивание по условиям
		for row in self.results:
			d1 = datetime.datetime.today() + datetime.timedelta(days=60)
			if d1 > datetime.datetime.strptime(row[2], '%Y-%m-%d'):
				self.exam_table.insert("", END, values=row, tags=('deadline',))
				self.exam.insert("", END, values=row, tags=('red',))
			else:
				self.exam_table.insert("", END, values=row, tags=('allok',))