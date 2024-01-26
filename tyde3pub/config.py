import logging
import sys

DEFAULT_REALM = "tyde3"
DEFAULT_KEYCLOAK_URL = "https://keycloak-prod-u9695.vm.elestio.app"
CLIENT_ID = "oauth2-proxy"
VERIFIER_AUDIENCE = "tyde3-rest-api"  # we verify tokens based on this audience
TYDE_BASE_URL = "https://tyde3.broentech.no"

ALL_ROLES = ["SuperAdministrator", "Administrator", "Operator", "api-access"]
LOGGER = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s~%(levelname)s~mod:%(module)s---> %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
LOGGER.addHandler(ch)



