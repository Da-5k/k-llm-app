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
    
    # 新しい構造の場合
    if 'basic_info' in couple_info:
        basic_info = couple_info.get('basic_info', {})
        wedding_info = couple_info.get('wedding_info', {})
        relationship = couple_info.get('relationship', {})
        values_future = couple_info.get('values_and_future', {})
        family = couple_info.get('family', {})
        daily_life = couple_info.get('daily_life', {})
        
        groom = basic_info.get('groom', {})
        bride = basic_info.get('bride', {})
        common = basic_info.get('common', {})
        meeting = relationship.get('meeting', {})
        dating = relationship.get('dating', {})
        proposal = relationship.get('proposal', {})
        wedding = relationship.get('wedding', {})
        
        profile = f"""
新郎: {groom.get('name', '')} (ニックネーム: {groom.get('nickname', '')})
年齢: {groom.get('age', '')}歳
出身: {groom.get('birthplace', '')}
職業: {groom.get('job', '')}
性格: {groom.get('personality', '')}
趣味: {', '.join(groom.get('hobbies', []))}

新婦: {bride.get('name', '')} (ニックネーム: {bride.get('nickname', '')})
年齢: {bride.get('age', '')}歳
出身: {bride.get('birthplace', '')}
職業: {bride.get('job', '')}
性格: {bride.get('personality', '')}
趣味: {', '.join(bride.get('hobbies', []))}

【結婚式情報】
日付: {wedding_info.get('date', '')}
会場: {wedding_info.get('venue', '')}

【二人の関係】
お互いの呼び方: {', '.join(common.get('call_each_other', []))}
共通の趣味: {', '.join(common.get('shared_hobbies', []))}

【出会い】
場所: {meeting.get('place', '')}
きっかけ: {meeting.get('trigger', '')}
第一印象:
- 新郎から見た新婦: {meeting.get('first_impression', {}).get('groom_about_bride', '')}
- 新婦から見た新郎: {meeting.get('first_impression', {}).get('bride_about_groom', '')}
仲良くなったきっかけ: {meeting.get('getting_closer', '')}

【交際】
デートスタイル: {dating.get('lifestyle', '')}
恒例イベント: {dating.get('events', '')}
結婚を意識した瞬間: {dating.get('marriage_moment', '')}

【プロポーズ】
場所: {proposal.get('location', '')}
内容: {proposal.get('surprise', '')}
プロポーズの言葉: {proposal.get('words', '')}
反応: {proposal.get('reaction', '')}

【結婚式】
コンセプト: {wedding.get('concept', '')}
準備: {wedding.get('preparation', '')}

【価値観・将来】
関係性: {values_future.get('relationship_dynamics', '')}
家庭像: {values_future.get('family_vision', '')}

【家族】
新郎の家族: {family.get('groom', '')}
新婦の家族: {family.get('bride', '')}

【日常生活】
過ごし方: {daily_life.get('routine', '')}
"""
    else:
        # 旧構造との互換性維持
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
あなたは結婚式の披露宴で質問に答える新郎新婦です。
以下の情報を基に、新郎新婦として直接回答してください。

新郎新婦の情報:
{couple_profile}

