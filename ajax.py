# -*- coding: utf-8-*-
import traceback
from flask import make_response, request, url_for, escape, Blueprint
from flask import Flask, render_template
import json

import pyodbc

ajax_bp = Blueprint('ajax', __name__)

name = 'zcx'

driver = '{ODBC Driver 17 for SQL Server}'
server = '127.0.0.1'
database = 'MMSD'
uid = 'sa'
pwd = '123456'
cnxn = pyodbc.connect("DRIVER=%s;SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"%(driver,server,database,uid,pwd))

@ajax_bp.route('/compute-all', methods=['post'])
def InDepot_compute_all():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    print(data,type(data))
    sql = "exec Count_material_IO_num_during_time " + "'" + data['0'] + "', " + "'" + data['1'] + "'" 
    print(sql)
    try:
        cursor.execute(sql)
        ret = cursor.fetchall()
        print(ret)
        ret = [list(i)[:3] for i in ret]
        print(ret)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
        ret = ''
    return json.dumps({'msg': msg, 'ret': ret})