import os
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows 기준: 맑은 고딕)
try:
    rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

# ============================================================
# 1. 사용자 입력 (CLI)
# ============================================================
def get_user_input():
    print("=" * 50)
    print("  Clark 지게차 브랜드 생성 CLI 프로그램")
    print("=" * 50)
    brief_path = input("브리프 JSON 파일 경로를 입력하세요: ").strip()
    output_dir = input("출력 폴더 경로 (엔터=기본값 ./output): ").strip()
    if not output_dir:
        output_dir = "./output"
    return brief_path, output_dir


# ============================================================
# 2. 브리프 로드 및 필수 필드 검증
# ============================================================
def load_brief(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
    with open(path, "r", encoding="utf-8") as f:
        brief = json.load(f)
    # 필수 필드 검증
    for field in ["industry", "target", "keywords"]:
        if field not in brief:
            raise ValueError(f"필수 필드 누락: {field}")
    return brief


# ============================================================
# 3. API 키 확인
# ============================================================
def get_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("[안내] OPENAI_API_KEY 환경변수가 없습니다. 데모 모드로 실행합니다.")
    return key


# ============================================================
# 4. 브랜드 요소 생성 (LLM 또는 데모)
# ============================================================
def generate_brand_elements(brief, api_key):
    if api_key:
        try:
            return call_llm_api(brief, api_key)
        except Exception as e:
            print(f"[에러] LLM 호출 실패: {e} → 데모 데이터로 대체합니다.")
    return demo_brand_elements(brief)


def call_llm_api(brief, api_key):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    prompt = f"""
    다음 브랜드 정보를 바탕으로 결과를 JSON으로 생성하세요.
    업종: {brief['industry']}
    타겟: {brief['target']}
    키워드: {', '.join(brief['keywords'])}
    톤앤매너: {brief.get('tone', '전문적')}

    출력 형식(JSON):
    {{
      "namings": [{{"name":"...", "meaning":"..."}}],  // 3~5개
      "slogans": ["...", "...", "..."],
      "story": "300자 내외",
      "colors": {{"main":"#RRGGBB", "subs":["#RRGGBB","#RRGGBB"]}}
    }}
    """
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(res.choices[0].message.content)


def demo_brand_elements(brief):
    """API 없이도 결과를 볼 수 있는 데모 데이터"""
    return {
        "namings": [
            {"name": "진주 클라크 마스터", "meaning": "지역명과 전문가 이미지를 결합해 신뢰도 강조"},
            {"name": "튼튼리프트 진주", "meaning": "고장 없는 내구성을 직관적으로 표현"},
            {"name": "클라크 프라임 경남", "meaning": "최고 품질의 프리미엄 서비스 이미지"},
            {"name": "강철현장 클라크", "meaning": "현장의 든든함과 강인함 강조"}
        ],
        "slogans": [
            "멈추지 않는 비즈니스, 클라크 지게차가 답입니다.",
            "품질은 높게, 가격은 가볍게. 진주 물류의 든든한 파트너.",
            "100년의 기술력, 진주 현장에서 증명합니다."
        ],
        "story": (
            "물류의 심장은 지게차입니다. 잦은 고장과 유지비는 현장의 가장 큰 고민이죠. "
            "우리는 세계 최초로 지게차를 만든 Clark의 100년 기술력을 진주 지역에 공급합니다. "
            "한 번 사면 평생 가는 튼튼함과 거품 없는 합리적 가격으로, "
            "사장님의 현장이 1분도 멈추지 않도록 가장 가까운 곳에서 지원합니다."
        ),
        "colors": {"main": "#2E7D32", "subs": ["#424242", "#FFD600"]}
    }


# ============================================================
# 5. 컬러 팔레트 시각화 → PNG 저장
# ============================================================
def save_color_palette(colors, output_dir):
    all_colors = [colors["main"]] + colors["subs"]
    labels = ["MAIN"] + [f"SUB {i+1}" for i in range(len(colors["subs"]))]

    fig, ax = plt.subplots(figsize=(len(all_colors) * 2, 3))
    for i, (hex_code, label) in enumerate(zip(all_colors, labels)):
        ax.add_patch(Rectangle((i, 0), 1, 1, color=hex_code))
        ax.text(i + 0.5, -0.15, f"{label}\n{hex_code}",
                ha="center", va="top", fontsize=10)
    ax.set_xlim(0, len(all_colors))
    ax.set_ylim(-0.4, 1)
    ax.axis("off")
    ax.set_title("Clark 지게차 브랜드 컬러 팔레트", fontsize=14, pad=15)

    path = os.path.join(output_dir, "palette.png")
    plt.savefig(path, bbox_inches="tight", dpi=120)
    plt.close()
    print(f"[저장] 컬러 팔레트: {path}")


# ============================================================
# 6. 로고 생성 (DALL-E 또는 데모 이미지)
# ============================================================
def generate_logos(brief, colors, api_key, output_dir):
    img_dir = os.path.join(output_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    if api_key:
        try:
            call_dalle_api(brief, api_key, img_dir)
            return
        except Exception as e:
            print(f"[에러] 로고 생성 실패: {e} → 데모 로고로 대체합니다.")
    demo_logos(colors, img_dir)


def call_dalle_api(brief, api_key, img_dir):
    import requests
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    prompt = (f"Professional minimalist logo for a forklift dealership, "
              f"strong forklift silhouette with shield, "
              f"forest green and industrial grey, white background, vector style")
    for i in range(2):
        res = client.images.generate(model="dall-e-3", prompt=prompt,
                                      size="1024x1024", n=1)
        url = res.data[0].url
        img = requests.get(url).content
        path = os.path.join(img_dir, f"logo_{i+1}.png")
        with open(path, "wb") as f:
            f.write(img)
        print(f"[저장] 로고: {path}")


def demo_logos(colors, img_dir):
    """PIL로 간단한 로고 플레이스홀더 생성"""
    from PIL import Image, ImageDraw
    for i in range(2):
        img = Image.new("RGB", (400, 400), "white")
        draw = ImageDraw.Draw(img)
        # 방패 모양 배경
        draw.polygon([(200, 40), (340, 100), (340, 240),
                      (200, 360), (60, 240), (60, 100)],
                     fill=colors["main"])
        # 지게차 느낌의 사각형(포크)
        draw.rectangle([150, 160, 170, 260], fill=colors["subs"][1])
        draw.rectangle([170, 240, 260, 260], fill=colors["subs"][1])
        draw.text((130, 300), f"CLARK {i+1}", fill=colors["subs"][0])
        path = os.path.join(img_dir, f"logo_{i+1}.png")
        img.save(path)
        print(f"[저장] 로고(데모): {path}")


# ============================================================
# 7. 결과 저장
# ============================================================
def save_result(brief, elements, output_dir):
    result = {"brief": brief, "brand": elements}
    path = os.path.join(output_dir, "brand_result.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[저장] 텍스트 결과: {path}")


# ============================================================
# 메인 흐름
# ============================================================
def main():
    try:
        brief_path, output_dir = get_user_input()
        os.makedirs(output_dir, exist_ok=True)

        brief = load_brief(brief_path)
        print("\n[1/4] 브리프 로드 완료 ✅")

        api_key = get_api_key()
        elements = generate_brand_elements(brief, api_key)
        print("[2/4] 브랜드 요소 생성 완료 ✅")

        save_color_palette(elements["colors"], output_dir)
        print("[3/4] 컬러 팔레트 생성 완료 ✅")

        generate_logos(brief, elements["colors"], api_key, output_dir)
        save_result(brief, elements, output_dir)
        print("[4/4] 전체 완료! 🎉")
        print(f"\n결과물은 '{output_dir}' 폴더를 확인하세요.")

    except Exception as e:
        print(f"[치명적 에러] {e}")


if __name__ == "__main__":
    main()