import streamlit as st

from ai_client import ask_ai
from database import (
    init_database,
    save_resume,
    get_resumes,
    get_resume_by_id,
    save_job,
    get_jobs,
    get_job_by_id
)


# ==========================================
# 页面基础设置
# ==========================================

st.set_page_config(
    page_title="AI 智能求职助手",
    page_icon="💼",
    layout="wide"
)


# ==========================================
# 初始化数据库
# ==========================================

init_database()


# ==========================================
# 通用 AI 调用函数
# ==========================================

def run_ai(prompt, task_name="AI 分析"):
    """
    调用 Xing4.0-29B，并在网页中显示等待状态。
    """

    try:
        with st.spinner(
            f"正在调用 Xing4.0-29B 进行{task_name}，请稍候..."
        ):
            result = ask_ai(prompt)

        if not result:
            st.error("AI 没有返回有效内容。")
            return None

        if result.startswith("AI调用失败"):
            st.error(result)
            return None

        return result

    except Exception as e:
        st.error(f"调用 AI 时出现错误：{e}")
        return None


# ==========================================
# 数据库辅助函数
# ==========================================

def get_resume_options():
    """
    获取数据库中的简历，并转换为：
    {显示名称: 简历记录}
    """

    resumes = get_resumes()

    options = {}

    for resume in resumes:
        resume_id = resume[0]
        resume_name = resume[1]

        display_name = f"{resume_name}（ID：{resume_id}）"

        options[display_name] = resume

    return options


def get_job_options():
    """
    获取数据库中的岗位，并转换为：
    {显示名称: 岗位记录}
    """

    jobs = get_jobs()

    options = {}

    for job in jobs:
        job_id = job[0]
        company = job[1]
        position = job[2]

        display_name = (
            f"{company} - {position}（ID：{job_id}）"
        )

        options[display_name] = job

    return options


# ==========================================
# 页面标题
# ==========================================

st.title("💼 AI 智能求职助手")

st.caption(
    "基于 Xing4.0-29B 的智能求职分析系统"
)

st.divider()


# ==========================================
# 左侧功能导航
# ==========================================

st.sidebar.title("功能导航")

page = st.sidebar.radio(
    "请选择功能",
    [
        "首页",
        "简历分析",
        "岗位分析",
        "简历 × 岗位匹配",
        "面试题生成",
        "自我介绍生成"
    ]
)


# ==========================================
# 首页
# ==========================================

if page == "首页":

    st.header("欢迎使用 AI 智能求职助手")

    st.write(
        """
        本系统面向求职者提供 AI 辅助求职分析功能，
        通过大语言模型帮助用户进行简历分析、
        岗位分析、岗位匹配和面试准备。
        """
    )

    st.subheader("主要功能")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            """
            📄 **简历分析**

            分析简历内容、优势、
            不足和优化方向。

            支持将简历保存到 SQLite 数据库。
            """
        )

    with col2:
        st.info(
            """
            💼 **岗位分析**

            分析岗位职责、能力要求、
            岗位特点和面试重点。

            支持保存目标岗位。
            """
        )

    with col3:
        st.info(
            """
            🎯 **简历 × 岗位匹配**

            综合分析个人简历与
            目标岗位之间的匹配程度。

            支持直接选择数据库记录。
            """
        )

    col4, col5 = st.columns(2)

    with col4:
        st.success(
            """
            💬 **面试题生成**

            根据公司、岗位和招聘要求
            生成针对性面试问题。
            """
        )

    with col5:
        st.success(
            """
            👤 **自我介绍生成**

            根据个人经历和目标岗位
            生成针对性自我介绍。
            """
        )

    st.divider()

    st.subheader("系统信息")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "AI 模型",
            "Xing4.0-29B"
        )

    with col2:
        st.metric(
            "数据库",
            "SQLite"
        )

    with col3:
        st.metric(
            "Web 框架",
            "Streamlit"
        )


# ==========================================
# 简历分析
# ==========================================

