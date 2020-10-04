#scratch.py
#!/bin/local/env python

import re

value = '222222 $helo abc'
v = value.split()
message_id = v[2]
# message_id = re.sub(r'^\W*\w+^\W*\w+\W*', '', value)

print(message_id)