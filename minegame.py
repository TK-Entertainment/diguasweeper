import tkinter
from minecore import Mine
import winsound

# ===============
# If you want to try chino mode, you can change this value to True to activate that function
dev_mode = True
# ===============

window = tkinter.Tk()
if dev_mode:
    window.title("踩地瓜 | 目前處於開發模式")
else:
    window.title("踩地瓜")
menubar = tkinter.Menu(window)

filemenu = tkinter.Menu(menubar)
filemenu.add_command(label="重開遊戲", command=lambda : restart())
filemenu.add_command(label="離開", command=lambda : exit(0))
menubar.add_cascade(label="遊戲", menu=filemenu)
menubar.add_cascade(label="關於", command=lambda : about())
# window.geometry("1000x1000")
# --- setup part ---
def start():
    global dev_mode
    global startframe
    global v
    global options
    global hideframe
    global modegetter
    global v_hide
    global customframe
    global custom_settings
    global icon_list
    startframe = tkinter.LabelFrame(window, text="請選擇您想要的遊戲模式，及設定其基本參數")
    startframe.pack()
    hideframe = [tkinter.LabelFrame(startframe, text="以下為自定義的範圍"), False]
    customframe = [tkinter.LabelFrame(hideframe[0], text="以下為真正自定義的範圍"), False]
    custom_settings = {
        'ratio' : tkinter.Entry(customframe[0], show=None),
        'height' : tkinter.Entry(customframe[0], show=None),
        'width' : tkinter.Entry(customframe[0], show=None),
    }

    if dev_mode:
        options = {
            'default' : [{'name' : "一顆地瓜(簡單)", 'ratio' : 0.1, 'size' : [8, 8], 'shape' : 'rectangle'}, {'name' : "三顆地瓜(中)", 'ratio' : 0.15, 'size' : [10, 10], 'shape' : 'rectangle'}, {'name' : "五顆地瓜(困難)", 'ratio' : 0.2, 'size' : [15, 15], 'shape' : 'rectangle'}, {'name' : "自定義地瓜"}], 
            'custom' : [{'name' : '終極地瓜', 'ratio' : 0.3, 'size' : [20, 20], 'shape' : 'rectangle'},  {'name' : '三角形', 'ratio' : 0.2, 'size' : [16], 'shape' : 'triangle'}, {'name' : 'chino (開發模式)', 'ratio' : 0.5, 'size' : [20, 20], 'shape' : 'rectangle'}, {'name' : "真正的自定義"}]
        }
    else:
        options = {
            'default' : [{'name' : "一顆地瓜(簡單)", 'ratio' : 0.1, 'size' : [8, 8], 'shape' : 'rectangle'}, {'name' : "三顆地瓜(中)", 'ratio' : 0.15, 'size' : [10, 10], 'shape' : 'rectangle'}, {'name' : "五顆地瓜(困難)", 'ratio' : 0.2, 'size' : [15, 15], 'shape' : 'rectangle'}, {'name' : "自定義地瓜"}], 
            'custom' : [{'name' : '終極地瓜', 'ratio' : 0.3, 'size' : [20, 20], 'shape' : 'rectangle'}, {'name' : '三角形', 'ratio' : 0.2, 'size' : [16], 'shape' : 'triangle'}, {'name' : "真正的自定義"}]
        }

    v = tkinter.IntVar()
    v_hide = tkinter.IntVar()

    modegetter = ['default', 0]

    # --- picture init ---
    icon_list = [
        tkinter.PhotoImage(file=r'photos\whiteblock.png'),
        tkinter.PhotoImage(file=r'photos\1.png'),
        tkinter.PhotoImage(file=r'photos\2.png'),
        tkinter.PhotoImage(file=r'photos\3.png'),
        tkinter.PhotoImage(file=r'photos\4.png'),
        tkinter.PhotoImage(file=r'photos\5.png'),
        tkinter.PhotoImage(file=r'photos\6.png'),
        tkinter.PhotoImage(file=r'photos\7.png'),
        tkinter.PhotoImage(file=r'photos\8.png'),
        tkinter.PhotoImage(file=r'photos\chinosmallsmallsmall.png'),
        tkinter.PhotoImage(file=r'photos\taiwansmallsmallsmall.png'),
        tkinter.PhotoImage(file=r'photos\selectedchino.png'),
        tkinter.PhotoImage(file=r'photos\selectedtaiwan.png'),
        tkinter.PhotoImage(file=r'photos\flag.png'),
        tkinter.PhotoImage(file=r'photos\notopened.png'),
    ]

    def mode():
        if (v.get() == len(options['default'])-1):
            if (modegetter[0] == 'default'):
                modegetter[0] = 'custom'
                hideframe[0].pack()
                if (hideframe[1] == False):
                    hideframe[1] = True
                    for i in range(len(options['custom'])):
                        tkinter.Radiobutton(hideframe[0], text=options['custom'][i]['name'], variable=v_hide, value=i, command=hidemode).pack(anchor='n')
        else:
            modegetter[0] = 'default'
            modegetter[1] = v.get()
            hideframe[0].pack_forget()

    def hidemode():
        if (v_hide.get() == len(options['custom'])-1):
            if (customframe[1] == False):
                customframe[1] = True

                tkinter.Label(customframe[0], text="比值：").grid(row=0)
                custom_settings['ratio'].grid(row=0, column=1)
                tkinter.Label(customframe[0], text="場地大小：").grid(row=1)
                custom_settings['height'].grid(row=1, column=1)
                tkinter.Label(customframe[0], text="場地大小：").grid(row=2)
                custom_settings['width'].grid(row=2, column=1)
                customframe[0].pack()
        else:
            customframe[1] = False
            customframe[0].pack_forget()
        modegetter[1] = v_hide.get()

    for i in range(len(options['default'])):
        tkinter.Radiobutton(startframe, text=options['default'][i]['name'], variable=v, value=i, command=mode).pack(anchor='n')

    def setup():
        global custom_settings
        global mainframe
        options['custom'][-1]['ratio'] = float(custom_settings['ratio'].get() or '1')
        options['custom'][-1]['size'] = [int(custom_settings['height'].get() or '10'), int(custom_settings['width'].get() or '10')]
        if dev_mode == True and modegetter[0] == 'custom' and modegetter[1] == 2:
            window.title("請問您今天要來點chino嗎？")
        elif modegetter[0] == 'custom' and modegetter[1] == 0:
            window.title("踩地瓜 (終極地瓜模式)")
        startframe.destroy()
        main()

    startbutton = tkinter.Button(startframe, text="確定", command=setup, relief='groove')
    startbutton.pack(side='bottom')

