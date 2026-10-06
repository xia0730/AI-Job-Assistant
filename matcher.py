from ai_client import ask_ai
from database import (
    get_resumes,
    get_resume_by_id,
    get_jobs,
    get_job_by_id
)


def match_resume_job():
    """
    简历 × 岗位智能匹配分析

    支持：
    1. 从数据库选择已有简历
    2. 手动粘贴新简历
    3. 从数据库选择已有岗位
    4. 手动粘贴新岗位
    5. 调用 Xing4.0-29B 进行智能匹配分析
    """

    print("\n" + "=" * 45)
    print("          简历 × 岗位智能匹配")
    print("=" * 45)

    # ==================================================
    # 第一部分：选择简历来源
    # ==================================================

    print("\n请选择简历来源：")
    print("1. 使用数据库中已保存的简历")
    print("2. 手动粘贴新简历")

    resume_choice = input("请输入选项（1/2）：").strip()

    # =========================
    # 方式1：读取数据库简历
    # =========================

    if resume_choice == "1":

        resumes = get_resumes()

        if not resumes:
            print("\n数据库中暂时没有保存的简历。")
            return

        print("\n已保存的简历：")
        print("-" * 45)

        for item in resumes:
            print(
                f"ID：{item[0]}  "
                f"名称：{item[1]}"
            )

        print("-" * 45)

        resume_id = input(
            "请输入要使用的简历 ID："
        ).strip()

        if not resume_id.isdigit():
            print("\n简历 ID 必须是数字。")
            return

        selected_resume = get_resume_by_id(
            int(resume_id)
        )

        if not selected_resume:
            print("\n没有找到对应的简历。")
            return

        resume = selected_resume[2]

        print(
            f"\n✓ 已选择简历："
            f"{selected_resume[1]}"
        )

    # =========================
    # 方式2：手动输入简历
    # =========================

    elif resume_choice == "2":

        print("\n请粘贴你的简历内容。")
        print(
            "输入完成后，请单独输入 END，"
            "然后按回车。"
        )
        print("-" * 45)

        resume_lines = []

        while True:
            line = input()

            if line.strip().upper() == "END":
                break

            resume_lines.append(line)

        resume = "\n".join(
            resume_lines
        ).strip()

        if not resume:
            print("\n没有检测到简历内容。")
            return

        print("\n✓ 已读取手动输入的简历。")

    else:
        print("\n输入有误，请输入 1 或 2。")
        return

    # ==================================================
    # 第二部分：选择岗位来源
    # ==================================================

    print("\n" + "=" * 45)
    print("              选择目标岗位")
    print("=" * 45)

    print("\n请选择岗位来源：")
    print("1. 使用数据库中已保存的岗位")
    print("2. 手动粘贴新岗位")

    job_choice = input(
        "请输入选项（1/2）："
    ).strip()

    # =========================
    # 方式1：读取数据库岗位
    # =========================

    if job_choice == "1":

        jobs = get_jobs()

        if not jobs:
            print("\n数据库中暂时没有保存的岗位。")
            return

        print("\n已保存的岗位：")
        print("-" * 45)

        for item in jobs:

            job_id = item[0]
            company = item[1]
            position = item[2]

            if not company:
                company = "未填写公司"

            print(
                f"ID：{job_id}  "
                f"公司：{company}  "
                f"岗位：{position}"
            )

        print("-" * 45)

        job_id = input(
            "请输入要使用的岗位 ID："
        ).strip()

        if not job_id.isdigit():
            print("\n岗位 ID 必须是数字。")
            return

        selected_job = get_job_by_id(
            int(job_id)
        )

        if not selected_job:
            print("\n没有找到对应的岗位。")
            return

        company = selected_job[1]
        position = selected_job[2]
        job_text = selected_job[3]

        if not company:
            company = "未填写公司"

        print(
            f"\n✓ 已选择岗位："
            f"{company} - {position}"
        )

    # =========================
    # 方式2：手动输入岗位
    # =========================

    elif job_choice == "2":

        print("\n请粘贴目标岗位招聘信息。")
        print(
            "输入完成后，请单独输入 END，"
            "然后按回车。"
        )
        print("-" * 45)

        job_lines = []

        while True:
            line = input()

            if line.strip().upper() == "END":
                break

            job_lines.append(line)

        job_text = "\n".join(
            job_lines
        ).strip()

        if not job_text:
            print("\n没有检测到岗位招聘信息。")
            return

        print("\n✓ 已读取手动输入的岗位信息。")

    else:
        print("\n输入有误，请输入 1 或 2。")
        return

    # ==================================================
    # 第三部分：AI 匹配分析
    # ==================================================

    print("\n" + "=" * 45)
    print("            AI 智能匹配分析")
    print("=" * 45)

    print(
        "\n正在调用 Xing4.0-29B "
        "进行匹配分析，请稍候...\n"
    )

    prompt = f"""
你是一名专业的招聘顾问、简历评估专家和面试辅导专家。

现在需要你对一名应届毕业生的简历和目标岗位招聘信息
进行深入的匹配分析。

【重要要求】

1. 必须严格依据候选人的简历和岗位招聘信息进行分析。
2. 不得虚构候选人不存在的经历、技能、成绩、证书或成果。
3. 不得虚构招聘信息中没有明确提出的硬性要求。
4. 必须区分“已经具备的能力”和“尚未体现的能力”。
5. 简历没有体现某项能力时，应表述为“简历中暂未体现”，
   不要直接判断候选人完全不具备该能力。
6. 匹配度评分必须给出具体理由，不能随意打分。
7. 建议必须具体、可执行。
8. 面向应届毕业生进行分析，不要按照有多年工作经验的
   社会招聘候选人标准进行评价。
9. 使用中文回答。
10. 输出结构清晰。

请按照以下结构进行分析：

【一、综合匹配度】

给出0-100分的综合匹配评分。

分别从以下几个方面进行评分：

- 教育背景匹配度
- 专业/技能匹配度
- 实习与项目经历匹配度
- 综合能力匹配度
- 岗位发展潜力

说明每项评分的理由。

【二、候选人的主要匹配优势】

总结3-5项与目标岗位最匹配的优势。

每一项必须说明：

候选人具有什么 →
简历中的依据是什么 →
为什么与岗位匹配。

【三、主要差距与风险点】

分析候选人与岗位要求之间存在的差距。

必须区分：

1. 明确不匹配的地方
2. 简历中暂未体现、需要进一步确认的地方
3. 可以通过面试准备弥补的地方

【四、岗位要求对应分析】

提取岗位最重要的5-8项要求。

针对每一项说明候选人目前属于：

- 高度匹配
- 基本匹配
- 部分匹配
- 简历暂未体现

并说明判断依据。

【五、简历针对性修改建议】

如果候选人准备投递这个岗位，
应该如何针对该岗位调整简历。

请具体指出：

- 哪些经历应该重点突出
- 哪些描述应该进一步具体化
- 哪些能力应该放在更明显的位置
- 哪些内容可以适当弱化

不得帮助候选人编造不存在的经历。

【六、面试官最可能追问的内容】

根据候选人的简历和岗位要求，
预测8个面试官最可能进一步追问的问题。

问题必须尽量结合候选人的真实经历，
不要只生成通用面试题。

【七、面试准备重点】

告诉候选人在参加这个岗位面试之前，
最应该准备哪些：

- 经历案例
- 专业知识
- 岗位知识
- 能力证明

【八、是否建议投递】

给出：

- 推荐投递
- 可以尝试
- 谨慎投递

三种结论中的一种。

然后说明理由。

注意：

不能仅仅根据匹配度数字判断，
还要考虑应届毕业生的成长潜力和岗位可培养性。

【九、一句话总结】

用一句话说明：

“候选人为什么适合/不适合这个岗位，
以及最大的优势和短板是什么。”

==============================
候选人简历
==============================

{resume}

==============================
目标岗位招聘信息
==============================

{job_text}

==============================
"""

    ai_result = ask_ai(prompt)

    print(ai_result)

    print("\n" + "=" * 45)
    print("智能匹配分析完成。")
    print("=" * 45)


if __name__ == "__main__":
    match_resume_job()