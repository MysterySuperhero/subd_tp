import urlparse


def check_params(params, required_params):
	for required_param in required_params:
		if required_param not in params:
			raise Exception("missing " + required_param)
		if params[required_param] is not None:
			try:
				params[required_param] = params[required_param].encode('utf-8mb4')
			except Exception:
				continue
	return


def json_from_get(request):
	parsed = urlparse.urlparse(request.url)
	return urlparse.parse_qs(parsed.query)


def related_exists(request):
	try:
		related = request["related"]
	except Exception:
		related = []
	return related


def get_optional_params(request, values):
	optional = dict([(k, request[k]) for k in set(values) if k in request])
	return optional
