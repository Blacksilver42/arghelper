import pycurl, cache

def blind_try(url, agent=None):
	"""Blindly return the http code for a url. Don't ask any questions."""
	curl = pycurl.Curl()
	curl.setopt(curl.NOBODY, True)
	curl.setopt(curl.URL, url)
	if(agent):
		curl.setopt(curl.USERAGENT, agent)
	curl.perform()
	code = curl.getinfo(pycurl.HTTP_CODE)
	print("> HEAD  {url:40}:{code}".format(url=url, code=code))
	return code

def blind_try_cached(url, cache, agent=None):
	"""Blindly look up the url, respecting the cache.
	Pass cache as {} if you don't want me to look up in the cache."""
	
	response = cache.get(url)
	if(response == None):
		response = blind_try(url, agent=agent)
		cache.add(url, response)
	else:
		print("(CACHED) {url:40}:{code}".format(url=url, code=response))
	
	return response

def try_url(url, opts={}):
	"""Actually use this function"""
	
	agent = opts.get("useragent")
	nocache = opts.get("nocache", False)
	if(nocache == True):
		arg_cache = {}
	else:
		arg_cache = cache.cache
	
	return blind_try_cached(url, arg_cache, agent=agent)
