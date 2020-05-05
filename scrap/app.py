from webscrap import all_details
from flask import Flask
from flask import request,url_for,render_template,flash,redirect
import os
import secrets
app=Flask(__name__)

app.secret_key=os.environ.get('APP_SECRET_KEY')


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webscrap',methods=['GET','POST'])
def webscrap():
    link=0
    for file in os.scandir("static/"):
        os.remove(file)

    df='Search products to get data here....'
    if request.method=="POST":
        search_string=request.form['search'] 
        df=all_details(search_string)
        
        if len(df)==0:
            df='Search products to get data here....'
            flash('No Results Found','danger')
            return redirect(url_for('index'))
        else:
            random=secrets.token_hex(10)
            df.to_csv(f'static/comments{random}.csv')
            link=url_for('static',filename=f'comments{random}.csv')

    if type(df)!=str:
        
        df=df.to_html()
    return render_template('index.html',df=df,link=link)

    

if __name__=='__main__': 
   
    app.run()