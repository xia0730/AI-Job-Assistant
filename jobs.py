from ai_client import ask_ai
from database import save_job


def analyze_job():
    """岗位分析功能"""

    print("\n" + "=" * 45)
    print("              岗位分析")
    print("=" * 45)

    # =========================
    # 输入岗位招聘信息
    # =========================

    print("请粘贴岗位招聘信息。")
    print("输入完成后，请单独输入 END，然后按回车。")
    print("-" * 45)

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    job_text = "\n".join(lines).strip()

    if not job_text:
        print("\n没有检测到岗位信息，请重新输入。")
        return

    # =========================
    # 保存岗位到数据库
    # =========================

    save_choice = input("\n是否保存这份岗位信息？(y/n)：").strip().lower()

    if save_choice == "y":

        company = input("请输入公司名称：").strip()
        position = input("请输入岗位名称：").strip()

        if not company:
            company = "未填写公司"

        if not position:
            position = "未命名岗位"

        save_job(company, position, job_text)

        print(
            f"\n✓ 岗位“{company} - {position}”"
            f"已保存到数据库。"
        )

    # =========================
    # 第一部分：Python 基础分析
    # =========================

    print("\n" + "=" * 45)
    print("            岗位基础分析结果")
    print("=" * 45)

    # 1. 基础信息
    print("\n【1. 基础信息】")
    print(f"岗位信息字数：{len(job_text)} 字")

    # 2. 关键词分析
    print("\n【2. 关键词分析】")

    keywords = [
        "沟通",
        "表达",
        "销售",
        "客户",
        "市场",
        "团队",
        "管理",
        "项目",
        "数据",
        "分析",
        "学习",
        "执行",
        "责任心",
        "抗压",
        "协调",
        "商务",
        "技术",
        "产品",
        "解决方案",
        "本科",
        "硕士",
        "实习",
        "经验",
        "Python",
        "Excel",
        "CAD",
        "Revit",
        "BIM"
    ]

    found_keywords = []

    for keyword in keywords:
        if keyword.lower() in job_text.lower():
            found_keywords.append(keyword)

    if found_keywords:
        print("检测到的岗位关键词：")

        for keyword in found_keywords:
            print(f"  ✓ {keyword}")

    else:
        print("暂未检测到预设关键词。")

    # =========================
    # 3. 能力要求分析
    # =========================

    print("\n【3. 能力要求分析】")

    ability_keywords = {
        "沟通表达能力": ["沟通", "表达", "交流", "汇报"],
        "客户能力": ["客户", "销售", "商务", "市场"],
        "团队协作能力": ["团队", "协作", "协调", "合作"],
        "学习能力": ["学习", "快速学习", "适应"],
        "执行能力": ["执行", "落实", "推进"],
        "分析能力": ["分析", "数据", "研究"],
        "项目能力": ["项目", "项目管理", "项目经验"],
        "技术能力": [
            "技术",
            "Python",
            "Excel",
            "CAD",
            "Revit",
            "BIM"
        ],
        "学历要求": ["本科", "硕士", "研究生"]
    }

    found_abilities = []

    for ability, words in ability_keywords.items():

        for word in words:

            if word.lower() in job_text.lower():
                found_abilities.append(ability)
                break

    if found_abilities:

        for ability in found_abilities:
            print(f"  ✓ {ability}")

    else:
        print("暂未识别出明确的能力要求。")

    # =========================
    # 4. 岗位特点判断
    # =========================

    print("\n【4. 岗位特点判断】")

    sales_words = [
        "销售",
        "客户",
        "市场",
        "商务",
        "业绩"
    ]

    technical_words = [
        "技术",
        "开发",
        "编程",
        "Python",
        "软件",
        "系统"
    ]

    management_words = [
        "管理",
        "项目管理",
        "协调",
        "负责人",
        "团队"
    ]

    sales_count = sum(
        1
        for word in sales_words
        if word.lower() in job_text.lower()
    )

    technical_count = sum(
        1
        for word in technical_words
        if word.lower() in job_text.lower()
    )

    management_count = sum(
        1
        for word in management_words
        if word.lower() in job_text.lower()
    )

    if sales_count > 0:
        print("  → 该岗位具有一定的客户/销售/市场属性。")

    if technical_count > 0:
        print("  → 该岗位具有一定的技术属性。")

    if management_count > 0:
        print("  → 该岗位具有一定的项目/管理/协调属性。")

    if (
        sales_count == 0
        and technical_count == 0
        and management_count == 0
    ):
        print("  → 当前规则暂未识别出明显的岗位类型。")

    # =========================
    # 5. 基础面试准备建议
    # =========================

    print("\n【5. 基础面试准备建议】")

    suggestions = []

    if "沟通表达能力" in found_abilities:
        suggestions.append(
            "准备一个能够体现沟通能力的校园或实践案例。"
        )

    if "客户能力" in found_abilities:
        suggestions.append(
            "准备客户沟通、需求理解或问题解决方面的案例。"
        )

    if "团队协作能力" in found_abilities:
        suggestions.append(
            "准备一个团队合作或组织协调的具体案例。"
        )

    if "学习能力" in found_abilities:
        suggestions.append(
            "准备一个快速学习新知识或新工具的案例。"
        )

    if "项目能力" in found_abilities:
        suggestions.append(
            "准备一个完整项目经历，并说明自己的具体职责。"
        )

    if "技术能力" in found_abilities:
        suggestions.append(
            "提前梳理简历中的软件、工具和技术经历。"
        )

    if suggestions:

        for suggestion in suggestions:
            print(f"  ✓ {suggestion}")

    else:
        print("  → 建议结合岗位职责进一步准备针对性案例。")

    # =========================
    # 第二部分：Xing4.0 AI 深度分析
    # =========================

    print("\n" + "=" * 45)
    print("            AI 深度岗位分析")
    print("=" * 45)

    print("\n正在调用 Xing4.0-29B 分析岗位，请稍候...\n")

    prompt = f"""
你是一名专业的招聘顾问、职业规划顾问和面试辅导专家。

请认真分析下面这份岗位招聘信息。

【重要要求】
1. 必须严格依据提供的岗位信息分析。
2. 不得虚构招聘信息中不存在的要求。
3. 如果某项要求招聘信息没有明确说明，
   请指出“招聘信息未明确说明”。
4. 不要只重复招聘原文，要分析招聘方真正关注的能力。
5. 给出的建议必须具体、可执行。
6. 使用中文回答。
7. 输出结构清晰，适合应届毕业生阅读。

请按照以下结构进行分析：

【一、岗位核心职责】
提炼这个岗位最主要的工作内容，并按照重要程度进行说明。

【二、硬性要求】
提取学历、专业、技能、工作经验、证书等明确要求。
没有明确说明的内容不要自行补充。

【三、核心能力要求】
总结招聘方最看重的能力，并说明你的判断依据。

【四、岗位关键词】
提取5-10个最值得求职者关注的关键词，并解释其含义。

【五、岗位类型与工作特点】
判断该岗位偏向销售、市场、技术、运营、管理、
项目、客户服务或其他哪些方向，并说明理由。

【六、招聘方可能重点考察的内容】
分析面试过程中招聘方最可能重点考察哪些方面。

【七、可能出现的面试问题】
根据这份岗位招聘信息生成10个针对性较强的面试问题，
不要只生成通用面试题。

【八、面试准备建议】
告诉求职者应该重点准备哪些知识、经历和案例。

【九、岗位潜在难点】
分析实际从事这个岗位可能遇到的压力、挑战或能力门槛。

【十、岗位总结】
用简洁的语言总结：
这个岗位主要是做什么的、
最需要什么样的人、
求职者在面试前最应该准备什么。

以下是岗位招聘信息：

--------------------
{job_text}
--------------------
"""

    ai_result = ask_ai(prompt)

    print(ai_result)

    print("\n" + "=" * 45)
    print("岗位分析完成。")
    print("=" * 45)