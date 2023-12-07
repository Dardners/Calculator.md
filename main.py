# -*- coding: utf-8 -*-

# @autor: Михаил Голосов
# @github: github.com/Dardners

# Модули
import tkinter as tk

from app.Calculator import Calculator

if __name__ == '__main__':
    master = tk.Tk()
    main = Calculator(master)
    main.start()