elif page == "简历分析":

    st.header("📄 简历分析")

    st.write(
        "输入你的简历内容，AI 将帮助你分析优势、问题和优化方向。"
    )

    st.subheader("1. 输入简历")

    resume_name = st.text_input(
        "简历名称",
        placeholder="例如：我的通用简历"
    )

    resume_text = st.text_area(
        "请输入简历内容",
        height=350,
        placeholder="请在这里粘贴你的简历……"
    )

    save_resume_option = st.checkbox(
        "将这份简历保存到 SQLite 数据库"
    )

    if st.button(
        "开始分析",
        type="primary",
        use_container_width=True
    ):

        if not resume_text.strip():

            st.warning(
                "请先输入简历内容。"
            )

        elif (
            save_resume_option
            and not resume_name.strip()
        ):

            st.warning(
                "你选择了保存简历，请填写简历名称。"
            )

        else:

            # ==================================
            # 保存简历
            # ==================================

            if save_resume_option:

                try:
                    save_resume(
                        resume_name.strip(),
                        resume_text.strip()
                    )

                    st.success(
                        f"简历「{resume_name.strip()}」已保存到数据库。"
                    )

                except Exception as e:

                    st.error(
                        f"保存简历失败：{e}"
                    )

                    st.stop()

            # ==================================
            # AI Prompt
            # ==================================

            prompt = f"""
你是一名专业的校园招聘顾问、简历优化专家和面试辅导专家。

请认真分析下面这份应届毕业生简历。

【重要要求】

1. 必须严格依据简历中的真实内容进行分析。
2. 不得虚构候选人不存在的经历、成绩、技能、证书或成果。
3. 如果某项能力简历中没有体现，请明确说明“简历中暂未体现”。
4. 不要只进行表面评价，要分析简历对招聘方的实际吸引力。
5. 修改建议必须具体、可执行。
6. 面向应届毕业生进行评价。
7. 使用中文回答。
8. 输出结构清晰。

请按照以下结构进行分析：

【一、简历整体评价】

评价这份简历目前的整体水平，
并说明最突出的特点。

【二、主要优势】

总结3-5项最值得保留和强化的优势。

每一项说明：
候选人具有什么 →
简历中的依据 →
为什么具有求职价值。

【三、主要问题】

分析简历目前存在的问题，包括但不限于：

- 内容是否具体
- 经历是否有说服力
- 是否突出个人贡献
- 是否体现成果
- 技能描述是否合理
- 是否存在表达重复
- 是否存在重点不突出的问题

【四、经历分析】

分别分析：

- 教育背景
- 实习/实践经历
- 项目经历
- 校园经历
- 技能
- 个人优势

没有对应内容时，请说明简历中暂未体现。

【五、简历修改建议】

给出具体的修改建议。

请指出：

- 哪些内容应该重点突出
- 哪些描述应该进一步具体化
- 哪些内容可以精简
- 哪些能力应该放到更明显的位置
- 如何提高简历与招聘岗位的匹配能力

不得帮助候选人编造不存在的经历。

【六、面试官可能追问的内容】

根据这份简历，
预测8个面试官最可能进一步追问的问题。

问题尽量结合简历中的真实经历。

【七、综合建议】

总结候选人目前最值得强化的三个方向。

==============================
候选人简历
==============================

{resume_text}

==============================
"""

            result = run_ai(
                prompt,
                "简历分析"
            )

            if result:

                st.success(
                    "简历分析完成。"
                )

                st.subheader(
                    "🤖 AI 简历分析结果"
                )

                st.markdown(result)


# ==========================================
# 岗位分析
# ==========================================

elif page == "岗位分析":

    st.header("💼 岗位分析")

    st.write(
        "粘贴目标岗位招聘信息，AI 将分析岗位核心要求和面试重点。"
    )

    st.subheader("1. 输入岗位")

    company = st.text_input(
        "公司名称",
        placeholder="例如：深信服科技"
    )

    position = st.text_input(
        "岗位名称",
        placeholder="例如：客户经理"
    )

    job_text = st.text_area(
        "请输入岗位招聘信息",
        height=350,
        placeholder="请在这里粘贴岗位 JD……"
    )

    save_job_option = st.checkbox(
        "将这个岗位保存到 SQLite 数据库"
    )

    if st.button(
        "开始分析",
        type="primary",
        use_container_width=True
    ):

        if not job_text.strip():

            st.warning(
                "请先输入岗位招聘信息。"
            )

        elif (
            save_job_option
            and not position.strip()
        ):

            st.warning(
                "你选择了保存岗位，请填写岗位名称。"
            )

        else:

            # ==================================
            # 保存岗位
            # ==================================

            if save_job_option:

                company_name = (
                    company.strip()
                    if company.strip()
                    else "未填写公司"
                )

                try:

                    save_job(
                        company_name,
                        position.strip(),
                        job_text.strip()
                    )

                    st.success(
                        f"岗位「{company_name} - {position.strip()}」"
                        "已保存到数据库。"
                    )

                except Exception as e:

                    st.error(
                        f"保存岗位失败：{e}"
                    )

                    st.stop()

            # ==================================
            # AI Prompt
            # ==================================

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

