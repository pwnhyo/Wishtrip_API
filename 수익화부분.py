
import itertools
import numpy as np

# min_val ~ max_val 범위를 step으로 쪼개어 return 한다.
def get_numbers_between_inclusive(min_val, max_val, step):
    result = []
    
    cur = min_val
    while(cur <= max_val):
        result.append(cur)
        cur += step
      
    return result

# 주어진 두 점을 기준으로 직사각형 범위를 생성한다.
def get_rectangle_range(point1, point2):
    base_x = 0
    base_y = 0
    end_x = 0
    end_y = 0

    if point1[0] > point2[0]:
        base_x = point2[0]
        end_x = point1[0]
    else:
        base_x = point1[0]
        end_x = point2[0]
    
    if point1[1] > point2[1]:
        base_y = point2[1]
        end_y = point1[1]
    else:
        base_y = point1[1]
        end_y = point2[1]

    return ((base_x, end_x), (base_y, end_y))

# 특정 좌표에 대하여 가장 근접한 key를 판단한다.
def find_close_key_coordinates(key_table, coordinates):
    
    key_x_table = []
    key_y_table = []
    for key in key_table:
        key_x_table.append(key[0])
        key_y_table.append(key[1])
    
    array1 = np.asarray(key_x_table)
    idx1 = (np.abs(array1 - coordinates[0])).argmin()

    array2 = np.asarray(key_y_table)
    idx2 = (np.abs(array2 - coordinates[1])).argmin()

    return array1[idx1], array2[idx2]

if __name__ == "__main__":
    rectangle = get_rectangle_range((131.87222222,38.45000000), (125.06666667,33.10000000)) # south korea
    print(rectangle)

    x_list = get_numbers_between_inclusive(rectangle[0][0], rectangle[0][1], 0.005)
    y_list = get_numbers_between_inclusive(rectangle[1][0], rectangle[1][1], 0.005)
    print(len(x_list))
    print(len(y_list))

    #result = list(itertools.product(x_list, y_list))
    #print(len(result))
    #print(result[0:10])

    #key = find_close_key_coordinates(key_table=result, coordinates=(127.02939748443758, 37.58604068332279))
   # print(key)

    