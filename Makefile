tanenbaum-up:
	@bash ./tanenbaum-up.sh
.PHONY: tanenbaum-up

tanenbaum-down:
	docker-compose stop
.PHONY: tanenbaum-down

tanenbaum-clean:
	docker-compose down
	docker image ls 'sentinel' --format='{{.Repository}}' | xargs -r docker rmi
	docker volume ls --filter name=sentinel --format='{{.Name}}' | xargs -r docker volume rm
.PHONY: tanenbaum-clean
