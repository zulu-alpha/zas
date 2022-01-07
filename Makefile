shell:
	@poetry run python manage.py shell_plus --ipython
notebook:
	@poetry run python manage.py shell_plus --notebook
collectstatic:
	@poetry run python manage.py collectstatic
makemigrations:
	@poetry run python manage.py makemigrations
migrate:
	@poetry run python manage.py migrate
mergemigrations:
	@poetry run python manage.py makemigrations --merge
initdb:
	@poetry run python manage.py migrate
db:
	@docker-compose -f docker-compose.dev.yml up db
