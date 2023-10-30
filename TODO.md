# Improvements

- Can we use a database? What for? SQL or NoSQL?

  - given this usecase, I don't see much use for a database. We're dependent from github data, so we shouldn't store any of its content, because it would introduce potential inconsistency (a user could delete a file from a gist, or an entire gist). At most we could use it for briefly caching the content, just to avoid calling github too frequently, but the expiration should be relatively quick. For this case, a NoSQL database could work, because there aren't complicated relationships between our models

- How can we protect the api from abusing it?

  - there could be different levels of protection. From the authentication/authorization point of view, we could add a simple jwt beaker token, or, if we had some kind of user pool, we could even configure a RBAC model to have fine grained control over who can call the service endpoints.
  - from the performance point of view, we may also want to add a throttling rate to forbid an excessive use of the endpoints

- How can we deploy the application in a cloud environment?

  - having a docker image, it's usually suggested to deploy it using a IaaC approach, so that the resources are configured and versioned, and the environment is reproducible. Apart from this, it could be deployed in a serverless environment, or in a more traditional sense where we have to take care also of the server configuration and scalability.

- How can we be sure the application is alive and works as expected when deployed into a cloud environment?

  - first of all, is always good to have observability into the service, through structured logging and metrics, so we can get proactively notified if something behaves strangely. Additionally, there are tools to periodically check that the service is alive, for example calling the _ping_ endpoint that was already set up in this service boilerplate.
