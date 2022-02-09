import tkinter
from turtle import width


def table(root, data, column_widths):
    for i in range(len(data)):
        for j in range(len(data[0])):
            e = tkinter.Entry(root, width=column_widths[j])
            e.grid(row=i, column=j)
            e.insert(tkinter.END, data[i][j])
    return e
