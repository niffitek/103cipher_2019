#! /usr/bin/env python3

import math
import sys
import re

def usage():
    if len(sys.argv) != 4 and len(sys.argv) != 2:
        sys.exit(84)
    elif sys.argv[1] == '-h':
        print("USAGE")
        print("     ./103cipher message key flag")
        print()
        print("DESCRIPTION")
        print("message a message, made of ASCII characters")
        print("key the encryption key, made of ASCII characters")
        print("flag 0 for the message to be encrypted, 1 to be decrypted")
        sys.exit(0)


def char_to_ascii(string):
    array = []
    for i in range(0, len(string)):
        array.append(ord(string[i]))
    return (array)


def ascii_to_char(array):
    string = ""
    for i in range(0, len(array)):
        if int(array[i]) > 0:
            string += chr(int(array[i]))
    return (string)


def get_empty_matrix(rows, columns):
    ret = []
    for i in range(0, rows):
        ret.append([])
        for j in range(0, columns):
            ret[i].append(0.0)
    return (ret)


def matrix_mult(message, key):
    ret_matrix = get_empty_matrix(len(message), len(key[0]))
    for i in range(len(message)):
            for j in range(len(key[0])):
                total = 0
                for k in range(len(message[0])):
                    total += message[i][k] * key[k][j]
                ret_matrix[i][j] = total
    return (ret_matrix)


def key_to_matrix(array):
    matrix = []
    row = []
    max_len = 1
    add = 3
    while max_len < len(array):
        max_len += add
        add += 2
    max_len = int(math.sqrt(max_len))
    if len(array) == 1:
        row.append(array[0])
        matrix.append(row)
        return (matrix)
    for i in range(0, max_len * max_len):
        if (i >= len(array)):
            row.append(0)
        else:
            row.append(array[i])
        if (i + 1) % max_len == 0 and i > 0:
            matrix.append(row)
            row = []
    return (matrix)


def message_to_matrix(message, key_len):
    matrix = []
    row = []
    max_len = len(message)
    while (max_len % key_len != 0):
        max_len += 1
    if (key_len == 1):
        for i in range(0, len(message)):
            row.append(message[i])
            matrix.append(row)
            row = []
        return (matrix)
    for i in range(0, max_len):
        if i >= len(message):
            row.append(0)
        else:
            row.append(message[i])
        if (i + 1) % key_len == 0 and i > 0:
            matrix.append(row)
            row = []
    return (matrix)


def my_get_int_array(string):
    list = re.findall(r'\d+', string)
    list_ret = []
    for i in range(len(list)):
        list_ret.append(int(list[i]))
    return list_ret

def input():
    usage()
    try:
        message = str(sys.argv[1])
        key = str(sys.argv[2])
        flag = int(sys.argv[3])
        if flag < 0 or flag > 1:
            exit(84)
        if flag == 0:
            key = char_to_ascii(key)
            message = char_to_ascii(message)
            matrix_key = key_to_matrix(key)
            matrix_message = message_to_matrix(message, len(matrix_key))
            encrypted_message = encrypt(matrix_message, matrix_key)
            output(matrix_key, encrypted_message, flag)
        if flag == 1:
            key = char_to_ascii(key)
            matrix_key = key_to_matrix(key)
            matrix_message = my_get_int_array(message)
            matrix_message = message_to_matrix(matrix_message, len(matrix_key))
            matrix_key2 = rev_matrix2(matrix_key)
            decrypted_message = decrypt(matrix_message, matrix_key2)
            output(matrix_key2, decrypted_message, flag)

    except ValueError:
        exit(84)
    return (0)


def encrypt(message, key):
    return matrix_mult(message, key)


def get_identity_matrix(square):
    ret_matrix = get_empty_matrix(square, square)
    for i in range(square):
        ret_matrix[i][i] = 1
    return ret_matrix


def copy_matrix(M):
        rows = len(M)
        cols = len(M[0])

        MC = get_empty_matrix(rows, cols)

        for i in range(rows):
            for j in range(rows):
                MC[i][j] = M[i][j]
        return MC


def round_matrix(matrix):
    n = len(matrix)
    nn = len(matrix[0])
    new_list = []
    new_element = []
    for i in range(n):
        for j in range(nn):
            new_element.append(round(matrix[i][j]))
        new_list.append(new_element)
        new_element = []
    return new_list


def rev_matrix2(AM):
    n = len(AM)
    identity = get_identity_matrix(n)
    indices = list(range(n))
    for fd in range(n):
        fdScaler = 1.0 / AM[fd][fd]
        for j in range(n):
            AM[fd][j] *= fdScaler
            identity[fd][j] *= fdScaler
        for i in indices[0:fd] + indices[fd + 1:]:
            crScaler = AM[i][fd]
            for j in range(n):
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                identity[i][j] = identity[i][j] - crScaler * identity[fd][j]
    return identity


def decrypt(message, key):
    string2 = matrix_mult(message, key)
    string2 = round_matrix(string2)
    return string2

def output(matrix, message, flag):
    message_str = ""
    print("Key matrix:")
    for i in range (len(matrix)):
        for j in range (len(matrix[i])):
            print("%g" % (round(matrix[i][j], 3)), end = '')
            if j < len(matrix[i]) - 1:
                print("\t", end = '')
            else:
                print()
    print()
    if flag == 0:
        print("Encrypted message:")
        for i in range(0, len(message)):
            for j in range(0, len(message[i])):
                message_str += str(message[i][j]) + " "
        message_str = message_str[:-1]
        print(message_str)
    if flag == 1:
        print("Decrypted message:")
        for i in range(0, len(message)):
            message_str += ascii_to_char(message[i])
        print(message_str)


input()