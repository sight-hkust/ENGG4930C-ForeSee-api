# ENGG4930C(SIGHT) ForeSee API

HKUST Spring 2020, Hong Kong Eye Health Tracking Application

# Introduction

ForeSee is an application for tracking of eye health metrics such as myopia. This repository contains the API of the project.
It is written to be deployed to [AWS Lambda](https://aws.amazon.com/lambda/) using microframework [Chalice](https://github.com/aws/chalice).

# Getting Started
1. Create an AWS account
2. Follow the steps on Chalice [Quickstart](https://github.com/aws/chalice#credentials) and [Credentials](https://github.com/aws/chalice#credentials)
3. `cd` into `ENGG4930C-ForeSee-api/chalicelib` and create a file named `rdsconfig.py` with the following format. Look at [ENGG4930C-ForeSee-database](https://github.com/DoguD/ENGG4930C-ForeSee-database) for further reference.
```python
db_username = <YOUR_DB_USERNAME>
db_password = <YOUR_DB_PASSWORD>
db_name = <YOUR_DB_NAME>
db_endpoint = <YOUR_DB_ENDPOUNT>
```


4. `cd` into `ENGG4930C-ForeSee-api` and run `chalice deploy`
5. Copy the output URL, your API will be serving there.


![image of output URL](https://github.com/DoguD/ENGG4930C-ForeSee-api/blob/master/github-src/output_url.png )
