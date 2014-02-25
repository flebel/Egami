#!/usr/bin/env python

# Egami: a very simple image gallery built using Flask, which
# serves image files found in the directory where it is executed.
# Copyright (C) 2011-2014 Francois Lebel <francoislebel@gmail.com>
# http://github.com/flebel/egami
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import glob
import json
import os

from flask import Flask, send_from_directory
from jinja2 import Template

# Look for files with an image extension (case insensitive.)
# Note that glob does not support regular expressions, hence the duplications.
IMAGE_EXTENSIONS = ('[gG][iI][fF]', '[jJ][pP][gG]', '[jJ][pP][eE][gG]', '[pP][nN][gG]')

# Path from where images are served. Must end with a forward slash.
IMAGES_URL = '/images/'

HTML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>{{cwd}}</title>
        <script src="http://www.google.com/jsapi" type="text/javascript"></script>
        <script type="text/javascript" charset="utf-8">
            google.load("jquery", "1.7.0");
        </script>
        <script type="text/javascript">
        //<![CDATA[
            $(document).ready(function() {
                var images = {{images}};
                var currentIndex = images.length - 1;

                function changeImage(index) {
                    validIndex = getValidIndex(index);
                    $('a.current').attr('href', '{{images_url}}' + images[validIndex]);
                    $('img.current').attr('alt', images[validIndex]);
                    $('img.current').attr('src', '{{images_url}}' + images[validIndex]);
                    $('span.status').text("Now serving image " + (validIndex + 1) + " of {{number_images}} image(s) from '{{cwd}}':");
                    $('span.filename').text(images[validIndex]);
                    currentIndex = validIndex;
                }

                function getValidIndex(index) {
                    if (index < 0) {
                        index = 0;
                    }
                    if (index > images.length - 1) {
                        index = images.length - 1;
                    }
                    return index;
                }

                function preloadImage(index) {
                    validIndex = getValidIndex(index);
                    $('<img />').attr('src', '{{images_url}}' + images[validIndex]).appendTo('body').hide();
                }

                // Initially set the current image to the last one
                if (images.length > 0) {
                    changeImage(currentIndex);
                } else {
                    $('img.current').hide();
                }

                $('button#first').click(function(e) {
                    e.preventDefault();
                    changeImage(0);
                });

                $('button#previous').click(function(e) {
                    e.preventDefault();
                    var offset = parseInt($('#offset').val());
                    changeImage(currentIndex - offset);
                    // Preload the previous image according to the (new) current position
                    preloadImage(currentIndex - offset);
                });

                $('button#next').click(function(e) {
                    e.preventDefault();
                    var offset = parseInt($('#offset').val());
                    changeImage(currentIndex + offset);
                    // Preload the next image according to the (new) current position
                    preloadImage(currentIndex + offset);
                });

                $('button#last').click(function(e) {
                    e.preventDefault();
                    changeImage(images.length - 1);
                });

                $('button#preload').click(function(e) {
                    e.preventDefault();
                    var offset = parseInt($('#offset').val());
                    for (var i = currentIndex, n = images.length; i < n; i += offset) {
                        preloadImage(i);
                    }
                });
            });
        //]]>
        </script>
        <style type="text/css">
            button, select {
                height: 50px;
                margin-right: 20px;
            }
            select#offset {
                width: 50px;
            }
            img.current {
                max-height: 640px;
                max-width: 640px;
            }

            img.thumb {
                max-height: 150px;
                max-width: 150px;
            }
        </style>
    </head>
    <body>
        <div id="nav">
            <button id="first">First</button>
            <button id="previous">Previous</button>
            <select id="offset">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
            </select>
            <button id="next">Next</button>
            <button id="last">Last</button>
            <button id="preload">Preload next images</button>
            <hr/>
        </div>
        <div id="content">
            <p><span class="status"></span> <span class="filename"></span></p>
            <a class="current" href=""><img alt="" class="current" src=""/></a>
        </div>
    </body>
</html>"""

app = Flask(__name__)

def get_images():
    files = []
    for extension in IMAGE_EXTENSIONS:
        files.extend(glob.glob("*.%s" % extension))
    files.sort()
    return files

@app.route('/')
def album():
    images = get_images()
    template = Template(HTML)
    return template.render(cwd = os.getcwdu(),
                           images = json.dumps(images),
                           images_url = IMAGES_URL,
                           number_images = len(images))

@app.route(IMAGES_URL + '<filename>')
def images(filename):
    return send_from_directory(os.getcwdu(), filename)

if __name__ == '__main__':
    #app.debug = True
    app.run(port=1235)

