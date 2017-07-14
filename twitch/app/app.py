import sqlite3
from collections import OrderedDict
from flask import Flask, request, g, render_template, url_for, redirect, session

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['submit'] == 'Recommendations':
            return redirect(url_for('recommendations', name=request.form['name']))
        elif request.form['submit'] == 'Recommended To':
            return redirect(url_for('recommendedto', name=request.form['name']))
    else:
        return render_template('home.html')


@app.route('/recommendations/<name>')
def recommendations(name):
    db1 = getattr(g, 'db', None)
    if db1 is None:
        db1 = g.db1 = sqlite3.connect('twitch.db')
    cur = db1.execute("""SELECT rec10, rec9, rec8, rec7, rec6, rec5, rec4, rec3, rec2, rec1 \
                        FROM twitch WHERE name == ?""", [name])
    recs = cur.fetchall()
    cur.close()
    results = []
    for row in recs:
        for value in row:
            results.append(value)
    db2 = getattr(g, 'db', None)
    if db2 is None:
        db2 = g.db2 = sqlite3.connect('emotes.db')
    channels = OrderedDict()
    for i in xrange(len(results)):
    # for result in results:
        cur = db2.execute("""SELECT url, emote FROM emotes WHERE name == ?""", [results[i]])
        channel = cur.fetchall()
        channels[results[i]] = channel
    cur.close()
    db1.close()
    db2.close()
    test = []
    for key, value in channels.iteritems():
        test.append(value)
    return render_template('emotes.html', results=results, channels=channels)

@app.route('/recommendedto/<name>')
def recommendedto(name):
    db1 = getattr(g, 'db', None)
    if db1 is None:
        db1 = g.db1 = sqlite3.connect('twitch.db')
    cur = db1.execute("""SELECT name FROM twitch WHERE (rec1 == ? AND rec1 != name) \
                        OR (rec2 == ? AND rec2 != name) OR (rec3 == ? AND rec3 != name) \
                        OR (rec4 == ? AND rec4 != name) OR (rec5 == ? AND rec5 != name) \
                        OR (rec6 == ? AND rec6 != name) OR (rec7 == ? AND rec7 != name) \
                        OR (rec8 == ? AND rec8 != name) OR (rec9 == ? AND rec9 != name) \
                        OR (rec10 == ? AND rec10 != name)""",
                        [name, name, name, name, name, name, name, name, name, name])
    recs = cur.fetchall()
    cur.close()
    results = []
    for row in recs:
        for value in row:
            results.append(value)
    db2 = getattr(g, 'db', None)
    if db2 is None:
        db2 = g.db2 = sqlite3.connect('emotes.db')
    channels = OrderedDict()
    for i in xrange(len(results)):
    # for result in results:
        cur = db2.execute("""SELECT url, emote FROM emotes WHERE name == ?""", [results[i]])
        channel = cur.fetchall()
        channels[results[i]] = channel
    cur.close()
    db1.close()
    db2.close()
    test = []
    for key, value in channels.iteritems():
        test.append(value)
    return render_template('emotes.html', results=results, channels=channels)


@app.route('/example_channels')
def example_channels():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect('twitch.db')
    cur = db.execute("""SELECT name FROM twitch ORDER BY RANDOM() LIMIT 10""")
    rows = cur.fetchall()
    cur.close()
    results = []
    for row in rows:
        for value in row:
            results.append(value)
    return render_template('example_channels.html', results=results)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
