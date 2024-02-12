"""SQLAlchemy models for blogly."""
"""The last part will be to add a “tagging” feature.Overall, this model structure allows for the representation of users, blog posts, and tags, and it establishes relationships between them to support features such as associating multiple tags with a post and linking posts to specific users."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User(db.Model):
    """Site user."""
    #Represents a user on the site with attributes such as id, first_name, last_name, and image_url.
    #Includes a relationship with the Post model through the posts attribute, establishing a one-to-many relationship where a user can have multiple posts.
    #Defines a property full_name that returns the full name of the user by concatenating the first_name and last_name attributes.

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Blog post."""
    #Represents a blog post with attributes like id, title, content, created_at, and user_id.
    #The created_at attribute is a timestamp representing when the post was created.
    #Establishes a relationship with the User model through the user attribute, creating a many-to-one relationship where multiple posts can be associated with a single user.
    #Defines a property friendly_date that returns a nicely-formatted date string.

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class PostTag(db.Model):
    """Tag on a post."""
    #Acts as an association table for the many-to-many relationship between posts and tags.
    #Includes post_id and tag_id columns as foreign keys referencing the Post and Tag models, respectively.

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts."""
    #Represents a tag that can be added to posts with attributes id and name.
    #Defines a relationship with the Post model through the posts attribute, establishing a many-to-many relationship using the posts_tags association table.

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
