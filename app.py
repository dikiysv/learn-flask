import urllib
from flask import Flask, request
from threading import Timer
from IPython.display import display
from IPython.display import Javascript as JS

# XXX: Get this value from your Facebook application's settings for the OAuth flow
# at https://developers.facebook.com/apps

APP_ID = '' 

# This value is where Facebook will redirect. We'll configure an embedded
# web server to be serving requests here

REDIRECT_URI = 'http://localhost:5000/oauth_helper'

# You could customize which extended permissions are being requested for your app
# by adding additional items to the list below. See
# https://developers.facebook.com/docs/reference/login/extended-permissions/

EXTENDED_PERMS = ['user_likes']

# A temporary file to store a code from the web server

OAUTH_FILE = 'resources/ch02-facebook/access_token.txt'

# Configure an emedded web server that accepts one request, parses
# the fragment identifier out of the browser window redirects to another
# handler with the parsed out value in the query string where it can be captured
# and stored to disk. (A webserver cannot capture information in the fragment 
# identifier or that work would simply be done in here.)

webserver = Flask("FacebookOAuth")
@webserver.route("/oauth_helper")
def oauth_helper():
    return '''<script type="text/javascript">
    var at = window.location.hash.substring("access_token=".length+1).split("&")[0]; 
    setTimeout(function() { window.location = "/access_token_capture?access_token=" + at }, 1000 /*ms*/);
    </script>'''

# Parses out a query string parameter and stores it to disk. This is required because
# the address space that Flask uses is not shared with IPython Notebook, so there is really
# no other way to share the information than to store it to a file and access it afterward
@webserver.route("/access_token_capture")
def access_token_capture():
    access_token = request.args.get('access_token')
    f = open(OAUTH_FILE, 'w') # Store the code as a file
    f.write(access_token)
    f.close()
    
    # It is safe (and convenient) to shut down the web server after this request
    shutdown_after_request = request.environ.get('werkzeug.server.shutdown')
    shutdown_after_request()
    return access_token


# Send an OAuth request to Facebook, handle the redirect, and display the access
# token that's included in the redirect for the user to copy and paste
    
args = dict(client_id=APP_ID, redirect_uri=REDIRECT_URI,
            scope=','.join(EXTENDED_PERMS), type='user_agent', display='popup'
            )

oauth_url = 'https://facebook.com/dialog/oauth?' + urllib.parse.urlencode(args)

Timer(1, lambda: display(JS("window.open('%s')" % oauth_url))).start()


webserver.run(host='0.0.0.0')

access_token = open(OAUTH_FILE).read()

print(access_token)
