from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
import time

app = Flask(__name__)
app.secret_key = 'Shubham@123'

# MongoDB Connection
mongo_url = os.getenv("MONGO_URI", "mongodb://mongodb:27017/employee_db")
client = None

# Wait for MongoDB to be ready
while True:
    try:
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("MongoDB connected!")
        break
    except ServerSelectionTimeoutError:
        print("Waiting for MongoDB...")
        time.sleep(2)

db = client['employee_db']
collection = db['employees']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'insert' in request.form:
            duplicate_id = collection.find_one({"empid": request.form['empid']})
            if not duplicate_id:
                data = {
                    "empid": request.form['empid'],
                    'name': request.form['name'],
                    'designation': request.form['designation']
                }
                collection.insert_one(data)
                return redirect(url_for('index'))
            else:
                flash('Duplicate empid', 'duplicate')
                return redirect(url_for('index'))

        elif 'update' in request.form:
            document_id = request.form['empid']
            new_name = request.form['name']
            new_designation = request.form['designation']
            if document_id:
                collection.update_one(
                    {'empid': document_id},
                    {'$set': {'name': new_name, 'designation': new_designation}}
                )
            return redirect(url_for('index'))

        elif 'delete' in request.form:
            document_id = request.form['empid']
            if document_id:
                collection.delete_one({'empid': document_id})
            return redirect(url_for('index'))

    all_data = list(collection.find())
    return render_template('index.html', data=all_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
