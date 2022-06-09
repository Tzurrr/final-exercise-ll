import datetime
import os
import dot_finder


def verify(first_half_arr: list, second_half_arr: list):
    for i in first_half_arr:
        dot = dot_finder.find(i[0])
        for j in second_half_arr:
            second_file_dot = dot_finder.find(j[0])
            if i[0][:dot] == j[0][:second_file_dot - 1] + "a":
                first_file_creation_time = i[1]
                second_file_creation_time = j[1]
                distance = first_file_creation_time - second_file_creation_time
                minute_time = datetime.timedelta(0, 0, 0, 0, 1, 0, 0)
                if distance <= minute_time:
                    return True
        return False
