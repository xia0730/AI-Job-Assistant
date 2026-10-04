from ai_client import ask_ai


def generate_interview_questions():
    """
    面试题生成
    根据岗位、公司和招聘信息生成针对性面试题。
    """

    print("\n" + "=" * 45)
    print("              AI 面试题生成")
    print("=" * 45)

    position = input("请输入应聘岗位：").strip()
    company = input("请输入公司名称（可直接回车）：").strip()

    if not position:
        position = "目标岗位"

    if not company:
        company = "目标公司"

    print("\n如果有岗位招聘信息，可以粘贴在下面。")
    print("如果没有，可以直接输入 END。")
    print("输入完成后，请单独输入 END，然后按回车。")
    print("-" * 45)

    job_lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        job_lines.append(line)

    job_text = "\n".join(job_lines).strip()

    # =========================
    # 第一部分：通用面试题
    # =========================

    print("\n" + "=" * 45)
    print("              通用面试题")
    print("=" * 45)

    general_questions = [
        "1. 请做一下自我介绍。",
        "2. 为什么选择这个岗位？",
        "3. 为什么选择我们公司？",
        "4. 你认为自己的优势是什么？",
        "5. 你认为自己的不足是什么？",
        "6. 请介绍一段你比较有代表性的经历。",
        "7. 在团队合作中，你通常承担什么角色？",
        "8. 如果遇到自己不会的问题，你会怎么解决？",
        "9. 如果工作中遇到较大的压力，你会怎么处理？",
        "10. 你未来三到五年的职业规划是什么？"
    ]

    for question in general_questions:
        print(question)

    # =========================
    # 第二部分：AI 针对性面试题
    # =========================

    print("\n" + "=" * 45)
    print("           AI 针对性面试题")
    print("=" * 45)

    print("\n正在调用 Xing4.0-29B 生成面试题，请稍候...\n")

    if job_text:
        job_information = f"""
以下是该岗位的招聘信息：

--------------------
{job_text}
--------------------
"""
    else:
        job_information = """
用户没有提供具体招聘信息。
请根据岗位名称和公司信息进行合理分析，
但不要虚构该公司的具体招聘要求。
"""

    prompt = f"""
你是一名专业的招聘面试官和求职辅导专家。

候选人正在准备以下面试：

公司：{company}
岗位：{position}

{job_information}

请为候选人生成针对性较强的面试题。

【重要要求】

1. 不要重复最基础的通用问题。
2. 优先围绕岗位实际工作内容和核心能力提问。
3. 如果提供了招聘信息，要充分结合招聘信息。
4. 不得虚构招聘信息中不存在的明确要求。
5. 问题应该接近真实企业面试场景。
6. 使用中文回答。
7. 面向应届毕业生，不要默认候选人拥有多年工作经验。

请按照以下结构输出：

【一、岗位理解类问题】
生成3个问题。

【二、能力考察类问题】
生成5个问题。

【三、经历深挖类问题】
生成4个问题。
如果没有候选人的具体简历，
问题应设计成可以让候选人结合自己的经历回答，
不要虚构候选人的经历。

【四、情景模拟类问题】
生成4个真实工作场景问题。

【五、压力与挑战类问题】
生成2个问题。

【六、职业规划与岗位匹配类问题】
生成2个问题。

【七、最值得重点准备的5道题】
从上面的题目中选择最重要的5道，
并分别说明为什么面试官可能会问。

最后总结：
这个岗位面试最主要考察候选人的哪些能力。
"""

    ai_result = ask_ai(prompt)

    print(ai_result)

    print("\n" + "=" * 45)
    print("面试题生成完成。")
    print("=" * 45)


def generate_self_intro():
    """
    AI 自我介绍生成
    根据岗位、公司、教育背景、经历和个人优势生成自我介绍。
    """

    print("\n" + "=" * 45)
    print("             AI 自我介绍生成")
    print("=" * 45)

    position = input("请输入应聘岗位：").strip()
    company = input("请输入公司名称（可直接回车）：").strip()
    education = input("请输入你的教育背景：").strip()

    if not position:
        position = "目标岗位"

    if not company:
        company = "贵公司"

    if not education:
        education = "本科在读"

    # =========================
    # 多行输入个人经历
    # =========================

    print("\n请输入你的实习、项目、校园等经历。")
    print("可以输入多行，完成后单独输入 END。")
    print("-" * 45)

    experience_lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        experience_lines.append(line)

    experience = "\n".join(experience_lines).strip()

    if not experience:
        experience = "未提供具体经历"

    # =========================
    # 个人优势
    # =========================

    strengths = input("\n请输入你的个人优势：").strip()

    if not strengths:
        strengths = "学习能力、沟通能力和执行力"

    # =========================
    # 岗位招聘信息
    # =========================

    print("\n如果有岗位招聘信息，可以继续粘贴。")
    print("如果没有，直接输入 END。")
    print("输入完成后单独输入 END。")
    print("-" * 45)

    job_lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        job_lines.append(line)

    job_text = "\n".join(job_lines).strip()

    print("\n正在调用 Xing4.0-29B 生成自我介绍，请稍候...\n")

    if job_text:
        job_information = f"""
【岗位招聘信息】
{job_text}
"""
    else:
        job_information = """
【岗位招聘信息】
未提供具体招聘信息。
请主要根据岗位名称进行适度匹配，
不要虚构公司的具体要求。
"""

    prompt = f"""
你是一名专业的求职辅导顾问。

请根据下面的信息，为一名应届毕业生生成一份真实、自然、
适合面试现场口头表达的中文自我介绍。

【目标公司】
{company}

【目标岗位】
{position}

【教育背景】
{education}

【个人经历】
{experience}

【个人优势】
{strengths}

{job_information}

【生成要求】

1. 自我介绍控制在约1-2分钟的正常口语表达长度。
2. 不得虚构候选人没有提供的经历、成绩、技能、奖项或成果。
3. 不要机械地把用户输入内容全部重复一遍。
4. 要筛选与目标岗位最相关的内容重点表达。
5. 要体现“教育背景 → 实践经历 → 能力优势 → 岗位匹配”的逻辑。
6. 语言自然，不要像机器生成的文章。
7. 避免大量空泛词语。
8. 不要过度夸大候选人的能力。
9. 如果提供了招聘信息，要结合岗位要求调整表达重点。
10. 使用第一人称。
11. 适合直接在真实面试中说出来。
12. 最后自然表达希望加入公司的意愿，不要过度吹捧公司。

请直接输出：

【自我介绍】

然后再输出：

【这版自我介绍的设计思路】

用3-5点简要说明为什么重点突出这些内容。
"""

    ai_result = ask_ai(prompt)

    print("\n" + "=" * 45)
    print("          AI 自我介绍生成结果")
    print("=" * 45)

    print(ai_result)

    print("\n" + "=" * 45)
    print("自我介绍生成完成。")
    print("=" * 45)