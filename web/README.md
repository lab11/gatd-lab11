GATD Web Pages
==============

These webpages display data from GATD.

View the demos live at http://gatd.eecs.umich.edu/

Install
-------

gatd-web uses [bower](http://bower.io/) to get all the required javascript
files needed to view the pages. The included `bower.json` file has all of the
dependencies and to get them simply:

    bower install

If the webpages can't find javascript files, it's likely that something in
bower-land is broken. My suggestion? Removed the `bower_components` folder
and re-run `bower install`.

The `run.py` script needs some python packages:

    pip3 install -r requirements.pip

Build & Debug
-------------

Once you have the dependencies installed, you can build (and serve) the site
using the `run.py` script. By default, the script will

1. Update bower
2. Build the site
3. Start a webserver at localhost:8000
4. Monitor the source for changes and automatically re-build (goto 2)

The script accepts a few options:
* `--no-bower`: Don't update the bower dependencies
* `--debug`: Run a local webserver
* `--monitor`: Track filesystem changes and re-build the website
