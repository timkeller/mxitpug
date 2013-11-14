import requests
import json
from flask import Flask, render_template
from StringIO import StringIO
import os
import hashlib

app = Flask(__name__)

user_agent = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.25 (KHTML, like Gecko) Chrome/12.0.706.0 Safari/534.25"
pug_file_sizes = {}

def getPug():
    
    # Fetch a pug from the API
    r = requests.get("http://pugme.herokuapp.com/random", headers={'User-agent': user_agent})
    parsed = json.loads(r.text)
    pug_url = parsed['pug']

    # Ensure the file size is below 100kb
    if not pug_url in pug_file_sizes.keys():
        filename = "/tmp/"+hashlib.sha224(pug_url).hexdigest()
        with open(filename, 'wb') as handle:
            response = requests.get(pug_url)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

        pug_file_sizes[pug_url] = os.stat(filename).st_size
        os.remove(filename)

    if pug_file_sizes[pug_url] < 100000:
        print "File Size OK: %s is %s bytes" % (pug_url, pug_file_sizes[pug_url])
        return pug_url
    else:
        print "File Too large: %s is %s bytes" % (pug_url, pug_file_sizes[pug_url])
        return getPug()

@app.route("/")
def index():
    img_src = getPug()
    return render_template('pug.html', image=img_src)

if __name__ == "__main__":
    app.run(debug=True)