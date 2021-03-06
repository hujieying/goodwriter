#coding:utf-8
#蓝本中定义的程序路由
from flask import render_template
from . import main
from flask import Flask,render_template,redirect,url_for,session,request,make_response
import xml.etree.ElementTree as ET
import config
from ..models import User,Material,Article
from app import db
from app.main.wx import valication, reply_text, reply_event, reply_else
from datetime import datetime
from sqlalchemy import desc

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route("/get_material",methods=['GET','POST'])
def get_material():
    """用于查询标签"""
    if request.method == "GET":
        key = request.args.get('key')
        tag = request.args.get('tag')
    else:
        key = request.form['key']
        tag = request.form['tag']
    print(key,tag)
    if key:
        materials = Material.query.filter(Material.content.like(f"%{key}%"),Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
    elif tag:
        materials = Material.query.filter(Material.tag.like(f"%{tag}%"),Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
    else:
        materials = Material.query.filter(Material.user_id==session['user_id']).order_by(desc(Material.edit_time))

    return render_template('get_material.html',materials=materials)

@main.route('/material_edit', methods=['GET','POST'])
def material_edit():
    if request.method == 'GET':
        mater_id = request.args.get('mater_id')
        if mater_id:
            # return session['user_id']
            material = Material.query.filter(Material.mater_id==int(mater_id),Material.user_id==session['user_id']).first()
            # return str(Material.query.filter(Material.mater_id==mater_id,Material.user_id==session['user_id']))
            return render_template('material_edit.html', material=material)
        else:
            return render_template('material_edit.html')
    else:
        mater_id = request.form['mater_id']
        tag = request.form['tag']
        content = request.form['content']
        edit_time = datetime.utcnow()
        user_id = session['user_id']
        # print(mater_id,tag,content,edit_time,user_id)
        if mater_id:
            material = Material.query.filter(Material.mater_id==int(mater_id),Material.user_id==session['user_id'])
            material.tag = tag
            material.content = content
            material.edit_time = edit_time
            db.session.commit()
        else:
            material = Material(tag=tag,content=content,user_id=user_id,edit_time=edit_time)
            db.session.add(material)
            db.session.commit()

        # return u"提交成功"
        return redirect(url_for('main.material_list'))

@main.route('/material_list', methods=['GET'])
def material_list():
    mater_id = request.args.get("mater_id")
    tag = request.args.get("tag")
    # 标签唯一问题
    tag_all = Material.query.with_entities(Material.tag.distinct().label("tag")).filter(Material.user_id==session['user_id'])
    # return str(tag_all)
    if mater_id:
        materials = Material.query.filter(Material.mater_id==int(mater_id),Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
        return render_template("material_list.html",materials=materials,tags=tag_all)
    elif tag:
        materials = Material.query.filter(Material.tag==tag,Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
        return render_template("material_list.html",materials=materials,tags=tag_all)
    else:
        materials = Material.query.filter(Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
        return render_template("material_list.html",materials=materials,tags=tag_all)


@main.route('/article_edit', methods=['GET','POST'])
def article_edit():
    if request.method == 'GET':
        artic_id = request.args.get('artic_id')
        tag_all = Material.query.with_entities(Material.tag.distinct().label("tag")).filter(Material.user_id==session['user_id'])
        if artic_id:
            article = Article.query.filter(Article.artic_id==int(artic_id),Article.user_id==session['user_id']).first()
            # return str(Material.query.filter(Material.mater_id==mater_id,Material.user_id==session['user_id']))
            return render_template('article_edit.html', article=article,tags=tag_all)
        else:
            return render_template('article_edit.html',tags=tag_all)
    else:
        artic_id = request.form['artic_id']
        title = request.form['title']
        content = request.form['content']
        edit_time = datetime.utcnow()
        user_id = session['user_id']
        # print(mater_id,title,content,edit_time,user_id)
        if artic_id:
            article = Article.query.filter(Article.artic_id==int(artic_id),Article.user_id==session['user_id'])
            article.title = title
            article.content = content
            article.edit_time = edit_time
            db.session.commit()
        else:
            article = Article(title=title,content=content,user_id=user_id,edit_time=edit_time)
            db.session.add(article)
            db.session.commit()

        # return u"提交成功"
        return redirect(url_for('main.article_list'))

@main.route('/article_list', methods=['GET'])
def article_list():
    artic_id = request.args.get("artic_id")
    title = request.args.get("title")
    tag_all = Material.query.with_entities(Material.tag.distinct().label("tag")).filter(Material.user_id==session['user_id'])

    if artic_id:
        articles = Article.query.filter(Article.artic_id==int(artic_id),Article.user_id==session['user_id']).order_by(desc(Article.edit_time))
        return render_template("article_list.html",articles=articles,tags=tag_all)
    elif title:
        articles = Article.query.filter(Article.title==title,Article.user_id==session['user_id']).order_by(desc(Article.edit_time))
        return render_template("article_list.html",articles=articles,tags=tag_all)
    else:
        articles = Article.query.filter(Article.user_id==session['user_id']).order_by(desc(Article.edit_time))
        return render_template("article_list.html",articles=articles,tags=tag_all)

@main.route('/wx', methods=['GET','POST'])
def wx():
    if request.method == 'GET':
        valicate_params = request.args
        return valication(valicate_params)
    else:
        xml_recv = ET.fromstring(request.data)
        msgtype = xml_recv.find("MsgType").text
        # print(request.data)
        if msgtype == "event":
            xml_reply = reply_event(xml_recv)
        elif msgtype == "text":
            xml_reply = reply_text(xml_recv)
        else:
            xml_reply = reply_else(xml_recv)
        response = make_response(xml_reply)
        response.content_type = 'application/xml'
        return response
