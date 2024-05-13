import requests
import json
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import time

class Budget:

    __endpoint = 'http://budget.gov.ru/epbs/registry/7710568760-repexecutincome/data'
    __dflt_columns = ['period','blockOktmo.oktmoname', 'blockOktmo.regioncode', 
                 'blockKd.code', 'blockKd.name', 'blockStrcode.code', 
                 'blockStrcode.name', 'perkb']

    def __init__(self):
        self.__periodicity = None
        self.__periods = set()
        self.__reg_codes = []
        self.__kd_codes = []
        self.__oktmonames = []
        self.__blocks_info = None
        self.__code_okud = None
        self.__query_params = {"filterperiod": None, 
                                "filterperiodicity": self.__periodicity,
                                "filteroktmo.regioncode": self.__reg_codes,
                                "filteroktmo.oktmoname": self.__oktmonames,
                                "pageSize": "1000",
                                "filterblocks.info": self.__blocks_info,
                                "FORMCODEOKUD": self.__code_okud,
                                "filterkd.code": self.__kd_codes}
        self.__data = []
        self.__df = None
        self.__columns = Budget.__dflt_columns
        self.__budget = None
        self.__filt = None
    @property
    def columns(self) -> list:
        return self.__columns
    
    @columns.setter
    def columns(self, columns:list):
        #if not all(i in df.columns? for i in columns): raise Exception('Wrong columns names')
        self.__columns = columns

    @property
    def kd_codes(self) -> list:
        return self.__kd_codes

    @kd_codes.setter
    def kd_codes(self, codes:list):
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
    
    def set_periods(self, start_date:str, end_date:str):
        try:
            start_date = datetime.datetime.strptime(start_date, '%d.%m.%Y')
            end_date = datetime.datetime.strptime(end_date, '%d.%m.%Y')
        except:
            raise Exception('Date should be in format dd.mm.yyyy')
        
        if start_date > end_date:
            print(start_date, end_date)
            raise Exception('Start date should be less than end date')
        
        if start_date.year not in range(2018, 2025) or end_date.year not in range(2018, 2025):
            raise Exception('Year should be in range 2018-2024')
        
        if start_date.month not in range(1, 13) or end_date.month not in range(1, 13):
            raise Exception('Month should be in range 1-12')
        
        if start_date.day != 1 or end_date.day != 1:
            raise Exception('Day should be 1')

        if self.__periodicity == 'M':
            m, y = 1, 0
        elif self.__periodicity == 'Y':
            m, y = 0, 1
        else:
            raise Exception('Periodicity', self.__periodicity, 'is not supported')
        
        date = start_date
        periods_temp = set()
        while str(end_date.strftime('%d%m%Y')) not in periods_temp:
            periods_temp.add(str(date.strftime('%d%m%Y')))
            date += relativedelta(months=m, years=y)

        self.__periods.clear()
        self.__periods = sorted(periods_temp)

    @property
    def reg_codes(self) -> set:
        return self.__reg_codes

    @reg_codes.setter
    def reg_codes(self, codes:list):
        if not (i in range(1, 91) for i in codes):
            raise Exception('Region code should be in range 1-90')
        self.__reg_codes.clear()
        self.__reg_codes = sorted([f'{int(i):02d}' for i in codes])

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
    
    def set_oktmonames(self, names:list):
        self.__oktmonames.clear()
        self.__oktmonames = sorted(names)

    def update_query_params(self):
        if self.__oktmonames == [] and self.__reg_codes == []:
            print('No region codes or oktmo names specified')
        elif self.__reg_codes != []:
            self.__query_params["filteroktmo.regioncode"] = self.__reg_codes
            if "filteroktmo.oktmoname" in self.__query_params:
                self.__query_params.pop("filteroktmo.oktmoname")
        elif self.__oktmonames != []:
            self.__query_params["filteroktmo.oktmoname"] = self.__oktmonames
            if "filteroktmo.regioncode" in self.__query_params:
                self.__query_params.pop("filteroktmo.regioncode")

        if self.__periods == set():
            print('No periods specified')

        if self.__kd_codes == []:
            print('No kd codes specified')
        else:
            self.__query_params["filterkd.code"] = self.__kd_codes

        if self.__blocks_info == None:
            print('No blocks info specified')
        else:
            self.__query_params["filterblocks.info"] = self.__blocks_info

        if self.__code_okud == None:
            print('No code okud specified')
        else:
            self.__query_params["FORMCODEOKUD"] = self.__code_okud

        if self.__periodicity == None:
            print('No periodicity specified')
        else:
            self.__query_params["filterperiodicity"] = self.__periodicity

        #print(self.__query_params)
    
    def read_file_prms(self, file:str):
        params = {}
        with open(f'{file}.txt', 'r', encoding='utf-8') as f:
            for line in f:
                name, value = line.strip().split(':')
                if name == 'filterperiod':
                    periods = list(i.strip() for i in value.strip().split(','))
                if len(list(value.strip().split(','))) > 1:
                    value = list(i.strip() for i in value.strip().split(','))
                else:
                    value = value.strip()

                if name != 'filterperiod':
                    params[name] = value
        if params.get('filteroktmo.oktmoname') is not None:
            self.set_oktmonames(params['filteroktmo.oktmoname'])
        if params.get('filteroktmo.regioncode') is not None:
            self.reg_codes = params['filteroktmo.regioncode']
        self.blocks_info = params['filterblocks.info']
        self.code_okud = params['FORMCODEOKUD']
        self.kd_codes = params['filterkd.code']
        self.periodicity = params['filterperiodicity']
        self.set_periods(periods[0], periods[1])
        self.update_query_params()

    def get_data(self):
        self.update_query_params()
        for period in self.__periods:
            self.__query_params["filterperiod"] = period
            print(self.__query_params["filterperiod"], "Start")
            resp = requests.get(Budget.__endpoint, params=self.__query_params)
            if resp.status_code == 200:
                self.__data.append(resp.json())
            else:
                print(resp.status_code)
            print(self.__query_params["filterperiod"], "Done")

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
    def budget(self, columns:list=None) -> pd.DataFrame:
        if columns is None:
            columns = self.__columns
        if self.__budget is None:
            self.__budget = self.__df[columns]
        return self.__budget
    
    def filt_budget(self, columns:list=None, filt=None) -> pd.DataFrame:
        if columns is None:
            columns = self.__columns
        if self.__budget is None:
            self.__budget = self.__df[columns]
        if filt is None:
            self.__filt = ((self.__df['blockKd.name'] == 
                            'Доходы бюджета - всего, в том числе:') | 
                            (self.__df['blockStrcode.name'] == 
                             'Доходы бюджета - всего, в том числе:'))
            filt = self.__filt
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