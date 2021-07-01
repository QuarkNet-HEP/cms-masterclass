import json

from flask import (
    Flask,
    render_template
)

from flask_bootstrap import (
    Bootstrap
)

app = Flask(__name__)
bootstrap = Bootstrap(app)

zh_events = json.load(
    app.open_resource('data/test.json')
)

print(
    zh_events
)

@app.route('/')
def index():
    return render_template(
        'index.html',
        title='CMS Masterclass',
    )

@app.route('/contents')
def contents():
    return render_template(
        'contents.html',
        title='Contents',
    )

@app.route('/introduction')
def introduction():
    return render_template(
        'introduction.html',
        title='Introduction',
    )

@app.route('/detector')
def detector():
    return render_template(
        'detector.html',
        title='Detector',
    )

@app.route('/events')
def events():
    return render_template(
        'events.html',
        title='Events',
        events=zh_events,
    )

@app.route('/events/<id>')
def event(id):
    return render_template(
        'event.html',
        title=f'Event {id}',
        nevents=len(zh_events),
        back_id=int(id)-1,
        next_id=int(id)+1,
        event=list(filter(lambda e: e["id"] == id, zh_events))[0],
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

