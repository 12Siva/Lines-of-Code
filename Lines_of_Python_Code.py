import os
import matplotlib.pyplot as plt
from collections import Counter
import datetime

# Motivation: Get Key Programming Statistics From Your Programming Directory
# Given a directory of programming files (currently only python files are supported)
# get the number of lines of code written, total number of comment lines, and total number of embedded comments

def raw_file_length(file_path, show=False):
    # given a file length (file path), return the number of lines
    # show set to true will output the contents of the file
    # includes blank lines and comments
    lines = open(file_path, 'r')
    line_number = 0
    for line_number, line in enumerate(lines, 1):
        # start with the first line as line 1
        if (show==True):
            print line_number, line
    lines.close()
    return line_number

def file_length(file_path, show=False):
    # return file length excluding blank lines and total number of line comments and embedded comments in the file
    with open(file_path, 'r') as f_in:
        lines = (line.strip() for line in f_in) # all lines including blank lines
        lines = list(line for line in lines if line) # non-blank lines in a list

    linenum = 0
    linecomments = 0 # whole lines that are just comments
    embeddedcomments = 0 # embedded comments in lines of code
    for line in lines:
        if (line.find('#') != -1):
            if (line.startswith('#')):
                linecomments += 1
            embeddedcomments += 1
        linenum += 1
        if (show==True):
            print linenum, line
    f_in.close()
    embeddedcomments = embeddedcomments - linecomments
    return linenum, linecomments, embeddedcomments

def gen_files(directory):
    # generator to get all python files in a directory
    for file in directory:
        if file.endswith('.py'):
            yield file

def line_calculator(directory_path, statslist, pltlist):
    # files in the current directory
    files = os.listdir(directory_path)
    files = [file for file in files if file != '.idea']
    templinecount = 0
    templinecomments = 0
    tempembeddedcomments = 0
    for file in files:
        file_path = directory_path + '\\' + file
        if (os.path.isdir(file_path) == True):
            # if the file path is a directory, look inside of it
            line_calculator(file_path, statslist, pltlist)
        elif file.endswith('.py'):
            # only for python lines get the line count
            templinecount, templinecomments, tempembeddedcomments = file_length(file_path)
            statslist[0] = statslist[0] + templinecount
            pltlist.append(templinecount)
            statslist[1] = statslist[1] + templinecomments
            statslist[2] = statslist[2] + tempembeddedcomments

def plot_stats(pltlist, display=False):
    # scatter plot of num of lines in each programming file
    plt.figure()
    plt.plot(pltlist, 'ro')
    plt.grid(True)
    plt.ylabel('Line Count')
    plt.title('Line Counts of Each Program File in Directory')
    plt.savefig('plots\\linecounts.png', bbox_inches='tight')

    # frequency bar graph
    freq = Counter(pltlist)
    height = [] # the number of times a program file with a certain length is seen
    left = [] # the program file length
    for ele in freq.most_common(50):
        left.append(ele[0])
        height.append(ele[1])

    plt.figure()
    plt.bar(left, height, width=1.2, align='center', color=['y'])
    plt.grid(True)
    plt.xlabel("Length of Program File")
    plt.ylabel("The Number of Occurrences in the Directory")
    plt.title(" 50 Most Common File Lengths")
    plt.xticks(range(0, max(left) + 5, 5))
    plt.yticks(range(0, max(height) + 2, 1))
    plt.savefig('plots\\freq.png', bbox_inches='tight')
    if (display == True):
        plt.show()


if __name__ == '__main__':
    # current working directory
    current_directory = os.getcwd()
    # parent directory name
    directory_name = os.path.dirname(current_directory)
    # ASSUMPTION: the parent directory has all targeted programming files

    pltlist = [] # list of the line count of each program file
    # 0 -> total line count
    # 1 -> total number of line comments
    # 2 -> total number of embedded comments
    statslist = [0,0,0] # list that will hold the wanted statistics

    line_calculator(directory_name, statslist, pltlist)
    results = open('sample.txt', 'a')
    results.write(str(datetime.date.today()) + '\n')
    results.write("Root Directory: " + directory_name + '\n')
    results.write("Total Number of Lines of Code: {} Total Number of Comment Lines: {} Total Number of Embedded Comments: {} \n".format(statslist[0] - statslist[1], statslist[1], statslist[2]))
    results.write("Total Number of Program Files: {} \n".format(len(pltlist)))
    results.write("Ratio of Lines of Code to Comments: {} (lines of code) to 1 (line of comments) \n".format((statslist[0]-statslist[1])/(statslist[1]+statslist[2])))
    pltlist = [x for x in pltlist if x != 0]
    plot_stats(pltlist, display=False)