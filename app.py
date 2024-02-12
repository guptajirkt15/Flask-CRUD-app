import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_user = os.environ.get('MYSQL_USER')



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = mysql_user
app.config['MYSQL_PASSWORD'] = mysql_password
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)


# Create a video
@app.route('/videos', methods=['POST'])
def create_video():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    views = 0  # Initial views

    if name and description:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO videos (name, description, views) VALUES (%s, %s, %s)", (name, description, views))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Video created successfully"}), 201
    else:
        return jsonify({"error": "Invalid data"}), 400

# Update a video
@app.route('/videos/<int:video_id>', methods=['PUT'])
def update_video(video_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')

    cur = mysql.connection.cursor()
    cur.execute("UPDATE videos SET name=%s, description=%s WHERE id=%s", (name, description, video_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Video updated successfully"}), 200

# Delete a video
@app.route('/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM videos WHERE id=%s", (video_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Video deleted successfully"}), 200

# List all videos
@app.route('/videos', methods=['GET'])
def list_videos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, description, views FROM videos")
    videos = cur.fetchall()
    cur.close()

    return jsonify({"videos": videos}), 200

# Get a video by ID
@app.route('/videos/<int:video_id>', methods=['GET'])
def get_video(video_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, description, views FROM videos WHERE id=%s", (video_id,))
    video = cur.fetchone()
    cur.close()

    if video:
        return jsonify({"video": video}), 200
    else:
        return jsonify({"error": "Video not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
