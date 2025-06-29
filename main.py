import streamlit as st
import openai
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# 環境変数を読み込み
load_dotenv()

# OpenAI APIキーを設定
openai.api_key = os.getenv('OPENAI_API_KEY')

# ページ設定
st.set_page_config(
    page_title="DAIGO & RIN AI",
    page_icon="💒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #8B4513;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .couple-info {
        background: linear-gradient(135deg, #FFE4E1, #FFF8DC);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #DAA520;
        margin: 1rem 0;
    }
    .question-box {
        background: linear-gradient(135deg, #F0F8FF, #E6E6FA);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #4169E1;
        margin: 1rem 0;
    }
    .answer-box {
        background: linear-gradient(135deg, #F5FFFA, #F0FFF0);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #32CD32;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #FFB6C1, #FFC0CB);
        color: #8B4513;
        font-weight: bold;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFC0CB, #FFB6C1);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

def load_couple_info():
    """JSONファイルから新郎新婦の情報を読み込み"""
    try:
        with open('couple_info.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("couple_info.jsonファイルが見つかりません。")
        return {}
    except json.JSONDecodeError:
        st.error("couple_info.jsonファイルの形式が正しくありません。")
        return {}

def initialize_session_state():
    """セッション状態を初期化"""
    if 'couple_info' not in st.session_state:
        st.session_state.couple_info = load_couple_info()
    
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []

def create_couple_profile():
    """新郎新婦のプロフィールを作成"""
    couple_info = st.session_state.couple_info
    
    profile = f"""
新郎: {couple_info.get('groom_name', '')}
新婦: {couple_info.get('bride_name', '')}
結婚式日: {couple_info.get('wedding_date', '')}
会場: {couple_info.get('venue', '')}

【二人の出会い】
{couple_info.get('how_they_met', '')}

【プロポーズのエピソード】
{couple_info.get('proposal_story', '')}

【趣味・特技】
{couple_info.get('hobbies', '')}

【好きなもの】
{couple_info.get('favorite_things', '')}

【将来の計画】
{couple_info.get('future_plans', '')}

【ゲストへのメッセージ】
{couple_info.get('message_to_guests', '')}
"""
    return profile

def get_ai_response(question, couple_profile):
    """OpenAI APIを使用してAIの回答を生成"""
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        system_prompt = f"""
あなたは結婚式の披露宴で新郎新婦の代わりに質問に答えるAIアシスタントです。
以下の新郎新婦の情報を基に、温かく、親しみやすく、そして感動的な回答をしてください。

新郎新婦の情報:
{couple_profile}

回答する際の注意事項:
- 敬語を使い、丁寧な言葉遣いで答える
- 新郎新婦の気持ちになって答える
- 感謝の気持ちを込める
- 具体的なエピソードがあれば含める
- 回答は200文字以内にまとめる
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"申し訳ございません。システムエラーが発生しました: {str(e)}"

def main():
    """メイン関数"""
    initialize_session_state()
    
    # ヘッダー
    st.markdown('<h1 class="main-header">💒 DAIGO & RIN AI 💒</h1>', unsafe_allow_html=True)
    
    # サイドバーで新郎新婦の情報を表示
    with st.sidebar:
        st.header("👰🤵 新郎新婦の情報")
        
        if st.session_state.couple_info:
            st.write(f"**新郎:** {st.session_state.couple_info.get('groom_name', '')}")
            st.write(f"**新婦:** {st.session_state.couple_info.get('bride_name', '')}")
            st.write(f"**結婚式:** {st.session_state.couple_info.get('wedding_date', '')}")
            st.write(f"**会場:** {st.session_state.couple_info.get('venue', '')}")
            
            with st.expander("詳細情報"):
                if st.session_state.couple_info.get('how_they_met'):
                    st.write("**出会い:**")
                    st.write(st.session_state.couple_info['how_they_met'])
                
                if st.session_state.couple_info.get('proposal_story'):
                    st.write("**プロポーズ:**")
                    st.write(st.session_state.couple_info['proposal_story'])
                
                if st.session_state.couple_info.get('hobbies'):
                    st.write("**趣味・特技:**")
                    st.write(st.session_state.couple_info['hobbies'])
                
                if st.session_state.couple_info.get('favorite_things'):
                    st.write("**好きなもの:**")
                    st.write(st.session_state.couple_info['favorite_things'])
                
                if st.session_state.couple_info.get('future_plans'):
                    st.write("**将来の計画:**")
                    st.write(st.session_state.couple_info['future_plans'])
        else:
            st.warning("couple_info.jsonから情報を読み込めませんでした。")
        
        if st.button("🔄 情報を再読み込み"):
            st.session_state.couple_info = load_couple_info()
            st.success("情報を再読み込みしました！")
    
    # メインエリア
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 新郎新婦の情報表示
        if st.session_state.couple_info.get('groom_name') or st.session_state.couple_info.get('bride_name'):
            st.markdown('<div class="couple-info">', unsafe_allow_html=True)
            st.subheader("👰🤵 新郎新婦のご紹介")
            
            if st.session_state.couple_info.get('groom_name'):
                st.write(f"**新郎:** {st.session_state.couple_info['groom_name']} 様")
            if st.session_state.couple_info.get('bride_name'):
                st.write(f"**新婦:** {st.session_state.couple_info['bride_name']} 様")
            if st.session_state.couple_info.get('wedding_date'):
                st.write(f"**結婚式:** {st.session_state.couple_info['wedding_date']}")
            if st.session_state.couple_info.get('venue'):
                st.write(f"**会場:** {st.session_state.couple_info['venue']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 質問入力フォーム
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.subheader("💭 DAIGO & RINへの質問")
        question = st.text_area(
            "DAIGOとRINに聞きたいことがありましたら、こちらにご記入ください：",
            placeholder="例：どこで出会ったのですか？\n例：お互いの第一印象は？\n例：結婚を決めたきっかけは？"
        )
        
        if st.button("🤖 AIに質問する", key="ask_question"):
            if question.strip():
                if st.session_state.couple_info:
                    with st.spinner("AIが回答を考えています..."):
                        couple_profile = create_couple_profile()
                        answer = get_ai_response(question, couple_profile)
                        
                        # 回答を表示
                        st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                        st.subheader("🤖 AIからの回答")
                        st.write(answer)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.success("回答が生成されました！")
                else:
                    st.warning("新郎新婦の情報を読み込めませんでした。couple_info.jsonファイルを確認してください。")
            else:
                st.warning("質問を入力してください。")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎉 使い方")
        st.info("""
        1. 左のサイドバーで新郎新婦の情報を確認
        2. 質問を入力してAIに聞く
        3. AIがDAIGOとRINの代わりに答えてくれます
        """)
        
        st.subheader("💡 質問例")
        st.write("""
        - どこで出会ったのですか？
        - お互いの第一印象は？
        - プロポーズはどんな感じでしたか？
        - 結婚を決めたきっかけは？
        - 好きな食べ物は何ですか？
        - 将来の夢はありますか？
        - ゲストへのメッセージ
        """)

if __name__ == "__main__":
    main()