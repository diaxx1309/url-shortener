from flask import Flask,render_temple,request,redirect
import string,random

app=Flask(__name__)

urls={}
def generate_short():
    return''.join(random.choices(string.ascii_letters+string.digits,k=6))

@app.route('/',methods=['GET','POST'])
def index():
        short_url=None
        if request.method=='post':
              long_url=request.form['long_url']
              code= generate_short()
              urls[code]=long_urlshort_url=request.host_url +code
        return render_template('index.html',short_url=short_url)

@app.route('/<code>')
def redirect_url(code):
      long_url=urls.get(code)
      if long_url:
            return redirect(long_url)
      return "URL NOT FOUND",404

if __name__ =='__main__': 
    app.run(debug=True)