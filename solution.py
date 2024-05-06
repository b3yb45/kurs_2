import requests
import json
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import time

class Budget:
    def __init__(self):
        self.__periodicity = None
        self.__period_list = []
        self.__reg_list = []
        self.__kd_code_list = set()
        self.__query_params = {}
        self.__blocks_info = None
        self.__code_okud = None

    @property
    def kd_code_list(self):
        return self.__kd_code_list

    @kd_code_list.setter
    def kd_code_list(self, *args):
        if not isinstance((i for i in args), str):
            raise Exception('Kd code must be string, example input: "00000000000000000", "10000000000000000", "20000000000000000"')

        self.__kd_code_list.update(set(args))

    @property
    def periodicity(self):
        return self.__periodicity

    @periodicity.setter
    def periodicity(self, value):
        if value != 'M' or value != 'Y':
            raise Exception('Periodicity must be M or Y')
        self.__periodicity = value

    @property
    def period_list(self):
        return self.__period_list

    @property
    def reg_list(self):
        return self.__reg_list
    
    @reg_list.setter
    def reg_list(self, start_year, start_month, end_year, end_month):
        if start_year not in range(2018, 2025) or end_year not in range(2018, 2025):
            raise Exception('Year should be in range 2018-2024')
        if start_month not in range(1, 13) or end_month not in range(1, 13):
            raise Exception('Month should be in range 1-12')
        
        if self.__periodicity == 'M':
            m, y = 1, 0
        elif self.__periodicity == 'Y':
            m, y = 0, 1
        else:
            raise Exception('Periodicity', self.__periodicity, 'is not supported')
        
        date = datetime.date(year=start_year, month=start_month, day=1)
        while str(datetime.date(year=end_year, month=end_month, day=1).strftime('%d%m%Y')) \
            not in self.__period_list:
            self.__period_list.append(str(date.strftime('%d%m%Y')))
            date += relativedelta(months=m, years=y)

    