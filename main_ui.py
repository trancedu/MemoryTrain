# import pandas as pd
# import numpy as np
import random
import re
import os 
# import easygui as G
import PySimpleGUI as sg  
# sg.theme('Material1')
# sg.theme('DarkPurple')
memories = dict() ## 存储已经记过的信息

file = "早晨从中午开始.txt"
file = "一只特立独行的猪.txt"
# file = "周杰伦.txt"
# file = "我们为什么会分手.txt"
# file = "阳谋高手.txt"
# file = "从林肯到奥巴马时代.txt"
# file = "原则.txt"
# file = "人类简史.txt"
# file = "金融帝国博弈.txt"


# 去掉txt 中特殊字符 首尾空格 分句
def normal_cut_sentence(text):
    text = re.sub('([。！？\?])([^’”])',r'\1\n\2',text)#普通断句符号且后面没有引号
    text = re.sub('(\.{6})([^’”])',r'\1\n\2',text)#英文省略号且后面没有引号
    text = re.sub('(\…{2})([^’”])',r'\1\n\2',text)#中文省略号且后面没有引号
    text = re.sub('([.。！？\?\.{6}\…{2}][’”])([^’”])',r'\1\n\2',text)#断句号+引号且后面没有引号
    text = text.rstrip()    # 去掉段尾的\n，然后
    texts = text.split("\n")
    texts = [x.strip() for x in texts if x.strip()]
    return texts

# 读取 txt 文件
def read_text(file):
    with open(file, encoding="utf-8") as f:
        content = f.read()
        content = normal_cut_sentence(content)
        return content

texts = read_text(file)
# print(read_text(file))


# 随机选取句子
def select_sentence(texts, paragraphs=1, lower_limit=40, upper_limit=100):
    """_summary_

    Args:
        texts (str): 列表
        paragraphs (int, optional): 选取内容最多多少段. Defaults to 1.
        lower_limit (int, optional): 选取内容至少多少字. Defaults to 40.
        upper_limit (int, optional): 选取内容最多多少字. Defaults to 100.

    Returns:
        str: 需要记忆的内容
    """
    length = len(texts)
    cnt = 0
    if len(texts) <= 3: return " ".join(texts)
    while True:
        start = random.randint(0, length-paragraphs)
        text = texts[start: start + random.randint(1, paragraphs+1)]
        text = " ".join(text)
        text_length = len(text)
        if upper_limit >= text_length >= lower_limit:
            break
    return text

# paras = select_sentence(texts, 2)
# print(paras)

### 计算相似度 (只计算中文字符的相似度) 并将相似度结果写入 log
# 这里面计算方法是有一点问题的 不过影响不大 参考参考就行
def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', file)
    return chinese 

