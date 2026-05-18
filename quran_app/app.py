from flask import Flask, render_template
from flask_cors import CORS
from routes import quran_bp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

app.register_blueprint(quran_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("=" * 50)
    print("  http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)