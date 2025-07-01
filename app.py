from flask import Flask, render_template, request, redirect
from datetime import datetime
import requests

app = Flask(__name__)

BOT_TOKEN = '7555243004:AAEKoSZAgZ53QLhRv5dnMF1c3hy8qOo-dKw'  # <-- o'z tokeningizni yozing
ADMIN_CHAT_IDS = [6855997739]  # <-- admin ID larni yozing

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ismi = request.form['ismi']
        kurs = request.form['kurs']
        tel1 = request.form['tel1']
        tel2 = request.form.get('tel2', '').strip() or "Yo‘q"

        sana = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        message = (
            f"📥 *Yangi ro‘yxat!*\n\n"
            f"👤 Ismi: {ismi}\n"
            f"📘 Kurs: {kurs}\n"
            f"📞 Tel 1: {tel1}\n"
            f"📞 Tel 2: {tel2}\n"
            f"📅 Sana: {sana}"
        )

        for admin_id in ADMIN_CHAT_IDS:
            try:
                requests.get(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    params={
                        "chat_id": admin_id,
                        "text": message,
                        "parse_mode": "Markdown"
                    }
                )
            except Exception as e:
                print("Telegramga yuborishda xatolik:", e)

        return redirect('/thanks')

    return render_template('form.html')

@app.route('/thanks')
def thanks():
    return "<h3>✅ Muvaffaqiyatli yuborildi! Tez orada siz bilan bog'lanamiz.</h3>"

if __name__ == '__main__':
    app.run(debug=True)
