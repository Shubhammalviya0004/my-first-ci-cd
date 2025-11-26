
from flask import Flask, render_template, request, redirect, url_for , flash
from pymongo import MongoClient


app = Flask(__name__)

app.secret_key = 'Shubham@123'

client = MongoClient('mongodb://localhost:27017')
db = client['employee_db'] 
collection = db['employees']  

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'insert' in request.form:
            duplicate_id = collection.find_one({"empid": request.form['empid']})
            if not duplicate_id:
                # Insert operation
                data = {"empid": request.form['empid'],'name': request.form['name'], 'designation': request.form['designation']}
                collection.insert_one(data)
                return redirect(url_for('index'))
            else:
                flash('Duplicate empid','dupicated')
                return redirect(url_for('index'))

        elif 'update' in request.form:
            #  Update operation
            document_id = request.form['empid']
            new_name = request.form['name']
            new_designation = request.form['designation']
       
            # Update 
            if document_id:
                collection.update_one(
                    {'empid': document_id},
                    {'$set': {'name': new_name, 'designation': new_designation}}
                )
            return redirect(url_for('index'))

        elif 'delete' in request.form:
            #  Delete operation
            document_id = request.form['empid']
            
            # Delete 
            if document_id:
                collection.delete_one({'empid': document_id})
            return redirect(url_for('index'))

    #  Show All Data 
    all_data = list(collection.find())
    return render_template('index.html', data=all_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


