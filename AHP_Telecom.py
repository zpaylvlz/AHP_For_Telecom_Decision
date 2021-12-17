import tkinter as tk
from tkinter import *
import numpy as np


AHP_val = 0
RI = [1, 1, 0.58, 0.9, 1.12]
stage_weight = [0] * 13

def Get_Result(label):
    temp1 = np.concatenate((stage_weight[4], stage_weight[5]), axis=1)
    temp1 = temp1 * stage_weight[1]
    temp2 = np.concatenate((stage_weight[6], stage_weight[7]), axis=1)
    temp2 = np.concatenate((temp2, stage_weight[8]), axis=1)
    temp2 = np.concatenate((temp2, stage_weight[9]), axis=1)
    temp2 = temp2 * stage_weight[2]
    temp3 = np.concatenate((stage_weight[10], stage_weight[11]), axis=1)
    temp3 = np.concatenate((temp3, stage_weight[12]), axis=1)
    temp3 = temp3 * stage_weight[3]
    temp0= np.concatenate((temp1, temp1), axis=1)
    temp0= np.concatenate((temp0, temp3), axis=1)
    
    Result= temp0 * stage_weight[0]
    label['text'] = '結果:\n中華電信: '+str(round(Result[0,0], 5))+'\n台灣大哥大: '+str(round(Result[1,0], 5))+ \
    '\n遠傳電信: '+str(round(Result[2,0], 5))+'\n台灣之星:'+str(round(Result[3,0], 5))+'\n亞太電信: '+str(round(Result[4,0], 5))

def Get_Scale(value):
    global AHP_val
    AHP_val = int(value)

def Calculate_matrix(size, Ctrls, stage, CR):
    matrix=[]
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[i].append(float(Ctrls[i][j]['text']))
    
    x = np.matrix(matrix)
    e, v = np.linalg.eig(x)
    max_eigen = max(e.real)
    CR_val = ((max_eigen-size)/ (size-1)) / RI[size-1]
    CR['text'] = 'CR='+str(round(CR_val, 5))
    sum_of_col = x.sum(axis=0)
    
    for j in range(size):
        for i in range(size):
            x[i,j] /= sum_of_col.item((0,j))
    sum_of_row= x.sum(axis=1)
    sum_of_row /= size
    stage_weight[stage]=sum_of_row
    global AHP_val
    AHP_val = 0
    #print(stage_weight)

def Set_Weight(i, j, Ctrls, val):
    if (val > 0):
        val += 1
        Ctrls[i][j]['text'] = str(val)
        Ctrls[j][i]['text'] = str(round(1/val,3))
    else:
        val *= -1
        val += 1
        Ctrls[j][i]['text'] = str(val)
        Ctrls[i][j]['text'] = str(round(1/val,3))
    
    return

def Set_Matrix(solution_num, group, stage):
    Set_Window = tk.Tk()
    Set_Window.title('set')
    Set_Window.geometry('900x400')
    Set_Window.configure(background='white')
    global AHP_val
    
    scale_h = tk.Scale(Set_Window, from_=-8, to=8, tickinterval=16, length=750, resolution=1, orient="horizontal", command = Get_Scale)
    scale_h.pack()
    
    Ctrls = []
    lbl = []
    for i in range(solution_num):
        Ctrls.append([])
        tmpx = tk.Label(Set_Window, text=(group[i]), bg='white', fg='black', font=('Arial', 12))
        tmpx.place(relx=0.15+0.15*i, rely=0.2, anchor='center')
        tmpx['width']=8
        tmpx['height']=1
        lbl.append(tmpx)
        tmpy = tk.Label(Set_Window, text=(group[i]), bg='white', fg='black', font=('Arial', 12))
        tmpy.place(relx=0.05, rely=0.35 + 0.15 * i, anchor='center')
        tmpy['width']=8
        tmpy['height']=1
        lbl.append(tmpy)
        for j in range(solution_num):
            if (j > i):
                Ctrls[i].append(tk.Button(Set_Window, text=('0'), bg='black', fg='white', font=('Arial', 12)))
                Ctrls[i][j].place(relx=0.15 + 0.15 * j, rely=0.35 + 0.15 * i, anchor='center')
                Ctrls[i][j]['width']=5
                Ctrls[i][j]['height']=1
                Ctrls[i][j]['command'] = lambda x=i, y=j: Set_Weight(x, y, Ctrls, AHP_val)
            else:
                Ctrls[i].append(tk.Label(Set_Window, text=('0'), bg='gray', fg='white', font=('Arial', 12)))
                Ctrls[i][j].place(relx=0.15 + 0.15 * j, rely=0.35 + 0.15 * i, anchor='center')
                Ctrls[i][j]['width']=5
                Ctrls[i][j]['height']=1
            if (i == j):
                Ctrls[i][j]['text'] = '1'
    LblCR = tk.Label(Set_Window, text=('CR='), bg='black', fg='white', font=('Arial', 12))
    LblCR.place(relx=0.90, rely=0.85, anchor='center')
    LblCR['width']=12
    LblCR['height']=1
    Btn_calculate = tk.Button(Set_Window, text=('Calculate'), bg='white', fg='black', font=('Arial', 12))
    Btn_calculate.place(relx=0.95, rely=0.95, anchor='center')
    Btn_calculate['width']=8
    Btn_calculate['height']=1
    Btn_calculate['command']= lambda : Calculate_matrix(solution_num, Ctrls, stage,LblCR)
    Set_Window.mainloop()
    return 

