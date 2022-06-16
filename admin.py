# -*- coding: utf-8-*-
import traceback
from flask import make_response, request, url_for, escape
from flask import Flask, render_template
import json

import pyodbc

admin_bp = Flask(__name__)

@admin_bp.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@admin_bp.route('/test')
def test_url_for():
    print(url_for('user_page', name = 'zcx'))
    print(url_for('user_page', name = 'zzz'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num = 2))
    return 'Test page'

name = 'zcx'

driver = '{ODBC Driver 17 for SQL Server}'
server = '127.0.0.1'
database = 'MMSD'
uid = 'sa'
pwd = '123456'
cnxn = pyodbc.connect("DRIVER=%s;SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"%(driver,server,database,uid,pwd))

@admin_bp.route('/')
def login():
    return render_template('login.html')

@admin_bp.route('/staff')
def staff_Management():
    # 获取员工信息表的内容
    cursor = cnxn.cursor()
    sql = "select Sno '编号', Sname '姓名', Ssex '性别', Spos '职位', Sphone '电话', convert(char(10),Sbirth,120) '生日',dbo.GetAge(Sbirth) '年龄', SBranch '所属部门号', B.Bname '所属部门名' from S, B where B.Bno = S.SBranch"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    uneditableLabelsIndex= [0,6,8]
    uninsertableLabelsIndex = [6,8]
    return render_template('staff.html',
    content=content,
    labels=labels, 
    uneditableLabelsIndex = uneditableLabelsIndex, 
    uninsertableLabelsIndex = uninsertableLabelsIndex,
    name = name)

@admin_bp.route('/staff/edit', methods=['post'])
def staff_edit():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    sql = "update S " + \
        "set Sname = " + "'"+ data['1'].strip() + "'," +\
        "Ssex = " + "'" + data['2'].strip() + "'," +\
        "Spos = " + "'" + data['3'].strip() + "'," +\
        "Sphone = " + "'" + data['4'].strip() + "'," +\
        "Sbirth = " + "'" + data['5'] + "'," +\
        "SBranch = " + "'" + data['7'].strip() + "'" +\
        "where Sno = " + "'" + data['0'].strip() + "' "
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

@admin_bp.route('/staff/insert', methods=['post'])
def staff_insert():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    print(data,type(data))
    values = ""
    for key in data:
        print(key)
        values += "'"+ data[key].strip() + "',"
    values = values[:-1]
    sql = "insert into S values(" + values + ")"
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

@admin_bp.route('/branch')
def branch_Management():
    # 获取部门信息表的内容
    cursor = cnxn.cursor()
    sql = "select Bno '编号', Bname '部门名', Baddr '部门地址', Bphone '联系电话' from B"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    uneditableLabelsIndex= [0]
    uninsertableLabelsIndex = []
    return render_template('branch.html',
    content=content, 
    labels=labels, 
    uneditableLabelsIndex = uneditableLabelsIndex, 
    uninsertableLabelsIndex = uninsertableLabelsIndex,
    name = name)

@admin_bp.route('/branch/edit', methods=['post'])
def branch_edit():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    sql = "update B " + \
        "set Bname = " + "'"+ data['1'].strip() + "'," +\
        "Baddr = " + "'" + data['2'].strip() + "'," +\
        "Bphone = " + "'" + data['3'].strip() + "' " +\
        "where Bno = " + "'" + data['0'].strip() + "' "
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

@admin_bp.route('/branch/insert', methods=['post'])
def branch_insert():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    print(data,type(data))
    values = ""
    for key in data:
        print(key)
        values += "'"+ data[key].strip() + "',"
    values = values[:-1]
    sql = "insert into B values(" + values + ")"
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

@admin_bp.route('/depot')
def depot_Management():
    # 获取仓库信息表的内容
    cursor = cnxn.cursor()
    sql = "select Dno '编号', Dname '仓库名', Daddr '仓库地址', Dphone '联系电话' from D"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    uneditableLabelsIndex= [0]
    uninsertableLabelsIndex = []
    return render_template('depot.html',
    content=content, labels=labels, 
    uneditableLabelsIndex = uneditableLabelsIndex, 
    uninsertableLabelsIndex = uninsertableLabelsIndex,
    name = name)

@admin_bp.route('/depot/edit', methods=['post'])
def depot_edit():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    sql = "update D " + \
        "set Dname = " + "'"+ data['1'].strip() + "'," +\
        "Daddr = " + "'" + data['2'].strip() + "'," +\
        "Dphone = " + "'" + data['3'].strip() + "' " +\
        "where Dno = " + "'" + data['0'].strip() + "' "
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

@admin_bp.route('/depot/insert', methods=['post'])
def depot_insert():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    print(data,type(data))
    values = ""
    for key in data:
        print(key)
        values += "'"+ data[key].strip() + "',"
    values = values[:-1]
    sql = "insert into D values(" + values + ")"
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

@admin_bp.route('/classify')
def classify_Management():
    # 获取物料信息表的内容
    cursor = cnxn.cursor()
    sql = "select Mno '编号', Mname '名称', Mfunc '功能', Mattr '属性', Mstatus '生产状态' from M"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    uneditableLabelsIndex= [0]
    uninsertableLabelsIndex = []
    return render_template('classify.html',
    content=content, 
    labels=labels, 
    uneditableLabelsIndex = uneditableLabelsIndex,
    uninsertableLabelsIndex = uninsertableLabelsIndex,
    name = name)

