# prompt_manager.py
# 프롬프트 관리 프로그램 - STEP 1 뼈대
# prompt_manager.py
# 프롬프트 관리 프로그램 - STEP 2

# 프롬프트를 저장할 리스트 (서류철)
prompts = [
    {"title": "블로그 글쓰기", "content": "너는 전문 블로거야. 주제에 맞춰 친근한 글을 써줘."},
    {"title": "고양이 이미지", "content": "귀여운 아기 고양이가 창가에 앉아있는 사진, 따뜻한 햇살."},
    {"title": "상담사 페르소나", "content": "너는 따뜻한 상담사야. 공감하며 조언해줘."},
]
def show_menu():
    """메뉴를 화면에 보여주는 함수"""
    print("\n===== 프롬프트 관리 프로그램 =====")
    print("1. 프롬프트 전체 보기")
    print("2. 프롬프트 추가")
    print("3. 프롬프트 삭제")
    print("0. 종료")
    print("=" * 33)

def show_all_prompts():
    """저장된 프롬프트를 전부 보여주는 함수"""
    print("\n----- 저장된 프롬프트 목록 -----")

    if len(prompts) == 0:
        print("아직 저장된 프롬프트가 없어요!")
        return

    for i, p in enumerate(prompts, start=1):
        print(f"{i}. {p['title']}")
        print(f"   내용: {p['content']}")
def add_prompt():
    """새 프롬프트를 추가하는 함수"""
    print("\n----- 새 프롬프트 추가 -----")

    title = input("제목을 입력하세요: ")
    content = input("내용을 입력하세요: ")

    prompts.append({"title": title, "content": content})

    print(f"✅ '{title}' 프롬프트가 추가되었어요!")
def main():
    """프로그램의 메인 실행 흐름"""
    while True:
        show_menu()
        choice = input("원하는 작업 번호를 입력하세요: ")

        if choice == "1":
             show_all_prompts()
        elif choice == "2":
            add_prompt()
        elif choice == "3":
            print("➡️ (준비중) 삭제 기능")
        elif choice == "0":
            print("프로그램을 종료합니다. 수고하셨어요! 👋")
            break
        else:
            print("⚠️ 잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()