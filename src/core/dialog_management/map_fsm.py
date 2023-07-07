map_order_entity = {}
map_order_entity['major_name'] = ['point','subject_group']
map_order_entity['major_code']=['major_name','type_edu']
map_order_entity['point']=['major_name','subject_group','year','type_edu','case']
map_order_entity['subject_group']=['major_name']
map_order_entity['subject']=['major_name','subject_group']
map_order_entity['tuition']=['type_edu']
map_order_entity['year'] = ['major_name','subject_group','point']
map_order_entity['object'] = ['case','type_edu','major_name']
map_order_entity['register'] = ['case','type_edu','major_name']
map_order_entity['criteria'] = ['major_name','case','type_edu']
# intent deep learning
# label = ['other','type_edu','case','career']
map_order_entity['type_edu']=['major_name','subject_group','case']
map_order_entity['case']=['major_name','type_edu']
map_order_entity['career']=['major_name']

map_order_entity['all_slot'] = ['major_name','type_edu','subject_group','year','case','point','career','subject','tuition','major_code','criteria','object','register']