def compare_similarity(paras, words, flag=0):
    memories[paras] = memories.get(paras, 0) + 1
    recall_count = memories[paras]
    # print(f"第{recall_count}次回忆")
    paras_chinese = find_chinese(paras)
    words_chinese = find_chinese(words)
    words_chinese = "空白" if not words_chinese else words_chinese
    # 计算正确词汇和错误词汇的个数
    count = 0
    wrong = 0
    wrong_words = []
    for word in words_chinese:
        if word in paras_chinese:
            count += 1
        else:
            wrong += 1
            wrong_words.append(word)
    
    # 计算遗漏的词汇和个数
    lack_count = 0
    lack_words = []
    for word in paras_chinese:
        if word not in words_chinese:
            lack_count += 1
            lack_words.append(word)
            
    lack_words = " ".join(lack_words)
    wrong_words = " ".join(wrong_words)
    accuracy = round(count / len(paras_chinese), 3)
    precision = round(count / len(words_chinese), 3)
    infos = [words, paras, f"{accuracy} ({count}/{len(paras_chinese)})", f"{precision} ({count}/{len(words_chinese)})",\
        f"{count} ({len(words_chinese)})", f"{wrong} ({len(words_chinese)})", wrong_words, lack_words]
    info = f"回忆内容: {words}\n正确答案: {paras}\n\n"
    info += f"回忆覆盖率: {accuracy} ({count}/{len(paras_chinese)}), 回忆准确率: {precision} ({count}/{len(words_chinese)}), \n回忆正确字数: {count} ({len(words_chinese)}) 回忆错误字数: {wrong} ({len(words_chinese)})\n\n"
    info += f"错误列表: {wrong_words}\n遗漏列表: {lack_words}\n"
    # print(info)
    # print("回忆内容:", words)
    # print("正确答案:", paras)
    # print(f"回忆覆盖率: {accuracy} ({count}/{len(paras_chinese)}), 回忆准确率: {precision} ({count}/{len(words_chinese)}), \n回忆正确字数: {count} ({len(words_chinese)}) 回忆错误字数: {wrong} ({len(words_chinese)})")
    # print("错误列表:", wrong_words)
    # print("遗漏列表:", lack_words)
    with open("log.csv", "a+", encoding="utf-8") as f:
        f.write(f'"{paras}", "{words}", {recall_count}, {accuracy}, {precision}, "{lack_words}", "{wrong_words}", {len(paras_chinese)}\n')
    with open("log_readable.txt", "a+", encoding="utf-8") as f:
        f.write(f'{paras}\n')
        f.write(f'{words}\n')
        f.write(f"回忆覆盖率: {accuracy} ({count}/{len(paras_chinese)}), 回忆准确率: {precision} ({count}/{len(words_chinese)}), \n回忆正确字数: {count} ({len(words_chinese)}) 回忆错误字数: {wrong} ({len(words_chinese)})\n\n")
    if flag == 0:
        return info
    if flag == 1:
        return infos
# compare_similarity(paras, "要从眼前《人生》所造成的暖融融的气氛中，再一次踏进冰天雪地去进行一次看不见前 退堂的鼓声")

# def get_input(message, default):
#     number = input(message).strip()
#     try:
#         number = int(number)
#     except:
#         number = default
#     return number

def get_input(message, default):
    number = input(message).strip()
    try:
        number = int(number)
    except:
        number = default
    return number

def text2int(message, default):
    number = message.strip()
    try:
        number = int(number)
    except:
        number = default
    return number

# Test GUI
# m = G.enterbox("输入这里")
# G.msgbox(m + " 你好")


def input_window(message):
    # Define the window's contents
    layout = [  [sg.Text(message, font=("宋体", 25),)],     # Part 2 - The Layout
                [sg.Input(size=(100, 2), font=("宋体", 25))],
                # [sg.Text(size=(40,2), key='-INPUT-')],
                [sg.Button('完成', font=("宋体", 25), bind_return_key=True)] ]

    window = sg.Window('输入框', layout, size=(800, 200)) 
    # Display and interact with the Window
    event, values = window.read()                   # Part 4 - Event loop or Window.read call

    # Do something with the information gathered
    # print('Hello', values[0], "! Thanks for trying PySimpleGUI")

    # Finish up by removing from the screen
    window.close()     
    return values[0]

# input_window()

# 记忆难度参数
paragraphs=3
lower_limit=40
upper_limit=50

SmallFont = ("宋体", 15)
FONT = ("宋体", 20)
BigFont = ("宋体", 30)
sg.set_options(font=FONT)
def make_window_menu():
    layout =  [
        [sg.Text("---欢迎使用记忆力练习小程序!---", )],
        [sg.Button("开始记忆", font=BigFont), sg.Button("修改难度", font=BigFont)],
        [sg.Button("切换书籍", font=BigFont), sg.Button("手动粘贴", font=BigFont)],
        [sg.Exit("退出程序")]
        ]
    return sg.Window('记忆练习', layout, finalize=True, element_justification='c')

# window = sg.Window('记忆练习', layout)
# event, values = window.read()

