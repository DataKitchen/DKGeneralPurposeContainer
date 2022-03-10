

test:
	docker run \
		-v $(PWD)/tests/docker-share:/dk/docker-share \
		$(IMAGE) 
	nosetests $(PWD)/tests

