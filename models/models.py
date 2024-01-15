from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# USERS
class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    title = db.Column(db.String)
    company = db.Column(db.String)
    region = db.Column(db.String)
    company_size = db.Column(db.String)
    function = db.Column(db.String)
    product_bought = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    def __repr__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Email: {self.email}"
# TEAMS
class Teams(db.Model):
    __tablename__ = "teams"

    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    owner = db.relationship('Users', foreign_keys=[owner_id])

    def __repr__(self):
        return f"Team ID: {self.team_id}, Name: {self.name}"
    
# TEAM USERS
class TeamUsers(db.Model):
    __tablename__ = "team_users"

    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    role = db.Column(db.String)

    team = db.relationship('Teams', foreign_keys=[team_id])
    user = db.relationship('Users', foreign_keys=[user_id])

    def __repr__(self):
        return f"Team ID: {self.team_id}, User ID: {self.user_id}, Role: {self.role}"


# INVITATIONS
class Invitations(db.Model):
    __tablename__ = "invitations"

    invitation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    role = db.Column(db.String)
    email = db.Column(db.String)
    token = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    team = db.relationship('Teams', foreign_keys=[team_id])
    user = db.relationship('Users', foreign_keys=[user_id])

    def __repr__(self):
        return f"Invitation ID: {self.invitation_id}, Team ID: {self.team_id}, User ID: {self.user_id}, Role: {self.role}"

# INTRODUCTIONS
class Introductions(db.Model):
    __tablename__ = "introductions"

    introduction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    introductor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    target_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime)
    status = db.Column(db.String)

    user = db.relationship('Users', foreign_keys=[user_id])
    introductor = db.relationship('Users', foreign_keys=[introductor_id])
    target = db.relationship('Users', foreign_keys=[target_id])

    def __repr__(self):
        return f"Introduction ID: {self.introduction_id}, User ID: {self.user_id}, Introductor ID: {self.introductor_id}, Target ID: {self.target_id}"

# NOTIFICATIONS
class Notifications(db.Model):
    __tablename__ = "notifications"

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    body = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    title = db.Column(db.String)
    icon = db.Column(db.String)

    user = db.relationship('Users', foreign_keys=[user_id])

    def __repr__(self):
        return f"Notification ID: {self.notification_id}, User ID: {self.user_id}, Body: {self.body}"

# SUBSCRIPTION
class Subscriptions(db.Model):
    __tablename__ = "subscriptions"

    subscription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    name = db.Column(db.String)
    stripe_id = db.Column(db.String, unique=True)
    stripe_plan = db.Column(db.String)
    stripe_status = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    user = db.relationship('Users', foreign_keys=[user_id])

    def __repr__(self):
        return f"Subscription ID: {self.subscription_id}, Name: {self.name}, User ID: {self.user_id}"

    
# CONNECTIONS
class Connections(db.Model):
    __tablename__ = "connections"

    subscription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    connection_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('Users', foreign_keys=[user_id])
    connection_user = db.relationship('Users', foreign_keys=[connection_user_id])

    def __repr__(self):
        return f"Connection ID: {self.connection_id}, User ID: {self.user_id}, Connection User ID: {self.connection_user_id}"