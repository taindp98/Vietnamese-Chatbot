import pandas as pd
import uuid
question = pd.read_csv('./question_livestream_label.csv')
list_id = []
for i in range(len(question)):
    list_id.append(str(uuid.uuid4())[:8])
question['_id'] = list_id
# print(question.head())
question.to_csv('./question_id.csv',header=True,index=False)
