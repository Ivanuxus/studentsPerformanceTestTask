import csv
import argparse
import sys
from tabulate import tabulate
     
def parse_args(args):
        parser = argparse.ArgumentParser(description="Files")
        parser.add_argument('--files', type=argparse.FileType('r', encoding='UTF-8'), nargs='*')
        return parser.parse_args(args)

def read_data(args=parse_args(sys.argv[1:])):
        for file in args.files:
                students = [[],[],[],[]]
                fieldNames = ['student_name', 'subject', 'teacher_name', 'date', 'grade']
                reader = csv.DictReader(file, fieldNames)
                for row in reader:
                        if(row['student_name'] not in students[0] and row['student_name'] != 'student_name'):
                                students[0].append(row['student_name'])
                                students[1].append(int(row['grade']))
                                students[2].append(int(1))
                        elif(row['student_name'] in students[0] and row['student_name'] != 'student_name'):
                                students[1][students[0].index(row['student_name'])] += int(row['grade'])
                                students[2][students[0].index(row['student_name'])] += int(1)
        return students
 
def calculate_averages(students=read_data()):                                   
        for i in range(0, len(students[0])):
                students[3].append(0)
                students[3][i] = int(students[1][i] / students[2][i])    
        while 0 in students[3]:
                students[3].pop()
        return students

def sort_by_grade(students=calculate_averages()):
        print(students[0])
        print(students[1])
        print(students[2])
        print(students[3])
        for i in range(len(students[3])):
                pass
                

def form_grades():
        read_data()
        calculate_averages()
        sort_by_grade()

if __name__ == "__main__":
        form_grades()