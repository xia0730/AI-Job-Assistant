from resume import analyze_resume
from jobs import analyze_job
from interview import generate_interview_questions, generate_self_intro


def show_menu():
    print("\n" + "=" * 45)
    print("              AI 求职助手")
    print("=" * 45)
    print("1. 简历分析")
    print("2. 岗位分析")
    print("3. 面试题生成")
    print("4. 自我介绍生成")
    print("5. 退出")
    print("=" * 45)


def main():
    while True:

        show_menu()

        choice = input("请输入功能编号：").strip()

        # =========================
        # 1. 简历分析
        # =========================
        if choice == "1":
            analyze_resume()

        # =========================
        # 2. 岗位分析
        # =========================
        elif choice == "2":
            analyze_job()

        # =========================
        # 3. 面试题生成
        # =========================
        elif choice == "3":
            generate_interview_questions()

        # =========================
        # 4. 自我介绍生成
        # =========================
        elif choice == "4":
            generate_self_intro()

        # =========================
        # 5. 退出
        # =========================
        elif choice == "5":
            print("\n程序已退出。")
            break

        # =========================
        # 输入错误
        # =========================
        else:
            print("\n输入有误，请输入 1-5。")


if __name__ == "__main__":
    main()