import streamlit as st
import openai
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import time

# 環境変数を読み込み
load_dotenv()

# OpenAI APIキーを設定
openai.api_key = os.getenv('OPENAI_API_KEY')

# ページ設定
st.set_page_config(
    page_title="Daigo & Rin AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# カスタムCSS
st.markdown("""
<style>
    /* 全体の背景を青ベースに */
    .stApp {
        background: linear-gradient(135deg, #1E3A8A, #3B82F6);
        min-height: 100vh;
    }
    
    /* メインコンテンツエリアの背景を透明に変更 */
    .main .block-container {
        background: transparent;
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 1rem;
        max-width: 100%;
    }
    
    /* 青い背景の文字を白に */
    .main {
        color: white;
    }
    
    .stMarkdown, .stWrite, .stText, p, div {
        color: white !important;
    }
    
    /* スマホ対応: 小さい画面での調整 */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
            margin: 0.5rem;
            border-radius: 10px;
        }
        
        .main-header {
            font-size: 2rem !important;
            margin-bottom: 1rem !important;
        }
        
        .couple-info, .question-box, .answer-box {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
        }
        
        .stButton > button {
            width: 100%;
            padding: 0.75rem 1rem !important;
            font-size: 1rem;
        }
        
        .stTextArea textarea {
            min-height: 100px !important;
        }
    }
    
    /* サイドバーのスタイル */
    .css-1d391kg {
        background: #3B82F6;
    }
    
    .css-1d391kg .element-container {
        color: white;
    }
    
    /* スマホでのサイドバー調整 */
    @media (max-width: 768px) {
        .css-1d391kg {
            padding: 1rem 0.5rem;
        }
    }
    
    /* ヘッダーのスタイル */
    .main-header {
        text-align: center;
        color: white !important;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        line-height: 1.2;
    }
    
    /* セクションタイトルの濃い黄色 */
    .section-title {
        color: #FFD600 !important;
        font-weight: bold;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* 回答ボックス */
    .answer-box {
        background: linear-gradient(135deg, #FEF9E7, #FFFFFF);
        padding: 1.2rem;
        border-radius: 12px;
        border: 3px solid #EAB308;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(234, 179, 8, 0.2);
    }
    
    .answer-box * {
        color: #1F2937 !important;
    }
    
    /* ボタンのスタイル */
    .stButton > button {
        background: #000000;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        background: #333333;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* サイドバーのテキスト色を白に */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: white !important;
    }
    
    .css-1d391kg p, .css-1d391kg div {
        color: white !important;
    }
    
    /* サイドバーの強調文字 */
    .css-1d391kg strong {
        color: white !important;
    }
    
    /* 右カラムの白背景を削除 */
    .right-column {
        background: transparent;
        color: white !important;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .right-column * {
        color: white !important;
    }
    
    .right-column h3 {
        color: white !important;
        font-weight: bold;
    }
    
    /* インフォボックスの色調整 */
    .stInfo {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
        color: white !important;
    }
    
    .stInfo * {
        color: white !important;
    }
    
    /* テキストエリアのスタイル調整 */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #EAB308;
        font-size: 1rem;
        background-color: white;
        color: #1F2937;
    }
    
    /* ラベルの色調整 */
    .stTextArea label {
        color: #1F2937 !important;
    }
    
    /* スマホでの文字サイズ調整 */
    @media (max-width: 768px) {
        .stMarkdown p, .stWrite p {
            font-size: 0.9rem;
        }
        
        .stSubheader {
            font-size: 1.2rem;
        }
    }
    
    /* カラムレイアウトのスマホ対応 */
    @media (max-width: 768px) {
        .row-widget.stHorizontal {
            flex-direction: column !important;
        }
        
        .element-container {
            width: 100% !important;
        }
    }
    
    /* 右側カラムの文字色調整 */
    .right-column {
        color: #1F2937 !important;
    }
    
    /* サブヘッダーの色調整 */
    h2, h3 {
        color: white !important;
    }
    
    /* 使い方セクションの背景調整 */
    .element-container h3 {
        color: white !important;
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

def load_usage_stats():
    """使用統計を読み込み"""
    try:
        with open('usage_stats.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "daily_requests": {},
            "last_reset": datetime.now().strftime("%Y-%m-%d")
        }
    except json.JSONDecodeError:
        return {
            "daily_requests": {},
            "last_reset": datetime.now().strftime("%Y-%m-%d")
        }

def save_usage_stats(stats):
    """使用統計を保存"""
    try:
        with open('usage_stats.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"使用統計の保存に失敗しました: {str(e)}")

def check_usage_limits():
    """使用制限をチェック"""
    stats = load_usage_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 日次リセット
    if stats["last_reset"] != today:
        stats["daily_requests"] = {}
        stats["last_reset"] = today
        save_usage_stats(stats)
    
    # 本日の使用回数をチェック
    today_requests = stats["daily_requests"].get(today, 0)
    
    # 制限値の設定（5,000円以内 = 約2,500-3,000回）
    # GPT-3.5-turbo: 約$0.002/回 → 2,500回で$5 ≈ 5,000円
    DAILY_LIMIT = 2500  # 1日あたり2500回（安全マージン含む）
    
    if today_requests >= DAILY_LIMIT:
        return False, f"本日の使用回数上限（{DAILY_LIMIT}回）に達しました。明日再度お試しください。"
    
    return True, ""

def check_rate_limit():
    """レート制限をチェック（連続リクエスト防止）"""
    current_time = time.time()
    time_since_last = current_time - st.session_state.last_request_time
    
    # 2秒以内の連続リクエストを制限（複数名同時使用を考慮して短縮）
    MIN_INTERVAL = 2
    
    if time_since_last < MIN_INTERVAL:
        remaining_time = MIN_INTERVAL - time_since_last
        return False, f"少し時間をおいてから再度お試しください。（あと{remaining_time:.0f}秒）"
    
    # セッション内での連続リクエスト制限を緩和（1セッションあたり最大20回）
    SESSION_LIMIT = 20
    if st.session_state.request_count_session >= SESSION_LIMIT:
        return False, f"1回のセッションでは最大{SESSION_LIMIT}回までの質問が可能です。ページをリロードしてください。"
    
    return True, ""

def increment_usage():
    """使用回数をインクリメント"""
    stats = load_usage_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 本日の使用回数を増加
    if today not in stats["daily_requests"]:
        stats["daily_requests"][today] = 0
    stats["daily_requests"][today] += 1
    
    save_usage_stats(stats)
    return stats

def initialize_session_state():
    """セッション状態を初期化"""
    if 'couple_info' not in st.session_state:
        st.session_state.couple_info = load_couple_info()
    
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []
    
    if 'last_request_time' not in st.session_state:
        st.session_state.last_request_time = 0
    
    if 'request_count_session' not in st.session_state:
        st.session_state.request_count_session = 0

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
        # 使用制限チェック
        usage_ok, usage_msg = check_usage_limits()
        if not usage_ok:
            return usage_msg
        
        # レート制限チェック
        rate_ok, rate_msg = check_rate_limit()
        if not rate_ok:
            return rate_msg
        
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        system_prompt = f"""
あなたは新郎新婦（大悟と凜）について詳しく知っているAIアシスタントです。
以下の情報を基に、新郎新婦に関する質問に答えてください。

新郎新婦の情報:
{couple_profile}

回答する際の注意事項:
- 新郎新婦の代わりに回答するのではなく、二人について詳しく知っているAIとして回答する
- 「大悟さんと凜さんは〜」「お二人は〜」という形で客観的に説明する
- 敬語を使い、丁寧で親しみやすい口調で回答する
- 「です」「ます」調で答える
- 具体的なエピソードがあれば含める
- 回答は100-150文字程度で簡潔にまとめ、必ず文章として完結させる
- 情報にない内容については推測せず、「詳しい情報がありません」と答える
- 結婚式のゲストに向けた温かい雰囲気で回答する
- 回答は必ず「。」で終わるように完結した文章にする
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=150,  # トークン数を適切に調整
            temperature=0.7,
            stop=["。\n", "\n\n"]  # 文の終わりで適切に停止
        )
        
        # 使用回数をインクリメント
        increment_usage()
        
        # セッション内の使用回数とタイムスタンプを更新
        st.session_state.last_request_time = time.time()
        st.session_state.request_count_session += 1
        
        # 回答の後処理：文章が途中で切れている場合の対処
        answer = response.choices[0].message.content.strip()
        
        # 文章が「。」で終わっていない場合は、適切に終了させる
        if answer and not answer.endswith('。'):
            # 最後の完全な文を取得
            sentences = answer.split('。')
            if len(sentences) > 1:
                # 最後の不完全な文を除去
                answer = '。'.join(sentences[:-1]) + '。'
            else:
                # 単一の不完全な文の場合は「。」を追加
                answer = answer.rstrip('、') + '。'
        
        return answer
    
    except Exception as e:
        return f"申し訳ございません。システムエラーが発生しました: {str(e)}"

def detect_mobile():
    """モバイルデバイスを検出"""
    # Streamlitではブラウザの情報を直接取得できないため、
    # 画面サイズに基づいてレスポンシブ対応を行う
    return False  # デフォルトはデスクトップ表示

def main():
    """メイン関数"""
    initialize_session_state()
    
    # モバイル検出（実際の実装では JavaScript が必要）
    st.session_state.mobile_view = detect_mobile()
    
    # ヘッダー
    st.markdown('<h1 class="main-header">Daigo & Rin AI</h1>', unsafe_allow_html=True)
    
    # メインエリア - スマホ対応
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 新郎新婦の情報表示
        couple_info = st.session_state.couple_info
        display_info = False
        
        # 新しい構造の場合
        if 'basic_info' in couple_info:
            basic_info = couple_info['basic_info']
            if basic_info.get('groom', {}).get('name') or basic_info.get('bride', {}).get('name'):
                display_info = True
                st.markdown('<h2 class="section-title">新郎新婦のご紹介</h2>', unsafe_allow_html=True)
                
                if basic_info.get('groom', {}).get('name'):
                    st.write(f"**新郎:** {basic_info['groom']['name']}")
                if basic_info.get('bride', {}).get('name'):
                    st.write(f"**新婦:** {basic_info['bride']['name']}")
                
                # 結婚式情報の表示
                if 'wedding_info' in couple_info:
                    wedding_info = couple_info['wedding_info']
                    if wedding_info.get('date'):
                        st.write(f"**結婚式:** {wedding_info['date']}")
                    if wedding_info.get('venue'):
                        st.write(f"**会場:** {wedding_info['venue']}")
        
        # 旧構造との互換性維持
        elif couple_info.get('groom_name') or couple_info.get('bride_name'):
            display_info = True
            st.markdown('<h2 class="section-title">新郎新婦のご紹介</h2>', unsafe_allow_html=True)
            
            if couple_info.get('groom_name'):
                st.write(f"**新郎:** {couple_info['groom_name']}")
            if couple_info.get('bride_name'):
                st.write(f"**新婦:** {couple_info['bride_name']}")
            if couple_info.get('wedding_date'):
                st.write(f"**結婚式:** {couple_info['wedding_date']}")
            if couple_info.get('venue'):
                st.write(f"**会場:** {couple_info['venue']}")
        
        # 質問入力フォーム
        st.markdown('<h2 class="section-title">AIへの質問</h2>', unsafe_allow_html=True)
        question = st.text_area(
            "大悟と凜に聞きたいことがありましたら、こちらに入力して下さい。",
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
    
    with col2:
        st.markdown('<div class="right-column">', unsafe_allow_html=True)
        st.subheader("使い方")
        st.info("""
        1. 質問を入力してAIに聞く
        2. AIが大悟さんと凜さんについて詳しく教えてくれます
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="right-column">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()