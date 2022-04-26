# Summary
This is a data engineering project, with the goal of setting up a data pipeline that will ingest labor statistics data from various sources, and keep the data updated at regular intervals. A dashboard is built in the end to visualize the data and for data analysts to derive further insights. You can feel free to adapt this project to collect any other data that requires regular refreshes.

## Infrastructure
The infrastructure used in this project are AWS S3 and AWS RDS. AWS offers a [free tier](https://aws.amazon.com/rds/free/) that we can use to experiment with.

### Set up infrastructure with Terraform
Instead of setting up my infrastructure manually, Terraform was used. **[Terraform]**(https://www.terraform.io/) is an Infrastructure-as-Code tool that allows us to create, manage, destroy infrastructure through declarative configuration language. It provides support for all the major Cloud service providers like AWS, GCP or Azure.

![enter image description here](https://mktg-content-api-hashicorp.vercel.app/api/assets?product=terraform&version=refs/heads/stable-website&asset=website/img/docs/intro-terraform-workflow.png)
In my terraform files, I wrote code to create a bucket on S3 and to create a Postgres database on RDS. See the `terraform` directory for implementation details.

To apply the terraform changes (i.e. create the bucket and dataset), `cd` into the `terraform` directory, run:
```
terraform init
terraform apply
```
Terraform will list out the changes that will be applied. You simply have to type in 'yes' to confirm.
After the command finishes, if you log into your AWS Console, you should see your newly created bucket and dataset.

## Airflow
Next, we set up Airflow on our local machine through **Docker** with **Docker Compose**.

### Setting up Airflow with Docker
Airflow provides [official documentation](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) on how to run Airflow on Docker Compose. We will not reinvent the wheel here and simply copy over the official configuration. We will, however, use our own custom image. Notably, we want to install some python packages we will use and also AWS SDK.
You can find the implementation of the custom image in the `Dockerfile`.

In the `airflow` directory, run to build the custom image:
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
![Screenshot 2022-04-27 010545](https://user-images.githubusercontent.com/7219284/165354728-524b3e19-82d5-490b-aa12-11ac70ef2691.png)


### DAGs

There are currently 5 existing DAGs in the repository that pulls data from these respective places:
- ingest_economic_inactivity_data
	- https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/economicinactivity/timeseries/lf2m/lms
- ingest_female_employment_data
	- https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/lf25/lms
- ingest_male_employment_data
   - https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/mgsv/lms
- ingest_unemployment_data
	- https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/mgsx/lms
- ingest_wages_data
	- https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/timeseries/kab9/emp

They are set to run once every month to pull the latest updates from the source. 

They first download the CSVs, uploads them to S3, then some data transformation is done on them before they are inserted into a managed PostgreSQL database.

![image](https://user-images.githubusercontent.com/7219284/165355554-600b0f1c-65aa-4fa7-9a6a-adbef41f783b.png)

Most of the logic is abstracted to custom operators, since all 5 tasks are very similar and can share the same custom operators.

## Visualization
The data is then visualized with a BI tool. In this case, I have chosen to use Apache Superset hosted by Preset.

The dashboard is connected to the PostgreSQL database and therefore will have the newest data always: https://dc824a2a.us2a.app.preset.io/superset/dashboard/p/82VrgKZlbPz/
(Preset account is required to view)

![image](https://user-images.githubusercontent.com/7219284/165369989-2d49d1c1-3d6e-4296-a6a1-ac4f22f38b51.png)

