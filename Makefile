COMPOSE_PROJECT_NAME := betting_software

run:
	docker-compose -p ${COMPOSE_PROJECT_NAME} up --build

down:
	docker-compose -p ${COMPOSE_PROJECT_NAME} down

clean: down
	docker volume rm ${COMPOSE_PROJECT_NAME}_bet_maker_db_data && docker volume rm ${COMPOSE_PROJECT_NAME}_rabbit_data