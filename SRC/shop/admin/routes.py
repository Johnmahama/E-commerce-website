from flask import render_template,session,request,redirect,url_for,flash,current_app

from shop.admin import app, db,bcrypt,photos
from .forms import RegistrationForm,LoginForm, AddproductForm
from .models import User, Brand, Category,Addproduct
import secrets
import json


import os




@app.route('/')
def home():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    page = request.args.get('page',1,type=int)
    products  = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc())
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories  = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html' , products=products , brands= brands, categories=categories)


@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories  = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return render_template('products/single_page.html', product=product ,brands=brands, categories=categories)




@app.route('/brand/<int:id>')
def get_brand(id):
    get_b = Brand.query.filter_by(id=id).first_or_404()
    page = request.args.get('page',1,type=int)
    brand = Addproduct.query.filter_by(brand=get_b).paginate(page=page,per_page=8)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories  = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html' , brand= brand, brands =brands ,categories=categories ,get_b=get_b)



@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1,type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page , per_page=8)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories  = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', get_cat_prod=get_cat_prod,categories=categories, brands=brands,get_cat = get_cat)



    
@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    
    return render_template('admin/index.html',title="Admin Page",products=products)




@app.route('/brands') 
def brands():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html',title="Brand Page", brands=brands)





@app.route('/category') 
def category():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html',title="Brand Page",categories=categories)





@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data,email= form.email.data,
                    password= hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data}, Thanks you for registering','success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form,title="Registration page")




@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method =="POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data}.  You are login','success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password please try again', 'danger')
    return render_template('admin/login.html',form=form,title="Login Page")




@app.route('/addbrand' ,methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        db.session.commit()
        flash(f'The Brand {getbrand} was added to your database','success')
        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html', brands='brands')





@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
    updatebrand= Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'Your brand has been updated','success')
        db.session.commit()
        return redirect(url_for('brands'))

    return render_template('products/updatebrand.html',title="Update brand Page",updatebrand=updatebrand)






@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method =="POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database','success')
        return redirect(url_for('admin'))
    flash(f'The brand {brand.name} cant be deleted','warning')
    return redirect(url_for('admin'))





@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
    updatecat= Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =="POST":
        updatecat.name = category
        flash(f'Your category has been updated','success')
        db.session.commit()
        return redirect(url_for('category'))

    return render_template('products/updatebrand.html',title="Update Category Page",updatecat=updatecat)






@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory (id):
    category = Category.query.get_or_404(id)
    if request.method =="POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'The  category  { category.name} was deleted from your database','success')
        return redirect(url_for('admin'))
    flash(f'The brand { category .name} cant be deleted','warning')
    return redirect(url_for('admin'))






@app.route('/addcat' ,methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        db.session.commit()
        flash(f'The Category {getbrand} was added to your database','success')
        
        return redirect(url_for('addcat'))

    return render_template('products/addbrand.html')






@app.route('/addproduct',methods=['POST','GET'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddproductForm(request.form)
    if request.method =="POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
                                                                                           
        image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")

        addpro = Addproduct(name=name,price=price,discount=discount,stock=stock,colors=colors,description=description,brand_id=brand,category_id=category,
        image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database','success')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('products/addproducts.html',title="Add Products page",form=form , brands=brands,categories=categories) 






@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product= Addproduct.query.get_or_404(id)
    if request.method =="POST":
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" +product.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/" +product.image_2))    
                os.unlink(os.path.join(current_app.root_path, "static/images/" +product.image_3))
            except  Exception as e:
                print(e)
                    
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was deleted from your record','success')
        return redirect(url_for('admin'))
    flash(f'Cant delete the product' ,'danger')
    return redirect(url_for('admin'))




@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form =  AddproductForm(request.form)
    if request.method =="POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.description= form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" +product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'),name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" +product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'),name=secrets.token_hex(10) + ".")
        
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" +product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'),name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'You product have been updated','success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.description.data = product.description
    form.colors.data = product.colors
    return render_template('products/updateproduct.html',form=form,  brands= brands, categories=categories,  product= product)



def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
       return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()
        
        if product_id and colors and quantity and request.method == "POST":
            DictItems = { product_id:{'name':product.name, 'price':product.price , 'discount':product.discount, 
            'colors':product, 'quantity':quantity, 'image':product.image_1,'colors':product.colors} }

            if "Shoppingcart" in session:
                print(session["Shoppingcart"])
                if product_id in session["Shoppingcart"]:
                    for key, item in session['Shoppingcart'].items():
                        if int(key)==int(product_id):
                            session.modified =True
                            item['quantity']+=1
                    print("This product is already in your cart")
                else:
                    session["Shoppingcart"] = MagerDicts( session["Shoppingcart"], DictItems)
                    return redirect(request.referrer)
            else:
                session["Shoppingcart"] = DictItems
                return redirect(request.referrer)
    except Exception as e:
       print(e)
    finally:
        return redirect(request.referrer)



@app.route('/carts')
def getCart():
    if  'Shoppingcart' not in session or len(session['Shoppingcart']):
        return redirect(url_for('home'))
        subtotal =0
        grandtotal =0 
        for key,product in session["Shoppingcart"]:
            discount = (product['discount']/100) * float(product['price'])
            subtotal = float(product['price']) * int(product['quantity'])
            subtotal-= discount
            tax = ("%.2f" % (.06 * float(subtotal)))
            grandtotal = float("%.2f" % (1.06 * subtotal))

    return render_template('products/carts.html',tax=tax, grandtotal=grandtotal)



@app.route('/updatecart/<int:code>' , methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shopingcart']) <=0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity']=quantity
                    item['color']= color
                    flash("Item is updated")
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/clearcat')
def clearcat():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)



@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if Shoppingcart not in session and len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == id:
                    session['Shoppingcart'].pop(key,None)
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))



@app.route('/empty')
def empty_carts():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)