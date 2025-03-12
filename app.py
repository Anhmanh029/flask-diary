from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# Cấu hình SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tạo bảng dữ liệu
class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Tạo database
with app.app_context():
    db.create_all()

# Trang chính
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date = request.form["date"]
        content = request.form["content"]
        
        new_entry = DiaryEntry(date=date, content=content)
        db.session.add(new_entry)
        db.session.commit()
        
        return redirect("/")
    
    # Lấy danh sách nhật ký
    entries = DiaryEntry.query.order_by(DiaryEntry.date.desc()).all()
    return render_template("index.html", entries=entries)

if __name__ == "__main__":
    app.run(debug=True)
