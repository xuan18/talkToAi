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
            print(f"\n\n{pyperclip.paste()}\n")
            history.append(pyperclip.paste())
            #write_history(f"# 明义优化文本 \n user: {pyperclip.paste()}\n")
            #print(f"# 明义优化文本 \n ")
            text = input("\nWhat?\n")
            #write_history(text)
            history.append(text)

        # 步骤二（简称：寻找意图）
        # 询问用户：‘为何提出此？’
        if step_two == True:
            step_two = False
            #print("\n# 寻找意图")
            ask_intent = input(f"\nassistant: 为何提出【{text}】\n")
            if ask_intent == '返回':
                step_one = True
                step_two = True
                break
            #write_history(ask_intent)
            pyperclip.copy(ask_intent)

        # 步骤四（此待办属于个人，还是超越个人？）
        #print("\n# 询问问题")
        if step_four == True:
            temporary = input("\n此待办属于个人，还是超越个人？\n") #依据：https://workflowy.com/#/fc4dd028269b
            step_four = False
            if temporary == '返回':
                step_two = True
                step_four = True
                break

            #保存上一次该问题的答案
            if save_target == False:
                ultimate_goal = temporary
                # print(ultimate_goal)
                save_target = True
            #开启下一步
            step_five = True

        # 步骤五（询问：目标倾向和最终目标是什么？）
        if step_five == True:
            temporary = input("\n目标倾向和最终目标是什么？\n")
            step_five = False
            if temporary == '返回':
                step_four = True
                step_five = True
                break

            #保存上一次该问题的答案
            if save_target == False:
                ultimate_goal = temporary
                # print(ultimate_goal)
                save_target = True

            #开启下一步
            step_six = True

        # 步骤六（询问：决策场景是什么？）
        if step_six == True:
            decision_scene = input("\n assistant: 决策场景是什么？\n")
            step_six = False
            if temporary == "返回":
                step_five = True
                step_six = True
                break
            else:
                ultimate_goal = temporary
                #decision_scene = input("\n assistant: 决策场景是什么？\n")
                #write_history(decision_scene)
                loop_controler = False
                loop_step = False
                break


# 步骤七
# 复制对话内容
pyperclip.copy(f"最终目标：{ultimate_goal}\n\n决策场景：{decision_scene}\n\nhttps://workflowy.com/#/05b597b39bdf\n\n已记录依据？")

# #将对话记录写入文件
# write_history(f"最终目标：{ultimate_goal}\n\n决策场景：{decision_scene}")
#time.sleep(1)