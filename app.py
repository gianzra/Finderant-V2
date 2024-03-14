from flask import Flask, render_template, request
import pandas as pd

# import resystem as rec
import bykeywords as bk
# import books_data as bd
# import search as src

app = Flask(__name__)
app.config['assets_FOLDER'] = 'assets'
app.config['STATIC_FOLDER'] = 'static'
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/keywords', methods=['GET'])
def keywords():
    return render_template('rekomendasi2.html')

@app.route('/keywords', methods=['POST'])
def keywordsrec():
    book = request.form['book']
    jumlah = request.form['jumlah']
    book = book.lower()
    peringatan = 'Silahkan masukkan keyword terlebih dahulu.'
    if book == '':
        return render_template("rekomendasi2.html", warning=peringatan) 
    elif jumlah == '':
        jumlah = 10

    df = pd.read_csv("data_soup.csv", sep='\t', on_bad_lines='skip')
    x = df.title.values
    search_book = list(map(lambda x: x.lower(), x))
    gagal = 'Keyword tersebut sesuai dengan judul buku yang tersedia, mencari rekomendasi buku dapat melalui halaman'
    if book in search_book:
        return render_template("rekomendasi2.html", salah=gagal)
    else:
        rekomendasi = bk.get_recommendations(book, jumlah)

    # mengubah link menjadi tag HTML
    def path_to_image_html(path):
        return '<img src="'+ path + '" width="5px" >'

    image_cols = rekomendasi['Cover']  #<- menentukan kolom - kolom yang akan diubah menjadi HTML

    # membuat kamus yang bakal digunakan untuk formatter
    format_dict = {}
    for image_col in image_cols:
        format_dict[image_col] = path_to_image_html
    
    return render_template("rekomendasi2.html", tables=[rekomendasi.to_html(classes='data', escape=False ,formatters=format_dict)], titles=['Title'], buku_dicari=book)

if __name__ == "__main__":
    app.run()