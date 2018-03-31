from . import db


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    au_book = db.relationship('Book', backref='author')

    def __repr__(self):
        return 'Author:%s' % self.name


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    au_book = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __str__(self):
        return 'Book:%s,%s' % (self.info, self.lead)