def MainWindow():
    window = tk.Tk()
    window.title('AHP')
    window.geometry('720x720')
    window.configure(background='white')
    canvas = Canvas(window)
    canvas.create_line(360, 50, 140, 130)
    canvas.create_line(360, 50, 360, 130)
    canvas.create_line(360, 50, 570, 130)
    
    canvas.create_line(144, 160, 72, 210)
    canvas.create_line(144, 160, 144, 210)
    canvas.create_line(360, 160, 216, 210)
    canvas.create_line(360, 160, 288, 210)
    canvas.create_line(360, 160, 360, 210)
    canvas.create_line(360, 160, 432, 210)
    canvas.create_line(576, 160, 504, 210)
    canvas.create_line(576, 160, 576, 210)
    canvas.create_line(576, 160, 648, 210)
    
    canvas.create_line(72, 365, 72, 495)
    canvas.create_line(144, 365, 72, 495)
    canvas.create_line(216, 365, 72, 495)
    canvas.create_line(288, 365, 72, 495)
    canvas.create_line(360, 365, 72, 495)
    canvas.create_line(432, 365, 72, 495)
    canvas.create_line(504, 365, 72, 495)
    canvas.create_line(576, 365, 72, 495)
    canvas.create_line(648, 365, 72, 495)
    
    canvas.create_line(72, 365, 216, 495)
    canvas.create_line(144, 365, 216, 495)
    canvas.create_line(216, 365, 216, 495)
    canvas.create_line(288, 365, 216, 495)
    canvas.create_line(360, 365, 216, 495)
    canvas.create_line(432, 365, 216, 495)
    canvas.create_line(504, 365, 216, 495)
    canvas.create_line(576, 365, 216, 495)
    canvas.create_line(648, 365, 216, 495)
    
    canvas.create_line(72, 365, 360, 495)
    canvas.create_line(144, 365, 360, 495)
    canvas.create_line(216, 365, 360, 495)
    canvas.create_line(288, 365, 360, 495)
    canvas.create_line(360, 365, 360, 495)
    canvas.create_line(432, 365, 360, 495)
    canvas.create_line(504, 365, 360, 495)
    canvas.create_line(576, 365, 360, 495)
    canvas.create_line(648, 365, 360, 495)
    
    canvas.create_line(72, 365, 504, 495)
    canvas.create_line(144, 365, 504, 495)
    canvas.create_line(216, 365, 504, 495)
    canvas.create_line(288, 365, 504, 495)
    canvas.create_line(360, 365, 504, 495)
    canvas.create_line(432, 365, 504, 495)
    canvas.create_line(504, 365, 504, 495)
    canvas.create_line(576, 365, 504, 495)
    canvas.create_line(648, 365, 504, 495)
    
    canvas.create_line(72, 365, 648, 495)
    canvas.create_line(144, 365, 648, 495)
    canvas.create_line(216, 365, 648, 495)
    canvas.create_line(288, 365, 648, 495)
    canvas.create_line(360, 365, 648, 495)
    canvas.create_line(432, 365, 648, 495)
    canvas.create_line(504, 365, 648, 495)
    canvas.create_line(576, 365, 648, 495)
    canvas.create_line(648, 365, 648, 495)
    canvas.pack(fill=BOTH, expand=1)


    Telecom_btn = tk.Button(window, text='選擇電信業者', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(3, ['經濟考量', '通信服務', '網路服務'], 0))
    Telecom_btn.place(relx = 0.5, rely = 0.05, anchor = 'center')
    Telecom_btn['width'] = 10
    Telecom_btn['height'] = 1


    Economical_btn = tk.Button(window, text='經濟考量', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(2, ['月租費', '綁訂合約時間'],1))
    Economical_btn.place(relx = 0.2, rely = 0.2, anchor = 'center')
    Economical_btn['width'] = 8
    Economical_btn['height'] = 1


    Comm_btn = tk.Button(window, text='通信服務', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(4, ['通話品質', '網內互打','市內電話','簡訊'],2))
    Comm_btn.place(relx = 0.5, rely = 0.2, anchor = 'center')
    Comm_btn['width'] = 8
    Comm_btn['height'] = 1


    Internet_btn = tk.Button(window, text='網路服務', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(3,['網路訊號範圍','網路速度','5G網路頻段'],3))
    Internet_btn.place(relx = 0.8, rely = 0.2, anchor = 'center')
    Internet_btn['width'] = 8
    Internet_btn['height'] = 1

    BillCost_btn = tk.Button(window, text='月\n租\n費', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],4))
    BillCost_btn.place(relx = 0.1, rely = 0.4, anchor = 'center')
    BillCost_btn['width'] = 2
    BillCost_btn['height'] = 8

    ContractTime_btn = tk.Button(window, text='合\n約\n時\n間', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],5))
    ContractTime_btn.place(relx = 0.2, rely = 0.4, anchor = 'center')
    ContractTime_btn['width'] = 2
    ContractTime_btn['height'] = 8

    CommQuality_btn = tk.Button(window, text='通\n話\n品\n質', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],6))
    CommQuality_btn.place(relx = 0.3, rely = 0.4, anchor = 'center')
    CommQuality_btn['width'] = 2
    CommQuality_btn['height'] = 8

    CommCall_btn = tk.Button(window, text='網\n內\n互\n打', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],7))
    CommCall_btn.place(relx = 0.4, rely = 0.4, anchor = 'center')
    CommCall_btn['width'] = 2
    CommCall_btn['height'] = 8

    CommPhone_btn = tk.Button(window, text='市\n內\n電\n話', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],8))
    CommPhone_btn.place(relx = 0.5, rely = 0.4, anchor = 'center')
    CommPhone_btn['width'] = 2
    CommPhone_btn['height'] = 8

    CommMsg_btn = tk.Button(window, text='簡\n訊', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],9))
    CommMsg_btn.place(relx = 0.6, rely = 0.4, anchor = 'center')
    CommMsg_btn['width'] = 2
    CommMsg_btn['height'] = 8

    InternetRange_btn = tk.Button(window, text='網\n路\n訊\n號\n範\n圍', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],10))
    InternetRange_btn.place(relx = 0.7, rely = 0.4, anchor = 'center')
    InternetRange_btn['width'] = 2
    InternetRange_btn['height'] = 8

    InternetSpeed_btn = tk.Button(window, text='網\n路\n速\n度', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],11))
    InternetSpeed_btn.place(relx = 0.8, rely = 0.4, anchor = 'center')
    InternetSpeed_btn['width'] = 2
    InternetSpeed_btn['height'] = 8

    Internet5G_btn = tk.Button(window, text='5G\n網\n路\n頻\n段', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],12))
    Internet5G_btn.place(relx = 0.9, rely = 0.4, anchor = 'center')
    Internet5G_btn['width'] = 2
    Internet5G_btn['height'] = 8

    CHT_label = tk.Label(window, text='中華電信', bg='black', fg='white', font=('Arial', 12))
    CHT_label.place(relx=0.1, rely=0.7, anchor='center')
    CHT_label['width']=8
    CHT_label['height']=1

    TMobile_label = tk.Label(window, text='台灣大哥大', bg='black', fg='white', font=('Arial', 12))
    TMobile_label.place(relx=0.3, rely=0.7, anchor='center')
    TMobile_label['width']=8
    TMobile_label['height']=1

    FarEast_label = tk.Label(window, text='遠傳電信', bg='black', fg='white', font=('Arial', 12))
    FarEast_label.place(relx=0.5, rely=0.7, anchor='center')
    FarEast_label['width']=8
    FarEast_label['height']=1

    TStar_label = tk.Label(window, text='台灣之星', bg='black', fg='white', font=('Arial', 12))
    TStar_label.place(relx=0.7, rely=0.7, anchor='center')
    TStar_label['width']=8
    TStar_label['height']=1

    AP_label = tk.Label(window, text='亞太電信', bg='black', fg='white', font=('Arial', 12))
    AP_label.place(relx=0.9, rely=0.7, anchor='center')
    AP_label['width']=8
    AP_label['height']=1
    
    Result_label = tk.Label(window, text='結果:\n', bg = 'white', fg='black',font=('Arial, 12'), justify=LEFT)
    Result_label.place(relx=0.6, rely = 0.85,anchor='center')
    Result_label['width'] = 20
    Result_label['height'] = 8
    
    Result_btn = tk.Button(window, text='計算', bg='white', fg='black', font=('Arial', 12), command= lambda: Get_Result(Result_label))
    Result_btn.place(relx = 0.9, rely = 0.8, anchor = 'center')
    Result_btn['width'] = 6
    Result_btn['height'] = 1
    

    window.mainloop()

MainWindow()
