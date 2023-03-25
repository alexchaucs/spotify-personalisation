img ?= boiler-plate

build-image:
	docker build -t $(img) .

run-container:
	docker run -d -p 8080:80 $(img)

create-container:
	make build-image && make run-container

dev-container:
	docker-compose up --build