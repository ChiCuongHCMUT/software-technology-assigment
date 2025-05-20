import  json
import exceptions as ex
from jsonschema.exceptions import ValidationError
import utils
import handlers
from dao.schema import SchemaBase
from dao.device import DeviceBase
from config import logger
from acquired_lock import acquire_lock_decorator
from dao.base import DBConnection
from dao.schema import SchemaBase


@acquire_lock_decorator
def handle_sqs_event(message, attributes, conn, **kwargs):
    action_type = utils.detect_action_type(attributes)

    try:
        device_uid = kwargs.pop('device_uid')
        logger.append_keys(device_uid=device_uid)
        schema_name = SchemaBase(conn).find_schema_name_by_device_uid(device_uid)
        if not schema_name:
            logger.error("Cannot found schema name by device_uid %s" % device_uid)
            return
        is_registered = action_type == "enrol"
        device = DeviceBase(conn, schema_name).find_by_device_uid(device_uid=device_uid, is_basic=is_registered)
        if not device:
            logger.error("Cannot found device %s" % device_uid)
            return
        messages = utils.message_builder(message=message, attributes=attributes)
        if is_registered:
            handlers.enrol(conn, schema_name, device_uid, device, **messages)
        elif action_type == "action_notify":
            handlers.handle_action_notify(message, attributes, device=device)
        else:
            handlers.checkin(conn, schema_name, device_uid, device, **messages)
    except (ValidationError, ex.EnrolError, ex.CheckinError, ex.DBError) as error:
        error_message = str(error)
        error_reason = None
        if isinstance(error, ValidationError):
            error_reason = "MISSING_REQUIRED_FIELDS"
        elif isinstance(error, ex.EnrolError):
            error_reason = "ENROL_ERROR"
        elif isinstance(error, ex.CheckinError):
            error_reason = "CHECKIN_ERROR"
        elif isinstance(error, ex.DBError):
            error_reason = "DB_ERROR"
        return utils.error_response(400, error_message, error_reason)