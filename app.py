import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

todos = [{
    "id": 1,
    "title": 'todo1',
    "completed": True
}, {
    "id": 2,
    "title": 'todo2',
    "completed": False
}]

conn = sqlite3.connect(r"todos.db", check_same_thread=False)
c = conn.cursor()
c.execute(
    """
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title text,
        completed bool
    )
    """
)
conn.commit()
c.close()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/v1/todos', methods=['GET'])
def get_todo_list():
    return jsonify(todos)


@app.route('/api/v1/todos/<int:id>', methods=['GET'])
def get_todo_by_id(id):
    c1 = conn.cursor()
    query = "select * from todos where id = :id"
    c1.execute(query, {"id": id})
    result = c1.fetchone()
    founded_todo = {
        "id": result[0],
        "title": result[1],
        "completed": result[2]
    }
    return jsonify(founded_todo)


@app.route('/api/v1/todos', methods=['POST'])
def create_todo():
    print(request.json)
    str(request.json["completed"])
    query = "insert into todos ('title', 'completed') values (:title, :completed)"
    c1 = conn.cursor()
    c1.execute(query, {"title": request.json["title"], "completed": request.json["completed"]})
    conn.commit()

    request.json["id"] = c1.lastrowid

    return jsonify(request.json)


@app.route('/api/v1/todos/<int:id>', methods=['PUT'])
def update_todo_by_id(id):
    return str(request.json["completed"])


@app.route('/api/v1/todos/<int:id>', methods=['DELETE'])
def delete_todo_by_id(id):
    return str(id)


if __name__ == '__main__':
    app.run()
