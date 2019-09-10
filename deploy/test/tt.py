import datetime

now_datetime = datetime.datetime.now()
delta = datetime.timedelta(minutes=1)
print(now_datetime - delta, now_datetime + delta)

now = "{}-{}-{} {}-{}-{}.0".format(
    str(now_datetime.year),
    str(now_datetime.month),
    str(now_datetime.day),
    str(now_datetime.hour),
    str(now_datetime.minute),
    0
)
