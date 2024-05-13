from solution import Budget
import pandas as pd

b = pd.read_pickle('b_df_test.pkl')
b2 = pd.read_pickle('b1_df_test.pkl')

new = Budget()
new.df = pd.concat([b, b2])

new.budget
new.save_budget("new_test")
new.filt_budget()
new.save_budget("new_test_filt")
new.save_excel("new_df_test")