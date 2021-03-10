import sqlite3, random
from sqlite3 import Error
from itertools import product
import os.path

CHAR_LEN = 5000
NUM_LIST = list(range(CHAR_LEN))

def sql_connection():
    try:
        con = sqlite3.connect('char_brothers.db')
        return con
    except Error:
        print(Error)

def sql_table():
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE char_table(char_id integer PRIMARY KEY, char text, brothers_list text)")
    con.commit()

def sql_insert(entities):
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO char_table(char_id, char, brothers_list) VALUES(?, ?, ?)', entities)
    con.commit()

def sql_fetch(char_id):
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute('SELECT brothers_list FROM char_table WHERE char_id = %s'%char_id)
    rows = cursorObj.fetchall()
    #print(rows[0][0])
    return rows[0][0]

def str_to_list(str_text):
    try:
        if "-" in str_text or "+" in str_text:
            list_out=[]
            double_list = []
            char_list = str_text.split(',')
            for char in char_list:
                if "-" in char:
                    range_list = list(map(int,(char.split("-")))) # "10-13" -> [10,13]
                    list_out.extend(range(range_list[0],range_list[1]+1)) # [10,13] -> 10,11,12,13
                elif "+" in char:
                    double_list.append(list(map(int,(char.split("+")))))
                else:
                    list_out.append(int(char))
            return [list_out,double_list]
        elif str_text.isspace() or str_text == "":
            return [[],[]]
        else:
            return [list(map(int,(str_text.split(',')))),[]]
    except ValueError:
        return ["Не верный формат данных! Должны быть только числа  | %s" % str_text]

def get_variants(word): #Выдаёт варианты без двойных символов
    con = sql_connection()
    str_len=len(word)
    matrix = []
    output = []
    for char in word:
        char_var = [ord(char)]
        char_var.extend(str_to_list(sql_fetch(ord(char)))[0])
        #print(str_to_list(sql_fetch(ord(char))))
        matrix.append(char_var)
        #print(ord(char),char_var)
    return matrix
    #apply_tuple = lambda f: lambda args: f(*args)
    #return list(apply_tuple(product)(tuple(matrix)))

def get_full_variants(word):
    con = sql_connection()
    str_len = len(word)
    matrix = []
    output = []
    for char in word:
        char_var = str_to_list(sql_fetch(ord(char)))
        char_var[0].insert(0,ord(char)) #Добавляет в начало списка вариантов начальную букву(как один из вариантов)
        #print(str_to_list(sql_fetch(ord(char))))
        matrix.append(char_var)
        # print(ord(char),char_var)
    return matrix

def get_combinations_double(word):
    matrix_combo = get_full_variants(word)

    matrix_simple = get_variants(word)
    apply_tuple = lambda f: lambda args: f(*args)
    simple_combo = list(apply_tuple(product)(tuple(matrix_simple)))
    #print(simple_combo)
    double_combo = []
    for i in range(len(matrix_combo)):
        #print("matrix_combo", matrix_combo)
        for z in matrix_combo[i][1]:
            #print("z",z)
            #double_combo.append()
            for x in simple_combo:
                simple_word = list(x).copy()
                #print(chr(z[0]),chr(z[1]))
                simple_word.pop(i)
                simple_word[i:i]=z
                #print(simple_word)
                #print(tuple(simple_word))
                #simple_word.insert(i,z[0])
                #simple_word.insert(i+1, z[1])
                double_combo.append(tuple(simple_word))
    return(vars_to_str(double_combo))


def get_all_combinations(word):
    matrix = get_variants(word)
    apply_tuple = lambda f: lambda args: f(*args)
    return vars_to_str(list(apply_tuple(product)(tuple(matrix))))

#def double_from_

def vars_to_str(vars):
    strs = []
    for word in vars:
        #print(word[0])
        word_str=""
        for let in word:
            #print(let)
            word_str+=chr(let)
            #print(word_str)
        strs.append(word_str)
    return strs

def random_combo(word, word_count, let_count=-1):
    combos = []
    #print(let_count)
    letters = len(word)
    if let_count == -1:
        let_count = letters
    elif let_count > letters &  let_count<=0:
        let_count = letters
        print("Число изменяемых букв не может быть больше числа букв в слове \ меньше или ровно нулю. Было изменино на кол-во букв в слове")
    stable_let = letters - let_count
    stable_list = [random.randint(0,letters) for i in range(stable_let)]
    matrix = get_variants(word)
    #print(matrix)
    #print(chr(matrix[0][0]))
    for i in range(word_count):
        word=""
        stable_ind= [random.randint(0, letters-1) for i in range(stable_let)]
        #print("stable_ind",stable_ind)
        for let in range(letters):
            #print("let out = ",let)
            if let in stable_ind:
                #print("let",let)
                word+=chr(matrix[let][0])
            else:
                word+=chr(random.choice(matrix[let]))

        combos.append(word)
    return combos

def random_stable(word, stable_ind = []):
    letters = len(word)
    matrix = get_variants(word)
    word = ""
    # print("stable_ind",stable_ind)
    for let in range(letters):
        # print("let out = ",let)
        if let in stable_ind:
            # print("let",let)
            word += chr(matrix[let][0])
        else:
            word += chr(random.choice(matrix[let]))
    return word
    #print(matrix)


con = sql_connection()
print(get_all_combinations("shit"))
#print(get_combinations_double("ravik"))
#for i in get_combinations_double("rav ik"):
#    print(i,end=" ")
#print(get_all_combinations('fuck'))
#print(get_all_combinations("fuck"))
#print(get_full_variants('fuck'))
#print(random_stable("RAVIK",[0,3]))
#print(random_combo("RAVIK MOROZOV",10 ))
#print(get_variants("ABS"))
#print(" ".join(vars_to_str(get_all_combinations("NAGATO"))))
#print(vars_to_str(get_variants(con, "RAVIK MOROZOV")))

#print(str_to_list(sql_fetch(con,64)))
#sql_table(con)

#for i in NUM_LIST:
#    sql_insert(con, (i,chr(i),""))
