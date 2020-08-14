import json
import requests

ans = 'http://172.17.0.4/api/v1/search?key=EDc8Fzkh9CyTr9D7PZ9GQa&elem=q_text&table=Qoption&where=q_id&val=1'
rev = requests.get(ans)
rev = rev.json()

groups_list = []
for k,v in enumerate(rev):
    groups_list.append((k, v[0]))

print(groups_list)
