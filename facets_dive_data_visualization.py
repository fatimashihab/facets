#!/usr/bin/env python
import json
import pandas as pd

# Facets Dive settings. Inital layout of the visualized data.
PRESETS = {
    u'verticalFacet': u'BUY_JEWELRY',
    u'horizontalFacet': u'GENDER',
    u'verticalBuckets': 4,
    u'horizontalBuckets': 6,
    u'colorBy': u'AGE',
    u'imageFieldName': u'FN',
}


#Set Data Environment
CSV_FILE_PATH='https://raw.githubusercontent.com/fatimashihab/facets/master/100.csv'
OUTPUT_FILE_PATH = './facets_dive_data_visualization.html'
dataset = pd.read_csv(CSV_FILE_PATH)

#Set the html template
HTML_TEMPLATE = u"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>%(title)s</title>
    <script>
        window.addEventListener('DOMContentLoaded', function() {
            var link = document.createElement('link');
            link.rel = "import";
            link.href = "https://raw.githubusercontent.com/PAIR-code/facets/master/facets-dist/facets-jupyter.html";
            link.onload = function() {
                var dive = document.createElement('facets-dive');
                dive.crossOrigin = "anonymous";
                dive.data = %(data)s;
                var presets = %(presets)s;
                for (var key in presets) {
                    if (presets.hasOwnProperty(key))
                        dive[key] = presets[key];
                }
                document.body.appendChild(dive);
            }
            document.head.appendChild(link);
        });
    </script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/0.7.24/webcomponents-lite.js"></script>
    <style>body, html { height: 100%%; margin: 0; padding: 0; width: 100%%; }</style>
</head>
<body></body>
</html>
""".strip()

#export data
with open(OUTPUT_FILE_PATH, "wb") as f:
    final_template = HTML_TEMPLATE % {
        'title':'Data Visualization',
        'data': dataset.to_json(orient='records'),
        'presets': json.dumps(PRESETS)
    }
    f.write(final_template.encode('utf-8'))