def restart():
    global mainframe
    global startframe
    if dev_mode:
        window.title("踩地瓜 | 目前處於開發模式")
    else:
        window.title("踩地瓜")
    winsound.PlaySound(None, winsound.SND_PURGE)
    startframe.destroy()
    try:
        mainframe.destroy()
    except:
        pass
    start()   

def about():
    global aboutmain
    aboutwindow = tkinter.Toplevel()
    aboutwindow.title("關於 踩地瓜")
    mark = tkinter.PhotoImage(file=r'photos\mark.png')
    tkinter.Label(aboutwindow, image=mark).pack()
    aboutmain = tkinter.LabelFrame(aboutwindow, text='關於 踩地瓜 Diguasweeper')
    aboutmain.pack()
    if dev_mode:
        tkinter.Label(aboutmain, text='版本 v0.2-20210721 alpha\n========\n已載入 chino.mod 模組\n========\n目前開發模式已開啟\n此版本為初期版本，有諸多ㄉbug還沒修，請小心取用owo\n註:如果你心臟夠大顆，可以試試chino版本\n========\n本程式及部分圖檔(不含chino)皆由 TK Entertainment 製作\nChino 圖片由 NBC環球娛樂 及 Koi 版權所有\nNo Poi! 音樂由 NBC唱片公司 版權所有\n========\nDiguasweeper | Copyright 2021 TK Entertainment / All right reserved').pack()
    else:
        tkinter.Label(aboutmain, text='版本 v0.2-20210721 alpha\n此版本為初期版本，有諸多ㄉbug還沒修，請小心取用owo\n註:如果你心臟夠大顆，可以試試終極地瓜版本\n========\n本程式及圖檔皆由 TK Entertainment 製作\n========\nDiguasweeper | Copyright 2021 TK Entertainment / All right reserved').pack()
    aboutwindow.mainloop()
