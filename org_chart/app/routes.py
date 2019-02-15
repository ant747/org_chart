# -*- coding: utf-8 -*-
from flask import render_template
from flask import jsonify
from app import app, db
from flask import request, make_response
from app.models import Tree
from sqlalchemy.exc import IntegrityError


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv



@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    app.logger.error('InvalidUsage: %s' %(error))
    app.logger.error('%s' %vars(error))
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found: %s' %(request.path))
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s' %(error))
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
    # return render_template('500.html'), 500


@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s, during request %s' %(error, request.url))
    message = {
            'status': 500,
            'message': 'Internal server error on handling ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
    # return render_template('500.html'), 500


@app.route('/')
@app.route('/index')
@app.route('/api/orgchart/')
def index():

    def display_comment(node):
        res = {}
        for rel in node.rels:
            r = display_comment(rel)
            res[rel.name] = r

        return res

    root = Tree.query.get(1)
    res = {root.name: display_comment(root)} if root else {}

    return render_template('index.html', tree_dict=res)
    # return jsonify(res)


@app.route('/api/orgchart/new', methods=['POST'])
def reset():
    # return {'resul': 'OrgChart is empty!'}
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print ('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()

    return make_response(jsonify({'result': 'OrgChart is reset. You can start from the scratch.'}), 200)



@app.route('/api/orgchart/add', methods=['POST'])
def add():
    try:
        try:
            parent_name = request.args['parent']
            childs_names = request.args['childs'].split(',')
        except:
            raise InvalidUsage(
                'Request must contain 2 fields: parent and childs. ' +
                'args received: %s' %jsonify(request.args),
                status_code=410)

        if not db.session.query(Tree).count():      # first epl in db - big boss
            p = Tree(name=parent_name)
            db.session.add(p)
            db.session.commit()

        p = Tree.query.filter_by(name=parent_name).first()
        if not p:
            raise InvalidUsage(
                "Employee '%s' not found in DB. Add his boss subtree first." %parent_name,
                status_code=410)

        childs = [Tree(name=child, parent=p) for child in childs_names]
        db.session.add_all(childs)
        db.session.commit()

        return make_response(jsonify({'result': 'Subtree added.'}), 200)

    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage(
            'IntegrityError: check that you a not trying to add employee, that aready exist in chart.',
            status_code=410)



@app.route('/api/orgchart/<name>', methods=['DELETE'])
def delete(name):

    def delete_node(node):
        i = 1
        for rel in node.rels:
            i += 1
            delete_node(rel)
        db.session.delete(node)
        db.session.commit()
        return i

    empl = Tree.query.filter_by(name=name).first()
    if not empl:
        raise InvalidUsage(
            "Cannot delete employee '%s': not found in DB." % name,
            status_code=410)

    count = delete_node(empl)

    return make_response(jsonify({'result': "Employee '%s' and his %s childs deleted." %(name, count-1)}), 200)
