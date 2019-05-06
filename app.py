# imports
from flask import Flask, render_template,redirect
import pymongo
import scrape

# create instance of Flask app
app = Flask(__name__)

# create mongo connection
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data_entries

@app.route("/")
def home():
    mars_data = list(db.collection.find())[0]
    return  render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def web_scrape():
    db.collection.remove({})
    mars_data = scrape.scrape()
    #print('----after getting data---')
    #print(mars_data)
    db.collection.insert_one(mars_data)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)