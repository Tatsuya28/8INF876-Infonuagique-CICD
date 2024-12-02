# Help notes

## Login with your API Token

```bash
docker login registry.digitalocean.com
```

## Build your container image locally

```bash
docker build -t registry.digitalocean.com/uqac-8inf876/django-cicd-src:latest -f Dockerfile .
```

## Push your container image

```bash
docker push registry.digitalocean.com/uqac-8inf876/django-cicd-src --all-tags
```

Naturally, for all these steps replace `registry.digitalocean.com/uqac-8inf876/` with your container registry and `django-cicd-src` with whatever image name you want to give your Django project.
