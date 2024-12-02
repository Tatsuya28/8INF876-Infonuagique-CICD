# Guide de déploiement

1. Test Django

```bash
python manage.py test
```

2. Build container

```bash
docker build -f Dockerfile -t registry.digitalocean.com/uqac-8inf876/django-cicd-src:latest -t registry.digitalocean.com/uqac-8inf876/django-cicd-src:v1 .
```

3. Push container to registry Digital Ocean

```bash
docker push registry.digitalocean.com/uqac-8inf876/django-cicd-src --all-tags
```

4. Update secrets

```bash
kubectl delete secret django-cicd-k8s-src-prod-env
# on Linux
kubectl create secret generic django-cicd-k8s-src-prod-env --from-env-file=src/.env.prod
# on Windows
kubectl create secret generic django-cicd-k8s-src-prod-env --from-env-file=src\.env.prod
```

5. Update deployment

```bash
# on Linux
kubectl apply -f k8s/apps/django-cicd-src.yaml
# on Windows
kubectl apply -f k8s\apps\django-cicd-src.yaml
```

6. Wait for the deployment rollout to be finished

```bash
kubectl rollout status deployment deployment/django-cicd-src-deployment
```

7. Migrate database

```bash
# on Linux
export SINGLE_POD_NAME=$(kubectl get pods -o jsonpath="{.items[0].metadata.name}")
# on Windows
set SINGLE_POD_NAME=$(kubectl get pods -o jsonpath="{.items[0].metadata.name}")
kubectl exec -it $SINGLE_POD_NAME -- bash /app/migrate.sh
```
