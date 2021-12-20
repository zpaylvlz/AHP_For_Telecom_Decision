import tkinter as tk
from tkinter import *
import numpy as np


AHP_val = 0
RI = [1, 1, 0.58, 0.9, 1.12]
stage_weight = [0] * 13
weight_initial = [False,False,False,False,False,False,False,False,False,False,False,False,False]

def Get_Result(label):
    calculated_stage = [0] * 13
    for n in range(13):
        Msize = int(stage_weight[n].shape[0])
        sum_of_col = stage_weight[n].sum(axis=0)
        stage_weight_calculate = stage_weight[n].copy()
        for j in range(Msize):
            for i in range(Msize):
                stage_weight_calculate[i,j] /= sum_of_col.item((0,j))
        sum_of_row= stage_weight_calculate.sum(axis=1)
        sum_of_row /= Msize
        calculated_stage[n]=sum_of_row

    temp1 = np.concatenate((calculated_stage[4], calculated_stage[5]), axis=1)
    temp1 = np.concatenate((temp1, calculated_stage[6]), axis=1)
    temp1 = temp1 * calculated_stage[1]
    temp2 = np.concatenate((calculated_stage[7], calculated_stage[8]), axis=1)
    temp2 = temp2 * calculated_stage[2]
    temp3 = np.concatenate((calculated_stage[9], calculated_stage[10]), axis=1)
    temp3 = np.concatenate((temp3, calculated_stage[11]), axis=1)
    temp3 = np.concatenate((temp3, calculated_stage[12]), axis=1)
    temp3 = temp3 * calculated_stage[3]
    temp0= np.concatenate((temp1, temp2), axis=1)
    temp0= np.concatenate((temp0, temp3), axis=1)
    
    Result= temp0 * calculated_stage[0]
    label['text'] = '結果:\n中華電信: '+str(round(Result[0,0], 5))+'\n台灣大哥大: '+str(round(Result[1,0], 5))+ \
    '\n遠傳電信: '+str(round(Result[2,0], 5))+'\n台灣之星:'+str(round(Result[3,0], 5))+'\n亞太電信: '+str(round(Result[4,0], 5))

def Get_Scale(value):
    global AHP_val
    AHP_val = int(value)

def Calculate_matrix(size, Ctrls, stage, CR, stage_ctrl):
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
    stage_weight[stage] = x
    
    stage_ctrl['bg'] = 'yellow'
    weight_initial[stage] = True
    global AHP_val
    AHP_val = 0
    
    #print(stage_weight)

def Set_Weight(i, j, Ctrls, val):
    if (val >= 0):
        val += 1
        Ctrls[i][j]['text'] = str(val)
        Ctrls[j][i]['text'] = str(round(1/val,3))
    else:
        val *= -1
        val += 1
        Ctrls[j][i]['text'] = str(val)
        Ctrls[i][j]['text'] = str(round(1/val,3))
    
    return

