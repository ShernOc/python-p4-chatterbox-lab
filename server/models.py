from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
    
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable = False)
    body = db.Column(db.String(256), nullable = False)
    created_at = db.Column(db.DateTime, server_default = db.func.now(), nullable = False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # relationship 
    
    def __repr__(self):
        return f'Message(id={self.id}, {self.username}, {self.body},{self.create_at},{self.updated_at}'
    
    
    
    
    
    
    
    
    
    
    