def make_window_jiyi(content="你要记住我"):
    layout = [
        [sg.Text("请记忆以下内容", font=("宋体", 15))],
        [sg.Text(content, font=("宋体", 20), size=(60, 5))],
        [sg.Button("已记住"), sg.Button("换一句")]
    ]
    return sg.Window('开始记忆', layout, finalize=True)
    
def make_window_huiyi():

    # Define the window's contents
    layout = [  [sg.Text("请输入回忆内容: ", font=("宋体", 20))],     # Part 2 - The Layout
                [sg.Multiline(size=(80, 4), font=("宋体", 20), key="-huiyi-")],
                # [sg.Text(size=(40,2), key='-INPUT-')],
                [sg.Button('完成', font=("宋体", 20), bind_return_key=True)] ]

    window = sg.Window('输入框', layout, size=(800, 200), finalize=True) 
    return window

def make_window_accuracy(infos):
    sg.set_options(font=SmallFont)
    info_texts = ["回忆内容为: ", "正确答案为: ", "回忆覆盖率: ", "回忆准确率: ", "回忆正确数: ", "回忆错误数: ", "回忆错误字: ", "回忆遗漏字: "]
    width = max(len(infos[0]), len(infos[1]), len(infos[-1]), len(infos[-2]))
    width = int(width * 1.6) if width < 80 else 120
    layout = [[sg.Text(info_texts[i], text_color="black"), sg.Text(infos[i], size=(width, None))] for i in range(2)]
    layout+= [[sg.Text(info_texts[i], text_color="black"), sg.Text(infos[i], size=(12, 1)), sg.Text(info_texts[i+1], text_color="black"), sg.Text(infos[i+1], size=(20,1))] for i in [2, 4]]
    layout+= [[sg.Text(info_texts[i], text_color="black"), sg.Text(infos[i], size=(width, None))] for i in range(6,8)]
        # [sg.Text(info, font=("宋体", 15), size=(120, 13))],
    layout+= [[sg.Button("重新回忆"), sg.Button("下一句"), sg.Button("返回菜单")]]
    window = sg.Window('回忆评估', layout, finalize=True) 
    sg.set_options(font=FONT)
    return window

def make_window_difficulty():
    layout = [
        [sg.Text("请滑动进度条选择难度", font=BigFont)],
        # [sg.Text("请输入记忆内容最大句子数(默认为3): "), sg.Input(key="-paragraphs-")],
        # [sg.Text("请输入记忆内容最小字数(默认为40): "), sg.Input(key="-minwords-")],
        # [sg.Text("请输入记忆内容最大字数(默认为50): "), sg.Input(key="-maxwords-")],
        [sg.Text("请输入记忆内容最大句子数(默认为3): "), sg.Slider(range=(1,10), default_value=3, size=(29,15), orientation='horizontal', key="-paragraphs-", tick_interval=3)],
        [sg.Text("请输入记忆内容最小字数(默认为40): "),sg.Slider(range=(10,150), default_value=40, size=(30,15), orientation='horizontal', key="-minwords-", tick_interval=30)],
        [sg.Text("请输入记忆内容最大字数(默认为50): "),sg.Slider(range=(10,150), default_value=50, size=(30,15), orientation='horizontal', key="-maxwords-", tick_interval=30)],
        [sg.Text(f"调整之前参数----最大句子数: {int(paragraphs)} 最小字数: {int(lower_limit)} 最大字数 {int(upper_limit)}", key="-parameters-")],
        [sg.Button("确定")],
        

    ]
    window = sg.Window('修改难度', layout, finalize=True, element_justification="c") 
    return window
    
def make_window_changebook():
    files = [x for x in os.listdir(".") if x.endswith(".txt") and "log" not in x]
    layout = [
        [sg.Text("请选择记忆的书籍: ")],
        [sg.DropDown([file[:-4] for file in files], key="-book-", size=(30, 10), default_value=files[0][:-4])],
        [sg.Button("确定")]
    ]
    window = sg.Window('切换书籍', layout, finalize=True) 
    return window
