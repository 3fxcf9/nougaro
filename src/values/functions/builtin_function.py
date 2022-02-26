#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# this file is part of the NOUGARO language, created by Jean Dubois (https://github.com/jd-develop)
# Public Domain

# IMPORTS
# nougaro modules imports
from src.values.functions.base_function import BaseFunction
from src.context import Context
from src.values.basevalues import *
from src.values.specific_values.number import *
from src.misc import CustomBuiltInFuncMethod
# built-in python imports
from os import system as os_system, name as os_name
from math import sqrt as math_sqrt, degrees as math_degrees, radians as math_radians, sin as math_sin, cos as math_cos
from math import tan as math_tan, asin as math_asin, acos as math_acos, atan as math_atan


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
        self.type_ = 'built-in func'

    def __repr__(self):
        return f'<built-in function {self.name}>'

    def execute(self, args, interpreter_):
        result = RTResult()
        exec_context = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method: CustomBuiltInFuncMethod = getattr(self, method_name, self.no_visit_method)

        result.register(self.check_and_populate_args(method.arg_names, args, exec_context,
                                                     optional_args=method.optional_args,
                                                     have_to_respect_args_number=method.have_to_respect_args_number))
        if result.error is not None:
            return result

        try:
            return_value = result.register(method(exec_context))
        except TypeError:
            try:
                return_value = result.register(method())
            except TypeError:  # it only executes when coding
                return_value = result.register(method(exec_context))
        if result.error is not None:
            return result
        return result.success(return_value)

    def no_visit_method(self, exec_context: Context):
        print(exec_context)
        print(f"NOUGARO INTERNAL ERROR : No execute_{self.name} method defined in nougaro.BuildInFunction.\n"
              f"Please report this bug at https://jd-develop.github.io/nougaro/redirect1.html with all informations "
              f"above.")
        raise Exception(f'No execute_{self.name} method defined in nougaro.BuildInFunction.')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    # ==================
    # BUILD IN FUNCTIONS
    # ==================

    def execute_void(self):
        """Return nothing"""
        # No params.
        result = RTResult()
        return result.success(NoneValue(False))

    execute_void.arg_names = []
    execute_void.optional_args = []
    execute_void.have_to_respect_args_number = False

    def execute_print(self, exec_context: Context):
        """Print 'value'"""
        # Params:
        # * value
        try:
            print(exec_context.symbol_table.get('value').to_str())
        except Exception:
            print(str(exec_context.symbol_table.get('value')))
        return RTResult().success(NoneValue(False))

    execute_print.arg_names = ["value"]
    execute_print.optional_args = []
    execute_print.have_to_respect_args_number = True

    def execute_print_ret(self, exec_context: Context):
        """Print 'value' and returns 'value'"""
        # Params:
        # * value
        try:
            print(exec_context.symbol_table.get('value').to_str())
            return RTResult().success(
                String(
                    exec_context.symbol_table.get('value').to_str()
                )
            )
        except Exception:
            print(str(exec_context.symbol_table.get('value')))
            return RTResult().success(
                String(
                    str(exec_context.symbol_table.get('value'))
                )
            )

    execute_print_ret.arg_names = ["value"]
    execute_print_ret.optional_args = []
    execute_print_ret.have_to_respect_args_number = True

    def execute_input(self, exec_context: Context):
        """Basic input (str)"""
        # Optional params:
        # * text_to_display
        text_to_display = exec_context.symbol_table.get('text_to_display')
        if text_to_display is None:
            text = input()
        elif isinstance(text_to_display, String) or isinstance(text_to_display, Number):
            text = input(text_to_display.value)
        else:
            text = input()
        return RTResult().success(String(text))

    execute_input.arg_names = []
    execute_input.optional_args = ['text_to_display']
    execute_input.have_to_respect_args_number = True

    def execute_input_int(self, exec_context: Context):
        """Basic input (int). Repeat while entered value is not an int."""
        # Optional params:
        # * text_to_display
        while True:
            text_to_display = exec_context.symbol_table.get('text_to_display')
            if text_to_display is None:
                text = input()
            elif isinstance(text_to_display, String) or isinstance(text_to_display, Number):
                text = input(text_to_display.value)
            else:
                text = input()

            try:
                number = int(text)
                break
            except ValueError:
                print(f'{text} must be an integer. Try again :')
        return RTResult().success(Number(number))

    execute_input_int.arg_names = []
    execute_input_int.optional_args = ['text_to_display']
    execute_input_int.have_to_respect_args_number = True

    def execute_clear(self):
        """Clear the screen"""
        # No params.
        os_system('cls' if (os_name == "nt" or os_name == "Windows") else 'clear')
        return RTResult().success(NoneValue(False))

    execute_clear.arg_names = []
    execute_clear.optional_args = []
    execute_clear.have_to_respect_args_number = False

    def execute_is_int(self, exec_context: Context):
        """Check if 'value' is an integer"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        is_number = isinstance(value, Number)
        if is_number:
            if value.type_ == 'int':
                is_int = True
            else:
                is_int = False
        else:
            is_int = False
        return RTResult().success(TRUE if is_int else FALSE)

    execute_is_int.arg_names = ['value']
    execute_is_int.optional_args = []
    execute_is_int.have_to_respect_args_number = True

    def execute_is_float(self, exec_context: Context):
        """Check if 'value' is a float"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        is_number = isinstance(value, Number)
        if is_number:
            if value.type_ == 'float':
                is_float = True
            else:
                is_float = False
        else:
            is_float = False
        return RTResult().success(TRUE if is_float else FALSE)

    execute_is_float.arg_names = ['value']
    execute_is_float.optional_args = []
    execute_is_float.have_to_respect_args_number = True

    def execute_is_num(self, exec_context: Context):
        """Check if 'value' is an int or a float"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        is_number = isinstance(value, Number)
        return RTResult().success(TRUE if is_number else FALSE)

    execute_is_num.arg_names = ['value']
    execute_is_num.optional_args = []
    execute_is_num.have_to_respect_args_number = True

    def execute_is_list(self, exec_context: Context):
        """Check if 'value' is a List"""
        # Params:
        # * value
        is_list = isinstance(exec_context.symbol_table.get('value'), List)
        return RTResult().success(TRUE if is_list else FALSE)

    execute_is_list.arg_names = ['value']
    execute_is_list.optional_args = []
    execute_is_list.have_to_respect_args_number = True

    def execute_is_str(self, exec_context: Context):
        """Check if 'value' is a String"""
        # Params:
        # * value
        is_str = isinstance(exec_context.symbol_table.get('value'), String)
        return RTResult().success(TRUE if is_str else FALSE)

    execute_is_str.arg_names = ['value']
    execute_is_str.optional_args = []
    execute_is_str.have_to_respect_args_number = True

    def execute_is_func(self, exec_context: Context):
        """Check if 'value' is a BaseFunction"""
        # Params:
        # * value
        is_func = isinstance(exec_context.symbol_table.get('value'), BaseFunction)
        return RTResult().success(TRUE if is_func else FALSE)

    execute_is_func.arg_names = ['value']
    execute_is_func.optional_args = []
    execute_is_func.have_to_respect_args_number = True

    def execute_is_none(self, exec_context: Context):
        """Check if 'value' is a NoneValue"""
        # Params:
        # * value
        is_none = isinstance(exec_context.symbol_table.get('value'), NoneValue)
        return RTResult().success(TRUE if is_none else FALSE)

    execute_is_none.arg_names = ['value']
    execute_is_none.optional_args = []
    execute_is_none.have_to_respect_args_number = True

    def execute_append(self, exec_context: Context):
        """Append 'value' to 'list'"""
        # Params:
        # * list
        # * value
        list_ = exec_context.symbol_table.get('list')
        value = exec_context.symbol_table.get('value')

        if not isinstance(list_, List):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'append' must be a list.",
                exec_context
            ))

        list_.elements.append(value)
        return RTResult().success(list_)

    execute_append.arg_names = ['list', 'value']
    execute_append.optional_args = []
    execute_append.have_to_respect_args_number = True

    def execute_pop(self, exec_context: Context):
        """Remove element at 'index' from 'list'"""
        # Params:
        # * list
        # * index
        list_ = exec_context.symbol_table.get('list')
        index = exec_context.symbol_table.get('index')

        if not isinstance(list_, List):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'pop' must be a list.",
                exec_context
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "second argument of built-in function 'pop' must be a number.",
                exec_context
            ))

        try:
            list_.elements.pop(index.value)
        except Exception:
            return RTResult().failure(RTIndexError(
                self.pos_start, self.pos_end,
                f'pop index {index.value} out of range.',
                self.context
            ))
        return RTResult().success(list_)

    execute_pop.arg_names = ['list', 'index']
    execute_pop.optional_args = []
    execute_pop.have_to_respect_args_number = True

    def execute_extend(self, exec_context: Context):
        """Extend list 'list1' with the elements of 'list2'"""
        # Params:
        # * list1
        # * list2
        list1 = exec_context.symbol_table.get('list1')
        list2 = exec_context.symbol_table.get('list2')

        if not isinstance(list1, List):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'extend' must be a list.",
                exec_context
            ))

        if not isinstance(list2, List):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "second argument of built-in function 'extend' must be a list.",
                exec_context
            ))

        list1.elements.extend(list2.elements)
        return RTResult().success(list1)

    execute_extend.arg_names = ['list1', 'list2']
    execute_extend.optional_args = []
    execute_extend.have_to_respect_args_number = True

    def execute_get(self, exec_context: Context):
        # Params:
        # * list
        # * index
        list_ = exec_context.symbol_table.get('list')
        index_ = exec_context.symbol_table.get('index')

        if not isinstance(list_, List):
            return RTResult().failure(
                RunTimeError(
                    self.pos_start, self.pos_end,
                    "first argument of built-in function 'get' must be a list.",
                    exec_context
                )
            )

        if not isinstance(index_, Number):
            return RTResult().failure(
                RunTimeError(
                    self.pos_start, self.pos_end,
                    "second argument of built-in function 'get' must be an int.",
                    exec_context
                )
            )
        index_ = index_.value

        try:
            return RTResult().success(list_[index_])
        except Exception:
            return RTResult().failure(RTIndexError(
                self.pos_start, self.pos_end,
                f'index {index_} out of range.',
                exec_context
            ))

    execute_get.arg_names = ['list', 'index']
    execute_get.optional_args = []
    execute_get.have_to_respect_args_number = True

    def execute_max(self, exec_context: Context):
        """Calculates the max value of a list"""
        # Params:
        # * value
        # Optional params:
        # * ignore_not_num (default False)
        list_ = exec_context.symbol_table.get('list')
        if not isinstance(list_, List):
            return RTResult().failure(
                RunTimeError(
                    self.pos_start, self.pos_end,
                    "first argument of builtin function 'max' must be a list.",
                    exec_context
                )
            )
        ignore_not_num = exec_context.symbol_table.get('ignore_not_num')
        if ignore_not_num is None:
            ignore_not_num = FALSE
        if not isinstance(ignore_not_num, Number):
            return RTResult().failure(
                RunTimeError(
                    self.pos_start, self.pos_end,
                    "second argument of builtin function 'max' must be a number.",
                    exec_context
                )
            )
        max_ = None
        for element in list_.elements:
            if isinstance(element, Number):
                max_ = element
                break
            else:
                if ignore_not_num.value == FALSE.value:
                    return RTResult().failure(
                        RunTimeError(
                            self.pos_start, self.pos_end,
                            "first argument of builtin function 'max' must be a list containing only numbers. "
                            "You can execute the function with True as the second argument to avoid this error.",
                            exec_context
                        )
                    )
        if max_ is None:
            return RTResult().success(NoneValue())
        for element in list_.elements:
            if isinstance(element, Number):
                if element.value > max_.value:
                    max_ = element
            else:
                if ignore_not_num.value == FALSE.value:
                    return RTResult().failure(
                        RunTimeError(
                            self.pos_start, self.pos_end,
                            "first argument of builtin function 'max' must be a list containing only numbers. "
                            "You can execute the function with True as the second argument to avoid this error.",
                            exec_context
                        )
                    )
        return RTResult().success(max_)

    execute_max.arg_names = ['list']
    execute_max.optional_args = ['ignore_not_num']
    execute_max.have_to_respect_args_number = True

    def execute_min(self, exec_context: Context):
        """Calculates the min value of a list"""
        # Params:
        # * value
        # Optional params:
        # * ignore_not_num (default False)
        list_ = exec_context.symbol_table.get('list')
        if not isinstance(list_, List):
            return RTResult().failure(
                RunTimeError(
                    self.pos_start, self.pos_end,
                    "first argument of builtin function 'min' must be a list.",
                    exec_context
                )
            )
        ignore_not_num = exec_context.symbol_table.get('ignore_not_num')
        if ignore_not_num is None:
            ignore_not_num = FALSE
        if not isinstance(ignore_not_num, Number):
            return RTResult().failure(
                RunTimeError(
                    self.pos_start, self.pos_end,
                    "second argument of builtin function 'min' must be a number.",
                    exec_context
                )
            )
        min_ = None
        for element in list_.elements:
            if isinstance(element, Number):
                min_ = element
                break
            else:
                if ignore_not_num.value == FALSE.value:
                    return RTResult().failure(
                        RunTimeError(
                            self.pos_start, self.pos_end,
                            "first argument of builtin function 'min' must be a list containing only numbers. "
                            "You can execute the function with True as the second argument to avoid this error.",
                            exec_context
                        )
                    )
        if min_ is None:
            return RTResult().success(NoneValue())
        for element in list_.elements:
            if isinstance(element, Number):
                if element.value < min_.value:
                    min_ = element
            else:
                if ignore_not_num.value == FALSE.value:
                    return RTResult().failure(
                        RunTimeError(
                            self.pos_start, self.pos_end,
                            "first argument of builtin function 'min' must be a list containing only numbers. "
                            "You can execute the function with True as the second argument to avoid this error.",
                            exec_context
                        )
                    )
        return RTResult().success(min_)

    execute_min.arg_names = ['list']
    execute_min.optional_args = ['ignore_not_num']
    execute_min.have_to_respect_args_number = True

    def execute_sqrt(self, exec_context: Context):
        """Calculates square root of 'value'"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        if not isinstance(value, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'sqrt' must be a number.",
                exec_context
            ))

        if not value.value >= 0:
            return RTResult().failure(RTArithmeticError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'sqrt' must be greater than (or equal to) 0.",
                exec_context
            ))

        sqrt_ = math_sqrt(value.value)
        return RTResult().success(Number(sqrt_))

    execute_sqrt.arg_names = ['value']
    execute_sqrt.optional_args = []
    execute_sqrt.have_to_respect_args_number = True

    def execute_math_root(self, exec_context: Context):
        """Calculates ⁿ√value"""
        # Params:
        # * value
        # Optional params:
        # * n
        value = exec_context.symbol_table.get('value')
        if not isinstance(value, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'math_root' must be a number.",
                exec_context
            ))

        if value.value < 0:
            return RTResult().failure(RTArithmeticError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'math_root' must be greater than (or equal to) 0.",
                exec_context
            ))

        n = exec_context.symbol_table.get('n')
        if n is None:
            n = Number(2)

        if not isinstance(n, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "second argument of built-in function 'math_root' must be a number.",
                exec_context
            ))

        value_to_return = Number(value.value ** (1 / n.value))

        return RTResult().success(value_to_return)

    execute_math_root.arg_names = ['value']
    execute_math_root.optional_args = ['n']
    execute_math_root.have_to_respect_args_number = True

    def execute_degrees(self, exec_context: Context):
        """Converts 'value' (radians) to degrees"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        if not isinstance(value, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'degrees' must be a number (angle in radians).",
                exec_context
            ))
        degrees = math_degrees(value.value)
        return RTResult().success(Number(degrees))

    execute_degrees.arg_names = ['value']
    execute_degrees.optional_args = []
    execute_degrees.have_to_respect_args_number = True

    def execute_radians(self, exec_context: Context):
        """Converts 'value' (degrees) to radians"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        if not isinstance(value, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'radians' must be a number (angle in degrees).",
                exec_context
            ))
        radians = math_radians(value.value)
        return RTResult().success(Number(radians))

    execute_radians.arg_names = ['value']
    execute_radians.optional_args = []
    execute_radians.have_to_respect_args_number = True

    def execute_sin(self, exec_context: Context):
        """Calculates sin('value')"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        if not isinstance(value, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'sin' must be a number (angle in radians).",
                exec_context
            ))
        sin = math_sin(value.value)
        return RTResult().success(Number(sin))

    execute_sin.arg_names = ['value']
    execute_sin.optional_args = []
    execute_sin.have_to_respect_args_number = True

    def execute_cos(self, exec_context: Context):
        """Calculates cos('value')"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        if not isinstance(value, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'cos' must be a number (angle in radians).",
                exec_context
            ))
        cos = math_cos(value.value)
        return RTResult().success(Number(cos))

    execute_cos.arg_names = ['value']
    execute_cos.optional_args = []
    execute_cos.have_to_respect_args_number = True

    def execute_tan(self, exec_context: Context):
        """Calculates tan('value')"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        if not isinstance(value, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'tan' must be a number (angle in radians).",
                exec_context
            ))
        tan = math_tan(value.value)
        return RTResult().success(Number(tan))

    execute_tan.arg_names = ['value']
    execute_tan.optional_args = []
    execute_tan.have_to_respect_args_number = True

    def execute_asin(self, exec_context: Context):
        """Calculates asin('value')"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        if not isinstance(value, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'asin' must be a number.",
                exec_context
            ))
        try:
            asin = math_asin(value.value)
        except ValueError:
            return RTResult().failure(RTArithmeticError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'asin' must be a number between -1 and 1.",
                exec_context
            ))
        return RTResult().success(Number(asin))

    execute_asin.arg_names = ['value']
    execute_asin.optional_args = []
    execute_asin.have_to_respect_args_number = True

    def execute_acos(self, exec_context: Context):
        """Calculates acos('value')"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        if not isinstance(value, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'acos' must be a number.",
                exec_context
            ))
        try:
            acos = math_acos(value.value)
        except ValueError:
            return RTResult().failure(RTArithmeticError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'acos' must be a number between -1 and 1.",
                exec_context
            ))
        return RTResult().success(Number(acos))

    execute_acos.arg_names = ['value']
    execute_acos.optional_args = []
    execute_acos.have_to_respect_args_number = True

    def execute_atan(self, exec_context: Context):
        """Calculates atan('value')"""
        # Params:
        # * value
        value = exec_context.symbol_table.get('value')
        if not isinstance(value, Number):
            return RTResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "first argument of built-in function 'atan' must be a number.",
                exec_context
            ))
        atan = math_atan(value.value)
        return RTResult().success(Number(atan))

    execute_atan.arg_names = ['value']
    execute_atan.optional_args = []
    execute_atan.have_to_respect_args_number = True

    def execute_exit(self, exec_context: Context):
        """Stops the Nougaro Interpreter"""
        # Optional params:
        # * code
        code = exec_context.symbol_table.get('code')
        if isinstance(code, Number) or isinstance(code, String):
            exit(code.value)
        exit()

    execute_exit.arg_names = []
    execute_exit.optional_args = ['code']
    execute_exit.have_to_respect_args_number = True

    def execute_type(self, exec_context: Context):
        """Get the type of 'value'"""
        # Params :
        # * value
        value_to_get_type = exec_context.symbol_table.get('value')
        return RTResult().success(String(value_to_get_type.type_))

    execute_type.arg_names = ['value']
    execute_type.optional_args = []
    execute_type.have_to_respect_args_number = True

    def execute_str(self, exec_context: Context):
        """Python 'str()'"""
        # Params :
        # * value
        result = RTResult()
        value = exec_context.symbol_table.get('value')
        str_value, error = value.to_str_()
        if error is not None:
            return error

        return result.success(str_value)

    execute_str.arg_names = ['value']
    execute_str.optional_args = []
    execute_str.have_to_respect_args_number = True

    def execute_int(self, exec_context: Context):
        """Python 'int()'"""
        # Params :
        # * value
        result = RTResult()
        value = exec_context.symbol_table.get('value')
        int_value, error = value.to_int_()
        if error is not None:
            return error

        return result.success(int_value)

    execute_int.arg_names = ['value']
    execute_int.optional_args = []
    execute_int.have_to_respect_args_number = True

    def execute_float(self, exec_context: Context):
        """Python 'float()'"""
        # Params :
        # * value
        result = RTResult()
        value = exec_context.symbol_table.get('value')
        float_value, error = value.to_float_()
        if error is not None:
            return error

        return result.success(float_value)

    execute_float.arg_names = ['value']
    execute_float.optional_args = []
    execute_float.have_to_respect_args_number = True

    def execute_list(self, exec_context: Context):
        """Python 'list()'"""
        # Params :
        # * value
        result = RTResult()
        value = exec_context.symbol_table.get('value')
        list_value, error = value.to_list_()
        if error is not None:
            return error

        return result.success(list_value)

    execute_list.arg_names = ['value']
    execute_list.optional_args = []
    execute_list.have_to_respect_args_number = True

    def execute_rickroll(self):
        """Hum... You haven't seen anything. Close the doc please. Right now."""
        # no params
        import webbrowser
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ", new=2)
        return RTResult().success(String("I think you've been rickrolled..."))

    execute_rickroll.arg_names = []
    execute_rickroll.optional_args = []
    execute_rickroll.have_to_respect_args_number = False

    # ==================