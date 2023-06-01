import re

m = re.match(r'^(0[1-9]|1[0-2]|[0-9])-(0[1-9]|1[0-9]|2[0-9]|3[0-1]|[0-9])$', '2-30')
print(m.group(0))
print(m.group(1))
print(m.group(2))
print(m.groups())
