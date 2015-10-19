import urlparse
from flask import request

def check_params(params, required_params):
	for required_param in required_params:
		if required_param not in params:
			raise Exception("missing " + required_param)
		if params[required_param] is not None:
			try:
				params[required_param] = params[required_param].encode('utf-8')
			except Exception:
				continue
	return

# def json_from_get(request):
# 	parsed = urlparse.urlparse(request.url)
# 	return urlparse.parse_qs(parsed.query)

def json_from_get(request):
	return dict((k, v if len(v) > 1 else v[0] )
                    for k, v in urlparse.parse_qs(request.query_string).iteritems())


def related_exists(request):
	try:
		related = request["related"]
	except Exception:
		related = []
	return related