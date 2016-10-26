from flask import Flask, render_template, send_file, request, Response
app = Flask(__name__)
app.debug = True

# Routes

@app.route("/")
def index():
    return render_template('base.html')

@app.route('/login')
# GET renders HTML login form
def login():
    return render_template('partials/login.html')

@app.route('/upload', methods=['POST'])
def upload():
    import pb
    pdb.set_trace()
    print request


if __name__ == "__main__":
    app.run()