回答する際の注意事項:
- 新郎新婦の一人称で回答する（「私たち」「僕」「私」を使用）
- 自然で親しみやすい口調で答える
- 感謝の気持ちを込める
- 具体的なエピソードがあれば含める
- 回答は150-200文字程度にまとめる
- 質問の内容に応じて、新郎または新婦、または二人で答えるかを判断する
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
    st.markdown('<h1 class="main-header">DAIGO & RIN AI</h1>', unsafe_allow_html=True)
    
    # サイドバーで新郎新婦の情報を表示
    with st.sidebar:
        st.header("新郎新婦の情報")
        
        if st.session_state.couple_info:
            # 新しい構造に対応した基本情報の表示
            if 'basic_info' in st.session_state.couple_info:
                basic_info = st.session_state.couple_info['basic_info']
                if 'groom' in basic_info:
                    st.write(f"**新郎:** {basic_info['groom'].get('name', '')}")
                if 'bride' in basic_info:
                    st.write(f"**新婦:** {basic_info['bride'].get('name', '')}")
                
                # 結婚式情報の表示
                if 'wedding_info' in st.session_state.couple_info:
                    wedding_info = st.session_state.couple_info['wedding_info']
                    if wedding_info.get('date'):
                        st.write(f"**結婚式:** {wedding_info['date']}")
                    if wedding_info.get('venue'):
                        st.write(f"**会場:** {wedding_info['venue']}")
            
            # 旧形式との互換性維持
            if 'groom_name' in st.session_state.couple_info:
                st.write(f"**新郎:** {st.session_state.couple_info.get('groom_name', '')}")
            if 'bride_name' in st.session_state.couple_info:
                st.write(f"**新婦:** {st.session_state.couple_info.get('bride_name', '')}")
            if 'wedding_date' in st.session_state.couple_info:
                st.write(f"**結婚式:** {st.session_state.couple_info.get('wedding_date', '')}")
            if 'venue' in st.session_state.couple_info:
                st.write(f"**会場:** {st.session_state.couple_info.get('venue', '')}")
        else:
            st.warning("couple_info.jsonから情報を読み込めませんでした。")
        
        if st.button("情報を再読み込み"):
            st.session_state.couple_info = load_couple_info()
            st.success("情報を再読み込みしました！")
    
    # メインエリア
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 新郎新婦の情報表示
        couple_info = st.session_state.couple_info
        display_info = False
        
        # 新しい構造の場合
        if 'basic_info' in couple_info:
            basic_info = couple_info['basic_info']
            if basic_info.get('groom', {}).get('name') or basic_info.get('bride', {}).get('name'):
                display_info = True
                st.markdown('<div class="couple-info">', unsafe_allow_html=True)
                st.subheader("新郎新婦のご紹介")
                
                if basic_info.get('groom', {}).get('name'):
                    st.write(f"**新郎:** {basic_info['groom']['name']} 様")
                if basic_info.get('bride', {}).get('name'):
                    st.write(f"**新婦:** {basic_info['bride']['name']} 様")
                
                # 結婚式情報の表示
                if 'wedding_info' in couple_info:
                    wedding_info = couple_info['wedding_info']
                    if wedding_info.get('date'):
                        st.write(f"**結婚式:** {wedding_info['date']}")
                    if wedding_info.get('venue'):
                        st.write(f"**会場:** {wedding_info['venue']}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # 旧構造との互換性維持
        elif couple_info.get('groom_name') or couple_info.get('bride_name'):
            display_info = True
            st.markdown('<div class="couple-info">', unsafe_allow_html=True)
            st.subheader("新郎新婦のご紹介")
            
            if couple_info.get('groom_name'):
                st.write(f"**新郎:** {couple_info['groom_name']} 様")
            if couple_info.get('bride_name'):
                st.write(f"**新婦:** {couple_info['bride_name']} 様")
            if couple_info.get('wedding_date'):
                st.write(f"**結婚式:** {couple_info['wedding_date']}")
            if couple_info.get('venue'):
                st.write(f"**会場:** {couple_info['venue']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 質問入力フォーム
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.subheader("DAIGO & RINへの質問")
        question = st.text_area(
            "DAIGOとRINに聞きたいことがありましたら、こちらにご記入ください：",
            placeholder="例：どこで出会ったのですか？\n例：お互いの第一印象は？\n例：結婚を決めたきっかけは？"
        )
        
        if st.button("AIに質問する", key="ask_question"):
            if question.strip():
                if st.session_state.couple_info:
                    with st.spinner("回答を準備しています..."):
                        couple_profile = create_couple_profile()
                        answer = get_ai_response(question, couple_profile)
                        
                        # 回答を表示
                        st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                        st.subheader("回答")
                        st.write(answer)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.success("回答が生成されました！")
                else:
                    st.warning("新郎新婦の情報を読み込めませんでした。couple_info.jsonファイルを確認してください。")
            else:
                st.warning("質問を入力してください。")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("使い方")
        st.info("""
        1. 左のサイドバーで新郎新婦の情報を確認
        2. 質問を入力してAIに聞く
        3. AIがDAIGOとRINの代わりに答えてくれます
        """)
        
        st.subheader("質問例")
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