import asyncio
import os

from typing import Dict
from exceptions import DOHError
from models import APIGatewayV2HTTPEvent, APIGatewayV2HTTPResponse
from dohproxy import utils, constants
from dns.message import from_wire, QueryMessage
from dohproxy.server_protocol import DNSClient

from utils import encode, decode

UPSTREAM_RESOLVER = os.environ.get('UPSTREAM_RESOLVER', '1.1.1.1')
UPSTREAM_PORT = os.environ.get('UPSTREAM_PORT', '53')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

loop = asyncio.get_event_loop()
logger = utils.configure_logger('doh', LOG_LEVEL)
dns_client = DNSClient(UPSTREAM_RESOLVER, UPSTREAM_PORT, logger=logger)


def lambda_handler(args: Dict, _) -> Dict:
    """
    Main entry for AWS lambda, supplies API Gateway request payload that contains encoded DNS request.
    DNS request is decoded using Base64 and resolved using an upstream resolver.
    DNS response is then encoded back to Base64 and included as a part of API Gateway response.
    @param args: API Gateway request in raw, dictionary form containing encoded DNS request
    @param _: ignored context parameter, not used as part of this lambda
    @return: API Gateway response with encoded DNS response
    """
    logger.debug("Received API Gateway request: %s", args)
    api_gateway_request = APIGatewayV2HTTPEvent.parse_obj(args)
    source_ip = api_gateway_request.request_context.http.source_ip
    dns_request = construct_dns_request(api_gateway_request)
    logger.debug("Sending DNS request: %s", dns_request)
    dns_response: QueryMessage = loop.run_until_complete(dns_client.query(dns_request, source_ip))
    logger.debug("Received DNS response: %s", dns_response)
    response = construct_api_gateway_response(dns_response)
    logger.debug("Returning API Gateway response: %s", response)
    return response


def construct_dns_request(request: APIGatewayV2HTTPEvent) -> QueryMessage:
    """
    Extracts, decodes and deserializes DNS request from API Gateway request
    @param request: deserialized API Gateway request containing encoded DNS request
    @return: deserialized DNS request
    """
    encoded_body = extract_body(request)
    body = decode(encoded_body)
    return from_wire(body)


def extract_body(request: APIGatewayV2HTTPEvent) -> str:
    """
    Extracts DNS request body from API Gateway request based on HTTP method.
    GET requests have DNS requests encoded as part of the query string.
    POST requests have DNS requests encoded as part of the body
    @param request: API Gateway request containing encoded DNS request
    @return: encoded DNS request payload
    """
    method = request.request_context.http.method
    if method == 'GET':
        if 'dns' not in request.query_string_parameters:
            raise DOHError('Missing required query parameter \"dns\"')
        encoded_body = request.query_string_parameters['dns']
    elif method == 'POST':
        encoded_body = request.body
    else:
        raise DOHError('Unsupported HTTP method \"%s\"'.format(method))
    return encoded_body


def construct_api_gateway_response(dns_response: QueryMessage) -> Dict:
    """
    Constructs API Gateway response with encoded DNS response.
    @param dns_response: DNS request returned by the upstream resolver
    @return: response acceptable by API Gateway
    """
    encoded_response_body = encode(dns_response.to_wire())
    response = APIGatewayV2HTTPResponse(status_code=200,
                                        headers={'content_type': constants.DOH_MEDIA_TYPE},
                                        body=encoded_response_body,
                                        is_base_64_encoded=True)
    return response.dict(by_alias=True)  # return fields in camelCase
