import os.path
import uuid
from flask import Flask, render_template,request, flash
from flask_sqlalchemy import SQLAlchemy


UPLOAD_FOLDER = os.path.join("img","uploads")

app = Flask(__name__)
app.secret_key = "key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1042 * 1042
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/qwe/ad.db'
db = SQLAlchemy(app)


class Products(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    file = db.Column(db.String, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String, nullable=True)

    # def __repr__(self):
    #     return f"{self.ad}"


ALLOWED_EXTENSIONS = {"png","jpg","jpeg"}


@app.route('/upload',methods=["GET","POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]

        file_extensions = file.filename

        if file_extensions.split(".")[-1].lower() not in ALLOWED_EXTENSIONS:

            flash("Не поддерживаемый тип файла", category='error')

        else:

            file.filename = f'{uuid.uuid4()}.{file.filename.split(".")[-1].lower()}'
            file.save(os.path.join("static",UPLOAD_FOLDER,file.filename))

            title = request.form["title"]
            file = file.filename
            price = request.form["price"]
            description = request.form["description"]

            add_data = Products(

                title=title,
                file=file,
                price=price,
                description=description

            )

            db.session.add(add_data)
            db.session.flush()
            db.session.commit()

            img = os.path.join(UPLOAD_FOLDER,file)

            return render_template("ad.html",id=add_data.id,title=title,img=img,price=price,description=description)

    return render_template("uploads.html")


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    if request.method == "GET":

        res = Products.query.all()

        img = os.path.join(UPLOAD_FOLDER, res[post_id - 1].file)

        return render_template("ad.html", title=res[post_id - 1].title, img=img, price=res[post_id - 1].price, description=res[post_id - 1].description)


if __name__ == '__main__':
    app.run(debug=True)