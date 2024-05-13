from solution import Budget

b = Budget()
b.read_file_prms('test')

b.create_df()
b.budget
b.save_budget("read_test")
b.filt_budget()
b.save_budget("read_test_filt")
b.save_excel("read_test2")
