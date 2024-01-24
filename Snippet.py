from flask import Flask, jsonify, request
import sqlite3
app = Flask(__name__)

conn = sqlite3.connect('Snippets-db.db')
cursor = conn.cursor()
"""
cursor.execute('''CREATE TABLE "snip" (
	"id"	TEXT NOT NULL,
	"language"	TEXT NOT NULL,
	"code"	TEXT NOT NULL,
);''')


snippets = [
    (1, "Python", "print('Hello, World!')"),
    (2, "Python", "def add(a, b):\n    return a + b"),
    (3, "Python", "class Circle:\n    def __init__(self, radius):\n        self.radius = radius\n\n    def area(self):\n        return 3.14 * self.radius ** 2"),
    (4, "JavaScript", "console.log('Hello, World!');"),
    (5, "JavaScript", "function multiply(a, b) {\n    return a * b;\n}"),
    (6, "JavaScript", "const square = num => num * num;"),
    (7, "Java", "public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}"),
    (8, "Java", "public class Rectangle {\n    private int width;\n    private int height;\n\n    public Rectangle(int width, int height) {\n        this.width = width;\n        this.height = height;\n    }\n\n    public int getArea() {\n        return width * height;\n    }\n}")
]

# Insert data into the 'snip' table
cursor.executemany('INSERT OR IGNORE INTO snip VALUES (?, ?, ?)', snippets)

# Commit the changes and close the connection
conn.commit()
conn.close()
"""
cursor.execute("SELECT * FROM snip")
snippets = cursor.fetchall()

print(snippets)

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(snippets)


@app.route('/snippets', methods=['POST'])
def create_snippet():
    new_snippet = request.json
    new_snippet['id'] = len(snippets) + 1
    cursor.execute("INSERT INTO snip (id, language, code) VALUES (?, ?, ?)",(new_snippet['id'],new_snippet['language'],new_snippet['code']))
    return jsonify(new_snippet), 201

@app.route('/snippets', methods=['GET'])
def get_all_snippets():
    return jsonify(snippets)

@app.route('/snippets/<int:id>', methods=['GET'])
def get_snippet(id):
    snippet = next((s for s in snippets if s['id'] == id), None)
    if snippet:
        return jsonify(snippet)
    else:
        return jsonify({"error": "Snippet not found"}), 404

@app.route('/snippets/<string:lang>', methods=['GET'])
def get_snippets_by_language(lang):
    filtered_snippets = [s for s in snippets if s['language'].lower() == lang.lower()]
    return jsonify(filtered_snippets)

if __name__ == '__main__':
    app.run(debug=True, port=3000)