提炼这个岗位最主要的工作内容，
并按照重要程度进行说明。

【二、硬性要求】

提取学历、专业、技能、工作经验、
证书等明确要求。

没有明确说明的内容不要自行补充。

【三、核心能力要求】

总结招聘方最看重的能力，
并说明判断依据。

【四、岗位关键词】

提取5-10个最值得求职者关注的关键词，
并解释其含义。

【五、岗位类型与工作特点】

判断该岗位偏向销售、市场、技术、
运营、管理、项目、客户服务
或其他哪些方向，并说明理由。

【六、招聘方可能重点考察的内容】

分析面试过程中招聘方
最可能重点考察哪些方面。

【七、可能出现的面试问题】

根据这份岗位招聘信息
生成10个针对性较强的面试问题。

不要只生成通用面试题。

【八、面试准备建议】

告诉求职者应该重点准备
哪些知识、经历和案例。

【九、岗位潜在难点】

分析实际从事这个岗位可能遇到的
压力、挑战或能力门槛。

【十、岗位总结】

用简洁的语言总结：

这个岗位主要是做什么的、
最需要什么样的人、
求职者在面试前最应该准备什么。

==============================
岗位招聘信息
==============================

{job_text}

==============================
"""

            result = run_ai(
                prompt,
                "岗位分析"
            )

            if result:

                st.success(
                    "岗位分析完成。"
                )

                st.subheader(
                    "🤖 AI 岗位分析结果"
                )

                st.markdown(result)


# ==========================================
# 简历 × 岗位匹配
# ==========================================

elif page == "简历 × 岗位匹配":

    st.header(
        "🎯 简历 × 岗位智能匹配"
    )

    st.write(
        "可以直接选择数据库中保存的简历和岗位，"
        "也可以手动输入。"
    )

    st.divider()

    # ======================================
    # 简历来源
    # ======================================

    st.subheader("1. 选择简历")

    resume_source = st.radio(
        "简历来源",
        [
            "数据库已有简历",
            "手动输入"
        ],
        horizontal=True,
        key="resume_source"
    )

    resume_text = ""

    if resume_source == "数据库已有简历":

        resume_options = get_resume_options()

        if not resume_options:

            st.warning(
                "数据库中暂时没有保存的简历，"
                "请先在「简历分析」页面保存简历，"
                "或者选择「手动输入」。"
            )

        else:

            selected_resume_name = st.selectbox(
                "选择数据库中的简历",
                list(resume_options.keys())
            )

            selected_resume = (
                resume_options[
                    selected_resume_name
                ]
            )

            resume_id = selected_resume[0]

            full_resume = get_resume_by_id(
                resume_id
            )

            if full_resume:

                resume_text = full_resume[2]

                with st.expander(
                    "查看已选择的简历内容"
                ):

                    st.text(
                        resume_text
                    )

    else:

        resume_text = st.text_area(
            "请输入简历内容",
            height=300,
            placeholder="请粘贴简历……"
        )

    st.divider()

    # ======================================
    # 岗位来源
    # ======================================

    st.subheader("2. 选择目标岗位")

    job_source = st.radio(
        "岗位来源",
        [
            "数据库已有岗位",
            "手动输入"
        ],
        horizontal=True,
        key="job_source"
    )

    job_text = ""

    selected_company = ""
    selected_position = ""

    if job_source == "数据库已有岗位":

        job_options = get_job_options()

        if not job_options:

            st.warning(
                "数据库中暂时没有保存的岗位，"
                "请先在「岗位分析」页面保存岗位，"
                "或者选择「手动输入」。"
            )

        else:

            selected_job_name = st.selectbox(
                "选择数据库中的岗位",
                list(job_options.keys())
            )

            selected_job = (
                job_options[
                    selected_job_name
                ]
            )

            job_id = selected_job[0]

            full_job = get_job_by_id(
                job_id
            )

            if full_job:

                selected_company = (
                    full_job[1]
                )

                selected_position = (
                    full_job[2]
                )

                job_text = (
                    full_job[3]
                )

                st.info(
                    f"当前岗位："
                    f"{selected_company} - "
                    f"{selected_position}"
                )

                with st.expander(
                    "查看已选择的岗位 JD"
                ):

                    st.text(
                        job_text
                    )

    else:

        selected_company = st.text_input(
            "公司名称（可选）",
            key="manual_match_company"
        )

        selected_position = st.text_input(
            "岗位名称（可选）",
            key="manual_match_position"
        )

        job_text = st.text_area(
            "请输入岗位招聘信息",
            height=300,
            placeholder="请粘贴岗位 JD……",
            key="manual_match_job"
        )

    st.divider()

    # ======================================
    # 开始匹配
    # ======================================

    if st.button(
        "开始匹配分析",
        type="primary",
        use_container_width=True
    ):

        if not resume_text.strip():

            st.warning(
                "请先选择或输入简历内容。"
            )

        elif not job_text.strip():

            st.warning(
                "请先选择或输入岗位招聘信息。"
            )

        else:

            prompt = f"""
