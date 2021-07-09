import base64


def encode(body: str) -> str:
    """
    Encodes intput body into Base64 format.
    @param body: input to be encoded into Base64 format
    @return: Base64 encoded input
    """
    return base64.urlsafe_b64encode(body)


def decode(body: str) -> str:
    """
    Decodes input body from Base64 format.
    Some DOH clients send malformed body with missing padding.
    Thus, conditionally appending the padding.
    @param body: Base64 encoded input
    @return: decoded Base64 input
    """
    return base64.urlsafe_b64decode(body + '=' * (4 - len(body) % 4))


def to_camel(field: str) -> str:
    """
    Used by pydantic to convert fields between snake_case to camelCase.
    @param field: field in snake_case format
    @return: same field in camelCase format
    """
    words = field.split('_')
    return words[0].lower() + ''.join(w.capitalize() for w in words[1:])
