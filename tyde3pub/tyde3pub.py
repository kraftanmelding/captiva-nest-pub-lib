__author__ = 'Marius'
"""
    >File : tyde3pub.py

    >Date of creation : 15.01.2024

    >Copyrights : Captiva Digital Solutions AS

    >Project : Captiva Nest

    >Author : Marius Øgård (mo@captiva.no)

    Description :

        This is a public library that encapsule useful Captiva Nest API endpoints.

"""

from jwt import PyJWKClient
import jwt
import requests
import time
from . import config


class TydeClient:

    def __init__(self, configuration):
        """
        Constructor :
            return a new Auth object. Only one object should be instantiated. It implements:
            * get_access_token : return a valid access token.
            * Verifier: all the verifier methods are also accessible here.
        Args:
            configuration (dict): Configuration dictionary. Example: {
                                                                "username" : "pablo@broentech.no", <-- Required
                                                                "password" : "adsadad343143da",    <-- Required
                                                                "client_id" : "client_id",
                                                                "base_url" : "http://keycloak:8080",
                                                                "realm": "tyde3",
                                                                "audience": "tyde3-rest-api",
                                                                "tyde_base_url": "https://tyde.broentech.no"
                                                            }
        """
        self.access_token = None
        self.keycloak_url = f"{configuration.get('base_url', config.DEFAULT_KEYCLOAK_URL)}/realms/{configuration.get('realm', config.DEFAULT_REALM)}"
        self.client_id = configuration.get("client_id", config.CLIENT_ID)
        self.access_token_url = f"{self.keycloak_url}/protocol/openid-connect/token"
        self.username = configuration["username"]
        self.password = configuration["password"]
        self.target_audience = configuration.get("audience", config.VERIFIER_AUDIENCE)
        self.jwks_client = PyJWKClient(f"{self.keycloak_url}/protocol/openid-connect/certs")
        self.tyde_base_url = configuration.get('tyde_base_url', config.TYDE_BASE_URL)
        self.__fetch_access_token()

    # ######################  TOKEN/ AUTH RELATED FUNCTIONS #############################################

    def __fetch_access_token(self):
        data = {
            'username': self.username,
            'password': self.password,
            'client_id': self.client_id,
            'grant_type': 'password'
        }  # post body

        self.access_token = None
        while not self.access_token:
            try:
                response = requests.post(self.access_token_url, data=data)
                response.raise_for_status()
                # access json content
                json_response = response.json()
                self.access_token = json_response["access_token"]
            except Exception as e:
                config.LOGGER.warning(f"Failed to fetch online token! Trying again in 10 seconds {e}")
                time.sleep(10)

    def is_token_valid(self):
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(self.access_token)
            jwt.decode(
                self.access_token,
                signing_key.key,
                "RS256",
                audience=self.target_audience
            )

            return True

        except Exception as e:
            config.LOGGER.warning(f"Token Expired? {e}")
            return False

    def get_access_token(self, bearer=True):
        """ Return a valid access token. If the current access token is expired, it will automatically fetch a new one.
        Args:
            bearer (bool Optional def=False): Prepend the world 'Bearer' in front of the access token
        Returns:
            string (string): A valid access token.
        """
        # if token is not valid we need to fetch a new one.
        if not self.is_token_valid():
            config.LOGGER.debug("fetching token online")
            self.__fetch_access_token()
        # we prepend the word Bearer , if asked.
        return f"Bearer {self.access_token}" if bearer else self.access_token

    def print_role_info(self):
        access_token = self.get_access_token(False)
        signing_key = self.jwks_client.get_signing_key_from_jwt(access_token)
        userinfo = jwt.decode(
            access_token,
            signing_key.key,
            "RS256",
            audience=config.CLIENT_ID,
            options={"verify_signature": True}
        )

        roles = userinfo["realm_access"]["roles"]
        print(f"Your Email: {userinfo['email']} , Your Roles are: {list(set(roles) & set(config.ALL_ROLES))}")

    def get_upstream_status(self):
        print("checking Upstream ")
        head = {"Authorization": self.get_access_token()}
        try:
            my_res = requests.get(config.TYDE_BASE_URL + "/api/v1/healthz", headers=head)
            my_res.raise_for_status()
            print("Proxy Is online!")
        except Exception as e:
            config.LOGGER.warning(f"Something wrong with the proxy. Error is: {e}")
        try:
            my_res = requests.get(config.TYDE_BASE_URL + "/api/v1/context/healthz", headers=head)
            my_res.raise_for_status()
            print("Context manager Is online!")
        except Exception as e:
            config.LOGGER.warning(f"Something wrong with the Context manager. Error is: {e}")
        try:
            my_res = requests.get(config.TYDE_BASE_URL + "/api/v1/access/healthz", headers=head)
            my_res.raise_for_status()
            print("Access manager Is online!")
        except Exception as e:
            config.LOGGER.warning(f"Something wrong with the Access manager. Error is: {e}")

    def has_access_to_pp(self, pp_id):
        return self.make_request(f"/api/v1/access/users/hasaccess?email={self.username}&powerplant_id={pp_id}",
                                 "Something went wrong with the access request!")

    # ######################  POWER PLANT RELATED FUNCTIONS #############################################

    def make_request(self, url_suffix, log_message, method='get', data=None):
        request_url = config.TYDE_BASE_URL + url_suffix
        headers = {"Authorization": self.get_access_token()}
        response = None

        try:
            if method == 'get':
                response = requests.get(request_url, headers=headers, params=data)
            elif method == 'post':
                response = requests.post(request_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            error_details = f" Code {response.status_code} {response.text}" if response else ""
            config.LOGGER.warning(f"{log_message}{error_details} Error: {e}")
            return {}

    def get_powerplant_sensors(self, pp_id):
        data = {"id": pp_id}
        return self.make_request("/api/v1/context/context/plant",
                                 "Something went wrong with the Power plant list request!",
                                 data=data)

    def list_powerplants(self):
        return self.make_request("/api/v1/context/context/plants",
                                 "Something went wrong with the Power plant list request!")

    def get_powerplant_info(self, pp_id):
        return self.make_request(f"/api/v1/access/powerplants/{pp_id}/info",
                                 "Something went wrong with getting Power plant info!")

    # ########################## SENSORS RELATED FUNCTIONS ##############################################

    def get_sensors_for_powerplant(self, pp_id=None):
        data = {"id": pp_id}

        return self.make_request("/api/v1/context/context/sensor",
                                 "Something went wrong with the sensor request!",
                                 data=data)

    def get_sensors_for_all_powerplants(self):
        return self.make_request("/api/v1/context/context/sensors",
                                 "Something went wrong with the sensor request!")

    def get_sensor_info(self, sensor_ids):
        data = {"id": sensor_ids}

        return self.make_request("/api/v1/context/context/sensor",
                                 "Something went wrong with the sensor info request!",
                                 data=data)

    def delete_sensor_data(self, sensor_ids, from_time, to_time):
        data = {'sensor_ids': sensor_ids, "from_time": from_time, "to_time": to_time}
        config.LOGGER.warning(f"Deleting Sensor data {data}")

        return self.make_request("/api/v1/data/deletedata",
                                 "Something went wrong with the delete sensor data request!",
                                 method='post',
                                 data=data)

    def get_aggregated_data(self, sensor_ids, from_time=None, to_time=None, aggregation="HOURLY"):
        data = {
            'sensor_ids': sensor_ids,
            "from_time": from_time,
            "to_time": to_time,
            'aggregation': aggregation
        }

        return self.make_request("/api/v1/sensors/aggregated",
                                 "Something went wrong with the aggregated data request!",
                                 data=data)

    def get_raw_data(self, sensor_ids, from_time=None, to_time=None):
        data = {
            'sensor_ids': sensor_ids,
            "from_time": from_time,
            "to_time": to_time
        }

        return self.make_request("/api/v1/sensors/raw",
                                 "Something went wrong with the raw data request!",
                                 data=data)

    def get_alarms(self, sensor_ids, from_time=None, to_time=None):
        data = {
            'sensor_ids': sensor_ids,
            "from_time": from_time,
            "to_time": to_time
        }

        return self.make_request("/api/v1/alarms",
                                 "Something went wrong with the alarm request!",
                                 data=data)

    def get_latest_datapoint(self, sensor_ids):
        data = {'sensor_ids': sensor_ids}
        return self.make_request("/api/v1/sensors/latest",
                                 "Something went wrong with the latest datapoint request!",
                                 data=data)

    # ######################  PORTFOLIO RELATED FUNCTIONS ###############################################

    def list_portfolios(self):
        return self.make_request("/api/v1/access/portfolios/list",
                                 "Something went wrong with the portfolio list request!")

    def get_portfolio_info(self, pp_id):
        return self.make_request(f"/api/v1/access/portfolio/{pp_id}",
                                 "Something went wrong with getting portfolio info!")
