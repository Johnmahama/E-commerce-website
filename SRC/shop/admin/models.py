from shop.admin import db

from datetime import datetime

class Addproduct(db.Model):
    __tablename__ = "addproduct"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    price = db.Column(db.Numeric(10,2),nullable=False)
    discount = db.Column(db.Integer,nullable=False)
    stock = db.Column(db.Integer,nullable=False)
    colors = db.Column(db.Text,nullable=False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime,nullable=False,default= datetime.utcnow)

    brand_id = db.Column(db.Integer,db.ForeignKey('brand.id'),nullable=False)
    brand= db.relationship('Brand',backref=db.backref('brands',lazy=True))

    category_id = db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
    category= db.relationship('Category',backref=db.backref('categories',lazy=True))

    image_1 = db.Column(db.String(150), nullable = False,default='image.jpg')
    image_2 = db.Column(db.String(150), nullable = False,default='image.jpg')
    image_3 = db.Column(db.String(150), nullable = False,default='image.jpg')


    def __repr__(self):
        return '<Addproduct %r>' % self.name


 
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile = db.Column(db.String(80), unique=False, nullable=False ,default='profile.jpg')

    


class Brand( db.Model):
    __tablename__ = "brand"
    id  = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30), nullable=False,unique=True)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(130),nullable=False,unique=True)

    def __repr__(self):
        return '<User %r>' % self.username


db.create_all()