start()

# --- main part ---

def main():
    global window
    global mainframe
    global modegetter
    global options
    global photo

    mainframe = tkinter.Frame(window)
    mainframe.pack()
    mineframe = tkinter.Frame(mainframe)
    mineframe.pack(side='top')

    minemap = Mine(**options[ modegetter[0] ][ modegetter[1] ])
    minemap.setground()
    minemap.numsetting()
    
    showvar = [[tkinter.StringVar(value='-1') for j in range(options[ modegetter[0] ][ modegetter[1] ]['size'][1] if options[ modegetter[0] ][ modegetter[1] ]['shape'] == 'rectangle' else i+1)] for i in range(options[ modegetter[0] ][ modegetter[1] ]['size'][0])]

    def mine_hitleft(i, j):
        global play
        for item in minemap.click(i, j):
            showvar[item[0]][item[1]].set(minemap.showground[item[0]][item[1]])
            minebutton_list[item[0]][item[1]]['button']['command'] = 0; minebutton_list[item[0]][item[1]]['button']['relief'] = 'sunken'
            if minemap.showground[item[0]][item[1]] == 9:
                if dev_mode == True and modegetter[0] == 'custom' and modegetter[1] == 2:
                    minebutton_list[item[0]][item[1]]['button']['image'] = icon_list[-6]
                    minebutton_list[i][j]['button']['image'] = icon_list[-4]
                else:
                    minebutton_list[item[0]][item[1]]['button']['image'] = icon_list[-5]
                    minebutton_list[i][j]['button']['image'] = icon_list[-3]
            else:
                minebutton_list[item[0]][item[1]]['button']['image'] = icon_list[minemap.showground[item[0]][item[1]]]
            try:
                minebutton_list[i][j]['button'].unbind('<Button-3>', minebutton_list[i][j]['id'])
            except:
                pass
        if minemap.win == 'lose':
            print('owo')
            if dev_mode == True and modegetter[0] == 'custom' and modegetter[1] == 2:
                winsound.PlaySound(r"music\no poi.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            for i in range(options[ modegetter[0] ][ modegetter[1] ]['size'][0]):
                for j in range(options[ modegetter[0] ][ modegetter[1] ]['size'][1] if options[ modegetter[0] ][ modegetter[1] ]['shape'] == 'rectangle' else i+1):
                    minebutton_list[i][j]['button']['command'] = 0; minebutton_list[i][j]['button']['relief'] = 'sunken'
        elif minemap.win == 'win':
            print('oeo')

    
    def mine_hitright(i, j):
        minemap.flag(i, j)
        minebutton_list[i][j]['button']['image'] = icon_list[minemap.showground[i][j]]

    # tkinter.Label(mainframe, text='difficulty', bg='#90ab3e', font=('Arial', 12), width=30, height=2).pack()
    # tkinter.Label(mainframe, text=minemap.diff, bg='lightblue', font=('Arial', 12), width=30, height=2).pack()

    minebutton_list = []
    for i in range(options[ modegetter[0] ][ modegetter[1] ]['size'][0]):
        minebutton_list.append([])
        buttonframe = tkinter.Frame(mineframe)
        for j in range(options[ modegetter[0] ][ modegetter[1] ]['size'][1] if options[ modegetter[0] ][ modegetter[1] ]['shape'] == 'rectangle' else i+1):
            button = tkinter.Button(buttonframe, textvariable=showvar[i][j], image=icon_list[-1], command=lambda i=i, j=j : mine_hitleft(i, j), relief='groove')
            # button = tkinter.Button(frame_l, textvariable=var[i][j], command=lambda i=i, j=j : hit_me(i, j), image=image_list[i][j])
            button.grid(row=i, column=j, sticky="nsew", padx=1, pady=1, ipadx=0, ipady=0)
            minebutton_list[i].append({'button' : button, 'id' : button.bind('<Button-3>', func=lambda event, i=i, j=j : mine_hitright(i, j))})
        buttonframe.pack(anchor='center')

window.config(menu=menubar)
window.mainloop()