# ![](http://aptible-media-assets-manual.s3.amazonaws.com/web-horizontal-350.png)

## Deploy-demo-app

This application is intended to facilitate learning the features of the Aptible Aptible Deploy platform, wihtout needing to deploy _your_ application.

![](https://github.com/aptible/deploy-demo-app/blob/master/screenshots/demo.png)

There are two way you can use this application:

#### Guided experience

For new users of the Aptible Deploy platform, you can deploy this application follwing step by step instructions found [here](https://www.aptible.com/documentation/deploy/tutorials/deploy-demo-app.html).

This will help you deploy the app, and learn to configure additional features of the Aptible Deploy platform in a guided manner. This app even features a checklist that follows the step-by-step guide, to confirm that you have performed each step properly!

![](https://github.com/aptible/deploy-demo-app/blob/master/screenshots/checklist.png)


#### Quick start

For users who are familiar with Deploy, and simply need a web application to experiement with, these are the minimal steps needed to run this application.

* Create an application: `aptible apps:create $HANDLE`

* Deploy the App via [Direct Docker Image Deploy](https://www.aptible.com/documentation/deploy/reference/apps/image/direct-docker-image-deploy.html) : `aptible deploy --app $HANDLE --docker-image aptible/deploy-demo-app`

* Create an Endpoint for the application from your Dashboard.

## Copyright

Copyright (c) 2022 [Aptible](https://www.aptible.com). All rights reserved.

[<img src="https://avatars2.githubusercontent.com/u/1580788?v=4&s=60" />](https://github.com/UserNotFound)

