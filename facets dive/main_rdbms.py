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
from sshtunnel import SSHTunnelForwarder
import MySQLdb

def search(conn, *args):
    """ Search Database"""
    try:
        #write sql query
        cursor = conn.cursor()
        length = len(args)
        max = length
        print length

        #change query with databaset settings
        query = "SELECT * FROM fb_postal WHERE `"
        while length > 0:
            if max == length:
                query = query + args[length - 2] + "`= '" + args[length - 1] + "'"
            else:
                query = query + "OR `" + args[length - 2] + "`= '" + args[length - 1] + "'"
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
        dataset = pd.DataFrame(data=data[:,:],columns=['ID' , 'Email' , 'Facebook' , 'Facebook Name if Different' , 'FB Gender M F U-Unknown',
                                                    'First Name' , 'Last Name' , 'Address', 'City', 'State','Country', 'Zip', 'Phone', 'Phone1', 'Source',
                                                   'Signup IP', 'Signup Date Added', 'Signup Time Added', 'Gender' , 'DOB' , 'Birthday',
                                                    'ZCS_IP_DateTime' , 'ZCS_IP_AreaCode' , 'ZCS_IP_City', 'ZCS_IP_Continent', 'ZCS_IP_Country',
                                                    'ZCS_IP_CountryCode', 'ZCS_ISP' , 'ZCS_ISP_Latitude', 'ZCS_ISP_Longitude', 'ZCS_ISP_Organization',
                                                    'ZCS_ISP_State', 'ZCS_ISP_StateCode', 'src_id', 'TT_ID' , 'IW_SCORE'])
        cursor.close()
        return dataset

    except Error as e:
        print(e)

def dive(dataset):
    # Facets Dive settings. Inital layout of the visualized data.
    PRESETS = {
        u'verticalFacet': u'Gender',
        u'horizontalFacet': u'City',
        u'verticalBuckets': 2,
        u'horizontalBuckets': 1,
        u'colorBy': u'Birthday',
        u'imageFieldName': u'First Name',
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
    with SSHTunnelForwarder(('xx.xxx.xx.xx', 22), ssh_password='', ssh_username='fatima',
                            remote_bind_address=('127.0.0.3', 3306)) as server:
        conn = MySQLdb.connect(host='127.0.0.1', port=server.local_bind_port, user='root', db='')
        
        #search the database
        result= search(conn, *zipped)
        conn.close()
        


        #initialize dive settings
        dive(result)
