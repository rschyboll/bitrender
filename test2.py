import re

t = '"productId":"111111"'
m = re.match("\W*productId[^:]*:\D*(\d+)", t)
if m:
    print(m.group(1))
