from flask import request
from flask.views import View
from simplejson import dumps
from flask import current_app


#TODO: move this into __init__
#last attempt to do this resulted in import errors
def gethip():
    return current_app.blueprints['hipflask'].hipflask


def model_encoder(obj):
    return dict((field, getattr(obj, field)) for field in obj.__public__)


class ApiHandler(View):
    def __init__(self, model=None):
        self.model = model
        hipflask = gethip()
        self.session = hipflask.db.session

    def dispatch_request(self, id=None, model=None):
        if request.method == 'GET':
            func = self.get
        elif request.method == 'POST':
            func = self.post
        elif request.method == 'PUT':
            func = self.put
        elif request.method == 'DELETE':
            func = self.delete

        api_response = func(id, request.form)

        if type(api_response) is tuple and len(api_response) == 2:
            data = api_response[0]
            status = api_response[1]
        else:
            status = 200
            data = api_response

        return dumps(data, default=model_encoder), status

    def get(self, id=None, data=None):
        objects = self.session.query(self.model).all()

        return objects, 200

    def post(self, id=None, data=None):
        new_object = self.model(name=data.get('name'))
        self.session.add(new_object)
        self.session.commit()

        return new_object, 201

    def put(self, id=None, data=None):
        return 'Not Implemented', 501

    def delete(self, id=None, data=None):
        delete = self.model.query.get(id)
        self.session.delete(delete)
        self.session.commit()
        return 'Deleted', 200


def register_api_model(app, model):
    url = model.__url__
    apihandler = ApiHandler.as_view('{url}_api'.format(url=url), model=model)
    app.add_url_rule('/{url}/<int:id>'.format(url=url), view_func=apihandler, methods=['POST', 'GET', 'PUT', 'DELETE'])
    app.add_url_rule('/{url}'.format(url=url), view_func=apihandler, methods=['POST', 'GET', 'PUT', 'DELETE'])
