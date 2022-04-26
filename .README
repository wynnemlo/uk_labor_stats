# Summary
This is a data engineering project, with the goal of setting up a data pipeline that will ingest labor statistics data from various sources, and keep the data updated at regular intervals. A dashboard is built in the end to visualize the data and for data analysts to derive further insights. You can feel free to adapt this project to collect any other data that requires regular refreshes.

## Infrastructure
The infrastructure used in this project are Google Cloud Storage and Google BigQuery. GCP offers a [free tier](https://cloud.google.com/free/docs/gcp-free-tier) that has a 90-day trial and free $300 that anyone can sign up for.

### Set up infrastructure with Terraform
Instead of setting up my infrastructure manually, Terraform was used. **[Terraform]**(https://www.terraform.io/) is an Infrastructure-as-Code tool that allows us to create, manage, destroy infrastructure through declarative configuration language. It provides support for all the major Cloud service providers like AWS, GCP or Azure.

![enter image description here](https://mktg-content-api-hashicorp.vercel.app/api/assets?product=terraform&version=refs/heads/stable-website&asset=website/img/docs/intro-terraform-workflow.png)
In my terraform files, I wrote code to create a bucket on Google Cloud Storage and to create a dataset on Google BigQuery. See the `terraform` directory for implementation details.

To apply the terraform changes, run `terraform init` and `terraform apply` to create the bucket and the dataset.

## Airflow
Next, we set up Airflow on our local machine through **Docker** with **Docker Compose**.

### Setting up Airflow with Docker
Airflow provides [official documentation](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) on how to run Airflow on Docker Compose. We will not reinvent the wheel here and simply use the official one but use our own custom image. Notably, we want to install some python packages we will use and also GCloud SDK.

Run to build the custom image:
```
docker-compose build
```
Next, initialize the database:
```
docker-compose up airflow-init
```
Now run airflow:
```
docker-compose up
```
We should be able to access the web interface for this instance at `http://localhost:8080` in our browser:

