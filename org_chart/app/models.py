from app import db

'''
class Tree(db.Model):
    __tablename__ = 'tree'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('tree.id'))
    name = db.Column(db.String(128), nullable=False)
    rels = db.relationship(
        'Tree', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')

'''

class Tree(db.Model):
    __tablename__ = 'tree'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('tree.id'))
    name = db.Column(db.String(128), unique=True, nullable=False)
    rels = db.relationship(
        'Tree', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')


    def __repr__(self):
        return '<id {}, parent_id {}, name {}>'.format(self.id, self.parent_id, self.name)

