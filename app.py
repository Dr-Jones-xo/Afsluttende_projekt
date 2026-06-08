from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'super_hemmelig_key_vlan10'

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="projekt_db",
        user="jones",
        password="123"
    )
    return conn

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
        
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 10;') 
        data = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        data = []
        print(f"Databasefejl: {e}")
        
    return render_template('index.html', maalinger=data, username=session['username'])

@app.route('/api/live_data')
def api_live_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, value FROM sensor_data ORDER BY id DESC LIMIT 10;')
    maalinger = cur.fetchall()
    cur.close()
    conn.close()
    
    data_liste = []
    for m in maalinger:
        data_liste.append({
            "id": m[0],
            "value": m[1]
        })
        
    return jsonify(data_liste)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if (username == 'jones' and password == 'admin123') or \
           (username == 'adam' and password == 'admin123') or \
           (username == 'admin' and password == 'admin'):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Forkert brugernavn eller kodeord!'
            
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/historik')
def historik():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
        

    

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM sensor_data ORDER BY id DESC;') 
    alt_data = cur.fetchall()
    cur.close(); conn.close()
        
    return render_template('historik.html', maalinger=alt_data, username=session['username'])

@app.route('/data', methods=['POST'])
def recieve_data():
    content = request.json
    sensor_val = content.get('value')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO sensor_data (value) VALUES (%s)', (sensor_val,))
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"--- MODTAGET DATA FRA SIMULERING: {sensor_val} ---")
    return jsonify({"status": "succes", "received": sensor_val}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
