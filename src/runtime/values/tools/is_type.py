#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Nougaro : a python-interpreted high-level programming language
# Copyright (C) 2021-2024  Jean Dubois (https://github.com/jd-develop) <jd-dev@laposte.net>

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# IMPORTS
# nougaro modules imports
from src.runtime.values.basevalues.value import Value
# built-in python imports
# no imports


def is_type(value: Value, type_: str):
    """Types are 'BaseValue', 'str', 'int', 'float', 'list', 'module', 'constructor', 'object', 'NoneValue',
       'BaseFunction', 'func', 'built-in func'"""
    return value.type_ == type_


def is_noug_num(value: Value):
    return is_type(value, "int") or is_type(value, "float")


is_n_num = is_noug_num  # The function’s original name was is_n_num, so an alias is kept to ensure retro-compatibility
