prepare:
	sha1sum -c isolate.war.sha1 && unzip -d isolate isolate.war

up:
	docker-compose up -d
start:
	docker-compose start
stop:
	docker-compose stop
restart:
	docker-compose restart

clean: 
	docker-compose down
	rm -rf isolate

run: prepare up
