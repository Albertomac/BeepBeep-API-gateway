from flask import Blueprint, render_template, url_for
from stravalib import Client

from monolith.database import db, Run
from monolith.auth import current_user

home = Blueprint('home', __name__)


def _strava_auth_url(config):
    client = Client()
    client_id = config['STRAVA_CLIENT_ID']
    redirect = 'http://127.0.0.1:5000/strava_auth'
    url = client.authorization_url(client_id=client_id,
                                   redirect_uri=redirect)
    return url


@home.route('/')
def index():
    total_average_speed = None
    if current_user is not None and hasattr(current_user, 'id'):
        runs = db.session.query(Run).filter(Run.runner_id == current_user.id)
        if runs.count():
            total_average_speed = sum(run.average_speed for run in runs) / runs.count()
            total_average_speed = float('%.2f' % total_average_speed)

    else:
        runs = None
    strava_auth_url = _strava_auth_url(home.app.config)
    return render_template("index.html", runs=runs,
                           strava_auth_url=strava_auth_url,
                           total_average_speed=total_average_speed)
