from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import threading
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)

# Gmail 配置 - 从环境变量读取
GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "chengxiaozhou1@gmail.com")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD", "")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "chengxiaozhou1@gmail.com")

# 启动时打印配置状态（不打印密码）
print(f"[CONFIG] GMAIL_ADDRESS: {GMAIL_ADDRESS}")
print(f"[CONFIG] GMAIL_PASSWORD set: {'YES' if GMAIL_PASSWORD else 'NO'}")
print(f"[CONFIG] RECIPIENT_EMAIL: {RECIPIENT_EMAIL}")

def send_email_async(subject, html_content):
    """在后台线程中发送邮件"""
    def _send():
        try:
            print(f"[EMAIL] 开始发送邮件: {subject}")
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = GMAIL_ADDRESS
            msg['To'] = RECIPIENT_EMAIL
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
            server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            print(f"[EMAIL] 邮件发送成功: {subject}")
        except Exception as e:
            print(f"[EMAIL ERROR] 邮件发送失败: {str(e)}")
            traceback.print_exc()

    thread = threading.Thread(target=_send)
    thread.start()

@app.route('/api/booking', methods=['POST'])
def submit_booking():
    """处理预约表单提交"""
    try:
        data = request.json
        print(f"[BOOKING] 收到预约: {data.get('name', 'unknown')}")

        html_content = f"""
        <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: 'Noto Sans SC', Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; border-radius: 8px; }}
                    .header {{ background: linear-gradient(135deg, #ff8c1a, #ff6b6b); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                    .header h2 {{ margin: 0; }}
                    .section {{ background: white; padding: 15px; margin-bottom: 15px; border-radius: 6px; border-left: 4px solid #ff8c1a; }}
                    .label {{ font-weight: bold; color: #ff8c1a; }}
                    .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>🏠 新的预约陪伴服务申请</h2>
                        <p>来自伴邻网站的表单提交</p>
                    </div>
                    <div class="section">
                        <p><span class="label">申请人姓名：</span>{data.get('name', '未填写')}</p>
                        <p><span class="label">联系电话：</span>{data.get('phone', '未填写')}</p>
                        <p><span class="label">电子邮箱：</span>{data.get('email', '未填写')}</p>
                    </div>
                    <div class="section">
                        <p><span class="label">与长辈关系：</span>{data.get('relationship', '未填写')}</p>
                        <p><span class="label">长辈年龄：</span>{data.get('age', '未填写')}</p>
                        <p><span class="label">所在区域：</span>{data.get('district', '未填写')}</p>
                    </div>
                    <div class="section">
                        <p><span class="label">主要需求：</span></p>
                        <p>{', '.join(data.get('services', [])) if data.get('services') else '未选择'}</p>
                    </div>
                    <div class="section">
                        <p><span class="label">补充说明：</span></p>
                        <p>{data.get('remarks', '无')}</p>
                    </div>
                    <div class="footer">
                        <p>提交时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
                        <p>来自伴邻 BanLin 服务平台</p>
                    </div>
                </div>
            </body>
        </html>
        """

        # 异步发送邮件，立即返回成功
        send_email_async('【伴邻】新的预约陪伴服务申请', html_content)
        return jsonify({'success': True, 'message': '预约已提交，我们将在24小时内联系您'}), 200

    except Exception as e:
        print(f"[BOOKING ERROR] {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/apply', methods=['POST'])
def submit_apply():
    """处理伴邻申请表单提交"""
    try:
        data = request.json
        print(f"[APPLY] 收到申请: {data.get('name', 'unknown')}")

        html_content = f"""
        <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: 'Noto Sans SC', Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; border-radius: 8px; }}
                    .header {{ background: linear-gradient(135deg, #ff8c1a, #ff6b6b); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                    .header h2 {{ margin: 0; }}
                    .section {{ background: white; padding: 15px; margin-bottom: 15px; border-radius: 6px; border-left: 4px solid #ff8c1a; }}
                    .label {{ font-weight: bold; color: #ff8c1a; }}
                    .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>❤️ 新的伴邻伙伴申请</h2>
                        <p>有新的年轻伙伴想加入我们</p>
                    </div>
                    <div class="section">
                        <p><span class="label">申请人姓名：</span>{data.get('name', '未填写')}</p>
                        <p><span class="label">联系电话：</span>{data.get('phone', '未填写')}</p>
                        <p><span class="label">电子邮箱：</span>{data.get('email', '未填写')}</p>
                    </div>
                    <div class="section">
                        <p><span class="label">年龄：</span>{data.get('age', '未填写')}</p>
                        <p><span class="label">当前身份：</span>{data.get('identity', '未填写')}</p>
                        <p><span class="label">常住区域：</span>{data.get('district', '未填写')}</p>
                    </div>
                    <div class="section">
                        <p><span class="label">可服务时间：</span></p>
                        <p>{', '.join(data.get('availableTime', [])) if data.get('availableTime') else '未选择'}</p>
                    </div>
                    <div class="section">
                        <p><span class="label">申请理由：</span></p>
                        <p>{data.get('motivation', '无')}</p>
                    </div>
                    <div class="footer">
                        <p>提交时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
                        <p>来自伴邻 BanLin 服务平台</p>
                    </div>
                </div>
            </body>
        </html>
        """

        # 异步发送邮件，立即返回成功
        send_email_async('【伴邻】新的伴邻伙伴申请', html_content)
        return jsonify({'success': True, 'message': '申请已提交，我们将在24小时内联系您'}), 200

    except Exception as e:
        print(f"[APPLY ERROR] {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'gmail_configured': bool(GMAIL_PASSWORD),
        'message': 'Backend is running'
    }), 200

# 静态文件路由放在最后
@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(BASE_DIR, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
