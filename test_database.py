from database import init_database, save_resume, get_resumes


# 初始化数据库
init_database()


# 保存一份测试简历
save_resume(
    "测试简历",
    "西南交通大学土木工程专业，参与铁路斜拉桥BIM建模项目。"
)

print("测试简历保存成功。")


# 读取数据库中的简历
resumes = get_resumes()

print("\n数据库中的简历：")

for resume in resumes:
    print("------------------------------")
    print(f"ID：{resume[0]}")
    print(f"名称：{resume[1]}")
    print(f"内容：{resume[2]}")
    print(f"创建时间：{resume[3]}")