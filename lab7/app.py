from flask import Flask, request, render_template, redirect
import sqlite3

attempts = 0
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    global attempts
    stu = sqlite3.connect('creds.db')
    cur = stu.cursor()
    cur.execute(
        'create table if not exists creds (u_name varchar(255), pass varchar(255));')
    stu.commit()

    if(request.method == 'POST'):

        u_name = request.form['username']
        u_pass = request.form['password']
        print(u_name, u_pass)
        upper = any(ele.isupper() for ele in u_pass)
        lower = any(ele.islower() for ele in u_pass)
        num = any(ele.isnumeric() for ele in u_pass)
        upper_u = any(ele.isupper() for ele in u_name)
        lower_u = any(ele.islower() for ele in u_name)
        num_u = any(ele.isnumeric() for ele in u_name)

        if(upper and lower and num and upper_u and lower_u and num_u):
            attempts = 0
            cur.execute('insert into creds(u_name, pass) values(?,?)', [
                        str(u_name), str(u_pass)])
            stu.commit()
            return render_template('report.html', content=[upper, lower, num, upper_u, lower_u, num_u])
        else:
            attempts += 1
            if(attempts == 3):
                attempts = 0
                return render_template('index.html', content='3 times wrong')
            else:
                print(attempts)
                return render_template('report.html', content=[upper, lower, num, upper_u, lower_u, num_u])

    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():

    stu = sqlite3.connect('creds.db')


app.run(host='localhost', port=5000, debug=True)
