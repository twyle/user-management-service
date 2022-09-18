# user-management-service

> A Flask service for managing user registration, authentication and authorization.  

<p align="center">
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/feature-development-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/development-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/staging-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/release-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/production-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/security-bandit-yellow.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Made%20with- Python-1f425f.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/github/license/Naereen/StrapDown.js.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Medium-12100E?style=flat&logo=medium&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/github%20actions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=flat&logo=visual-studio-code&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/gunicorn-%298729.svg?style=flat&logo=gunicorn&logoColor=white" />
</p>

![](assets/images/user_management_service.png)

## Project Overview
This is a simple web application that makes the management of users easier. It enables a new user to register for an account and authenticates and authorizes registered users. It is built with flask and deployed to AWS Beanstalk.

## Working 

It's pretty easy to use the application. On the home page (http://localhost:5000/apidocs):

 1. Create an account (post details through registre route)
 2. Confirm your email address (paste the link given after registration into a browser).
 3. Access all the sites functionality.

 <p align=center>
  <img src="assets/videos/user-management-service-v3.gif" />
</p>

 ## Features

This application has several features including:

1. Deployed to an AWS EBS using Codedeploy.
2. Versioned using git and Hosted on GitHub.
3. Auto-deployed to AWS using AWS CodePipeline.
4. Uses gunicorn as the application servers.
5. Uses an Application Load Balancer to redirect traffic to the frontend
6. Uses AWS Opensearch and Firehose for logging.
7. Uses AWS SES to send confirmation emails.
8. Uses JWT to authorize users.

## Local Setup

Here is how to set up the application locally:

  1. Clone the application repo:</br>

      ```sh
      git clone https://github.com/twyle/user-management-service.git
      ```

  2. Navigate into the cloned repo:

      ```sh
      cd user-management-service
      ```

  3. Create a Virtual environment:

      ```sh
      python3 -m venv venv
      ```

  4. Activate the virtual environmnet:

      ```sh
      source venv/bin/activate
      ```

  5. Install the project dependancies:

      ```sh
      pip install --upgrade pip # update the package manager
      pip install -r requirements.txt  
      ```

  6. Create the environment variables for each service:

      ```sh
      touch .env
      ```

      Then paste the following into the file:

      ```sh

        FLASK_APP=manage.py
        FLASK_DEBUG=True
        FLASK_ENV=development

        POSTGRES_HOST=<YOUR_COMPUTER_IP_ADDRESS>
        POSTGRES_DB=lyle
        POSTGRES_PORT=5432
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=lyle

      ```

      Then create the database secrets:

      ```sh
      cd services/database
      touch .env
      ```

      Then paste the following into the file:

      ```sh
        POSTGRES_DB=lyle
        POSTGRES_PORT=5432
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=lyle
      ```

  7. Start the database containers:

      ```sh
      docker-compose -f database/docker-compose.yml up --build -d
      ```

  8. Create the database migrations:

      ```sh
      flask db migrate -m "Initial migration."
      flask db upgrade
      python manage.py seed_db
      ```

  9. Start the services:

      ```sh
      python manage.py run
      ```

  10. View the running application

      Head over to http://0.0.0.0:5000/apidocs 

