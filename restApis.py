from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
            database='cat_rescue',
            user='root',
            password='root'
    )
    return conn


# GET API to fetch all cats
@app.route('/api/cat', methods=['GET'])
def get_cats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cats")
    cats = cursor.fetchall()
    conn.close()
    return jsonify(cats)


# POST API to add a new cat
@app.route('/api/cat', methods=['POST'])
def add_cat():
    new_cat = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO cats (catname, ownername, gender, age, spayedneutered, vaccinated, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        new_cat['catname'], new_cat['ownername'], new_cat['gender'], 
        new_cat['age'], new_cat['spayedneutered'], 
        new_cat['vaccinated'], new_cat['status']
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cat added successfully!'}), 201


# PUT API to update spayed/neutered status of a cat by ID
@app.route('/api/cat/<int:id>', methods=['PUT'])
def update_cat(id):
    updated_status = request.get_json()['spayedneutered']
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE cats SET spayedneutered = %s WHERE id = %s"
    cursor.execute(query, (updated_status, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cat updated successfully!'})


# DELETE API to delete a cat by ID
@app.route('/api/cat/<int:id>', methods=['DELETE'])
def delete_cat(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM cats WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cat deleted successfully!'})


# Optional: Extra Credit - Update all columns of a cat record by ID
@app.route('/api/cat/update/<int:id>', methods=['PUT'])
def update_cat_all_columns(id):
    updated_cat = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE cats SET catname = %s, ownername = %s, gender = %s, age = %s, spayedneutered = %s,
    vaccinated = %s, status = %s WHERE id = %s
    """
    cursor.execute(query, (
        updated_cat['catname'], updated_cat['ownername'], updated_cat['gender'], 
        updated_cat['age'], updated_cat['spayedneutered'], updated_cat['vaccinated'], 
        updated_cat['status'], id
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cat updated successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
