import * as path from 'path';
import * as cdk from '@aws-cdk/core';
import * as lambda from "@aws-cdk/aws-lambda";
import * as apiGateway from "@aws-cdk/aws-apigatewayv2";
import * as apiGatewayIntegrations from "@aws-cdk/aws-apigatewayv2-integrations";

const DEFAULT_UPSTREAM_RESOLVER = '1.1.1.1';

export class DohLambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

      const dohLambda = new lambda.Function(this, 'DOHLambda', {
        runtime: lambda.Runtime.PYTHON_3_8,
        code: lambda.Code.fromAsset(path.join(__dirname, '../assets/doh-lambda')),
        handler: "doh.lambda_handler",
        environment: {
          UPSTREAM_RESOLVER: DEFAULT_UPSTREAM_RESOLVER
        }
      });

      const dohApiGateway = new apiGateway.HttpApi(this, 'DOHApiGateway');
      dohApiGateway.addRoutes({
        path: '/dns-query',
        methods: [apiGateway.HttpMethod.GET, apiGateway.HttpMethod.POST],
        integration: new apiGatewayIntegrations.LambdaProxyIntegration({
          handler: dohLambda
        })
      });

      const apiGatewayUrlOutput = new cdk.CfnOutput(this, 'ApiGatewayUrl', {
        value: dohApiGateway.url!,
        description: 'Generated API Gateway URL that is used to resolve DNSOverHTTPS requests',
        exportName: 'APIGatewayURL'
      });
  }
}
