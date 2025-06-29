# DAIGO & RIN AI 💒

DAIGOとRINへの質問にAIが答える結婚式披露宴用のWebアプリケーションです。

## 特徴

- 👰🤵 新郎新婦の詳細情報をJSONファイルから読み込み
- 🤖 OpenAI GPTを使用したインテリジェントな回答生成
- 💬 ゲストからの質問にDAIGOとRINの代わりにAIが回答
- 🎨 結婚式にふさわしい美しいUI
- 📁 ファイルベースの情報管理

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. OpenAI APIキーの設定

`.env`ファイルに以下を設定してください：

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. アプリケーションの起動

```bash
streamlit run main.py
```

## 使い方

### 1. 新郎新婦の情報設定
- `couple_info.json`ファイルを編集してDAIGOとRINの情報を設定
- アプリで「情報を再読み込み」ボタンをクリックして最新情報を反映

### 2. 質問の投稿
- メインエリアでゲストからの質問を入力
- 「AIに質問する」ボタンをクリック

### 3. AI回答の確認
- AIがDAIGOとRINの情報を基に温かい回答を生成
- リアルタイムで回答が表示される

## couple_info.json の設定

新郎新婦の情報は `couple_info.json` ファイルに以下の形式で保存します：

```json
{
  "groom_name": "DAIGO",
  "bride_name": "RIN",
  "wedding_date": "結婚式の日付",
  "venue": "会場名",
  "how_they_met": "出会いのエピソード",
  "proposal_story": "プロポーズのエピソード",
  "hobbies": "趣味・特技",
  "favorite_things": "好きなもの",
  "future_plans": "将来の計画",
  "message_to_guests": "ゲストへのメッセージ"
}
```

## 質問例

- どこで出会ったのですか？
- お互いの第一印象は？
- プロポーズはどんな感じでしたか？
- 結婚を決めたきっかけは？
- 好きな食べ物は何ですか？
- 将来の夢はありますか？
- ゲストへのメッセージをお聞かせください

## 使用シーン

- **披露宴中**: ゲストからの質問をリアルタイムで受け付け
- **二次会**: カジュアルな質問にも対応
- **ウェルカムパーティー**: ゲストとの交流ツールとして

## 技術スタック

- **Frontend**: Streamlit
- **AI**: OpenAI GPT-3.5-turbo
- **言語**: Python 3.11+
- **データ管理**: JSON
- **その他**: python-dotenv, requests

## ライセンス

MIT License