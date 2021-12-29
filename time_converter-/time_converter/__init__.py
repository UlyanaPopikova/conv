

import datetime as dt
from abc import ABCMeta, abstractmethod

try:
    import pandas as pd
except:
    pd = None

import numpy as np
from six import with_metaclass


class Converter(with_metaclass(ABCMeta)):
    

    @abstractmethod
    def supports(self, unit=None, datatype=None):
       
        pass

    @abstractmethod
    def convert_from_datetime(self, datetime):
       
        pass

    @abstractmethod
    def convert_to_datetime(self, value):
       
        pass


from time_converter.converters.earth import *
from time_converter.converters.msl import *
from time_converter.converters.change4 import *


class Time:
    converters = [clazz() for clazz in Converter.__subclasses__()]  

    def __init__(self, value, unit=None):
        if self._is_list(value):
            if len(value) == 0:
                self.dt = []
            else:
                converter = self._get_converter(unit, type(value[0]))
                self.dt = [converter.convert_to_datetime(val) for val in value]
            self.original_value = value
        else:
            converter = self._get_converter(unit, type(value))
            self.dt = converter.convert_to_datetime(value)

    def to(self, unit):
        converter = self._get_converter(unit)
        if self._is_list(self.dt):
            arr = np.array([converter.convert_from_datetime(d) for d in self.dt])
            if pd is not None and type(self.original_value) == pd.core.series.Series:
                return pd.Series(arr, index=self.original_value.index)
            else:
                return arr
        else:
            return converter.convert_from_datetime(self.dt)

    def _get_converter(self, unit, datatype=None):
        for converter in self.converters:
            if converter.supports(unit, datatype):
                return converter

        raise ValueError('unknown unit {} or unsupported type {}'.format(unit, datatype))

    def _is_list(self, value):
        return type(value) in [np.ndarray, list] or pd is not None and type(value) == pd.core.series.Series
