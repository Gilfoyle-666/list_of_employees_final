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