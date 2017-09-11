# ![](http://aptible-media-assets-manual.s3.amazonaws.com/web-horizontal-350.png)

## Enclave-demo-app

This application is intended to facilitate learning the features of the Aptible Enclave platform, wihtout needing to deploy _your_ application.

![](https://github.com/aptible/enclave-demo-app/blob/master/screenshots/demo.png)

There are two way you can use this application:

#### Guided experience

For new users of the Enclave platform, you can deploy this application follwing step by step instructions found [here](https://www.aptible.com/documentation/enclave/tutorials/enclave-demo-app.html).

This will help you deploy the app, and learn to configure additional features of the Enclave platform in a guided manner. This app even features a checklist that follows the step-by-step guide, to confirm that you have performed each step properly!

![](https://github.com/aptible/enclave-demo-app/blob/master/screenshots/checklist.png)


#### Quick start

For users who are familiar with Enclave, and simply need a web application to experiement with, these are the minimal steps needed to run this application.

* Create an application: `aptible apps:create $HANDLE`

* Deploy the App via [Direct Docker Image Deploy](https://www.aptible.com/documentation/enclave/reference/apps/image/direct-docker-image-deploy.html) : `aptible deploy --app $HANDLE --docker-image quay.io/aptible/enclave-demo-app`

* Create an Endpoint for the application from your Dashboard.

## Copyright

Copyright (c) 2017 [Aptible](https://www.aptible.com). All rights reserved.

[<img src="https://avatars2.githubusercontent.com/u/1580788?v=4&s=60" />](https://github.com/UserNotFound)

