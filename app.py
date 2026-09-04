from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key='super_secret_key_123'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# database initialization
def init_db():
    conn =sqlite3.connect('market.db')
    c = conn.cursor()

    # users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT)
    ''')
    #products table
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 description TEXT,
                 seller TEXT,
                 image TEXT)
    ''')

    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'supersecretpassword')")
        conn.commit()
    conn.close()

init_db()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('market.db')
        c = conn.cursor()

        # clear text password storage (broken authentication)
        # sql injection
        c.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
         
        conn = sqlite3.connect('market.db') 
        c = conn.cursor()

        # sql injection: login bypass
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            # saving the user id
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/products')
        else:
            return "please try again."
    return render_template('login.html')

@app.route('/logout')        
def logout():
    session.clear()
    return redirect('/')    

@app.route('/products', methods=['GET', 'POST'])
def products():
    if 'username' not in session:
        return redirect('/login')
   
    conn = sqlite3.connect('market.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        seller = session['username']

        # file upload
        file = request.files.get('image')
        filename = "default.png"

        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        c.execute(f"INSERT INTO products (name, description, seller, image) VALUES ('{name}', '{description}', '{seller}', '{filename}')")
        conn.commit()

    c.execute(f"SELECT * FROM products")
    items= c.fetchall()
    conn.close()

    return render_template('products.html', items=items)

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if session.get('username') != 'admin':
        return "please try again. admins only.", 403

    ping_result = ""

    if request.method == 'POST':
        target_ip = request.form.get('ip')

        # rce
        cmd = f"ping -c 2 {target_ip}"

        try:
            ping_result = os.popen(cmd).read()
        except Exception as e:
            ping_result = str(e)

    conn = sqlite3.connect('market.db')
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users")
    all_users = c.fetchall()
    conn.close()

    return render_template('admin.html', all_users=all_users, ping_result=ping_result)

@app.route('/delete_product', methods=['GET'])
def delete_product():
    if 'username' not in session:
        return redirect('/login')

    # get product id from url
    product_id = request.args.get('id')
    conn =sqlite3.connect('market.db')
    c = conn.cursor()

    # idor
    # no control over authorization
    c.execute(f"DELETE FROM products WHERE id ={product_id}")

    conn.commit()
    conn.close()

    return redirect('/products')

@app.route('/api/v1/users')
def api_users():
    conn = sqlite3.connect('market.db')
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users")
    users = c.fetchall()
    conn.close()

    import json 

    user_list= [{"id": u[0], "username": u[1], "password": u[2]} for u in users]

    return app.response_class(
        response = json.dumps(user_list),
        status = 200,
        mimetype = 'application/json'
    )

if __name__ == "__main__":
    app.run(host= '127.0.0.1' , port=5000, debug=True)
