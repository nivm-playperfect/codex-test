from flask import Flask, render_template, redirect, url_for, flash
from forms import ProductForm
from models import db, Product, init_app


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backoffice.db'
    app.config['SECRET_KEY'] = 'change-me'
    init_app(app)

    @app.route('/')
    def product_list():
        products = Product.query.all()
        return render_template('product_list.html', products=products)

    @app.route('/product/new', methods=['GET', 'POST'])
    def create_product():
        form = ProductForm()
        if form.validate_on_submit():
            product = Product(name=form.name.data, price=float(form.price.data))
            db.session.add(product)
            db.session.commit()
            flash('Product created')
            return redirect(url_for('product_list'))
        return render_template('product_form.html', form=form)

    @app.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
    def edit_product(product_id):
        product = Product.query.get_or_404(product_id)
        form = ProductForm(obj=product)
        if form.validate_on_submit():
            form.populate_obj(product)
            db.session.commit()
            flash('Product updated')
            return redirect(url_for('product_list'))
        return render_template('product_form.html', form=form)

    @app.route('/product/<int:product_id>/delete')
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted')
        return redirect(url_for('product_list'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
