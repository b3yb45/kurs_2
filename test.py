from solution import Budget

b = Budget()
b.kd_codes = ("00000000000000000", "10000000000000000", "20000000000000000")
b.periodicity = "Y"
b.set_periods(2018, 1, 2024, 1)
b.blocks_info = "PERKB"
b.code_okud = "0503317"
b.set_oktmonames({'Республика Алтай', 'Республика Тыва', 'Республика Хакасия', 'Алтайский край', 'Красноярский край', 'Иркутская область', 'Кемеровская область - Кузбасс', 'Новосибирская область', 'Омская область', 'Томская область', 'Республика Бурятия'})
print(b)
b.update_query_params()
b.create_df()
df = b.df
'''
b.budget
b.save_budget("test")
b.filt_budget()
b.save_budget("test_filt")
b.save_excel("test2")
'''

print(df[['period','blockOktmo.oktmoname']])