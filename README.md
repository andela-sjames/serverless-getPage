# serverless-getPage
**A simple serverless framework system used to retrieve minute details of a web page.**

# Reference:
https://serverless.com/framework/docs/providers/aws/guide/intro/


## Run locally?

download the zip file, unzip and change directory into document folder.

### Install serverless
```bash
npm install -g serverless
```

### setup AWS
*NB:* IAM AWS user should have programmatic access with policy to interact with lambda services
such as DynamoDB, S3, Lambda, Cloudformation, Cloudwatch and IAM amongst others depending on your use-case.
```bash
serverless config credentials --provider aws --key your_xxx_key --secret your_xxx_secret
```

## v3
Change directory to `document` & run  `npm install`
NB: You  should have docker running on your system before deploying, as this allows python packages to be added to the lambda function.


### deploy
```bash
serverless deploy
```

Once deployed you can go to the us-west-1 region on AWS to view the services and to invoke the lambda function as well.

OR

Run this command locally to invoke the AWS lambda function
```bash
serverless invoke -f create_request_identifier_handler -s dev -r us-east-1 -l -p event.json
```

### removal
```bash
serverless remove -v
```