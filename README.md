# serverless-getPage
**A simple serverless framework system used to retrieve minute details of a web page.**

# Reference:
https://serverless.com/framework/docs/providers/aws/guide/intro/


## Run locally?

### Install serverless
```bash
npm install serverless
```

### setup AWS
*NB:* IAM AWS user should have programmatic access with policy to interact with lambda services
such as DynamoDB, S3, Lambda, Cloudformation, Cloudwatch and IAM amongst others depending on your use-case.
```bash
serverless config credentials --provider aws --key your_xxx_key --secret your_xxx_secret
```

### Invoke the serverless locally V1.
#### link: https://serverless.com/framework/docs/providers/aws/cli-reference/invoke-local/
```bash
serverless invoke local --function get_page_title_handler -p event.json
```


### deploy
```bash
serverless deploy
```

### removal
```bash
serverless remove -v
```