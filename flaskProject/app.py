from flask import Flask, render_template, jsonify, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from destek import dolarkuru

app = Flask(__name__)

# Veritabanı ayarları
app.config['SQLALCHEMY_DATABASE_URI'] = r'mssql+pyodbc://DESKTOP-VF1FSBT\SQLEXPRESS/Blog?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Gereksiz işlemi önlüyoruz
db = SQLAlchemy(app) # SQLAlchemy'yi Flask'a bağladık

# BlogPost tablosunun modeli
class BlogPost(db.Model):
    __tablename__ = 'blog_post'  # Tabloyu aldık
    title = db.Column(db.String(100), primary_key=True)  # Başlık alanını birincil anahtar olarak ayarladık
    contentt = db.Column(db.Text, nullable=False)  # Yazının içeriği, boş bırakılamaz
@app.route('/add', methods=['POST'])#post metodu ile veri gödnerdim veya sunucuda işlem icn kullnılır
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        contentt = request.form['contentt']
        new_post = BlogPost(title=title, contentt=contentt)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')  # Ekleme işleminden sonra ana sayfaya yönlendir
    return render_template('add_post.html')

# Ana sayfa - Blog yazılarını listeleme
@app.route('/', methods=['GET'])
def home():
    dolar = dolarkuru()  # Dolar kuru için özel bir fonksiyon
    if not request.args:
        posts = BlogPost.query.order_by(BlogPost.title).all()  # Blog yazılarını başlığa göre sıralı çekiyoruz
        return render_template('ana.html', dolar=dolar, posts=posts)  # Blog yazılarını ana sayfada gösteriyoruz
    else:
        sorgu = request.args['blogSearch']
        # Aynı sorgu daha önce eklenmiş mi kontrol et
        var_query = BlogPost.query.filter(BlogPost.title.like(f'%{sorgu}%')).all()
        print(var_query)
        return render_template('ana.html', dolar = dolar, posts = var_query, search = sorgu)

# Blog yazısı ekleme sayfası

# Hakkımda bölümü
@app.route('/hakkimda')
def hakkimda():
    return render_template('hakkimda.html')

# Anasayfa yönlendirmesi
@app.route('/anasayfa')
def anasayfa():
    return render_template('anasayfa.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tabloları veritabanında oluştur
    app.run(debug=True)
