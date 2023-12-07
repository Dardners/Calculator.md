# -*- coding: utf-8 -*-

# @autor: Михаил Голосов
# @github: github.com/Dardners

# Модули
import sys
import os
import platform

import tkinter as tk
from tkinter import Menu, FALSE

from functools import partial
from json import load as json_load
from json import dump as json_dump

from copy import deepcopy

from .The_calculator import The_calculator


class Calculator(object):
    """Класс для создания макета калькулятора, распределения кнопок и добавления их функциональности.

        Кнопки в макете распределяются следующим образом:

            C | ( | ) | <
            7 | 8 | 9 | x
            4 | 5 | 6 | -
            1 | 2 | 3 | +
            . | 0 | = | /
              |   | ^ | √

            ПРИМЕЧАНИЕ: Необходимо импортировать модуль style из пакета view,
                 и выбрать один из его стилей.
        """

    def __init__(self, master):
        self.master = master
        self.calc = The_calculator()

        self.settings = self._load_settings()

        # Устанавливает стиль по умолчанию для macOS, если используется операционная система
        if platform.system() == 'Darwin':
            self.theme = self._get_theme('Default Theme For MacOS')
        else:
            self.theme = self._get_theme(self.settings['current_theme'])

        # Настройка Top-Level
        self.master.title('Калькулятор')
        self.master.maxsize(width=335, height=415)
        self.master.minsize(width=335, height=415)
        self.master.geometry('-150+100')
        self.master['bg'] = self.theme['master_bg']

        # Область ввода
        self._frame_input = tk.Frame(self.master, bg=self.theme['frame_bg'], pady=4)
        self._frame_input.pack()

        # Область кнопок
        self._frame_buttons = tk.Frame(self.master, bg=self.theme['frame_bg'], padx=2)
        self._frame_buttons.pack()

        # Инициализация функций
        self._create_input(self._frame_input)
        self._create_buttons(self._frame_buttons)
        self._create_menu(self.master)

    @staticmethod
    def _load_settings():
        """Утилита для загрузки файла настроек калькулятора."""
        with open('./app/settings/settings.json', mode='r', encoding='utf-8') as f:
            settings = json_load(f)

        return settings

    def _get_theme(self, name='Dark'):
        """Возвращает конфигурацию стиля для указанной темы."""

        list_of_themes = self.settings['themes']

        found_theme = None
        for t in list_of_themes:
            if name == t['name']:
                found_theme = deepcopy(t)
                break

        return found_theme

    def _create_input(self, master):
        self._entrada = tk.Entry(master, cnf=self.theme['INPUT'])
        self._entrada.insert(0,0)
        self._entrada.pack()

    def _create_menu(self, master):
        self.master.option_add('*tearOff', FALSE)
        calc_menu = Menu(self.master)
        self.master.config(menu=calc_menu)

        # Настройки
        config = Menu(calc_menu)
        theme = Menu(config)
        # Меню темы
        theme_incompatible = ['Default Theme For MacOS']
        for t in self.settings['themes']:

            name = t['name']
            if name in theme_incompatible:  # Ignora os temas não compatíveis.
                continue
            else:
                theme.add_command(label=name, command=partial(self._change_theme_to, name))
        # Настройки
        calc_menu.add_cascade(label='Настройки', menu=config)
        config.add_cascade(label='Тема', menu=theme)

        config.add_separator()
        config.add_command(label='выход', command=self._exit)

    def _change_theme_to(self, name='Dark'):
        self.settings['current_theme'] = name

        with open('./app/settings/settings.json', 'w') as outfile:
            json_dump(self.settings, outfile, indent=4)

        self._realod_app()

    def _create_buttons(self, master):
        """"Метод для создания всех кнопок калькулятора,
        от добавления событий для каждой кнопки до их распределения в сетке макета.
        """

        # Устанавливает глобальные настройки (ширина, высота шрифта и т. д.) в указанной кнопке.
        self.theme['BTN_NUMERICO'].update(self.settings['global'])

        self._BTN_NUM_0 = tk.Button(master, text=0, cnf=self.theme['BTN_NUMERICO'])
        self._BTN_NUM_1 = tk.Button(master, text=1, cnf=self.theme['BTN_NUMERICO'])
        self._BTN_NUM_2 = tk.Button(master, text=2, cnf=self.theme['BTN_NUMERICO'])
        self._BTN_NUM_3 = tk.Button(master, text=3, cnf=self.theme['BTN_NUMERICO'])
        self._BTN_NUM_4 = tk.Button(master, text=4, cnf=self.theme['BTN_NUMERICO'])
        self._BTN_NUM_5 = tk.Button(master, text=5, cnf=self.theme['BTN_NUMERICO'])
        self._BTN_NUM_6 = tk.Button(master, text=6, cnf=self.theme['BTN_NUMERICO'])
        self._BTN_NUM_7 = tk.Button(master, text=7, cnf=self.theme['BTN_NUMERICO'])
        self._BTN_NUM_8 = tk.Button(master, text=8, cnf=self.theme['BTN_NUMERICO'])
        self._BTN_NUM_9 = tk.Button(master, text=9, cnf=self.theme['BTN_NUMERICO'])

        # Устанавливает глобальные настройки (ширина, высота шрифта и т. д.) в указанной кнопке.
        self.theme['BTN_OPERADOR'].update(self.settings['global'])

        # Экземпляры кнопок числовых операторов
        self._BTN_SOMA = tk.Button(master, text='+', cnf=self.theme['BTN_OPERADOR'])
        self._BTN_SUB = tk.Button(master, text='-', cnf=self.theme['BTN_OPERADOR'])
        self._BTN_DIV = tk.Button(master, text='/', cnf=self.theme['BTN_OPERADOR'])
        self._BTN_MULT = tk.Button(master, text='*', cnf=self.theme['BTN_OPERADOR'])
        self._BTN_EXP = tk.Button(master, text='^', cnf=self.theme['BTN_OPERADOR'])
        self._BTN_RAIZ = tk.Button(master, text='√', cnf=self.theme['BTN_OPERADOR'])

        # Устанавливает глобальные настройки (ширина, высота шрифта и т. д.) в указанной кнопке.
        self.theme['BTN_DEFAULT'].update(self.settings['global'])
        self.theme['BTN_CLEAR'].update(self.settings['global'])

        # Экземпляры кнопок функций калькулятора
        self._BTN_ABRE_PARENTESE = tk.Button(master, text='(', cnf=self.theme['BTN_DEFAULT'])
        self._BTN_FECHA_PARENTESE = tk.Button(master, text=')', cnf=self.theme['BTN_DEFAULT'])
        self._BTN_CLEAR = tk.Button(master, text='C', cnf=self.theme['BTN_DEFAULT'])
        self._BTN_DEL = tk.Button(master, text='<', cnf=self.theme['BTN_CLEAR'])
        self._BTN_RESULT = tk.Button(master, text='=', cnf=self.theme['BTN_OPERADOR'])
        self._BTN_DOT = tk.Button(master, text='.', cnf=self.theme['BTN_DEFAULT'])

        # Экземпляры пустых кнопок для будущей реализации
        self._BTN_VAZIO1 = tk.Button(master, text='', cnf=self.theme['BTN_OPERADOR'])
        self._BTN_VAZIO2 = tk.Button(master, text='', cnf=self.theme['BTN_OPERADOR'])

        # Распределение кнопок в сетке
        # Строка 0
        self._BTN_CLEAR.grid(row=0, column=0, padx=1, pady=1)
        self._BTN_ABRE_PARENTESE.grid(row=0, column=1, padx=1, pady=1)
        self._BTN_FECHA_PARENTESE.grid(row=0, column=2, padx=1, pady=1)
        self._BTN_DEL.grid(row=0, column=3, padx=1, pady=1)

        # Строка 1
        self._BTN_NUM_7.grid(row=1, column=0, padx=1, pady=1)
        self._BTN_NUM_8.grid(row=1, column=1, padx=1, pady=1)
        self._BTN_NUM_9.grid(row=1, column=2, padx=1, pady=1)
        self._BTN_MULT.grid(row=1, column=3, padx=1, pady=1)

        # Строка 2
        self._BTN_NUM_4.grid(row=2, column=0, padx=1, pady=1)
        self._BTN_NUM_5.grid(row=2, column=1, padx=1, pady=1)
        self._BTN_NUM_6.grid(row=2, column=2, padx=1, pady=1)
        self._BTN_SUB.grid(row=2, column=3, padx=1, pady=1)

        # Строка 3
        self._BTN_NUM_1.grid(row=3, column=0, padx=1, pady=1)
        self._BTN_NUM_2.grid(row=3, column=1, padx=1, pady=1)
        self._BTN_NUM_3.grid(row=3, column=2, padx=1, pady=1)
        self._BTN_SOMA.grid(row=3, column=3, padx=1, pady=1)

        # Строка 4
        self._BTN_DOT.grid(row=4, column=0, padx=1, pady=1)
        self._BTN_NUM_0.grid(row=4, column=1, padx=1, pady=1)
        self._BTN_RESULT.grid(row=4, column=2, padx=1, pady=1)
        self._BTN_DIV.grid(row=4, column=3, padx=1, pady=1)

        # Строка 5
        self._BTN_VAZIO1.grid(row=5, column=0, padx=1, pady=1)
        self._BTN_VAZIO2.grid(row=5, column=1, padx=1, pady=1)
        self._BTN_EXP.grid(row=5, column=2, padx=1, pady=1)
        self._BTN_RAIZ.grid(row=5, column=3, padx=1, pady=1)

        # События для цифровых кнопок
        self._BTN_NUM_0['command'] = partial(self._set_values_in_input, 0)
        self._BTN_NUM_1['command'] = partial(self._set_values_in_input, 1)
        self._BTN_NUM_2['command'] = partial(self._set_values_in_input, 2)
        self._BTN_NUM_3['command'] = partial(self._set_values_in_input, 3)
        self._BTN_NUM_4['command'] = partial(self._set_values_in_input, 4)
        self._BTN_NUM_5['command'] = partial(self._set_values_in_input, 5)
        self._BTN_NUM_6['command'] = partial(self._set_values_in_input, 6)
        self._BTN_NUM_7['command'] = partial(self._set_values_in_input, 7)
        self._BTN_NUM_8['command'] = partial(self._set_values_in_input, 8)
        self._BTN_NUM_9['command'] = partial(self._set_values_in_input, 9)

        # События для кнопок математических операций
        self._BTN_SOMA['command'] = partial(self._set_operator_in_input, '+')
        self._BTN_SUB['command'] = partial(self._set_operator_in_input, '-')
        self._BTN_MULT['command'] = partial(self._set_operator_in_input, '*')
        self._BTN_DIV['command'] = partial(self._set_operator_in_input, '/')
        self._BTN_EXP['command'] = partial(self._set_operator_in_input, '**')
        self._BTN_RAIZ['command'] = partial(self._set_operator_in_input, '**(1/2)')


        # События для кнопок функций калькулятора
        self._BTN_DOT['command'] = partial(self._set_dot_in_input, '.')
        self._BTN_ABRE_PARENTESE['command'] = self._set_open_parent
        self._BTN_FECHA_PARENTESE['command'] = self._set_close_parent
        self._BTN_DEL['command'] = self._del_last_value_in_input
        self._BTN_CLEAR['command'] = self._clear_input
        self._BTN_RESULT['command'] = self._get_data_in_input

    def _set_values_in_input(self, value):
        """Метод для записи числа, выбранного пользователем, в поле ввода"""
        if self._entrada.get() == 'Erro':
            self._entrada.delete(0, len(self._entrada.get()))

        if self._entrada.get() == '0':
            self._entrada.delete(0)
            self._entrada.insert(0 ,value)
        elif self._lenght_max(self._entrada.get()):
            self._entrada.insert(len(self._entrada.get()) ,value)

    def _set_dot_in_input(self, dot):
        """Метод для установки десятичной точки в числе"""
        if self._entrada.get() == 'Erro':
            return

        if self._entrada.get()[-1] not in '.+-/*' and self._lenght_max(self._entrada.get()):
            self._entrada.insert(len(self._entrada.get()) ,dot)

    def _set_open_parent(self):
        """Метод установки открытия круглых скобок при вводе"""
        if self._entrada.get() == 'Erro':
            return

        if self._entrada.get() == '0':
            self._entrada.delete(0)
            self._entrada.insert(len(self._entrada.get()), '(')
        elif self._entrada.get()[-1] in '+-/*' and self._lenght_max(self._entrada.get()):
            self._entrada.insert(len(self._entrada.get()), '(')

    def _set_close_parent(self):
        """Метод установки закрывающей круглой скобки во входных данных"""
        if self._entrada.get() == 'Erro':
            return

        if self._entrada.get().count('(') <= self._entrada.get().count(')'):
            return
        if self._entrada.get()[-1] not in '+-/*(' and self._lenght_max(self._entrada.get()):
            self._entrada.insert(len(self._entrada.get()), ')')

    def _clear_input(self):
        """Сбрасывает вход калькулятора, полностью очищая его и вводя значение 0"""
        self._entrada.delete(0, len(self._entrada.get()))
        self._entrada.insert(0,0)

    def _del_last_value_in_input(self):
        """Сбрасывает вход калькулятора, полностью очищая его и вводя значение 0"""
        if self._entrada.get() == 'Erro':
            return

        if len(self._entrada.get()) == 1:
            self._entrada.delete(0)
            self._entrada.insert(0,0)
        else:
            self._entrada.delete(len(self._entrada.get()) - 1)

    def _set_operator_in_input(self, operator):
        """Метод, отвечающий за перехват нажатого математического оператора и установку его на вход"""
        if self._entrada.get() == 'Erro':
            return

        if self._entrada.get() == '':
            # print('\33[91mOperação inválida.\33[m')
            return
        # Evita casos de operadores repetidos sequêncialmente, para evitar erros
        if self._entrada.get()[-1] not in '+-*/' and self._lenght_max(self._entrada.get()):
            self._entrada.insert(len(self._entrada.get()) ,operator)

    def _get_data_in_input(self):
        """Он принимает данные со всеми операциями, содержащимися во входных данных для выполнения вычислений"""
        if self._entrada.get() == 'Erro':
            return

        result = self.calc.calculation(self._entrada.get())
        self._set_result_in_input(result=result)

    def _set_result_in_input(self, result=0):
        """Установите результат всей операции на входе"""
        if self._entrada.get() == 'Erro':
            return

        self._entrada.delete(0, len(self._entrada.get()))
        self._entrada.insert(0, result)

    def _lenght_max(self, data_in_input):
        """Чтобы проверить, достиг ли ввод максимального количества символов"""
        if len(str(data_in_input)) >= 15:
            return False
        return True

    def start(self):
        print('\33[Calculator запускается. . .\33[m\n')
        self.master.mainloop()

    def _realod_app(self):
        """Перезапуск приложения."""
        python = sys.executable  # Recupera o path do executável do python
        os.execl(python, python, * sys.argv)

    def _exit(self):
        exit()
