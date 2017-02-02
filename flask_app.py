#!/usr/bin/env python
#
# Date: Feb-01-2017
# Author: somnath.banerjee

from flask import Flask
from flask import request
from flask import render_template

import os
import urlparse
import gcloud_analysis

app = Flask(__name__)

@app.route("/api", methods=["POST", "GET"])
def hello():
    image_url = None
    if request.method == "GET":
        image_url = request.args.get('image_url', '')

    if not image_url:
        return render_template("input.html")

    # check if valid URL
    error_msg = None
    tks = urlparse.urlparse(image_url)
    if not tks.scheme or not tks.path:
        error_msg = "Not a valid url {}".format(image_url)
        return render_template("input.html", error_msg=error_msg)

    # check if supported image format
    supported_format = False
    base_url = "{}://{}{}".format(tks.scheme, tks.netloc, tks.path)
    exts = ["jpeg", "jpg", "png", "webp"]
    for e in exts:
        if base_url.endswith(e):
            supported_format = True

    if not supported_format:
        error_msg = "Not a supported image format %s" % image_url
        return render_template("input.html", error_msg=error_msg)

    image_file = os.path.basename(tks.path)
    prefix = os.path.splitext(image_file)[0]
    gcloud_analysis.analyze_image_url(image_url, image_file, prefix)

    return render_template("input.html", image_url=image_url, prefix=prefix,
                           image_file=image_file, error_msg=error_msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
