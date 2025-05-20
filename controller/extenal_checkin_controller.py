import handlers
from jsonschema.exceptions import ValidationError
import exceptions as ex
from config import (
    ErrorCode,
    logger
)
import config
import utils
import constants
from helpers import get_token_auth_header, decode_jwt_token
import s3_handler
import json
from constants import ProvisionType


def device_checkin_controller(event):
    try:
        if type(event.get('body')) is str:
            body = event.get('body')
            event['body'] = json.loads(body) if body else body
        body = event.get('body')
        headers = event.get('headers', {})
        bearer_token = get_token_auth_header(headers)
        jwt_decode = decode_jwt_token(bearer_token)
        if not jwt_decode:
            return constants.INVALID_TOKEN_RESPONSE
        device_uid = jwt_decode.get("imei")
        response_body = handlers.checkin_from_api_gateway(body=body, device_uid=device_uid, **jwt_decode)
        if response_body and response_body.get("message", None) == ErrorCode.INVALID_STATE:
            raise ex.InvalidStateError(ErrorCode.INVALID_STATE)
        logger.info(f"Policy response_body: {response_body}")
        status_code = get_status_code(response_body)
        response_body = enrich_response_for_gateway(event, response_body)
        return {
            "isBase64Encoded": False,
            "statusCode": status_code,
            "body": response_body
        }
    except (ex.UnsupportedProvisioningType, ValidationError, ex.CheckinError, ex.DBError) as error:
        error_message, error_reason = str(error), None
        if isinstance(error, ex.UnsupportedProvisioningType):
            error_reason = "OEM_NOT_SUPPORTED"
        elif isinstance(error, ValidationError):
            error_reason = "MISSING_REQUIRED_FIELDS"
        elif isinstance(error, ex.CheckinError):
            error_reason = "CHECKIN_ERROR"
        elif isinstance(error, ex.DBError):
            error_reason = "DB_ERROR"
        return utils.error_response(400, error_message, error_reason)
    except Exception as e:
        error_reason = ErrorCode.INVALID_STATE if str(e) == ErrorCode.INVALID_STATE else str(e)
        return utils.error_response(400, str(e), error_reason)


def device_enroll_controller(event):
    try:
        if type(event.get('body')) is str:
            body = event.get('body')
            event['body'] = json.loads(body) if body else body
        body = event.get('body')
        device_uid = body.get("core", {}).get("imei")
        response_body =  handlers.enrol_from_api_gateway(body=body, device_uid=device_uid)
        status_code = get_status_code_for_enrol(response_body)
        return {
            "isBase64Encoded": False,
            "statusCode": status_code,
            "body": json.dumps(response_body)
        }
    except (ex.UnsupportedProvisioningType, ValidationError, ex.EnrolError, ex.DBError) as error:
        error_message, error_reason = str(error), None
        if isinstance(error, ex.UnsupportedProvisioningType):
            error_reason = "OEM_NOT_SUPPORTED"
        elif isinstance(error, ValidationError):
            error_reason = "MISSING_REQUIRED_FIELDS"
        elif isinstance(error, ex.EnrolError):
            error_reason = "ENROL_ERROR"
        elif isinstance(error, ex.DBError):
            error_reason = "DB_ERROR"
        return utils.error_response(400, error_message, error_reason)


def enrich_response_for_gateway(event, response_body):
    logger.debug(f"event: {event}; response_body: {response_body}")
    if response_body and response_body.get("imei") and response_body.get("service_type_id") and response_body.get(
            "service_type_id") != config.ServiceType.INVENTORY and response_body.get("provision_type"):
        prov_type = response_body.get("provision_type")
        # In case of G_LOCK we need to get the config bundle from S3 from ZERO_TOUCH which supports GLOCK in the enhancement ticket: TPP-3850
        prov_type = ProvisionType.ZERO_TOUCH if prov_type == ProvisionType.G_LOCK else prov_type
        eTag = s3_handler.get_bundle(response_body.get("schema_name"), response_body.get("service_type_id"),
                                     event['body'].get("currentStatus").get("configBundleVersion"), prov_type)
        if eTag:
            response_body["eTag"] = eTag

    if response_body.get("policy"):
        response_body["policy"] = json.dumps(response_body.get("policy"))
    else:
        response_body = json.dumps(response_body)

    return response_body


def get_status_code(body):
    status_code = body.get("status_code")
    if status_code:
        return status_code
    return 200


def get_status_code_for_enrol(body):
    status_code = body.get("error", {}).get("code")
    status_code = status_code or 200
    return status_code