def make_window_paste():

    layout = [
        [sg.Text("请粘贴需要背诵的语句: ")],
        [sg.Multiline(size=(80, 10), key="-paste-")],
        [sg.Button("确定")]
    ]
    window = sg.Window('手动粘贴', layout, finalize=True) 
    return window

def make_window_insist():
    layout = [
        [sg.Text("你真的要离开吗? 坚持就是胜利!")],
        [sg.Text()],
        [sg.Button("佛系躺平"), sg.Button("为爱加油", button_color="red")]
    ]
    window = sg.Window('加油', layout, finalize=True, element_justification="c") 
    return window 

if __name__ == "__main__":
    window_menu, window_jiyi, window_huiyi, window_accuracy, window_difficulty, window_changebook, window_paste = \
        make_window_menu(), None, None, None, None, None, None
    while True:
        window, event, values = sg.read_all_windows()
        if window == window_menu and event in (sg.WIN_CLOSED, '退出程序'):
            break

        elif window == window_menu:
            if event == '开始记忆':
                window_menu.hide()
                paras = select_sentence(texts, paragraphs=paragraphs, lower_limit=lower_limit, upper_limit=upper_limit)
                window_jiyi = make_window_jiyi(paras)
            elif event == '修改难度':
                window_menu.hide()
                window_difficulty = make_window_difficulty()
            elif event == "切换书籍":
                window_menu.hide()
                window_changebook = make_window_changebook()
            elif event == "手动粘贴":
                window_menu.hide()
                window_paste = make_window_paste()
            # window1['-OUTPUT-'].update(values['-IN-'])

        elif window == window_jiyi:
            if event == '已记住':
                window_jiyi.hide()
                window_huiyi = make_window_huiyi()
            elif event == "换一句":
                window_jiyi.close()
                paras = select_sentence(texts, paragraphs=paragraphs, lower_limit=lower_limit, upper_limit=upper_limit)
                window_jiyi = make_window_jiyi(paras)

            # elif event in (sg.WIN_CLOSED, '< Prev'):
            #     window2.close()
            #     window1.un_hide()

        elif window == window_huiyi:
            if event == "完成":
                window_huiyi.close()
                words = values["-huiyi-"].strip()
                window_huiyi.close()
                # info = compare_similarity(paras, words)
                # window_accuracy = make_window_accuracy(info)
                infos = compare_similarity(paras, words, flag=1)
                window_accuracy = make_window_accuracy(infos)
            # window2.un_hide()
        
        elif window == window_accuracy:
            if event == "返回菜单":
                window_menu.un_hide()
                window_accuracy.close()
            elif event == "重新回忆":
                window_huiyi = make_window_huiyi()
                window_accuracy.close()
                pass
            elif event == "下一句":
                paras = select_sentence(texts, paragraphs=paragraphs, lower_limit=lower_limit, upper_limit=upper_limit)
                window_jiyi = make_window_jiyi(paras)
                window_accuracy.close()
                pass
        
        elif window == window_difficulty:
            if event == "确定":
                paragraphs = values["-paragraphs-"]
                lower_limit = values["-minwords-"]
                upper_limit = values["-maxwords-"]
                # window["-paragraphs-"].update(paragraphs)
                # window["-minwords-"].update(lower_limit)
                # window["-maxwords-"].update(upper_limit)
                window_difficulty.close()
                window_menu.un_hide()
        
        elif window == window_changebook:
            if event == "确定":
                book = values["-book-"] + ".txt"
                texts = read_text(book)
                window_changebook.close()
                window_menu.un_hide()
        
        elif window == window_paste:
            if event == "确定":
                content = values["-paste-"]
                texts = normal_cut_sentence(content)
                with open("自定义.txt", 'a+', encoding="utf-8") as f:
                    f.write("\n".join(texts))
                    # print("已加入自定义.txt")
                window_paste.close()
                window_menu.un_hide()
            
        if event in (sg.WIN_CLOSED, '退出程序'):
            window_insist = make_window_insist()
            window, event, values = sg.read_all_windows()
            if event in ("佛系躺平", sg.WIN_CLOSED):
                window_insist.close()
                break
            elif event == "为爱加油":
                window_insist.close()
                  
    window.close()
    
