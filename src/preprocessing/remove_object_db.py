import re
file_in = open('/home/taindp/PycharmProjects/thesis/data/db_hcmut_full.json','r')
file_out = open('/home/taindp/PycharmProjects/thesis/data/db_hcmut_full123.json','w')
data_raw = file_in.read()
data_repl_space = data_raw.replace('\n',r'').replace(r'             ',r'').replace(r'        ',r'').replace(r'    ',r'')
re_token1=r'ObjectId\('
re_token2=r')'
data_repl_obj1 = re.sub(re_token1,r'',data_repl_space).replace(r')',r'')
# data_repl_obj2 = re.sub(re_token2,r'',data_repl_obj1)
# str_data_out = str(data_repl_obj1).replace(r"'",r'"')
# file_out.write(str_data_out)
print(data_repl_obj1)

