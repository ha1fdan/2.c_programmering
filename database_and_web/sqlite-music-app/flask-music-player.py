from flask import Flask, g, render_template, request, redirect, url_for, flash, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "jf2389qhudn27617uedik9012o"

# The audio files have no file extension, so Flask's static handler can't
# guess their type and serves them as application/octet-stream, which makes
# <audio> unreliably sniff duration/seekability. Serve them with the correct
# Content-Type explicitly instead.
@app.route("/static/audio/<path:filename>")
def audio_file(filename):
    return send_from_directory(
        os.path.join(app.static_folder, "audio"), filename, mimetype="audio/ogg"
    )

## TODO
# [*] List all albums 
#
# [*] Create view to list tracks on albums  (e.g. /albums/2 to view album with id 2)
#
# [*] list_artist_albums.html should create links to list tracks on albums (see 2.)
#
# [*] The search functionality only searches artists, extend so tracks and albums are searched as well.
#
# [*] Use the technique from flask-htmx-demo.py to make the search functionality more responsive.
#
# [ ] Add a login system to protect the playing of music
#
# [ ] Add playlists (hint: requires a join table)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("music.db")
        g.db.row_factory = sqlite3.Row
        g.db.set_trace_callback(print)
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    db = get_db()
    artist_count = db.execute("SELECT COUNT(*) FROM Artist").fetchone()[0]
    album_count = db.execute("SELECT COUNT(*) FROM Album").fetchone()[0]
    track_count = db.execute("SELECT COUNT(*) FROM Track").fetchone()[0]
    featured_albums = db.execute(
        "SELECT Album.AlbumId, Album.Title, Album.Cover, Artist.Name AS ArtistName "
        "FROM Album JOIN Artist ON Album.ArtistId = Artist.ArtistId "
        "ORDER BY RANDOM() LIMIT 6"
    ).fetchall()
    return render_template(
        "home.html",
        artist_count=artist_count,
        album_count=album_count,
        track_count=track_count,
        featured_albums=featured_albums,
    )


@app.route("/search")
def search():
    query = request.args.get('query') 
    db = get_db()
    cur = db.execute("SELECT Track.Name AS TrackName, Track.TrackId AS TrackId, Album.Title AS AlbumTitle, Album.AlbumId AS AlbumId, Artist.Name AS ArtistName, Artist.ArtistId AS ArtistId FROM Track JOIN Album ON Track.AlbumId = Album.AlbumId JOIN Artist ON Album.ArtistId = Artist.ArtistId WHERE Track.Name LIKE ? OR Album.Title LIKE ? OR Artist.Name LIKE ?", (f"%{query}%", f"%{query}%", f"%{query}%"))
    results = cur.fetchall()
    if not results:
        flash("No results found")
    return render_template("search.html", query = query, results=results)

@app.route("/search/live")
def search_live():
    query = request.args.get('query', default='').strip()
    results = []
    if query:
        db = get_db()
        cur = db.execute("SELECT Track.Name AS TrackName, Track.TrackId AS TrackId, Album.Title AS AlbumTitle, Album.AlbumId AS AlbumId, Artist.Name AS ArtistName, Artist.ArtistId AS ArtistId FROM Track JOIN Album ON Track.AlbumId = Album.AlbumId JOIN Artist ON Album.ArtistId = Artist.ArtistId WHERE Track.Name LIKE ? OR Album.Title LIKE ? OR Artist.Name LIKE ? LIMIT 8", (f"%{query}%", f"%{query}%", f"%{query}%"))
        results = cur.fetchall()
    return render_template("_search_results.html", query=query, results=results)

@app.route("/artists")
def list_artists():
    db = get_db()
    cur = db.execute('SELECT * FROM Artist')
    artists = cur.fetchall()

    return render_template('list_artists.html',artists=artists)

# A view (route decorator + function def)
@app.route("/albums")
def list_albums():
    db = get_db()
    cur = db.execute(
        'SELECT Album.AlbumId, Album.Title, Album.Cover, Artist.Name AS ArtistName '
        'FROM Album JOIN Artist ON Album.ArtistId = Artist.ArtistId '
        'ORDER BY Album.Title;'
    )
    albums = cur.fetchall()
    return render_template('list_albums.html', albums=albums)

@app.route("/tracks")
def list_all_tracks():
    db = get_db()
    cur = db.execute(
        'SELECT Track.TrackId, Track.Name AS TrackName, Track.Duration, Track.Audio, '
        'Album.AlbumId, Album.Title AS AlbumTitle, Album.Cover, Artist.Name AS ArtistName '
        'FROM Track '
        'JOIN Album ON Track.AlbumId = Album.AlbumId '
        'JOIN Artist ON Album.ArtistId = Artist.ArtistId '
        'ORDER BY Track.Name;'
    )
    tracks = cur.fetchall()
    return render_template('list_all_tracks.html', tracks=tracks)

@app.route("/album/<album_id>")
def list_tracks_on_album(album_id):
    db = get_db()
    cur = db.execute('SELECT Track.Name AS TrackName, Duration, Audio, Album.Title AS AlbumTitle, Cover, Release, Artist.Name AS ArtistName, Artist.ArtistId AS ArtistId FROM Track JOIN Album ON Track.AlbumId = Album.AlbumId JOIN Artist ON Album.ArtistId = Artist.ArtistId WHERE Track.AlbumId = ?;', (album_id,))
    tracks = cur.fetchall()
    #│ TrackName │ Duration │ Audio │ AlbumTitle │ Cover │ Release │ ArtistName │ ArtistId │
    if not tracks:
        flash(f"No album found with id {album_id!r}")
        return redirect(url_for("list_albums"))
    return render_template('list_tracks_on_album.html', tracks=tracks)

@app.route("/artist/<artist_id>")
def list_artist_albums(artist_id):
    db = get_db()
    cur = db.execute('SELECT * FROM Artist WHERE ArtistId=?', (artist_id,))
    artist = cur.fetchone()
    if artist is None:
        flash(f"No artist found with id {artist_id!r}")
        return redirect(url_for("list_artists"))

    cur = db.execute('SELECT * FROM Album WHERE ArtistId=?', (artist_id,))
    albums = cur.fetchall()

    return render_template('list_artist_albums.html', artist=artist, albums=albums)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
