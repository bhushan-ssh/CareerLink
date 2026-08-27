from controllers.user_datastore import user_datastore
from flask_restful import Resource
from controllers.database import db
from flask import request,make_response,jsonify
from flask_security import SQLAlchemyUserDatastore, RoleMixin, UserMixin, utils, auth_token_required,roles_required