@admin_bp.route('/classify/edit', methods=['post'])
def classify_edit():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    sql = "update M " + \
        "set Mname = " + "'"+ data['1'].strip() + "'," +\
        "Mfunc = " + "'" + data['2'].strip() + "'," +\
        "Mattr = " + "'" + data['3'].strip() + "'," +\
        "Mstatus = " + "'" + data['4'].strip() + "' " +\
        "where Mno = " + "'" + data['0'].strip() + "' "
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

@admin_bp.route('/classify/insert', methods=['post'])
def classify_insert():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    print(data,type(data))
    values = ""
    for key in data:
        print(key)
        values += "'"+ data[key].strip() + "',"
    values = values[:-1]
    sql = "insert into M values(" + values + ")"
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

@admin_bp.route('/inventory')
def inventory_Management():
    # 获取物料库存表的内容
    cursor = cnxn.cursor()
    sql = "select M.Mno '物料编号',M.Mname '物料名称', D.Dno '仓库编号',D.Dname '仓库名称', num '数量' from DM, M, D where DM.Dno = D.Dno and DM.Mno = M.Mno"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    return render_template('inventory.html',
    content=content, 
    labels=labels, 
    name = name)

@admin_bp.route('/InDepot')
def InDepot_Management():
    # 获取物料入库表的内容
    cursor = cnxn.cursor()
    sql = "select S.Sno '员工号', S.Sname '员工姓名', M.Mno '物料编号',M.Mname '物料名称', D.Dno '仓库编号',D.Dname '仓库名称', OpTime '存入时间', num '存入数量' from SMD, M, D, S where SMD.Dno = D.Dno and SMD.Mno = M.Mno and SMD.Sno = S.Sno and SMD.OpType = '存'"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    uninsertableLabelsIndex = [1,3,5]
    return render_template('InDepot.html',
    content=content, 
    labels=labels, 
    uninsertableLabelsIndex = uninsertableLabelsIndex,
    name = name)

@admin_bp.route('/InDepot/insert', methods=['post'])
def InDepot_insert():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    print(data,type(data))
    values = ""
    for key in data:
        print(key)
        if key == "4":
            values += "'存',"
            values += data[key].strip() + ","
            break
        values += "'"+ data[key].strip() + "',"
    values = values[:-1]
    sql = "insert into SMD values(" + values + ")"
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

@admin_bp.route('/OutDepot')
def OutDepot_Management():
    # 获取物料出库表的内容
    cursor = cnxn.cursor()
    sql = "select S.Sno '员工号', S.Sname '员工姓名', M.Mno '物料编号',M.Mname '物料名称', D.Dno '仓库编号',D.Dname '仓库名称', OpTime '领用时间', num '领用数量' from SMD, M, D, S where SMD.Dno = D.Dno and SMD.Mno = M.Mno and SMD.Sno = S.Sno and SMD.OpType = '取'"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    uninsertableLabelsIndex = [1,3,5]
    return render_template('OutDepot.html',
    content=content, 
    labels=labels, 
    uninsertableLabelsIndex = uninsertableLabelsIndex,
    name = name)

@admin_bp.route('/OutDepot/insert', methods=['post'])
def OutDepot_insert():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    print(data,type(data))
    values = ""
    for key in data:
        print(key)
        if key == "4":
            values += "'取',"
            values += data[key].strip() + ","
            break
        values += "'"+ data[key].strip() + "',"
    values = values[:-1]
    sql = "insert into SMD values(" + values + ")"
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

times = ['2000-01-01 00:00:00', '2000-01-01 00:00:00']

@admin_bp.route('/compute')
def compute():
    # 获取物料进出库的总数量的内容
    cursor = cnxn.cursor()
    sql = "exec Count_material_IO_num_during_time " + "'" + times[0] + "', " + "'" + times[1] + "'"  
    cursor.execute(sql)
    content = cursor.fetchall()
    print(content)
    return render_template('compute.html',
    content=content, 
    name = name)

@admin_bp.route('/compute-all')
def compute_all():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    times[0] = data['0']
    times[1] = data['1']
    json.dumps({'msg':"success"})

@admin_bp.route('/transport')
def transport_Management():
    # 获取物料转运表的内容
    cursor = cnxn.cursor()
    sql = "select M.Mno '物料编号',M.Mname '物料名称', SD.Dno '源仓库编号', SD.Dname '源仓库名称', DD.Dno '目的仓库编号', DD.Dname '目的仓库名称', TranTime '转运时间', num '转运数量' from DMD, D SD, D DD, M where DMD.SDno = SD.Dno and DMD.DDno = DD.Dno and DMD.Mno = M.Mno"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    uninsertableLabelsIndex = [1,3,5]
    return render_template('transport.html',
    content=content, 
    labels=labels, 
    uninsertableLabelsIndex = uninsertableLabelsIndex,
    name = name)

@admin_bp.route('/transport/insert', methods=['post'])
def transport_insert():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    cursor = cnxn.cursor()
    print(data,type(data))
    values = ""
    for key in data:
        print(key)
        if key == "4":
            values += data[key].strip() + ","
            break
        values += "'"+ data[key].strip() + "',"
    values = values[:-1]
    sql = "insert into DMD values(" + values + ")"
    print(sql)
    try:
        cursor.execute(sql)
        msg = 'success'
    except:
        traceback.print_exc()
        msg = 'failed'
    return json.dumps({'msg': msg})

