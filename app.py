from linebot import LineBotApi, WebhookHandler 
from linebot.models import MessageEvent, TextMessage, TextSendMessage 
from linebot.exceptions import InvalidSignatureError 
from flask import Flask, request, abort 
# LINE Botのチャンネルアクセストークンとチャンネルシークレット
CHANNEL_ACCESS_TOKEN = 'YOUR_CHANNEL_ACCESS_TOKEN' 
CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET' 

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN) 
handler = WebhookHandler(CHANNEL_SECRET) 
app = Flask(__name__) 
@app.route("/callback", methods=['POST']) 
def callback(): # LINEからのリクエストかどうかを確認 
    signature = request.headers['X-Line-Signature'] 
    try: 
        handler.handle(request.data.decode('utf-8'), signature) 
    except InvalidSignatureError: 
        abort(400) 
    return 'OK' 
@handler.add(MessageEvent, message=TextMessage) 
def handle_message(event): 
    user_input = event.message.text 
    try: 
        # evalを使用してユーザー入力を評価（セキュリティ上の問題に注意） 
        result = str(eval(user_input))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result)) 
    except Exception as e: line_bot_api.reply_message(event.reply_token, TextSendMessage(text='エラー: ' + str(e))) 
if __name__ == "__main__":
    app.run()
