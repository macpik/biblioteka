from flask import Flask, jsonify, abort, make_response, request
from models import library

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/api/v1/library/", methods=["GET"])
def library_list_api_v1():
    return jsonify(library.all())

@app.route("/api/v1/library/<int:libraries_id>", methods=["GET"])
def get_libraries(libraries_id):
    libraries = library.get(libraries_id)
    if not libraries:
        abort(404)
    return jsonify({"libraries": libraries})

@app.route("/api/v1/library/", methods=["POST"])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    libraries = {
        'id': library.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'read': False
    }
    library.create(libraries)
    return jsonify({'libreries': libraries}), 201

@app.route("/api/v1/library/<int:libraries_id>", methods=['DELETE'])
def delete_books(libraries_id):
    result = library.delete(libraries_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/library/<int:libraries_id>", methods=["PUT"])
def update_books(libraries_id):
    libraries = library.get(libraries_id)
    if not libraries:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'read' in data and not isinstance(data.get('read'), bool)
    ]):
        abort(400)
    libraries = {
        'title': data.get('title', libraries['title']),
        'description': data.get('description', libraries['description']),
        'read': data.get('read', libraries['read'])
    }
    library.update(libraries_id, libraries)
    return jsonify({'libraries': libraries})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)