# if event == "开始记忆":
#     window2 = make_window_kaishijiyi()
    
            
    
# elif event == "修改难度":
#     layout_sub = [
#         [sg.Text("请输入难度设置")]
#     ]


# window.close()

# while True:
#     os.system("clear")
#     print(
# """
# ---欢迎使用记忆力练习小程序!---
# 请输入选项:
# 1. 生成记忆内容并开始回忆
# 3. 查看记忆内容
# 4. 切换书籍
# 5. 修改记忆难度
# 6. 自定义背诵内容
# 0. 退出程序
# """
#           )
#     select = input("请输入选项: ")
#     if not select.strip().isdigit():
#         continue
#     select = int(select.strip())
#     if select == 0:
#         break 
#     if select == 1:  
#         outerBreak = False
#         while True:
#             while True:
#                 ### 记忆内容 记忆后请折叠该单元格
#                 if len(texts) <= 3:
#                     paras = " ".join(texts)
#                 else:
#                     paras = select_sentence(texts, paragraphs=paragraphs, lower_limit=lower_limit, upper_limit=upper_limit)
#                 os.system("clear")
#                 print(paras)
#                 wait = input("\n\n\n\n\n如果不想记可以按n切换记忆内容 记住后请按回车键 ")
#                 os.system("clear")
#                 if wait != "n":
#                     break
                
#             while True:
#                 os.system("clear")
#                 # words = G.enterbox("请输入回忆内容:")
#                 # words = input_window("请输入回忆内容:")
#                 words = input("请输入回忆内容: ")
#                 os.system("clear")
#                 compare_similarity(paras, words)
#                 cont = input("\n按回车键再次回忆 按m返回菜单 按n切换记忆内容: ")
#                 if cont == "n":
#                     break
#                 if cont == "m":
#                     outerBreak = True
#                     break
#             if outerBreak:
#                 break
    
#     if select == 3:
#         print(paras)
#         wait = input("\n按回车键继续")
#     if select == 4:
#         files = [x for x in os.listdir(".") if x.endswith(".txt") and "log" not in x]
#         files_dict = dict(zip(range(len(files)), files))
#         info = ""
#         for key, value in files_dict.items():
#             info += f"{key}: {value[:-4]}\n"
#         print(info)
#         choice = input("请输入书籍编号: ")
#         if not choice.strip().isdigit():
#             print("错误格式 请输入数字")
#         choice = int(choice.strip())
#         choice = choice if choice in files_dict else 0
#         texts = read_text(files_dict[choice])
#         print(f"已经切换到{files_dict[choice]}")
#         wait = input("\n按回车键继续")
#     if select == 5:
#         print("请在下方输入数字 来调整记忆难度")
#         paragraphs = get_input("请输入记忆内容包含最大句子数(默认为3): ", 3)
#         lower_limit = get_input("请输入记忆内容最小字数(默认为40): ", 40)
#         upper_limit = get_input("请输入记忆内容最大字数(默认为50): ", 50)
#         print("已修改记忆难度")
#         wait = input("\n按回车键继续")
#     if select == 6:
#         content = input("请粘贴需要背诵的话: ")
#         texts = normal_cut_sentence(content)
#         with open("自定义.txt", 'a+', encoding="utf-8") as f:
#             f.write("\n".join(texts))
#             print("已加入自定义.txt")
#         print(texts)
#         wait = input("\n按回车键继续")
        
        