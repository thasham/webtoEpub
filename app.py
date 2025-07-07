from flask import Flask, render_template, request, send_file
from ebooklib import epub
from newspaper import Article
import tempfile
import os
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    urls = request.form.get('urls', '').splitlines()
    book_title = request.form.get('title', 'Collected Articles')
    book_author = request.form.get('author', 'Web EPUB Generator')

    cover_file = request.files.get('cover')
    cover_path = None

    book = epub.EpubBook()
    book.set_identifier('web-to-epub')
    book.set_title(book_title)
    book.set_language('en')
    book.add_author(book_author)

    if cover_file and cover_file.filename:
        cover_path = os.path.join(app.config['UPLOAD_FOLDER'], "cover.jpg")
        cover_file.save(cover_path)
        try:
            img = Image.open(cover_path)
            img.convert("RGB").save(cover_path, "JPEG")
            book.set_cover("cover.jpg", open(cover_path, "rb").read())
        except Exception as e:
            print(f"Failed to use uploaded cover: {e}")

    chapters = []
    for i, url in enumerate(urls):
        url = url.strip()
        if not url:
            continue
        try:
            article = Article(url)
            article.download()
            article.parse()
            title = article.title or f"Chapter {i+1}"
            content = article.text.replace("\n", "<br>")
            chapter = epub.EpubHtml(title=title, file_name=f'chap_{i+1}.xhtml', lang='en')
            chapter.content = f"<h1>{title}</h1><p>{content}</p>"
            book.add_item(chapter)
            chapters.append((title.lower(), chapter))
        except Exception as e:
            print(f"Failed to process {url}: {e}")

    if not chapters:
        return "No valid articles found."

    sorted_chapters = [ch for _, ch in sorted(chapters, key=lambda x: x[0])]

    book.toc = tuple(sorted_chapters)
    book.spine = ['nav'] + sorted_chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp:
        epub.write_epub(tmp.name, book)
        tmp_path = tmp.name

    return send_file(tmp_path, as_attachment=True, download_name="output.epub")

if __name__ == '__main__':
    app.run(debug=True)
