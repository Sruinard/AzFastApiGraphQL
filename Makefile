test:
	python -m pytest tests

deploy:
	./deployment/infra.sh

redeploy_webapp:
	az webapp up

clean:
	rm -rf .azure
	az group delete -n graphql_webapp