你是一名专业的招聘顾问、简历评估专家和面试辅导专家。

现在需要你对一名应届毕业生的简历
和目标岗位招聘信息进行深入的匹配分析。

【重要要求】

1. 必须严格依据候选人的简历和岗位招聘信息进行分析。
2. 不得虚构候选人不存在的经历、技能、成绩、证书或成果。
3. 不得虚构招聘信息中没有明确提出的硬性要求。
4. 必须区分“已经具备的能力”和“尚未体现的能力”。
5. 简历没有体现某项能力时，应表述为“简历中暂未体现”，
   不要直接判断候选人完全不具备该能力。
6. 匹配度评分必须给出具体理由，不能随意打分。
7. 建议必须具体、可执行。
8. 面向应届毕业生进行分析。
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

必须区分：

1. 明确不匹配的地方
2. 简历中暂未体现、需要进一步确认的地方
3. 可以通过面试准备弥补的地方

【四、岗位要求对应分析】

提取岗位最重要的5-8项要求。

针对每一项说明候选人属于：

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

预测8个面试官最可能进一步追问的问题。

问题必须尽量结合候选人的真实经历。

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

三种结论中的一种，并说明理由。

【九、一句话总结】

用一句话说明：

候选人为什么适合或不适合这个岗位，
以及最大的优势和短板是什么。

==============================
候选人简历
==============================

{resume_text}

==============================
目标公司
==============================

{selected_company if selected_company else "未指定"}

==============================
目标岗位
==============================

{selected_position if selected_position else "未指定"}

==============================
目标岗位招聘信息
==============================

{job_text}

==============================
"""

            result = run_ai(
                prompt,
                "简历与岗位匹配分析"
            )

            if result:

                st.success(
                    "简历 × 岗位匹配分析完成。"
                )

                st.subheader(
                    "🤖 AI 智能匹配结果"
                )

                st.markdown(
                    result
                )


# ==========================================
# 面试题生成
# ==========================================

elif page == "面试题生成":

    st.header(
        "💬 面试题生成"
    )

    st.write(
        "填写目标公司和岗位，AI 将生成针对性面试问题。"
    )

    company = st.text_input(
        "公司名称",
        placeholder="例如：测试科技有限公司"
    )

    position = st.text_input(
        "岗位名称",
        placeholder="例如：客户经理"
    )

    job_text = st.text_area(
        "岗位招聘信息（可选）",
        height=250,
        placeholder=(
            "可以粘贴岗位 JD，"
            "提高生成结果的针对性……"
        )
    )

    if st.button(
        "生成面试题",
        type="primary",
        use_container_width=True
    ):

        if not position.strip():

            st.warning(
                "请至少填写岗位名称。"
            )

        else:

            company_text = (
                company.strip()
                if company.strip()
                else "未指定公司"
            )

            job_info = (
                job_text.strip()
                if job_text.strip()
                else "未提供具体岗位招聘信息"
            )

            prompt = f"""
你是一名专业的校园招聘面试官和面试辅导专家。

请根据下面的信息，
为一名应届毕业生生成针对性的面试问题。

【目标公司】
{company_text}

【目标岗位】
{position}

【岗位招聘信息】
{job_info}

【重要要求】

