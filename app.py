from flask import Flask, request, render_template, redirect, url_for
from datetime import date
import random as rn
import sqlite3
import os

app = Flask(__name__)

@app.route("/")
def result():
    conn = sqlite3.connect('bill_management.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM month""")
    month = c.fetchall()
    conn.close()
    return render_template("index.html",month=month)

@app.route('/update/<int:mid>')
def update(mid):
    conn = sqlite3.connect('bill_management.db')
    c = conn.cursor()

    sql_query = f'SELECT billid,item,price FROM bills where mid={mid}'
    c.execute(sql_query)

    result = c.fetchall()

    total = sum(list(i[2] for i in result))
    conn.close()
    return render_template("result.html",result=result,mid=mid,total=total)
    
@app.route('/add',methods=['POST'])
def add():
    conn = sqlite3.connect('bill_management.db')
    c = conn.cursor()

    mid = request.form.get('mid')

    item = request.form.get('item')
    price = request.form.get('price')

    dt = str(date.today()).split("-")
    billid = str.join("",dt)+f'{mid}'+str(rn.randrange(10,100))

    sql_query = f"INSERT INTO bills VALUES ('{billid}',{mid},'{item}','{price}')"
    c.execute(sql_query)
    conn.commit()

    return redirect(url_for('update',mid=mid))

@app.route('/edit/<mid>/<billid>',methods=['GET','POST'])
def edit(mid,billid):
    if request.method == 'GET':
        conn = sqlite3.connect('bill_management.db')
        c = conn.cursor()

        sql_query = f'SELECT item,price FROM bills WHERE billid={billid}'
        c.execute(sql_query)
        bill = c.fetchall()
        conn.close()
        
        return render_template('edit.html',bill=bill,mid=mid)
    else:
        conn = sqlite3.connect('bill_management.db')
        c = conn.cursor()
                
        item = request.form.get('item')
        price = request.form.get('price')

        sql_query = f"UPDATE bills SET  item='{item}',price={price} WHERE billid={billid}"
        c.execute(sql_query)
        conn.commit()
        conn.close()
        
        return redirect(url_for('update',mid=mid))
   
@app.route('/delete/<mid>/<billid>',methods=['GET'])
def delete(mid,billid):
    conn = sqlite3.connect('bill_management.db')
    c = conn.cursor()
    
    sql_query = f'DELETE FROM bills where billid={billid}'
    c.execute(sql_query)
    conn.commit()
    conn.close()

    return redirect(url_for('update',mid=mid))

if __name__ == "__main__":
    # port = int(os.environ.get('PORT'))
    app.run(debug=True)