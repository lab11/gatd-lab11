GATD Web Pages
==============

These webpages display data from GATD.

View the demos live at http://inductor.eecs.umich.edu/

Install
-------

gatd-web uses [bower](http://bower.io/) to get all the required javascript
files needed to view the pages. The included `bower.json` file has all of the
dependencies and to get them simply:

    bower install

Currently, leaflet doesn't quite work right, so you need to build that one
yourself.

    cd bower_components/leaflet
    npm install
    sudo npm install -g jake
    jake

If the webpages can't find javascript files, it's likely that something in
bower-land is broken. My suggestion? Removed the `bower_components` folder
and re-run `bower install`.

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
* `--once`: Just build the site (useful for a deploy hook, e.g. in response to a git push)
