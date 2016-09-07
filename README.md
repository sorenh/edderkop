Web crawler

[See it live on Heroku!](http://edderkop.herokuapp.com/)

("edderkop" is the Danish word for "spider")

[![Travis-CI Status](https://travis-ci.org/sorenh/edderkop.svg)](https://travis-ci.org/sorenh/edderkop)
[![codecov.io](https://codecov.io/github/sorenh/edderkop/coverage.svg?branch=master)](https://codecov.io/github/sorenh/edderkop?branch=master)

The easiest way to run it is with Docker:

    docker run sorenh/edderkop

Add a URL at the end:

    docker run sorenh/edderkop http://www.linux2go.dk/

...and you'll get a nice graph that you can use with Graphviz.

Example:

    docker run sorenh/edderkop http://www.linux2go.dk/ > linux2go.dot
    graphviz -Tx11 linux2go.dot

Any other output format from Graphviz works, too.

Alternatively, you can use the web based crawler which updates in real time:

    docker run -p 5000:5000 sorenh/edderkop web

TODO:

 *  Differentiate nodes based on whether they're images, links, scripts, etc.
 * Fetch images and include them in the output from Graphviz
