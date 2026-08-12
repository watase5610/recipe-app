import streamlit as st
from google import genai

# ページの設定
st.set_page_config(page_title="冷蔵庫のおかず提案", page_icon="🍳")

st.title("🍳 冷蔵庫のおかず提案アプリ")
st.write("今ある食材を選ぶだけで、AIが今日の夕飯おかずを提案します！")

# サイドバーでAPIキーを入力
api_key = st.sidebar.text_input("Gemini API Key を入力", type="password")

# 食材選択のマルチセレクト
ingredients = st.multiselect(
    "今日ある食材を選んでください（複数選択可）",
    ["豚肉", "鶏肉", "牛肉", "キャベツ", "玉ねぎ", "人参", "豆腐", "卵", "ナス", "もやし", "じゃがいも"]
)

# その他の食材入力
other_inputs = st.text_input("その他使いたい食材や調味料（例：ポン酢、みそ、めんつゆ）")

# 実行ボタン
if st.button("レシピを提案してもらう！", type="primary"):
    if not api_key:
        st.error("左側のサイドバーに Gemini API Key を入力してください。")
    elif not ingredients and not other_inputs:
        st.warning("食材を1つ以上選ぶか、自由記述に入力してください。")
    else:
        with st.spinner("AIが献立を考え中..."):
            try:
                client = genai.Client(api_key=api_key)

                # 食材リストの整理
                all_ingredients = ", ".join(ingredients)
                if other_inputs:
                    all_ingredients += f", {other_inputs}"

                prompt = f"""
あなたはプロの料理研究家です。
以下の条件で、晩御飯のメインおかずレシピを3つ提案してください。

【利用可能な食材】
{all_ingredients}

以下のフォーマットで出力してください：
### 1. [料理名]（調理時間：約◯分）
- **必要な材料・分量**:
- **作り手順**:
- **ポイント**:
---
"""
                # アカウントで利用可能なモデルを自動検索して実行
                response = None
                last_error = None
                
                for m in client.models.list():
                    actions = getattr(m, 'supported_actions', []) or []
                    if 'generateContent' in actions:
                        try:
                            response = client.models.generate_content(
                                model=m.name,
                                contents=prompt
                            )
                            if response and response.text:
                                break
                        except Exception as err:
                            last_error = err
                            continue

                if response and response.text:
                    st.success("おすすめレシピができました！")
                    st.markdown(response.text)
                else:
                    if last_error:
                        st.error(f"エラーが発生しました: {last_error}")
                    else:
                        st.error("利用可能なモデルが見つかりませんでした。APIキーを確認してください。")

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")