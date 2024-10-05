import pyperclip
import json
import time

# 将聊天记录写入文件
def write_history(talk_content):
    open_history = open('history.txt', 'a', encoding='utf-8', newline='\n')
    open_history.write(talk_content)

# 空行
def blank_line():
    print('\n')


loop_step = True

# 想返回的步骤的锚点
step_one = True
step_two = True
step_four = True
step_six = True

while loop_step:
    # 控制循环
    loop_controler = True

    # 用于判断是否返回上一步
    go_back = False

    # 循环步骤二到最后
    save_target = False

    while loop_controler:
    
        # 步骤一（简称：明义优化文本）
        # 针对用户提供的文本中可能存在的语义不明确之处，持续提问以获得更清晰的理解。然后，基于这一理解优化并重写文本。
        if step_one == True:
            step_one = False
            history = []
            first_talk = False

            # 开始对话
            print(f"# 明义优化文本 \n user: {pyperclip.paste()}\n")
            history.append(pyperclip.paste())
            write_history(f"# 明义优化文本 \n user: {pyperclip.paste()}\n")
            print(f"# 明义优化文本 \n ")
            text = input("What?\n")
            write_history(text)
            history.append(text)

        # 步骤二（简称：寻找意图）
        # 询问用户：‘为何提出此？’
        if step_two == True:
            step_two = False
            print("\n# 寻找意图")
            ask_intent = input(f"assistant: 为何提出【{text}】\n")
            if ask_intent == '返回':
                step_one = True
                break
            write_history(ask_intent)
            pyperclip.copy(ask_intent)

        # 步骤三（简称：明义优化回答）
        # 针对用户上述回答中可能存在的语义不明确之处，持续提问以获得更清晰的理解。然后，基于这一理解优化并重写回答。以 Markdown 代码输出：优化后的回答。

        # 步骤四（简称：询问问题）
        # 询问以下方括号内的问题，注意每次仅提出一个问题，且不添加额外的文字：
        # [
        # 最终目标是什么？
        # 目标是倾向于进取还是保守？
        # 决策场景是什么？
        # ]
        print("\n# 询问问题")
        if step_four == True:
            temporary = input("目标倾向和最终目标是什么？\n")
            step_four = False
            if temporary == '返回':
                step_two = True
                step_four = True
                break

            #保存上一次的最终目标
            if save_target == False:
                ultimate_goal = temporary
                # print(ultimate_goal)
                save_target = True

            # 步骤五（简称：重申）
            # 以 Markdown 代码输出：步骤三中优化后的回答。
            step_six = True

        # 步骤六（询问：决策场景是什么？）
        if step_six == True:
            step_six = False

            if temporary == "最后一步":
                break
            else:
                ultimate_goal = temporary
                decision_scene = input("\n assistant: 决策场景是什么？\n")
                write_history(decision_scene)
                loop_controler = False
                loop_step = False
                break


# 步骤七（简称：显示代码）
# 以 Markdown 代码输出，显示最终目标、目标倾向、决策场景。
pyperclip.copy(f"最终目标：{ultimate_goal}\n\n决策场景：{decision_scene}\n\nhttps://workflowy.com/#/05b597b39bdf\n\n已记录依据？")
write_history(f"最终目标：{ultimate_goal}\n\n决策场景：{decision_scene}")
time.sleep(1)