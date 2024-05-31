import pyperclip
from zhipuai import ZhipuAI
import json


# 创建Client实例
client = ZhipuAI(api_key="818ae5253337f2acefd85aacf76d0b38.xeyM0qoTFRegnXC9")

# 询问 AI
def talk_with_AI(json_list):
    response = client.chat.completions.create(
        model="glm-4",  # 替换为实际使用的模型名称
        messages=json_list,
        )
    optimized_text = response.choices[0].message.content
    response_content = {"role": "assistant", "content": optimized_text}
    json_list.append(response_content)
    print(f"assistant: {optimized_text}\n")
    return optimized_text

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

            # 只提出一到两个问题
            first_text = "针对我提供的句子'"+ pyperclip.paste() + "'，向我提出两个问题，第一个问题用于修正句法错误，第二个问题用于明确语义。注意，对话惜字如金和不客套，不问涉及句子的意图。"
            user_content = {"role": "user", "content": first_text}
            history.append(user_content)
            # print(f"# 明义优化文本 \n user: {pyperclip.paste()}\n")

            # 第一个问题
            print(f"# 明义优化文本（一） \n ")
            write_history(f"# 明义优化文本 \n user: {pyperclip.paste()}\n")
            talk_with_AI(history)
            text = input("user: ")
            blank_line()
            write_history(text)
            user_content = {"role": "user", "content": text}
            history.append(user_content)

            # 第二个问题
            print(f"# 明义优化文本（二） \n ")
            write_history(f"# 明义优化文本 \n user: {pyperclip.paste()}\n")
            talk_with_AI(history)
            text = input("user: ")
            blank_line()
            write_history(text)
            user_content = {"role": "user", "content": text}
            history.append(user_content)

            reiterate = {"role": "user", "content": "基于所有对话内容，优化并重写我提供的文本"}
            history.append(reiterate)
            print("\n\n # 明义优化文本")
            optimized_text = talk_with_AI(history)

            # 备份 history
            with open('history.txt', 'a', encoding='utf-8') as f:
                # 遍历字典列表
                for message in history:
                    # 创建格式化的字符串
                    formatted_message = f"{message['role']}: {message['content']}\n\n"
                    # 写入文件
                    f.write(formatted_message) 

        # 步骤二（简称：寻找意图）
        # 询问用户：‘为何提出此？’
        if step_two == True:
            step_two = False
            print("# 寻找意图")
            ask_intent = input(f"assistant: 为何提出【{optimized_text}】\n")
            blank_line()
            if ask_intent == '返回':
                step_one = True
                break
            write_history(ask_intent)
            blank_line()
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
        if step_four == True:
            temporary = input("\n最终目标是什么？\n")
            blank_line()
            step_four = False
            if temporary == '返回':
                step_two = True
                break

            #保存上一次的最终目标
            if save_target == False:
                ultimate_goal = temporary
                # print(ultimate_goal)
                save_target = True

            # 步骤五（简称：重申）
            # 以 Markdown 代码输出：步骤三中优化后的回答。
            print(f"优化后文本：{ask_intent}\n")
            step_six = True

        # 步骤六（简称：是否确定破坏主要目标）
        # 询问{忽略此文本，是否确定破坏主要目标？}。若用户回复“确定”，则返回步骤二。
        if step_six == True:
            step_six = False
            confirm = input(f"assistant: 忽略【{optimized_text}】，是否确定破坏主要目标？\n")
            blank_line()
            write_history(confirm)
            if confirm == '返回':
                step_four = True
                step_two = False
                break
            elif confirm == '确定':
                ask_goal_destroyed = input("assistant: 破坏了什么目标？\n")
                blank_line()
                write_history(ask_goal_destroyed)
                pyperclip.copy(ask_goal_destroyed)
            else:
                loop_controler = False
                loop_step = False
                break

            if temporary == "最后一步":
                break
            else:
                ultimate_goal = temporary
                goal_orientation = input("\n assistant: 目标是倾向于进取还是保守？\n")
                blank_line()
                write_history(goal_orientation)
                decision_scene = input("\n assistant: 决策场景是什么？\n")
                blank_line()
                write_history(decision_scene)


# 步骤七（简称：显示代码）
# 以 Markdown 代码输出，显示最终目标、目标倾向、决策场景。
if ultimate_goal != None:
    goal_orientation = ''
    pyperclip.copy(f"最终目标：{ultimate_goal}\n\n目标倾向：{goal_orientation}\n\n决策场景：{decision_scene}")
