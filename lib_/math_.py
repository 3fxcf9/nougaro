#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Nougaro : a python-interpreted high-level programming language
# Copyright (C) 2021-2024  Jean Dubois (https://github.com/jd-develop) <jd-dev@laposte.net>
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

""" Math module

    Math is a module that contains math stuff, such as functions and constants, that are very useful to do math
    things.
"""

# IMPORTS
# nougaro modules imports
from lib_.lib_to_make_libs import *
# Above line : Context, RTResult, errors and values are imported in lib_to_make_libs.py
# built-in python imports
import math

# constants
PI = Number(math.pi)
SQRT_PI = Number(math.sqrt(math.pi))
E = Number(math.e)


class Math(ModuleFunction):
    """ Math module """
    functions: dict[str, BuiltinFunctionDict] = {}

    def __init__(self, name: str):
        super().__init__("math", name, functions=self.functions)

    def copy(self):
        """Return a copy of self"""
        copy = Math(self.name)
        return self.set_context_and_pos_to_a_copy(copy)

    # =========
    # FUNCTIONS
    # =========
    def execute_math_sqrt(self, exec_context: Context):
        """Calculates square root of 'value'
        It returns the same as math.root(value, 2)"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.sqrt", "number", value,
                exec_context, "lib_.math_.Math.execute_math_sqrt"
            ))

        if value.value < 0:  # we check if the value is greater than (or equal to) 0
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTArithmeticError(
                value.pos_start, value.pos_end,
                "first argument of the built-in function 'math.sqrt' must be greater than (or equal to) 0.",
                exec_context, "lib_.math_.Math.execute_math_sqrt"
            ))

        sqrt_ = math.sqrt(value.value)  # we calculate the square root
        return RTResult().success(Number(sqrt_))

    functions["sqrt"] = {
        "function": execute_math_sqrt,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_isqrt(self, exec_context: Context):
        """Calculates the integer part of the square root of 'value'
        It returns the same as math.iroot(value, 2)"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not (isinstance(value, Number) and isinstance(value.value, int)):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.isqrt", "int", value,
                exec_context, "lib_.math_.Math.execute_math_isqrt"
            ))

        if value.value < 0:  # we check if the value is greater than (or equal to) 0
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTArithmeticError(
                value.pos_start, value.pos_end,
                "first argument of the built-in function 'math.isqrt' must be greater than (or equal to) 0.",
                exec_context, "lib_.math_.Math.execute_math_isqrt"
            ))

        sqrt_ = math.isqrt(value.value)  # we calculate the square root
        return RTResult().success(Number(sqrt_))

    functions["isqrt"] = {
        "function": execute_math_isqrt,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_root(self, exec_context: Context):
        """Calculates the n-root of 'value' (ⁿ√value)
        Default value for 'n' is 2 (sqrt)."""
        # Params:
        # * value
        # Optional params:
        # * n
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.root", "number", value,
                exec_context, "lib_.math_.Math.execute_math_root"
            ))

        if value.value < 0:  # we check if the value is greater than (or equal to) 0
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTArithmeticError(
                value.pos_start, value.pos_end,
                "first argument of the built-in function ‘math.root’ must be greater than (or equal to) 0.",
                exec_context, "lib_.math_.Math.execute_math_root"
            ))

        n = exec_context.symbol_table.getf('n')  # we get 'n'
        if n is None:  # if 'n' parameter is not filled, we set it to 2
            n = Number(2).set_pos(value.pos_end, self.pos_end)

        if not isinstance(n, Number):  # we check if 'n' is a number
            assert n.pos_start is not None
            assert n.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                n.pos_start, n.pos_end, "second", "math.root", "number", n,
                exec_context, "lib_.math_.Math.execute_math_root"
            ))

        value_to_return = Number(value.value ** (1 / n.value))  # we calculate the root

        return RTResult().success(value_to_return)

    functions["root"] = {
        "function": execute_math_root,
        "param_names": ["value"],
        "optional_params": ["n"],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_iroot(self, exec_context: Context):
        """Calculates the integer part of the n-root of 'value' (ⁿ√value)
        Default value for 'n' is 2 (isqrt)."""
        # Params:
        # * value
        # Optional params:
        # * n
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.iroot", "number", value,
                exec_context, "lib_.math_.Math.execute_math_root"
            ))

        if value.value < 0:  # we check if the value is greater than (or equal to) 0
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTArithmeticError(
                value.pos_start, value.pos_end,
                "first argument of the built-in function ‘math.iroot’ must be greater than (or equal to) 0.",
                exec_context, "lib_.math_.Math.execute_math_root"
            ))

        n = exec_context.symbol_table.getf('n')  # we get 'n'
        if n is None:  # if 'n' parameter is not filled, we set it to 2
            n = Number(2).set_pos(value.pos_end, self.pos_end)

        if not isinstance(n, Number):  # we check if 'n' is a number
            assert n.pos_start is not None
            assert n.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                n.pos_start, n.pos_end, "second", "math.iroot", "number", n,
                exec_context, "lib_.math_.Math.execute_math_root"
            ))

        value_to_return = Number(int(value.value ** (1 / n.value)))  # we calculate the root

        return RTResult().success(value_to_return)

    functions["iroot"] = {
        "function": execute_math_iroot,
        "param_names": ["value"],
        "optional_params": ["n"],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_degrees(self, exec_context: Context):
        """Converts 'value' (radians) to degrees"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.degrees", "number", value,
                exec_context, "lib_.math_.Math.execute_math_degrees"
            ))
        degrees = math.degrees(value.value)
        return RTResult().success(Number(degrees))

    functions["degrees"] = {
        "function": execute_math_degrees,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_radians(self, exec_context: Context):
        """Converts 'value' (degrees) to radians"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.radians", "number", value,
                exec_context, "lib_.math_.Math.execute_math_radians"
            ))
        radians = math.radians(value.value)
        return RTResult().success(Number(radians))

    functions["radians"] = {
        "function": execute_math_radians,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_sin(self, exec_context: Context):
        """Calculates sin('value')"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.sin", "number", value,
                exec_context, "lib_.math_.Math.execute_math_sin"
            ))
        sin = math.sin(value.value)
        return RTResult().success(Number(sin))

    functions["sin"] = {
        "function": execute_math_sin,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_cos(self, exec_context: Context):
        """Calculates cos('value')"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.cos", "number", value,
                exec_context, "lib_.math_.Math.execute_math_cos"
            ))
        cos = math.cos(value.value)
        return RTResult().success(Number(cos))

    functions["cos"] = {
        "function": execute_math_cos,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_tan(self, exec_context: Context):
        """Calculates tan('value')"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.tan", "number", value,
                exec_context, "lib_.math_.Math.execute_math_tan"
            ))
        tan = math.tan(value.value)
        return RTResult().success(Number(tan))

    functions["tan"] = {
        "function": execute_math_tan,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_asin(self, exec_context: Context):
        """Calculates asin('value')"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.asin", "number", value,
                exec_context, "lib_.math_.Math.execute_math_asin"
            ))
        try:
            asin = math.asin(value.value)
        except ValueError:
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTArithmeticError(
                value.pos_start, value.pos_end,
                "first argument of the built-in function ‘math.asin’ must be a number between -1 and 1.",
                exec_context, "lib_.math_.Math.execute_math_asin"
            ))
        return RTResult().success(Number(asin))

    functions["asin"] = {
        "function": execute_math_asin,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_acos(self, exec_context: Context):
        """Calculates acos('value')"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.acos", "number", value,
                exec_context, "lib_.math_.Math.execute_math_acos"
            ))
        try:
            acos = math.acos(value.value)
        except ValueError:  # 1 < value or value < -1
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTArithmeticError(
                value.pos_start, value.pos_end,
                "first argument of the built-in function ‘math.acos’ must be a number between -1 and 1.",
                exec_context, "lib_.math_.Math.execute_math_acos"
            ))
        return RTResult().success(Number(acos))

    functions["acos"] = {
        "function": execute_math_acos,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_atan(self, exec_context: Context):
        """Calculates atan('value')"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.atan", "number", value,
                exec_context, "lib_.math_.Math.execute_math_atan"
            ))
        atan = math.atan(value.value)
        return RTResult().success(Number(atan))

    functions["atan"] = {
        "function": execute_math_atan,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_abs(self, exec_context: Context):
        """Exactly like python `abs()` (absolute value)"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.abs", "number", value,
                exec_context, "lib_.math_.Math.execute_math_abs"
            ))

        value_to_return, error = value.abs_()
        if error is not None:
            return RTResult().failure(error)

        return RTResult().success(value_to_return)

    functions["abs"] = {
        "function": execute_math_abs,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_log(self, exec_context: Context):
        """Exactly like python 'log()'. Default base is 'e' (math_e)."""
        # Params:
        # * value
        # Optional params:
        # * base
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.log", "number", value,
                exec_context, "lib_.math_.Math.execute_math_log"
            ))

        base = exec_context.symbol_table.getf('base')  # we get the base
        if base is None:
            value_to_return = Number(math.log(value.value))
        else:
            if not isinstance(base, Number):  # we check if the base is a number
                assert base.pos_start is not None
                assert base.pos_end is not None
                return RTResult().failure(RTTypeErrorF(
                    base.pos_start, base.pos_end, "second", "math.log", "number", base,
                    exec_context, "lib_.math_.Math.execute_math_log"
                ))
            try:
                value_to_return = Number(math.log(value.value, base.value))
            except ValueError as e:
                assert self.pos_start is not None
                assert self.pos_end is not None
                return RTResult().failure(RunTimeError(
                    self.pos_start, self.pos_end,
                    f"Python ValueError: {e}",
                    exec_context,
                    origin_file="lib_.math_.Math.execute_math_log"
                ))

        return RTResult().success(value_to_return)

    functions["log"] = {
        "function": execute_math_log,
        "param_names": ["value"],
        "optional_params": ["base"],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }

    def execute_math_log2(self, exec_context: Context):
        """Exactly like python 'log2()', is log(n, 2)"""
        # Params:
        # * value
        assert exec_context.symbol_table is not None
        value = exec_context.symbol_table.getf('value')  # we get the value
        if not isinstance(value, Number):  # we check if the value is a number
            assert value is not None
            assert value.pos_start is not None
            assert value.pos_end is not None
            return RTResult().failure(RTTypeErrorF(
                value.pos_start, value.pos_end, "first", "math.log2", "number", value,
                exec_context, "lib_.math_.Math.execute_math_log2"
            ))

        value_to_return = Number(math.log2(value.value))

        return RTResult().success(value_to_return)

    functions["log2"] = {
        "function": execute_math_log2,
        "param_names": ["value"],
        "optional_params": [],
        "should_respect_args_number": True,
        "run_noug_dir_work_dir": False,
        "noug_dir": False
    }


WHAT_TO_IMPORT = {  # what are the new entries in the symbol table when the module is imported
    # Constants
    "pi": PI,
    "sqrt_pi": SQRT_PI,
    "e": E,

    # Functions
    "sqrt": Math("sqrt"),
    "isqrt": Math("isqrt"),
    "root": Math("root"),
    "iroot": Math("iroot"),
    "radians": Math("radians"),
    "degrees": Math("degrees"),
    "sin": Math("sin"),
    "cos": Math("cos"),
    "tan": Math("tan"),
    "asin": Math("asin"),
    "acos": Math("acos"),
    "atan": Math("atan"),
    "abs": Math("abs"),
    "log": Math("log"),
    "log2": Math("log2"),
}
