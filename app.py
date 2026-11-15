
from flask import Flask
from routes.main import main
from routes.products import products
from routes.customers import customers

app = Flask(__name__)
app.secret_key = "4d9f0017953cca3d9ef11636adeb01bd0151f9b270cceb7075ca05caee7aca43"

app.register_blueprint(main)
app.register_blueprint(products)
app.register_blueprint(customers)

if __name__ == "__main__":
    app.run(debug=True)
