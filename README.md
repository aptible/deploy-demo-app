# ![](https://github.com/aptible/mintlify-docs/blob/073bfba084ad9ea18217f5816568c3f832d5f0ae/logo/light.png)

## deploy-demo-app

This application is intended to facilitate learning the features of the Aptible Deploy platform, without
needing to deploy _your_ application.

![](https://github.com/aptible/deploy-demo-app/blob/main/screenshots/demo.png)

There are two ways you can use this application (in sections below): Guided Experience (1) and Quickstart (2)

### Guided experience (1)

For new users of the Aptible Deploy platform, you can deploy this application following step-by-step 
instructions found [here](https://www.aptible.com/docs/getting-started/deploy-starter-template/python-flask).

This will help you deploy the app, and learn to configure additional features of the Aptible Deploy platform 
in a guided manner. This app even features a checklist that follows the step-by-step guide, to confirm 
that you have performed each step properly!

![](https://github.com/aptible/deploy-demo-app/blob/main/screenshots/checklist.png)


### Quick start (2)

For users who are familiar with Deploy, and simply need a web application to experiment with, these
 are the minimal steps needed to run this application.

* Create an application: `aptible apps:create $HANDLE`
* Deploy the App - CHOOSE ONE:
  * [Direct Docker Deploy](https://www.aptible.com/documentation/deploy/reference/apps/image/direct-docker-image-deploy.html) : `aptible deploy --app $HANDLE --docker-image aptible/deploy-demo-app`
  * [Dockerfile Deploy](https://deploy-docs.aptible.com/docs/dockerfile-deploy-example): 
  
```shell
git clone git@github.com:aptible/deploy-demo-app.git 
cd deploy-demo-app 
git remote add aptible git@beta.aptible.com:$ENVIRONMENT/$HANDLE.git 
git push aptible main
```

* Set the configuration for your database, force HTTPS only, and increase the scale:

```shell
aptible -- apps:scale 
aptible config:set \
  DATABASE_URL="<<DATABASE_URL>>" \ 
  REDIS_URL="<<REDIS_URL>>" \
  FORCE_SSL=true \
  IDLE_TIMEOUT=90
```

* Create an Endpoint for the application from your Dashboard.

## Copyright

Copyright (c) 2024 [Aptible](https://www.aptible.com). All rights reserved.

[<img src="https://avatars2.githubusercontent.com/u/1580788?v=4&s=60" />](https://github.com/UserNotFound)

