"""
Usage:
test1.py [(FIELD INPUT)...]

Arguments:
  FIELD
  INPUT

"""

import mysql.connector
from mysql.connector import Error
from docopt import docopt
import json
import pandas as pd
import numpy as np


def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='TEST',
                                       user='root',
                                       password='123')
        if conn.is_connected():
            #print('Connected to MySQL database')
            return conn

    except Error as e:
        print(e)

def search(conn, *args):
    """ Search Database"""
    try:
        #write sql query
        cursor = conn.cursor()
        length = len(args)
        max = length
#        print length
        #change query with databaset settings
        query = "SELECT * FROM TEST3 WHERE "
        while length > 0:
            if max == length:
                query = query + args[length - 2] + "= '" + args[length - 1] + "'"
            else:
                query = query + "OR " + args[length - 2] + "= '" + args[length - 1] + "'"
            length-=2

        #customize result type
        result = []
        if max > 0:
            cursor.execute(query)
            x = cursor.fetchall()
            for row in x:
                result.append(row)

        if len(result) > 0:
            r=[]
            for row in result:
                row=list(row)
                r.append(row)
        else:
            print ('No matching records found')

        #create dataframe
        data = np.array(list(r))
        dataset = pd.DataFrame(data=data[:, :])
        cursor.close()
    except Error as e:
        print(e)

    return dataset

def dive(dataset):
    # Facets Dive settings. Inital layout of the visualized data.
    PRESETS = {
        u'verticalFacet': u'BUY_JEWELRY',
        u'horizontalFacet': u'GENDER',
        u'verticalBuckets': 1,
        u'horizontalBuckets': 1,
        u'colorBy': u'AGE',
        u'imageFieldName': u'FN',
    }

    # Set Data Environment
    #change output path file
    OUTPUT_FILE_PATH = '/home/fatma/Desktop/TEST.html'

    # Set the html template
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

    # export data
    with open(OUTPUT_FILE_PATH, "wb") as f:
        final_template = HTML_TEMPLATE % {
            'title': 'Data Visualization',
            'data': dataset.to_json(orient='records'),
            'presets': json.dumps(PRESETS)
        }
        f.write(final_template.encode('utf-8'))

if __name__ == '__main__':

    #take input from bash and assign to variables
    arguments = docopt(__doc__)
    field=arguments["FIELD"]
    input=arguments["INPUT"]
    zipped = map(list, zip(field, input))
    zipped = sum(zipped,[])

    #connect to sql server
    conn= connect()

    #search the database
    result= search(conn, *zipped)
    conn.close()
    print result



    #initialize dive settings
    dive(result)

