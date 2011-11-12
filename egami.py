#!/usr/bin/env python

# Egami: a very simple image gallery built using Flask, which
# serves image files found in the directory where it is executed.
# Copyright (C) 2011 Francois Lebel <francoislebel@gmail.com>
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

from flask import Flask, send_from_directory
from jinja2 import Template
import glob
import json
import os


# Look for files with an image extension (case insensitive.)
# Note that glob does not support regular expressions, hence the duplications.
IMAGE_EXTENSIONS = ('[gG][iI][fF]', '[jJ][pP][gG]', '[jJ][pP][eE][gG]', '[pP][nN][gG]')

# Directory from which to serve the images. Must end with a forward slash.
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
                    if (index < 0 || index > images.length - 1) {
                        return;
                    }
                    $('a.current').attr('href', '{{images_url}}' + images[index]);
                    $('img.current').attr('alt', images[index]);
                    $('img.current').attr('src', '{{images_url}}' + images[index]);
                    $('p#status').text("Now serving image " + (index + 1) + " of {{number_images}} image(s) from '{{cwd}}'.");
                    currentIndex = index;
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
                    changeImage(currentIndex - 1);
                });

                $('button#next').click(function(e) {
                    e.preventDefault();
                    changeImage(currentIndex + 1);
                });

                $('button#last').click(function(e) {
                    e.preventDefault();
                    changeImage(images.length - 1);
                });
            });
        //]]>
        </script>
        <style type="text/css">
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
            <button id="next">Next</button>
            <button id="last">Last</button>
            <hr/>
        </div>
        <div id="content">
            <p id="status"></p>
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

