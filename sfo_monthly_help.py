from solution import Budget

b = Budget()
b.read_file_prms('sfo_monthly_help')
b.create_df()

b.budget
b.save_budget("sfo_monthly_help")
b.filt_budget()
b.save_budget("sfo_monthly_help_filt")
b.save_excel("sfo_monthly_help_df")
b.save_df('sfo_monthly_help_df')