
from test import db,app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import LoginManager,UserMixin,login_user, logout_user, login_required,current_user

#for migrations
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ='login'

@login_manager.user_loader
def load_user(user_id):
       return Regtb.query.filter_by(id=user_id).first()

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)


class Regtb(db.Model,UserMixin):
       id = db.Column(db.Integer,primary_key=True)
       Name = db.Column(db.String(255))
       Email = db.Column(db.String, unique=True, nullable=False)
       Password = db.Column(db.String(255))
       Registered_id = db.Column(db.Integer)
       Reg_Datee=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



       @staticmethod
       def get_reset_token(self,expires_sec=300):
              s = Serializer(app.config['SECRET_KEY'], expires_sec)
              return s.dumps({'id': self.id}).decode('utf-8')

       def verify_reset_token(token):
              s = Serializer(app.config['SECRET_KEY'])
              try:
                     user_id = s.loads(token)['id']
              except:
                     return None
              return Regtb.query.get()(id)


              

# if __name__ =='__main__':
#     manager.run()