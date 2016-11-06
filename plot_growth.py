import numpy as np
import random
import rethinkdb as r
import matplotlib.pyplot as plt
import time

plt.axis([0, 50, 0, 50])
plt.ion()

host = "DESKTOP-K4G0PLO"
db_name = 'ArchHacks'
table_name = 'People'
r.connect(host=host).repl()

i = 0
x_len = 100
y_len = 100

while True:
    i += 1
    k = r.db(db_name).table(table_name).filter({'status': False}).count().run()
    print(k)
    x_len = x_len + (0 if (i<x_len/2) else i)
    y_len = y_len + (k if (k) > .8*y_len else 0)
    plt.axis([0, 50 + i*1.3, 0, k + k*.5])
    y = k
    plt.scatter(i, y)
    plt.pause(.05)