## Development

 #### 1. Application Design

  1. **Services**

      The application consists of one service and a lambda function for uploading images to S3:

      1. User Management Service 

      ![](assets/images/user_management_service.png)
        
        This service is resposible for the registration of new users, as well as the authentication and authorization of registered users. The routes include:

        | Route                   | Method  | Description                 |
        | ------------------------| ------- |---------------------------- |
        | 'api/v1/auth/register'  | POST    | Register a new user.        |
        | 'api/v1/auth/login'     | POST    | Login as a registered user. |
        | 'api/v1/auth/logout'    | POST    | Logout as a logged in user. |
        | 'api/v1/auth/confirm'   | GET     | Confirm email address.      |
        | 'api/v1/auth/send'      | POST    | Send activation email.      |
        | 'api/v1/auth/refresh'   | GET     | Get a new access token.     |
        | 'api/v1/user'           | DELETE  | Delete a user.              |
        | 'api/v1/user'           | PUT     | Update user info.           |
        | 'api/v1/user'           | GET     | Get a user's info.          |
        | 'api/v1/users'          | GET     | List all users.             |

        1. Register as a new user with a unique email address and password as well as name.(Generates a uniques token) 
        2. Proceed to your email address and click on the link given within 24 hours to activate your account. (marks account as activated)
        3. Log into your account using your email and password. (You get a unique token for authorization)

        This service uses the Postgres Database to store the user info. It uses an SQS queue to schedule the sending of account activation emails, handled by the emailer Lambda function. It also writes logs to the sqs queue to be processed by the logging lambda function.

      The lambda function:

      1. Image Processor (image)

      ![](assets/images/image_processor.png)

        This Lambda function takes in an image from the sqs queue, processes it and stores it in an S3 bucket. It then provedes the url of the stored image to the blog service.

  2. **Database**

      The application uses Postgres and AWS S3. The postgres database is used to store user details. The AWS S3 bucket is used to store the profile pictures.

  3. **Security**

      The application uses JSON Web Tokens to authorize access to protected routes. The passwords are also encrypted.

 #### 2. Project Management

   1. **Coding standards** </br>

      The application had to adhere to the following coding standards:
      1. Variable names
      2. Function names
      3. Test driven development
      4. Individual modules need 60% coverage and an overall coverage of 60%.
      5. CI/CD pipeline has to pass before deployments.
      6. Commit messages format has to be adhered to.
      7. Only push code to github using development branches.
      8. Releases have to be tagged.
      9. Use pre-commit to run code quality checks
      10. Use comitizen to format commit messages

   2. **Application development process management** </br>

      The project uses GitHub Projects for management.

 #### 3. Development Workflow

 The application uses atleast 5 branches:

  1. Features branch used to develop new features.
  2. Development branch used to hold the most upto date features that are yet to be deployed.
  3. Staging branch holds the code that is currently being tested for production.
  4. The release branch holds all the assets used when creating a release.
  5. The production branch holds the code for the currently deployed application.

The development workflow follows the following steps:

  1. A feature branch is created for the development of a new feature.
  2. The code is then pushed to GitHub, triggering the feature-development-workflow.yml workflow. If all the tests pass, the feature is reviewde and merged into the development branch.
  3. The code in the development branch is then deployed to the development environment. If the deployment is succesful, the development branch is merged into the staging branch.
  4. This triggers the staging workflow. If all the tests are succesful, this branch is reviewed and deployed to a staging environment.
  5. For creatinga release, the staging branch is merged into the release branch. This happens when a tag is pushed to GitHub.
  6. Once a release is created, the release branch is merged into the production branch, which is deployed into production.

The workflows require a couple of secrets to work:

      ```sh
        FLASK_APP=manage.py
        FLASK_ENV=development

        SECRET_KEY=supersecretkey

        POSTGRES_HOST=<YOUR-IP-ADDRESS>
        POSTGRES_DB=lyle
        POSTGRES_PORT=5432
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=lyle

      ```

The workflows also require the followingenvironments to work:

  1. Test
  2. Staging
  3. Development
  4. Production

And within each environment, create a secret that indicates the environment type i.e

  1. Test -> ```FLASK_ENV=test```
  2. Staging -> ```FLASK_ENV=stage```
  3. Development -> ```FLASK_ENV=development```
  4. Production -> ```FLASK_ENV=production```

  ## Contribution

1. Fork it https://github.com/twyle/repo-template/fork
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Developer

Lyle Okoth – [@lylethedesigner](https://twitter.com/lylethedesigner) on twitter </br>

[lyle okoth](https://medium.com/@lyle-okoth) on medium </br>

My email is lyceokoth@gmail.com </br>

Here is my [GitHub Profile](https://github.com/twyle/)

You can also find me on [LinkedIN](https://www.linkedin.com/in/lyle-okoth/)

## License

Distributed under the MIT license. See ``LICENSE`` for more information.
