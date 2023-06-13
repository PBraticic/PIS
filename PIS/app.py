from flask import Flask, request, jsonify, render_template
from pony.orm import Database, Required, PrimaryKey, db_session, select, count
from flask_cors import CORS

app = Flask(__name__, template_folder='frontend')
CORS(app)

db = Database()
db.bind(provider='sqlite', filename='music.sqlite', create_db=True)


class Music(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    artist = Required(str)
    release_year = Required(int)
    genre = Required(str)
    track_list = Required(str)


db.generate_mapping(create_tables=True)

@app.route('/music', methods=['POST'])
@db_session
def add_music():
    data = request.get_json()
    music = Music(
        title=data['title'],
        artist=data['artist'],
        release_year=data['release_year'],
        genre=data['genre'],
        track_list=data['track_list']
    )
    db.commit()
    return jsonify(success=True, id=music.id)


@app.route('/music/<int:music_id>', methods=['GET'])
@db_session
def get_music(music_id):
    music = Music.get(id=music_id)
    if music is None:
        return {"error": "Music not found"}, 404
    return jsonify(
        id=music.id,
        title=music.title,
        artist=music.artist,
        release_year=music.release_year,
        genre=music.genre,
        track_list=music.track_list
    )


@app.route('/music/<int:music_id>', methods=['PUT'])
@db_session
def update_music(music_id):
    music = Music.get(id=music_id)
    if music is None:
        return {"error": "Music not found"}, 404
    data = request.get_json()
    music.title = data.get('title', music.title)
    music.artist = data.get('artist', music.artist)
    music.release_year = data.get('release_year', music.release_year)
    music.genre = data.get('genre', music.genre)
    music.track_list = data.get('track_list', music.track_list)
    return jsonify(success=True)


@app.route('/music/<int:music_id>', methods=['DELETE'])
@db_session
def delete_music(music_id):
    music = Music.get(id=music_id)
    if music is None:
        return {"error": "Music not found"}, 404
    music.delete()
    return jsonify(success=True)


@app.route('/musics', methods=['GET'])
@db_session
def get_musics():
    track_list_filter = request.args.get('track_list_filter')
    if track_list_filter:
        musics = select(m for m in Music if track_list_filter in m.track_list)[:]
    else:
        musics = select(m for m in Music)[:]
    musics_list = [m.to_dict() for m in musics]
    return jsonify(musics_list)


@app.route('/genres', methods=['GET'])
@db_session
def get_genres():
    genres = select(m.genre for m in Music).distinct()
    genres_list = [str(genre) for genre in genres]
    return jsonify(genres_list)


@app.route('/musics-per-genre', methods=['GET'])
@db_session
def get_musics_per_genre():
    musics_per_genre = {}
    genres = select(m.genre for m in Music).distinct()
    for genre in genres:
        music_count = count(m for m in Music if m.genre == genre)
        musics_per_genre[genre] = music_count
    return jsonify(musics_per_genre)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

