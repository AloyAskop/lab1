'''
С клавиатуры вводится два числа K и N. 
Квадратная матрица А(N,N) заполняется случайным образом целыми числами в интервале [-10,10]. 
Для тестирования использовать не случайное заполнение, а целенаправленное, введенное из файла. 
Условно матрица имеет вид:
        1
    2       3
        4
Библиотечными методами (NumPy) пользоваться нельзя.
15.	Формируется матрица F следующим образом: 
Скопировать в нее матрицу А и если минимальный элемент в нечетных столбцах в области 1 меньше, 
чем сумма чисел в нечетных строках в области 3, то поменять симметрично области 3 и 2 местами, 
иначе 2 и 3 поменять местами несимметрично. При этом матрица А не меняется. 
После чего вычисляется выражение: (К*F)*А– K*AT . 
Выводятся по мере формирования А, F и все матричные операции последовательно.
'''
import random as ran
def matrix_create_from_txt():
    size = 0
    matrix = []
    with open("Lab1/input.txt", "r") as f:
        for line in f:
            row = list(map(int, line.split()))
            matrix.append(row)
            size += 1
    return matrix,size

def matrix_create_random(size):
    return [[ran.randint(-10, 10) for i in range(size)] for j in range(size)]

def area_part_counter(matrix, size, area_num, count_elements=False):
    area = []
    sum_ch = 0
    a = 0
    for i in range(size):
        for j in range(size):
            if in_area(i, j, size, area_num):
                area.append(matrix[i][j])
                if count_elements:
                    if area_num == 1 and j % 2 != 0 :
                        a = min(area)
                    if area_num == 3 and i % 2 != 0:
                        sum_ch += 1
    if count_elements:
        return area, a if area_num == 1 else sum_ch
    return area


def in_area(i, j, size, area_num):
    if area_num == 1:
        return i > j and i + j < size - 1
    if area_num == 2: 
        return i < j and i + j < size - 1
    elif area_num == 3:  
        return i < j and i + j > size - 1
    elif area_num == 4:  
        return i > j and i + j > size - 1
    return False

def area_replace(matrix, size, result, part2, part3, part4):
    if result:  
        replace_area(matrix, size, part3, 2)
        replace_area(matrix, size, part2, 3)
    else:  
        part2 = list(reversed(part2))
        part3 = sorted(part3)
        replace_area(matrix, size, part3, 2)
        replace_area(matrix, size, part2, 3)
    return matrix

def replace_area(matrix, size, new_values, area_num):
    idx = 0
    for i in range(size):
        for j in range(size):
            if in_area(i, j, size, area_num):
                matrix[i][j] = new_values[idx]
                idx += 1

def matrix_transpose(matrix, size):
    return [[matrix[j][i] for j in range(size)] for i in range(size)]

def matrix_multiply_by_k(matrix, size, k):
    return [[matrix[i][j] * k for j in range(size)] for i in range(size)]

def matrix_multiply_by_matrix(m1, m2, size):
    return [[m1[i][j] * m2[i][j] for j in range(size)] for i in range(size)]

def matrix_subtract(m1, m2, size):
    return [[m1[i][j] - m2[i][j] for j in range(size)] for i in range(size)]

def matrix_copy(matrix, size):
    return [[matrix[i][j] for j in range(size)] for i in range(size)]

def matrix_print(matrix):
    for row in matrix:
        print(row)
    print()

matrix_check = False
while True:
    try:
        k = int(input("Введите число K: "))
        break
    except:
        print("Ошибка при вводе числа К")
    
while not matrix_check:
    try:
        print("Как создаём матрицу\n1. Из .txt\n2. Рандом")
        choose = int(input("Выбор: "))
        if choose == 1:
            matrixA,size = matrix_create_from_txt()
            matrix_check = True
        elif choose == 2:
            size = int(input("Введите размер матрицы (>= 3): "))
            matrixA = matrix_create_random(size)
            matrix_check = True
        else:
            print("Неверный выбор")
    except:
        print("Ошибка при создании матрицы")

matrixF = matrix_copy(matrixA, size)
print("Ваша матрица(А): ")
matrix_print(matrixF)

print("Создаём матрицу(F)")
p1, minimum = area_part_counter(matrixF,size,1,count_elements=True)
p2 = area_part_counter(matrixF, size, 2)
p3, sum_ch = area_part_counter(matrixF, size, 3,count_elements=True)
p4 = area_part_counter(matrixF, size, 4)

matrixF = area_replace(matrixF, size, minimum < sum_ch, p2, p3, p4)
print("Матрица(F) создана: ")
matrix_print(matrixF)

print("(К*F)")
KF = matrix_multiply_by_k(matrixF,size,k)
matrix_print(KF)
print("(K*F)*A")
KFA = matrix_multiply_by_matrix(KF,matrixA,size)
matrix_print(KFA)
print("(At)")
AT = matrix_transpose(matrixA,size)
matrix_print(AT)
print("K*At")
KAT = matrix_multiply_by_k(AT,size,k)
matrix_print(KAT)
print("(K*F)*A-K*At")
matrix_print(matrix_subtract(KFA,KAT,size))