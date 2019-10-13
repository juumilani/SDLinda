import linda

from flask import Flask, json
from flask_restful import Api, Resource, reqparse

class MicroBlog(Resource):

	def get(self, user):

		parser = reqparse.RequestParser()
		parser.add_argument("topic")
		args = parser.parse_args()
		message = bloglinda._rd((user, args["topic"], str))
		messages = menssage.splitlines()

		if len(messages) > 0:
			response = app.response_class(

				response = json.dumps(menssages),
				# status 200 = ok
				status = 200,
				mimetype = 'application/json'

				)

			return response

		else:
			# status 404 = not found
			return 404


	def post(self, user):

		parser = reqparse.RequestParser()
		parser.add_argument("topic")
		parser.add_argument("menssage")
		args = parser.parse_args()
		bloglinda._out((user, args["topic"], args["message"]))

		# status 201 = created
		return 201

	def delete(self, user):

		parser = reqparse.RequestParser()
		parser.add_argument("topic")
		parser.add_argument("menssage")
		args = parser.parse_args()
		bloglinda._in((user, args["topic"], args["menssage"]))

		#status 200 = ok
		return "Message Deleted", 200


if __name__ == "__main__":

	app = Flask(__name__)
	api = Api(app)

	linda.connect()
	bloglinda = linda.TupleSpace()
	linda.universe._out(("Blog Linda", bloglinda))

	api.add_resource(MicroBlog, "/blog/<string:user")
	app.run(debug = True)


