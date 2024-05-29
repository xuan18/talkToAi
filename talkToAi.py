import pyperclip
from zhipuai import ZhipuAI
import json


# 创建Client实例
client = ZhipuAI(api_key="818ae5253337f2acefd85aacf76d0b38.xeyM0qoTFRegnXC9")

# 如何持续跟 ai 对话，直至我跟他说下一步？
def clarify_and_rewrite_with_ai(json_list):
    # 使用智谱AI模型来优化和重写文本
    response = client.chat.completions.create(
        model="glm-4",  # 替换为实际使用的模型名称
        messages=json_list,
        )
    optimized_text = response.choices[0].message.content
    response_content = {"role": "assistant", "content": optimized_text}
    json_list.append(response_content)
    print(f"assistant: {optimized_text}\n")
    return optimized_text


# 步骤一（简称：明义优化文本）
# 针对用户提供的文本中可能存在的语义不明确之处，持续提问以获得更清晰的理解。然后，基于这一理解优化并重写文本。
history = []
first_talk = False

# 只提出一到两个问题
first_text = "针对我提供的句子'"+ pyperclip.paste() + "'中可能存在的语义不明确之处，提出一个问题以获得更清晰的理解。注意，对话惜字如金和不客套，不问涉及句子的意图。"
user_content = {"role": "user", "content": first_text}
history.append(user_content)
print("# 明义优化文本")
print(f"user: {pyperclip.paste()}\n")
clarify_and_rewrite_with_ai(history)
text = input("user: ")
user_content = {"role": "user", "content": text}
history.append(user_content)
reiterate = {"role": "user", "content": "基于所有对话内容，优化并重写我提供的文本"}
history.append(reiterate)
print("\n\n # 明义优化文本")
optimized_text = clarify_and_rewrite_with_ai(history)

# 控制循环
loop_controler = True

# 循环步骤二到最后
save_target = False
while loop_controler:

    # 步骤二（简称：寻找意图）
    # 询问用户：‘为何提出此？’
    print("# 寻找意图")
    print(f"assistant: 为何提出【{optimized_text}】")
    ask_intent = input("\n")
    pyperclip(ask_intent)

    # 步骤三（简称：明义优化回答）
    # 针对用户上述回答中可能存在的语义不明确之处，持续提问以获得更清晰的理解。然后，基于这一理解优化并重写回答。以 Markdown 代码输出：优化后的回答。

    # 步骤四（简称：询问问题）
    # 询问以下方括号内的问题，注意每次仅提出一个问题，且不添加额外的文字：
    # [
    # 最终目标是什么？
    # 目标是倾向于进取还是保守？
    # 决策场景是什么？
    # ]

    temporary = input("\n最终目标是什么？\n")

    #保存上一次的最终目标
    if save_target == False:
        ultimate_goal = temporary
        # print(ultimate_goal)
        save_target = True

    # 步骤五（简称：重申）
    # 以 Markdown 代码输出：步骤三中优化后的回答。
    print(f"{ask_intent}\n")

    # 步骤六（简称：是否确定破坏主要目标）
    # 询问{忽略此文本，是否确定破坏主要目标？}。若用户回复“确定”，则返回步骤二。
    confirm = input(f"assistant: 忽略【{optimized_text}】，是否确定破坏主要目标？\n")
    if confirm != "确定":
        loop_controler = False
        break
    else:
        pyperclip.copy(input("assistant: 破坏了什么目标？\n"))

    if temporary == "最后一步":
        break
    else:
        ultimate_goal = temporary
        goal_orientation = input("\n assistant: 目标是倾向于进取还是保守？\n")
        decision_scene = input("\n assistant: 决策场景是什么？\n")

# 备份聊天记录
with open('history.txt', 'a') as f:
    # 遍历字典列表
    for message in history:
        # 创建格式化的字符串
        formatted_message = f"{message['role']}: {message['content']}\n\n"
        # 写入文件
        f.write(formatted_message)

# 步骤七（简称：显示代码）
# 以 Markdown 代码输出，显示最终目标、目标倾向、决策场景。
print(ultimate_goal)
print(goal_orientation)
print(decision_scene)
pyperclip.copy(f"最终目标：{ultimate_goal}\n\n目标倾向：{goal_orientation}\n\n决策场景：{decision_scene}")
