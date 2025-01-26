from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

#Get the message 
@app.route('/messages')
def messages():
    msg = Message.query.all()
    msg_list = []
    #get all messages 
    for message in msg:
        msg_list.append({
            "id": message.id,
            "username":message.username,
            "body":message.body,
            "create_at":message.created_at,
            "updated_at":message.updated_at
        })
        
    return jsonify(msg_list)

#create a message 
@app.route('/messages', methods = ['POST'])
def create_message():
    try:
        # get the data 
        data = request.get_json()
        # Validate input
        if 'username' not in data or 'body' not in data:
            return jsonify({"error": "Username and body are required"}), 400
        
        username = data['username']
        body = data['body']
        
        new_msg = Message(username=username,body=body)
        
        db.session.add(new_msg)
        db.session.commit()
        
    
        return jsonify({
            "id": new_msg.id,
            "username":new_msg.username,
            "body":new_msg.body,
            "create_at":new_msg.created_at,
            "updated_at":new_msg.updated_at
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)})
        
#Update message: 

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    try: 
        message = Message.query.get(id)
        
        if not message:  # Check if the message exists
            return jsonify({"error": "Message with id {id} not found"}),
        
        if request.method == 'PATCH':
            data = request.get_json()
            
            # Update only provided fields
            message.username = data.get('username', message.username)
            message.body = data.get('body', message.body)
            message.created_at = data.get('created_at', message.created_at)
            message.updated_at = data.get('updated_at', message.updated_at)
            
            db.session.commit()

            return jsonify({"success": "Message updated successfully", "message": message.to_dict()}), 200

        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            return jsonify({"deleted": True}), 200
        
    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()
        print(f"Error: {str(e)}")  # Debugging: Print the error to console
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(port=5555)
