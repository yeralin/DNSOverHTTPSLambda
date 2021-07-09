# DNSOverHTTPS based on AWS Lambda + API Gateway
Reproduces a CDK project based on the article: https://medium.com/@daniyaryeralin/dnsoverhttps-over-lambda-7c807e06721b


## Deployment intructions
1. `npm run prepare`
2. `cdk bootstrap`
3. `cdk deploy`

## Useful commands

 * `npm run prepare` download and store python dependencies under `assets/doh-lambda`
 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
 * `python -m unittest tests/tests.py`  run unittests
 