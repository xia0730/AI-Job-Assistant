from ai_client import ask_ai
from database import save_resume


def analyze_resume():
    print("\n==============================")
    print("        简历分析")
    print("==============================")

    print("请粘贴你的简历内容。")
    print("输入完成后，请单独输入 END，然后按回车。")
    print("--------------------------------")

    resume_text = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        resume_text.append(line)

    # =========================
    # 整理简历内容
    # =========================

    resume = "\n".join(resume_text).strip()

    if not resume:
        print("\n没有检测到简历内容。")
        return

    # =========================
    # 保存简历到数据库
    # =========================

    save_choice = input("\n是否保存这份简历？(y/n)：").strip().lower()

    if save_choice == "y":
        resume_name = input("请输入简历名称：").strip()

        if not resume_name:
            resume_name = "我的简历"

        save_resume(resume_name, resume)

        print(f"\n✓ 简历“{resume_name}”已保存到数据库。")

    # =========================
    # 第一部分：Python 基础分析
    # =========================

    print("\n==============================")
    print("        简历基础分析结果")
    print("==============================")

    print("\n【1. 内容长度】")
    print(f"简历字数：{len(resume)}")

    print("\n【2. 关键词检查】")

    keywords = [
        "教育经历",
        "实习经历",
        "项目经历",
        "校园经历",
        "技能",
        "自我评价"
    ]

    found = []
    missing = []

    for keyword in keywords:
        if keyword in resume:
            found.append(keyword)
        else:
            missing.append(keyword)

    if found:
        print("已包含：")
        for item in found:
            print(f"  ✓ {item}")

    if missing:
        print("建议关注：")
        for item in missing:
            print(f"  - {item}")

    print("\n【3. 基础优化建议】")

    basic_suggestions = []

    if len(resume) < 300:
        basic_suggestions.append(
            "简历内容偏少，可以进一步检查项目、实习或校园经历是否表达充分。"
        )

    if len(resume) > 2000:
        basic_suggestions.append(
            "简历内容较多，可以考虑适当精简，突出与目标岗位相关的经历。"
        )

    if "实习经历" not in resume:
        basic_suggestions.append(
            "未检测到“实习经历”标题，请检查简历是否包含相关实践经历。"
        )

    if "项目经历" not in resume:
        basic_suggestions.append(
            "未检测到“项目经历”标题，请检查项目经历是否得到充分展示。"
        )

    if "技能" not in resume:
        basic_suggestions.append(
            "未检测到“技能”相关标题，可以考虑突出专业软件、工具或技术能力。"
        )

    if basic_suggestions:
        for suggestion in basic_suggestions:
            print(f"  - {suggestion}")
    else:
        print("  ✓ 基础结构较完整。")

    # =========================
    # 第二部分：Xing4.0 AI 深度分析
    # =========================

    print("\n==============================")
    print("        AI 深度分析")
    print("==============================")

    print("\n正在调用 Xing4.0-29B 分析简历，请稍候...\n")

    prompt = f"""
你是一名专业的招聘顾问和简历优化专家。

现在请认真分析下面这份候选人简历。

【重要要求】
1. 必须严格依据候选人提供的简历内容进行分析。
2. 不得虚构候选人不存在的经历、成绩、技能或成果。
3. 不要仅仅给出空泛评价，要指出具体问题。
4. 优化建议应当具体、可执行。
5. 使用中文回答。
6. 输出结构清晰，适合求职者直接阅读。

请按照以下结构进行分析：

【一、简历整体评价】
分析简历整体完整度、清晰度和竞争力。

【二、教育背景分析】
分析教育背景中值得突出的内容，以及表达上存在的问题。

【三、实习经历分析】
分析实习经历的价值、具体程度和可以优化的地方。
如果简历没有实习经历，请明确说明，不得自行编造。

【四、项目经历分析】
分析项目经历是否能够体现候选人的实际能力，
并指出哪些内容值得进一步量化或具体化。

【五、校园经历与综合能力】
分析候选人的沟通、协作、组织、执行等能力体现。

【六、专业技能分析】
总结简历中已经体现出的技能，
并指出技能描述是否清晰。

【七、核心优势】
总结候选人最值得向招聘方展示的3-5项优势，
每一项说明判断依据。

【八、主要问题】
指出当前简历中最需要解决的问题。

【九、具体修改建议】
按照重要程度给出具体、可执行的修改建议。

【十、适合重点尝试的岗位方向】
只能根据这份简历已经体现出的经历和能力进行判断，
给出若干可以考虑的岗位方向，并说明原因。

以下是候选人的简历：

--------------------
{resume}
--------------------
"""

    ai_result = ask_ai(prompt)

    print(ai_result)

    print("\n==============================")
    print("简历分析完成。")
    print("==============================")