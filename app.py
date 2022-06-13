# -*- coding: utf-8-*-
from flask import url_for, escape
from flask import Flask, render_template

import pyodbc

app = Flask(__name__)

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@app.route('/test')
def test_url_for():
    print(url_for('user_page', name = 'zcx'))
    print(url_for('user_page', name = 'zzz'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num = 2))
    return 'Test page'

name = 'zcx'

driver = '{ODBC Driver 17 for SQL Server}'
server = 'DESKTOP-0N6RLJE\SQLEXPRESS'
database = 'MMSD'
uid = 'sa'
pwd = '123456'
cnxn = pyodbc.connect("DRIVER=%s;SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"%(driver,server,database,uid,pwd))

@app.route('/')
@app.route('/staff')
def staff_Management():
    # 获取员工信息表的内容
    cursor = cnxn.cursor()
    sql = "select Sno '编号', Sname '姓名', Ssex '性别', Spos '职位', Sphone '电话', convert(char(10),Sbirth,120) '生日',dbo.GetAge(Sbirth) '年龄', SBranch '所属部门号', B.Bname '所属部门名' from S, B where B.Bno = S.SBranch"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    return render_template('staff.html',content=content, labels=labels, name = name)

@app.route('/branch')
def branch_Management():
    # 获取部门信息表的内容
    cursor = cnxn.cursor()
    sql = "select Bno '编号', Bname '部门名', Baddr '部门地址', Bphone '联系电话' from B"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    return render_template('branch.html',content=content, labels=labels, name = name)

@app.route('/classify')
def classify_Management():
    # 获取物料信息表的内容
    cursor = cnxn.cursor()
    sql = "select Mno '编号', Mname '名称', Mfunc '功能', Mattr '属性', Mstatus '生产状态' from M"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    return render_template('classify.html',content=content, labels=labels, name = name)

@app.route('/inventory')
def inventory_Management():
    # 获取物料库存表的内容
    cursor = cnxn.cursor()
    sql = "select M.Mno '物料编号',M.Mname '物料名称', D.Dno '仓库编号',D.Dname '仓库名称', num '数量' from DM, M, D where DM.Dno = D.Dno and DM.Mno = M.Mno"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    return render_template('inventory.html',content=content, labels=labels, name = name)

@app.route('/InDepot')
def InDepot_Management():
    # 获取物料入库表的内容
    cursor = cnxn.cursor()
    sql = "select S.Sno '员工号', S.Sname '员工姓名', M.Mno '物料编号',M.Mname '物料名称', D.Dno '仓库编号',D.Dname '仓库名称', num '存入数量' from SMD, M, D, S where SMD.Dno = D.Dno and SMD.Mno = M.Mno and SMD.Sno = S.Sno and SMD.OpType = '存'"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    return render_template('InDepot.html',content=content, labels=labels, name = name)

@app.route('/OutDepot')
def OutDepot_Management():
    # 获取物料出库表的内容
    cursor = cnxn.cursor()
    sql = "select S.Sno '员工号', S.Sname '员工姓名', M.Mno '物料编号',M.Mname '物料名称', D.Dno '仓库编号',D.Dname '仓库名称', num '领用数量' from SMD, M, D, S where SMD.Dno = D.Dno and SMD.Mno = M.Mno and SMD.Sno = S.Sno and SMD.OpType = '取'"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    return render_template('OutDepot.html',content=content, labels=labels, name = name)

@app.route('/transport')
def transport_Management():
    # 获取物料转运表的内容
    cursor = cnxn.cursor()
    sql = "select M.Mno '物料编号',M.Mname '物料名称', SD.Dno '源仓库编号', SD.Dname '源仓库名称', DD.Dno '目的仓库编号', DD.Dname '目的仓库名称', num '转运数量' from DMD, D SD, D DD, M where DMD.SDno = SD.Dno and DMD.DDno = DD.Dno and DMD.Mno = M.Mno"
    cursor.execute(sql)
    content = cursor.fetchall()
    labels = [tuple[0] for tuple in cursor.description]
    return render_template('OutDepot.html',content=content, labels=labels, name = name)