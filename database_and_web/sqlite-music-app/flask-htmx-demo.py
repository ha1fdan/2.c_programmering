from flask import Flask, render_template_string, request, g
import sqlite3

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("music.db")
        g.db.row_factory = sqlite3.Row
        g.db.set_trace_callback(print)
    return g.db


# https://htmx.org/examples/active-search/
template =\
"""
<!doctype html>
<title>HTMX DEMO</title>
<script src="{{ url_for('static', filename='htmx.min.js') }}"></script>
<h1>HTMX DEMO - ACTIVE SEARCH</h1>

<input type="search" name="query" 
       placeholder="Typing to search tracks ..." 
       hx-get="/search" 
       hx-trigger="input changed delay:200ms,search" 
       hx-target="#search-results">

<h2>Search results:</h2>
<ul id="search-results">
{% for t in tracks %}
<li>{{t['Name']}}</li>
{% else %}
<li> No results</li>
{% endfor %}
</ul>
"""

@app.route("/")
def search():
    return render_template_string(template)

@app.route("/search")
def search_backend():
    query = request.args.get('query', default=None)
    db = get_db()
    cur = db.execute("SELECT * FROM Track WHERE Name LIKE ?;", (f"%{query}%",))
    tracks = cur.fetchall()
    tmpl_search_res =\
    """
    {% for t in tracks %}
    <li>{{ t['Name'] }}</li>
    {% else %}
    <li>No results</li>
    {% endfor %}
    """
    return render_template_string(tmpl_search_res, tracks=tracks) 

if __name__ == "__main__":
    app.run()