def Set_Matrix(stage_ctrl, solution_num, group, stage):
    Set_Window = tk.Tk()
    Set_Window.title('set')
    Set_Window.geometry('1000x400')
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
        tmpx['width']=10
        tmpx['height']=1
        lbl.append(tmpx)
        tmpy = tk.Label(Set_Window, text=(group[i]), bg='white', fg='black', font=('Arial', 12))
        tmpy.place(relx=0.05, rely=0.35 + 0.15 * i, anchor='center')
        tmpy['width']=10
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
            if (weight_initial[stage]):
                Ctrls[i][j]['text'] = str(stage_weight[stage][i,j])
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
    Btn_calculate['command']= lambda : Calculate_matrix(solution_num, Ctrls, stage,LblCR, stage_ctrl)
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
    canvas.create_line(144, 160, 216, 210)
    canvas.create_line(360, 160, 288, 210)
    canvas.create_line(360, 160, 360, 210)
    canvas.create_line(576, 160, 432, 210)
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


    Telecom_btn = tk.Button(window, text='選擇電信業者', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(Telecom_btn,3, ['經濟考量', '通信服務', '網路服務'], 0))
    Telecom_btn.place(relx = 0.5, rely = 0.05, anchor = 'center')
    Telecom_btn['width'] = 10
    Telecom_btn['height'] = 1


    Economical_btn = tk.Button(window, text='經濟考量', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(Economical_btn,3, ['資費方案', '購機價格','回饋方案'],1))
    Economical_btn.place(relx = 0.2, rely = 0.2, anchor = 'center')
    Economical_btn['width'] = 8
    Economical_btn['height'] = 1


    Comm_btn = tk.Button(window, text='通信服務', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(Comm_btn,2, ['市內電話','通訊品質'],2))
    Comm_btn.place(relx = 0.5, rely = 0.2, anchor = 'center')
    Comm_btn['width'] = 8
    Comm_btn['height'] = 1


    Internet_btn = tk.Button(window, text='網路服務', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(Internet_btn,4,['網路速度','網路穩定性','網路訊號範圍','5G網路頻段'],3))
    Internet_btn.place(relx = 0.8, rely = 0.2, anchor = 'center')
    Internet_btn['width'] = 8
    Internet_btn['height'] = 1

    BillCost_btn = tk.Button(window, text='資\n費\n方\n案', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(BillCost_btn,5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],4))
    BillCost_btn.place(relx = 0.1, rely = 0.4, anchor = 'center')
    BillCost_btn['width'] = 2
    BillCost_btn['height'] = 8

    PhonePrice_btn = tk.Button(window, text='購\n機\n價\n格', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(PhonePrice_btn,5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],5))
    PhonePrice_btn.place(relx = 0.2, rely = 0.4, anchor = 'center')
    PhonePrice_btn['width'] = 2
    PhonePrice_btn['height'] = 8
    
    Feedback_btn = tk.Button(window, text='回\n饋\n方\n案', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(Feedback_btn,5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],6))
    Feedback_btn.place(relx = 0.3, rely = 0.4, anchor = 'center')
    Feedback_btn['width'] = 2
    Feedback_btn['height'] = 8

    CommPhone_btn = tk.Button(window, text='市\n內\n電\n話', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(CommPhone_btn,5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],7))
    CommPhone_btn.place(relx = 0.5, rely = 0.4, anchor = 'center')
    CommPhone_btn['width'] = 2
    CommPhone_btn['height'] = 8

    CommQuality_btn = tk.Button(window, text='通\n訊\n品\n質', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(CommQuality_btn,5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],8))
    CommQuality_btn.place(relx = 0.4, rely = 0.4, anchor = 'center')
    CommQuality_btn['width'] = 2
    CommQuality_btn['height'] = 8
    
    InternetSpeed_btn = tk.Button(window, text='網\n路\n速\n度', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(InternetSpeed_btn,5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],9))
    InternetSpeed_btn.place(relx = 0.6, rely = 0.4, anchor = 'center')
    InternetSpeed_btn['width'] = 2
    InternetSpeed_btn['height'] = 8

    Internet_Stable = tk.Button(window, text='網\n路\n穩\n定\n性', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(Internet_Stable,5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],10))
    Internet_Stable.place(relx = 0.7, rely = 0.4, anchor = 'center')
    Internet_Stable['width'] = 2
    Internet_Stable['height'] = 8

    InternetRange_btn = tk.Button(window, text='網\n路\n訊\n號\n範\n圍', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(InternetRange_btn,5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],11))
    InternetRange_btn.place(relx = 0.8, rely = 0.4, anchor = 'center')
    InternetRange_btn['width'] = 2
    InternetRange_btn['height'] = 8

    Internet5G_btn = tk.Button(window, text='5G\n網\n路\n頻\n段', bg='white', fg='black', font=('Arial', 12), command= lambda: Set_Matrix(Internet5G_btn,5,['中華電信','台灣大哥大','遠傳電信','台灣之星','亞太電信'],12))
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
