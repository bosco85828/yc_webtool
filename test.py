import re 
a="""bosco.com,bosco123
bosco111
bosco222
bosco333,bosco444"""

b=re.findall(r'[a-zA-Z.:0-9]+',a)



print(b)