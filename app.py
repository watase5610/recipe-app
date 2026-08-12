
import streamlit as st
from google import genai

st.title("🍳 冷蔵庫のおかず提案アプリ")
st.write("今ある食材を選ぶだけで、AIが今日の夕飯おかずを提案します！")

# サイドバーでAPIキー入力
api_key = st.sidebar.text_input("Gemini API Key を入力", type="password")

# 食材選択
ingredients = st.multiselect(
    "今日ある食材を選んでください（複数選択可）",
    ["牛肉", "豚肉", "鶏肉", "ひき肉", "鮭", "サバ", "卵", "豆腐", "キャベツ", "白菜", "玉ねぎ", "じゃがいも", "人参", "大根", "もやし", "茄子", "ピーマン", "キノコ類"]
)

# 料理ジャンル選択
genre = st.selectbox(
    "料理のジャンルを選んでください",
    ["指定なし", "和食", "洋食", "中華", "エスニック", "イタリアン"]
)

# その他調味料・食材
other_ingredients = st.text_input("その他使いたい食材や調味料（例：ポン酢、みそ、めんつゆ）")

if st.button("レシピを提案してもらう！"):
    if not api_key:
        st.error("左のサイドバーに Gemini API Key を入力してください。")
    elif not ingredients:
        st.warning("食材を1つ以上選んでください。")
    else:
        try:
            # スマホのコピペで混入する前後の余計な空白・改行を自動除去
            clean_api_key = api_key.strip()
            client = genai.Client(api_key=clean_api_key)
            
            # ジャンル指定のテキストを作成
            genre_text = f"【希望ジャンル】: {genre}\n" if genre != "指定なし" else ""
            
            prompt = f"""
            あなたはプロの料理研究家です。
            以下の条件に合わせて、今夜のメインおかずのレシピを3つ提案してください。

            【使える食材】: {', '.join(ingredients)}
            【その他の食材・調味料】: {other_ingredients}
            {genre_text}

            各レシピには以下の項目を含めてください：
            1. 料理名と調理時間
            2. 簡単な説明
            3. 必要な材料・分量
            4. 作り方（手順）
            5. 美味しく作るポイント
            """

            with st.spinner("AIがレシピを考えています..."):
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt,
                )
                st.success("おすすめレシピができました！")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
