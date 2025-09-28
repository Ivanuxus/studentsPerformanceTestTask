import csv
import argparse
import sys
import os
from tabulate import tabulate
     
def parse_args(args):
        parser = argparse.ArgumentParser(description="Files")
        parser.add_argument('--files', type=argparse.FileType('r', encoding='UTF-8'), nargs='+', required=True)
        parser.add_argument('--report', type=argparse.FileType('w', encoding='UTF-8'), nargs='+', required=True)
        return parser.parse_args(args)

def read_data(args):
        for file in args.files:
                students = [[],[],[],[]]
                fieldNames = ['student_name', 'subject', 'teacher_name', 'date', 'grade']
                reader = csv.DictReader(file, fieldNames)
                for row in reader:
                        for item in fieldNames:
                                if(row[item] == ''):
                                        raise SystemError
                        if(row['student_name'] not in students[0] and row['student_name'] != 'student_name'):
                                students[0].append(row['student_name'])
                                students[1].append(int(row['grade']))
                                students[2].append(int(1))
                        elif(row['student_name'] in students[0] and row['student_name'] != 'student_name'):
                                students[1][students[0].index(row['student_name'])] += int(row['grade'])
                                students[2][students[0].index(row['student_name'])] += int(1)
        return students
 
def calculate_averages(students):
        marks = [0, 1, 2, 3, 4, 5]                                
        for i in range(0, len(students[0])):
                students[3].append(0)
                if(students[1][i] > 0 and students[2][i] > 0):
                        students[3][i] = int(students[1][i] / students[2][i])
                else:
                        raise SystemError
        while 0 in students[3]:
                students[3].pop()
        return students
def is_number(x):
    return isinstance(x, (int, float, complex))

def sort_by_grade(students):
        for i in range(len(students[3])):
                for j in range(i, len(students[3])):
                        if(is_number(students[3][j]) and is_number(students[3][i])):
                                if(students[3][j] < students[3][i]):
                                        students[0][j], students[0][i] = students[0][i], students[0][j]
                                        students[1][j], students[1][i] = students[1][i], students[1][j]
                                        students[2][j], students[2][i] = students[2][i], students[2][j]
                                        students[3][j], students[3][i] = students[3][i], students[3][j]
                        else:
                                raise SystemError
        return students
def print_grades_and_write(students, args):
        toPrint = []
        for i in range(len(students[0])):
                toPrint.append([students[0][i], students[3][i]])
        toPrint.reverse()
        table_string = (tabulate(toPrint, headers=['Name', 'Grade'], tablefmt='grid',showindex="always"))
        print(table_string)
        with open(args.report[0].name, 'w', encoding="utf-8") as f:
                f.write(table_string)
                
def form_grades():
        args = parse_args(sys.argv[1:])
        data = read_data(args)
        data = calculate_averages(data)
        data = sort_by_grade(data)
        print_grades_and_write(data, args)

if __name__ == "__main__":
        form_grades()