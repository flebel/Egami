=====
Egami
=====
Egami is a very simple image gallery which serves image files located in the
directory where it is run.

Goals
=====
- Do not require the configuration of a web server
- Keep everything* contained within a single file
- Lazy load images
- Support a very large number of files

Limitations
===========
- Does not create thumbnails of the images, but resizes them in the browser
- Serves files from a single directory and does not perform recursion
- Supports GIF, JPG, JPEG and PNG file extensions only

Usage
=====
#. Install Flask
#. Execute the script in the directory where the images to serve are located
#. Browse to http://127.0.0.1:1235

