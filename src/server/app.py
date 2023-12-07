from flask import Flask, jsonify, send_file
from models import db, File, add_files_from_localstorage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/files', methods=['GET'])
def get_files():
    try:
        files = File.query.all()
        file_list = [file.as_dict() for file in files]
        return jsonify(file_list)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    try:
        file = File.query.get(file_id)
        if file:
            return jsonify(file.as_dict())
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    
@app.route('/files/<int:file_id>/download', methods=['GET'])
def download_file(file_id):
    file = File.query.get(file_id) 
    if file:
        return send_file(file.filepath, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/files/<filename>', methods=['GET'])
def get_file_by_name(filename):
    try:
        file = File.query.filter_by(filename=filename).first()
        if file:
            return jsonify(file.as_dict())
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            add_files_from_localstorage()
        except Exception as e:
            print("ERROR: DB")
    
    app.run(host='10.42.0.1', port=8018, debug=True, threaded=True)

