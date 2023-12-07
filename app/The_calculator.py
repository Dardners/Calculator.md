# -*- coding: utf-8 -*-

# @autor: Михаил Голосов
# @github: github.com/Dardners

class The_calculator(object):
    """Класс отвечает за выполнение всех расчетов на калькуляторе"""

    def calculation(self, calc):
        """Отвечает за получение вычислений, которые должны быть выполнены,
        возвращает результат или сообщение об ошибке в случае неудачи
        """
        return self.__calculation_validation(calc=calc)

    def __calculation_validation(self, calc):
        """Отвечает за проверку возможности выполнения введенных расчетов"""

        try:
            result = eval(calc)

            return self.__format_result(result=result)
        except (NameError, ZeroDivisionError, SyntaxError, ValueError):
            return 'Erro'

    def __format_result(self, result):
        """Форматирует результат в научной нотации,
        если он слишком велик и возвращает отформатированное значение в виде строки"""

        result = str(result)
        if len(result) > 15:
            result = '{:5.5E}'.format(float(result))

        return result
