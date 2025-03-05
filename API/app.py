from flask import Flask, g, render_template, request, redirect, url_for, jsonify, session, flash
import sqlite3, os, hashlib
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "valador"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
 
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()

class User(UserMixin):
    def __init__(self, id, username, is_admin=False):
        self.id = id
        self.username = username
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user_row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if user_row:
        print("Loaded User:", user_row)  # Debugging
        return User(user_row['id'], user_row['username'], bool(user_row['is_admin']))  # ✅ Fix conversion

    return None

def admin_required(func):
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash("Access denied!", "error")
            return redirect(url_for('user_dashboard'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    db = get_db()
    joke = db.execute('SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1').fetchone()
    return render_template('index.html', joke=joke)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, 0)", (username, password))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "error")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            login_user(User(user['id'], user['username'], bool(user['is_admin'])))
            return redirect(url_for('user_dashboard'))
        
        flash("Invalid credentials!", "error")
    
    return render_template('login.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required!", "error")
            return render_template('admin_login.html')

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ? AND is_admin = 1", (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            login_user(User(user['id'], user['username'], user['is_admin']))
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
        
        flash("Invalid credentials! Please try again.", "error")
    
    return render_template('admin_login.html')

@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'GET':
        return render_template('admin_register.html')  # Show the registration form
    
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({"status": "error", "message": "Username and password required"}), 400

        hashed_password = generate_password_hash(password)
        db = get_db()  # ✅ Use get_db() instead of direct DB_PATH

        try:
            db.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, 1)", 
                       (username, hashed_password))
            db.commit()
            return jsonify({"status": "success"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"status": "error", "message": "Username already exists"}), 400


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user')
@login_required
def user_dashboard():
    db = get_db()
    jokes = db.execute("SELECT joke FROM jokes WHERE user_id = ?", (current_user.id,)).fetchall()
    return render_template('dashboard.html', jokes=jokes)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:  
        return redirect(url_for('user_dashboard'))  

    db = get_db()
    jokes = db.execute("SELECT * FROM jokes ORDER BY id DESC").fetchall()
    total_jokes = db.execute("SELECT COUNT(*) AS count FROM jokes").fetchone()["count"]
    top_jokes = db.execute("SELECT * FROM jokes ORDER BY upvotes DESC LIMIT 5").fetchall()

    return render_template('admin_dashboard.html', jokes=jokes, total_jokes=total_jokes, top_jokes=top_jokes)





@app.route('/submit_joke', methods=['GET', 'POST'])
@login_required  # Ensure only logged-in users can submit jokes
def submit_joke():
    if request.method == 'POST':
        joke_text = request.form.get('joke')

        if not joke_text:
            flash("Joke cannot be empty!", "error")
            return redirect(url_for('submit_joke'))

        db = get_db()
        db.execute("INSERT INTO jokes (user_id, joke, upvotes, downvotes) VALUES (?, ?, 0, 0)", 
                   (current_user.id, joke_text))
        db.commit()

        flash("Joke submitted successfully!", "success")
        return redirect(url_for('user_dashboard'))

    return render_template('submit_joke.html')

@app.route('/api/vote/<direction>/<int:joke_id>', methods=['POST'])
@login_required
def api_vote(direction, joke_id):
    db = get_db()
    joke = db.execute("SELECT id, upvotes, downvotes FROM jokes WHERE id = ?", (joke_id,)).fetchone()

    if not joke:
        return jsonify({"status": "error", "message": "Joke not found!"}), 404

    if direction == "up":
        db.execute("UPDATE jokes SET upvotes = upvotes + 1 WHERE id = ?", (joke_id,))
    elif direction == "down":
        db.execute("UPDATE jokes SET downvotes = downvotes + 1 WHERE id = ?", (joke_id,))
    else:
        return jsonify({"status": "error", "message": "Invalid vote action!"}), 400

    db.commit()

    # Fetch a new random joke after voting
    new_joke = db.execute("SELECT id, joke FROM jokes ORDER BY RANDOM() LIMIT 1").fetchone()

    if new_joke:
        return jsonify({"status": "success", "id": new_joke["id"], "joke": new_joke["joke"]})
    else:
        return jsonify({"status": "success", "message": "No more jokes!"})

@app.route('/api/joke', methods=['GET'])
def get_new_joke():
    db = get_db()
    joke = db.execute("SELECT id, joke FROM jokes ORDER BY RANDOM() LIMIT 1").fetchone()
    
    if joke:
        return jsonify({"id": joke["id"], "joke": joke["joke"]})
    else:
        return jsonify({"error": "No jokes available"}), 404



@app.route('/admin/edit/<int:joke_id>', methods=['GET', 'POST'])
@login_required
def edit_joke(joke_id):
    db = get_db()
    joke = db.execute("SELECT * FROM jokes WHERE id = ?", (joke_id,)).fetchone()

    if not joke:
        flash("Joke not found.", "error")
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        new_text = request.form['joke_text']
        db.execute("UPDATE jokes SET joke = ? WHERE id = ?", (new_text, joke_id))
        db.commit()
        flash("Joke updated successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_joke.html', joke=joke)

@app.route('/admin/delete/<int:joke_id>', methods=['POST','GET'])
@login_required
def delete_joke(joke_id):
    db = get_db()
    joke = db.execute("SELECT * FROM jokes WHERE id = ?", (joke_id,)).fetchone()

    if not joke:
        flash("Joke not found.", "error")
        return redirect(url_for('admin_dashboard'))

    db.execute("DELETE FROM jokes WHERE id = ?", (joke_id,))
    db.commit()
    flash("Joke deleted successfully!", "success")
    
    return redirect(url_for('admin_dashboard'))



@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            flash("All fields are required!", "error")
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash("New passwords do not match!", "error")
            return redirect(url_for('change_password'))

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (current_user.id,)).fetchone()

        if not check_password_hash(user['password'], old_password):
            flash("Old password is incorrect!", "error")
            return redirect(url_for('change_password'))

        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, current_user.id))
        db.commit()

        flash("Password changed successfully!", "success")
        return redirect(url_for('admin_dashboard')) if current_user.is_admin else redirect(url_for('user_dashboard'))



    return render_template('change_password.html')


if __name__ == '__main__':
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)
    app.run(debug=app.config['DEBUG'], port=5080)