1. 面试题必须尽量结合目标岗位。
2. 如果提供了岗位招聘信息，
   必须重点依据岗位招聘信息生成问题。
3. 不得虚构公司不存在的业务或招聘要求。
4. 面向应届毕业生设计问题。
5. 不要只生成非常宽泛的通用问题。
6. 使用中文回答。
7. 输出结构清晰。

请按照以下结构生成：

【一、基础了解类】

生成3个问题，
用于了解候选人的基本情况和求职动机。

【二、岗位理解类】

生成3个问题，
考察候选人对目标岗位的理解。

【三、能力与经历类】

生成5个问题，
重点考察沟通、学习、执行、
团队协作、项目经历等能力。

【四、情景问题】

生成3个与目标岗位相关的情景题。

【五、压力与挑战类】

生成2个问题，
考察候选人面对压力、失败或冲突时的处理方式。

【六、最值得重点准备的问题】

从上述问题中选出5个最值得重点准备的问题，
并分别说明：

- 为什么可能被问
- 面试官想考察什么
- 回答时应该重点体现什么

不要直接替候选人编造回答。
"""

            result = run_ai(
                prompt,
                "面试题生成"
            )

            if result:

                st.success(
                    "面试题生成完成。"
                )

                st.subheader(
                    "🤖 AI 面试题"
                )

                st.markdown(
                    result
                )


# ==========================================
# 自我介绍生成
# ==========================================

elif page == "自我介绍生成":

    st.header(
        "👤 自我介绍生成"
    )

    st.write(
        "填写个人经历和目标岗位，"
        "AI 将生成针对性的面试自我介绍。"
    )

    company = st.text_input(
        "目标公司",
        placeholder="例如：测试科技有限公司"
    )

    position = st.text_input(
        "目标岗位",
        placeholder="例如：客户经理"
    )

    experience = st.text_area(
        "个人经历",
        height=300,
        placeholder=(
            "可以填写教育背景、实习经历、"
            "项目经历、校园经历等……"
        )
    )

    strengths = st.text_area(
        "个人优势",
        height=150,
        placeholder=(
            "例如：沟通协调、学习能力、"
            "执行力、责任心等……"
        )
    )

    if st.button(
        "生成自我介绍",
        type="primary",
        use_container_width=True
    ):

        if not experience.strip():

            st.warning(
                "请先填写个人经历。"
            )

        elif not position.strip():

            st.warning(
                "请填写目标岗位。"
            )

        else:

            company_text = (
                company.strip()
                if company.strip()
                else "未指定公司"
            )

            strengths_text = (
                strengths.strip()
                if strengths.strip()
                else "未单独提供个人优势"
            )

            prompt = f"""
你是一名专业的校园招聘面试辅导专家。

请根据候选人的真实经历，
生成一篇适合面试使用的中文自我介绍。

【目标公司】
{company_text}

【目标岗位】
{position}

【个人经历】
{experience}

【个人优势】
{strengths_text}

【重要要求】

1. 必须严格依据候选人提供的真实经历。
2. 不得虚构不存在的实习、项目、成绩、技能或成果。
3. 自我介绍需要与目标岗位形成一定联系，
   但不要生硬堆砌岗位关键词。
4. 突出候选人的学习能力、实践能力和综合能力。
5. 语言自然，适合本人在真实面试中口头表达。
6. 不要写成书面简历摘要。
7. 避免夸张和空洞表达。
8. 控制在大约1分30秒到2分钟。
9. 使用第一人称。
10. 使用中文。

请按照以下思路组织：

第一部分：
简要介绍教育背景。

第二部分：
选择最有代表性的实践、实习或项目经历。

第三部分：
结合校园经历或其他经历，
体现候选人的综合能力。

第四部分：
总结个人优势，
并自然说明为什么希望应聘这个岗位。

最后请额外给出：

【自我介绍使用建议】

用3-5条简短建议告诉候选人，
实际面试表达时应该注意什么。
"""

            result = run_ai(
                prompt,
                "自我介绍生成"
            )

            if result:

                st.success(
                    "自我介绍生成完成。"
                )

                st.subheader(
                    "🤖 AI 自我介绍"
                )

                st.markdown(
                    result
                )


# ==========================================
# 页面底部
# ==========================================

st.sidebar.divider()

st.sidebar.caption(
    "AI-Job-Assistant"
)

st.sidebar.caption(
    "Xing4.0-29B + SQLite + Streamlit"
)