
#this conditional is only true if we run this script directly using python because python
#calls the script __main__
#if running through flask, remember to set environment variables:
# export FLASK_APP=flaskblog.py and
# export FLASK_DEBUG=1 to run in debug mode

from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)

