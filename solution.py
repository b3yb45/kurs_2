import requests
import json
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import time

class Budget:

    __endpoint = 'http://budget.gov.ru/epbs/registry/7710568760-repexecutincome/data'
    def __init__(self):
        self.__periodicity = None
        self.__periods = set()
        self.__reg_codes = set()
        self.__kd_codes = set()
        self.__oktmonames = set()
        self.__blocks_info = None
        self.__code_okud = None
        self.__query_params = {}
        self.__data = []
        self.__df = None
        self.__budget = None

    @property
    def kd_codes(self) -> set:
        return self.__kd_codes

    @kd_codes.setter
    def kd_codes(self, codes:set):
        self.__kd_codes.clear()
        self.__kd_codes = codes

    @property
    def periodicity(self) -> str:
        return self.__periodicity

    @periodicity.setter
    def periodicity(self, value:str):
        if not (value == 'M' or value == 'Y'):
            raise Exception('Periodicity must be M or Y')
        self.__periodicity = value

    @property
    def periods(self) -> set:
        return self.__periods
    
    def set_periods(self, start_year:int, start_month:int, end_year:int, end_month:int):
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
        periods_temp = set()
        while str(datetime.date(year=end_year, month=end_month, day=1).strftime('%d%m%Y')) \
            not in periods_temp:
            periods_temp.add(str(date.strftime('%d%m%Y')))
            date += relativedelta(months=m, years=y)

        self.__periods.clear()
        self.__periods = sorted(periods_temp)

    @property
    def reg_codes(self) -> set:
        return self.__reg_codes

    def set_reg_codes(self, codes:set):
        if not (i in range(1, 91) for i in codes):
            raise Exception('Region code should be in range 1-90')
        self.__reg_codes.clear()
        self.__reg_codes = sorted(set(f'{i:02d}' for i in codes))

    @property
    def blocks_info(self) -> str:
        return self.__blocks_info

    @blocks_info.setter
    def blocks_info(self, value:str):
        self.__blocks_info = value

    @property
    def code_okud(self) -> str:
        return self.__code_okud

    @code_okud.setter
    def code_okud(self, value:str):
        self.__code_okud = value

    @property
    def oktmonames(self) -> set:
        return self.__oktmonames
    
    def set_oktmonames(self, names:set):
        self.__oktmonames.clear()
        self.__oktmonames = sorted(names)

    def update_query_params(self):
        #if self.__oktmonames != set():
        #self.__query_params["filteroktmo.oktmoname"] = self.__oktmonames
        '''
        elif self.__reg_codes != set():
            self.__query_params["filteroktmo.regioncode"] = self.__reg_codes
        else:
            print('No region codes specified')
        '''

        if self.__periods == set():
            print('No periods specified')

        if self.__kd_codes == set():
            print('No kd codes specified')

        if self.__blocks_info == None:
            print('No blocks info specified')

        if self.__code_okud == None:
            print('No code okud specified')

        if self.__periodicity == None:
            print('No periodicity specified')

        self.__query_params = {"filterperiod": None, 
                               "filterperiodicity": self.__periodicity,
                                "pageSize": "1000",
                                "filteroktmo.oktmoname": self.__oktmonames,
                                "filterblocks.info": self.__blocks_info,
                                "FORMCODEOKUD": self.__code_okud,
                                "filterkd.code": self.__kd_codes}
        
        print(self.__query_params)
        
    def get_data(self):
        self.update_query_params()
        for period in self.__periods:
            print("Start")
            self.__query_params["filterperiod"] = period
            print(self.__query_params["filteroktmo.oktmoname"])
            resp = requests.get(Budget.__endpoint, params=self.__query_params)
            if resp.status_code == 200:
                self.__data.append(resp.json())
            else:
                print(resp.status_code)
            print("Done")

    def save_json(self, file:str):
        with open(f'{file}.json', 'w', encoding='utf-8') as f:
            json.dump(self.__data, f, ensure_ascii=False, indent=4)

    @property
    def df(self) -> pd.DataFrame:
        if self.__df is None:
            self.create_df()
        return self.__df

    def create_df(self) -> pd.DataFrame:
        if self.__data == []:
            self.get_data()
        self.__df = pd.json_normalize(self.__data, record_path=['data'])

    def save_df(self, file:str):
        if self.__df is None:
            self.create_df()
        self.__df.to_pickle(f"{file}.pkl")
    
    def save_excel(self, file:str):
        if self.__df is None:
            self.create_df()
        self.__df.to_excel(f"{file}.xlsx", index=False)

    @property
    def budget(self) -> pd.DataFrame:
        if self.__budget is None:
            self.__budget = self.__df[['period','blockOktmo.oktmoname', 'blockOktmo.regioncode', 'blockKd.code', 'blockKd.name', 'blockStrcode.code', 'blockStrcode.name', 'perkb']]
        return self.__budget
    
    def filt_budget(self) -> pd.DataFrame:
        if self.__budget is None:
            self.__budget = self.__df[['period','blockOktmo.oktmoname', 'blockOktmo.regioncode', 'blockKd.code', 'blockKd.name', 'blockStrcode.code', 'blockStrcode.name', 'perkb']]
        filt = ((self.__df['blockKd.name'] == 'Доходы бюджета - всего, в том числе:') | (self.__df['blockStrcode.name'] == 'Доходы бюджета - всего, в том числе:'))
        self.__budget.drop(index=self.__df[filt].index, inplace=True)
        
    def save_budget(self, file:str):
        self.__budget.to_excel(f"{file}.xlsx", index=False)

    def __str__(self):
        return f'Periodicity: {self.__periodicity}\n\
                Periods: {self.__periods}\n\
                Reg codes: {self.__reg_codes}\n\
                Oktmo names: {self.__oktmonames}\n\
                Kd codes: {self.__kd_codes}\n\
                Blocks info: {self.__blocks_info}\n\
                Code okud: {self.__code_okud}'
    
    def __repr__(self):
        return self.__str__()