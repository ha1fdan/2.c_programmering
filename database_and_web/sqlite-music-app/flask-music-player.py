from flask import Flask, g, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "jf2389qhudn27617uedik9012o"

## TODO
# [*] List all albums 
#
# [*] Create view to list tracks on albums  (e.g. /albums/2 to view album with id 2)
#
# [*] list_artist_albums.html should create links to list tracks on albums (see 2.)
#
# [*] The search functionality only searches artists, extend so tracks and albums are searched as well.
#
# [ ] Use the technique from flask-htmx-demo.py to make the search functionality more responsive.
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
    return redirect(url_for("list_artists"))


@app.route("/search")
def search():
    query = request.args.get('query') 
    db = get_db()
    cur = db.execute("SELECT Track.Name AS TrackName, Track.TrackId AS TrackId, Album.Title AS AlbumTitle, Album.AlbumId AS AlbumId, Artist.Name AS ArtistName, Artist.ArtistId AS ArtistId FROM Track JOIN Album ON Track.AlbumId = Album.AlbumId JOIN Artist ON Album.ArtistId = Artist.ArtistId WHERE Track.Name LIKE ? OR Album.Title LIKE ? OR Artist.Name LIKE ?", (f"%{query}%", f"%{query}%", f"%{query}%"))
    results = cur.fetchall()
    if not results:
        flash("No results found")
    return render_template("search.html", query = query, results=results)

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
    cur = db.execute('SELECT * FROM Album;')
    albums = cur.fetchall()
    return render_template('list_albums.html', albums=albums)

@app.route("/tracks")
def list_all_tracks():
    db = get_db()
    cur = db.execute('SELECT * FROM Track;')
    tracks = cur.fetchall()
    return render_template('list_all_tracks.html', tracks=tracks)

@app.route("/album/<album_id>")
def list_tracks_on_album(album_id):
    print(f"album_id: {album_id}")
    try:
        album_id = str(album_id)
    except ValueError:
        flash("Invalid album ID")
        return redirect(url_for("list_albums"))
    db = get_db()
    cur = db.execute('SELECT Track.Name AS TrackName, Duration, Audio, Album.Title AS AlbumTitle, Cover, Release, Artist.Name AS ArtistName FROM Track JOIN Album ON Track.AlbumId = Album.AlbumId JOIN Artist ON Album.ArtistId = Artist.ArtistId WHERE Track.AlbumId = ?;', (album_id,))
    tracks = cur.fetchall()
    #│ TrackName │ Duration │ Audio │ AlbumTitle │ Cover │ Release │ ArtistName │
    return render_template('list_tracks_on_album.html', tracks=tracks)

@app.route("/artist/<artist_id>")
def list_artist_albums(artist_id):
    db = get_db()
    cur = db.execute('SELECT * FROM Album WHERE ArtistId=?', (artist_id,))
    albums = cur.fetchall()

    cur = db.execute('SELECT * FROM Artist WHERE ArtistId=?', (artist_id,))
    artist = cur.fetchone()

    return render_template('list_artist_albums.html', artist=artist, albums=albums)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
