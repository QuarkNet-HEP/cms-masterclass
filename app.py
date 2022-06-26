import base64
import json
import urllib

import numpy as np

from flask import (
    Flask,
    render_template
)

from flask_bootstrap import (
    Bootstrap
)

from io import (
    BytesIO
)

from matplotlib.figure import (
    Figure
)

app = Flask(__name__)
bootstrap = Bootstrap(app)

h_events = json.load(
    app.open_resource('data/events.json')
)

masses = [e['m'] for e in h_events]

def make_hist(data=[],
              smh=False):
    
    rmin = 70
    rmax = 181
    nbins = 37
    
    M_hist = np.histogram(data, bins=nbins, range=(rmin,rmax))

    hist, bins = M_hist
    width = 1.0*(bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    xerrs = [width*0.5 for i in range(0, nbins)]
    yerrs = np.sqrt(hist)

    ttbar = np.array([
        0.00465086,0,0.00465086,
        0,0,0,0,0,0,0,0.00465086,
        0,0,0,0,0,0.00465086,
        0,0,0,0,0.00465086,
        0.00465086,0,0,0.0139526,
        0,0,0.00465086,0,0,0,
        0.00465086,0.00465086,
        0.0139526,0,0
    ])
    
    dy = np.array([
        0,0,0,0,0,
        0.354797,0.177398,2.60481,
        0,0,0,0,0,0,0,0,0,
        0.177398,0.177398,
        0,0.177398,
        0,0,0,0,0,0,0,0,0,0,0,
        0.177398,0,0,0,0
    ])
    
    zz = np.array([
        0.181215,0.257161,0.44846,0.830071,
        1.80272,4.57354,13.9677,14.0178,4.10974,
        1.58934,0.989974,0.839775,0.887188,0.967021,
        1.07882,1.27942,1.36681,1.4333,1.45141,1.41572,
        1.51464,1.45026,1.47328,1.42899,1.38757,
        1.33561,1.3075,1.29831,1.31402,1.30672,
        1.36442,1.39256,1.43472,1.58321,
        1.85313,2.19304,2.95083
    ])

    hzz = np.array([
        0.00340992,0.00450225,0.00808944,
        0.0080008,0.00801578,0.0108945,0.00794274,
        0.00950757,0.0130648,0.0163568,0.0233832,
        0.0334813,0.0427229,0.0738129,0.13282,0.256384,
        0.648352,2.38742,4.87193,0.944299,0.155005,
        0.0374193,0.0138906,0.00630364,0.00419265,
        0.00358719,0.00122527,0.000885718,0.000590479,
        0.000885718,0.000797085,8.86337e-05,0.000501845,
        8.86337e-05,0.000546162,4.43168e-05,8.86337e-05
    ])
    
    fig = Figure()
    ax = fig.subplots()

    data_bar = ax.errorbar(
        center, 
        hist, 
        xerr=xerrs, 
        yerr=yerrs, 
        linestyle='None', 
        color='black', 
        marker='o'
    )

    ttbar_bar = ax.bar(
        center, 
        ttbar, 
        align='center', 
        width=width, 
        color='gray', 
        linewidth=0, 
        edgecolor='b', 
        alpha=0.5
    )
    
    dy_bar = ax.bar(
        center,
        dy,
        align='center',
        width=width,
        color='g',
        linewidth=0,
        edgecolor='black',
        alpha=1,
        bottom=ttbar
    )

    zz_bar = ax.bar(
        center, 
        zz, 
        align='center', 
        width=width, 
        color='b', 
        linewidth=0, 
        edgecolor='black', 
        alpha=0.5,
        bottom=ttbar+dy
    )

    if smh == False:
        handles = [
            ttbar_bar,
            dy_bar,
            zz_bar,
            data_bar
        ]
        labels = [
            r'$\bf{t\bar{t}}$', 
            r'$\bf{Z/\gamma^{*} + X}$',
            r'$\bf{ZZ \rightarrow 4l}$',
            r'$\bf{Data}$'
        ] 
        
        ax.legend(
            handles,
            labels
        )

    else:
        hzz_bar = ax.bar(
            center, 
            hzz, 
            align='center', 
            width=width, 
            color='w', 
            linewidth=1, 
            edgecolor='r', 
            bottom=ttbar+dy+zz
        )

        handles = [
            ttbar_bar,
            dy_bar,
            zz_bar,
            hzz_bar,
            data_bar
        ]

        labels = [
            r'$\bf{t\bar{t}}$', 
            r'$\bf{Z/\gamma^{*} + X}$',
            r'$\bf{ZZ \rightarrow 4l}$', 
            r'$\bf{m_{H} = 125~GeV}$',
            r'$\bf{Data}$'
        ]
   
        ax.legend(
            handles,
            labels
        )
        
    ax.set_xlabel(r'$\bf{m_{4l}}$ [GeV]', fontsize=15)
    ax.set_ylabel(r'Events / 3 GeV', fontsize=15)
    ax.set_ylim(0,20)
    ax.set_xlim(80, 140)
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return img_data

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

    img_data = make_hist(
        data=[123.5],
        smh=False
    )
    
    return render_template(
        'events.html',
        title='Events',
        events=h_events,
        img_src=f"data:image/png;base64,{img_data}",
    )

@app.route('/events/<id>')
def event(id):
    
    smh = False
    
    if int(id) == 66:
        smh=True
    
    img_data = make_hist(
        data=masses[:int(id)],
        smh=smh
    )

    print(
        list(filter(lambda e: e["id"] == id, h_events))[0]
    )
    
    return render_template(
        'event.html',
        title=f'Event {id}',
        nevents=len(h_events),
        back_id=int(id)-1,
        next_id=int(id)+1,
        event=list(filter(lambda e: e["id"] == id, h_events))[0],
        img_src=f"data:image/png;base64,{img_data}",
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

