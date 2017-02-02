#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : May 19, 2016

import base64
import json
import os
import shutil
import urllib2
import urlparse

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

class GVImageAnalysis(object):

    def __init__(self):
        credentials = GoogleCredentials.get_application_default()
        self.gvision_service = discovery.build(
            'vision', 'v1', credentials=credentials,
            discoveryServiceUrl=DISCOVERY_URL)

    def analyze(self, image_file, max_results=5):
        with open(image_file) as f:
            image_content = f.read()
            image = base64.b64encode(image_content).decode('UTF-8')

        if not image:
            print "Image is not provided"
            return

        features = []
        request_types = ['LABEL_DETECTION', 'LOGO_DETECTION',
            'TEXT_DETECTION', 'IMAGE_PROPERTIES']
        for t in request_types:
            features.append({ 'type': t, 'maxResults': max_results})

        batch_request = [{
            'image': {
                'content': image
                },
            'features': features
        }]

        request = self.gvision_service.images().annotate(body={
            'requests': batch_request,
            })
        response = request.execute()
        response = response['responses'][0]

        self.labels = response.get('labelAnnotations', None)
        self.logos = response.get('logoAnnotations', None)
        self.colors = response['imagePropertiesAnnotation']['dominantColors']['colors']

        self.texts = None
        if 'textAnnotations' in response:
            text0 = response['textAnnotations'][0]
            self.texts = [{
                'locale': text0['locale'],
                'description' : text0['description'].replace('\n', '<br/>')
            }]

def write_json_to_file(json_data, filename):
    with open(filename, 'w') as f:
        if json_data:
            json.dump(json_data, f, indent=2)
        else:
            f.write("[]\n")

def analyze_image_url(image_url, image_file, prefix):
    outdirs = ["static/img", "static/data"]
    for o in outdirs:
        if not os.path.exists(o):
            os.makedirs(o)

    out_image = os.path.join("static/img", image_file)
    image = urllib2.urlopen(image_url)
    with open(out_image, 'w') as f:
        image_data = image.read()
        f.write(image_data)

    gv_image = GVImageAnalysis()
    gv_image.analyze(out_image)

    out_path = os.path.join("static/data/", prefix)
    write_json_to_file(gv_image.colors, out_path + "_colors.json")
    write_json_to_file(gv_image.labels, out_path + "_labels.json")
    write_json_to_file(gv_image.logos,  out_path + "_logos.json")
    write_json_to_file(gv_image.texts, out_path + "_texts.json")
