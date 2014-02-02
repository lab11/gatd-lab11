GATD Web Pages
==============

These webpages display data from GATD.

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
    npm install -g jake
    jake