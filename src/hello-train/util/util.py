import datetime

def get_current_time() -> str:
    current_datetime = datetime.datetime.today()
    return current_datetime.strftime("%Y/%m/%d %-I:%M:%S %p")

"""
Returns the next valid index sequentially in a list
"""
def get_next_i_in_list(current_i: int, ls: list):
    if current_i + 1 >= len(ls):
        current_i = 0
    else:
        current_i += 1
    return current_i
