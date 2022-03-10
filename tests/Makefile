

test:
	docker run \
		-v $(PWD)/tests/docker-share:/dk/docker-share \
		$(IMAGE) 
	python3 -m nose $(PWD)/tests

