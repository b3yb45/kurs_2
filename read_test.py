from solution import Budget
import pandas as pd

b = Budget()
b.read_file_prms('test')

b.create_df()
b.budget
b.save_budget("b_test")
b.filt_budget()
b.save_budget("b_test_filt")
b.save_excel("b_df_test")
b.save_df('b_df_test')

b2 = Budget()
b2.read_file_prms('test1')

b2.create_df()
b2.budget
b2.save_budget("b1_test")
b2.filt_budget()
b2.save_budget("b1_test_filt")
b2.save_excel("b1_df_test")
b2.save_df('b1_df_test')

