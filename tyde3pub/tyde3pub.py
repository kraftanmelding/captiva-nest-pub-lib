__author__ = 'Luca'
"""
    >File : tyde3pub.py

    >Date of creation : 15.01.2024

    >Copyrights : Broentech Solutions AS

    >Project : Next-Gen Tyde

    >Author : Luca Petricca (lucap@broentech.no)

    Description :

        This is a public library that encapsule useful tyde3 api.

"""

from jwt import PyJWKClient
import jwt
import json
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
            config (dict): Configuration dictionary. Example: {
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
            decoded = jwt.decode(self.access_token, signing_key.key, "RS256",
                                 audience=self.target_audience)
            return True

        except Exception as e:
            config.LOGGER.warning(f"Token Expired? {e}")
            return False

    def get_access_token(self, bearer=True):
        """ Return a valid access token. If the current access token is expired, it will automatically fetch a new one.
        Args:
            bearer (bool Optional def=False): Prepend the world 'Bearer' in front of the access token)
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

    def has_access_to_hpp(self, hppid):
        request_url = config.TYDE_BASE_URL + f"/api/v1/access/users/hasaccess?email={self.username}&powerplant_id={hppid}"
        try:
            head = {"Authorization": self.get_access_token()}
            my_res = requests.get(request_url, headers=head)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the request! Code{my_res.status_code} Error is:{e}")
            return {}

    # ######################  POWERPLANTS RELATED FUNCTIONS #############################################
    def list_powerplants(self):
        request_url = config.TYDE_BASE_URL + f"/api/v1/context/context/plants"
        try:
            head = {"Authorization": self.get_access_token()}
            my_res = requests.get(request_url, headers=head)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the request! Code{my_res.status_code} Error is:{e}")
            return {}

    def get_powerplant_info(self, hppid):
        request_url = config.TYDE_BASE_URL + f"/api/v1/access/powerplants/{hppid}/info"
        try:
            head = {"Authorization": self.get_access_token()}
            my_res = requests.get(request_url, headers=head)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the request! Code{my_res.status_code} Error is:{e}")
            return {}

    # ######################  SENSORS RELATED FUNCTIONS #############################################
    def get_sensor_for_powerplants(self, hpp_id=None):
        data = {}
        if hpp_id:
            data["associations"] = hpp_id
        request_url = config.TYDE_BASE_URL + f"/api/v1/context/context/sensors"
        try:
            head = {"Authorization": self.get_access_token()}
            my_res = requests.get(request_url, params=data, headers=head)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the request! Code{my_res.status_code} {my_res.text} Error is:{e}")
            return {}

    def get_sensor_info(self, sensorids):
        data = {"sensorids": sensorids}
        request_url = config.TYDE_BASE_URL + f"/api/v1/context/context/sensors"
        try:
            head = {"Authorization": self.get_access_token()}
            my_res = requests.get(request_url, params=data, headers=head)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the request! Code{my_res.status_code}  {my_res.text} Error is:{e}")
            return {}

    def delete_sensor_data(self, sensor_ids, timefrom, timeto):
        request_url = config.TYDE_BASE_URL + "/api/v1/data/deletedata"
        try:
            data = {'sensorids': sensor_ids, "timefrom": timefrom, "timeto": timeto}
            config.LOGGER.warning(f"Deleting Sensor data {data}")
            head = {"Authorization": self.get_access_token()}
            my_res = requests.delete(request_url, params=data, headers=head)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the request! Code{my_res.status_code}  {my_res.text} Error is:{e}")
            return {}

    def read_data(self, sensor_ids, timefrom=0, timeto=0, granularity="HOURLY", aligned=False):
        request_url = config.TYDE_BASE_URL + "/api/v1/data/readdata"
        try:
            data = {
                'sensorids': sensor_ids,
                'aggtype': granularity,
                "timefrom": timefrom,
                "timeto": timeto,
                "aligned": aligned
            }

            head = {"Authorization": self.get_access_token()}
            my_res = requests.get(request_url, params=data, headers=head)
            print(my_res.status_code)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the request! Code{my_res.status_code} {my_res.text} Error is:{e}")
            return {}

    def read_alarms(self, sensor_ids, timefrom=0, timeto=0):
        request_url = config.TYDE_BASE_URL + "/api/v1/data/readalarms"
        try:
            data = {'sensorids': sensor_ids, 'aggtype': "RAS", "timefrom": timefrom, "timeto": timeto}
            head = {"Authorization": self.get_access_token()}
            my_res = requests.get(request_url, params=data, headers=head)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the alarm request! Code{my_res.status_code} {my_res.text} Error is:{e}")
            return {}

    def get_latest_datapoint(self, sensor_ids):
        request_url = config.TYDE_BASE_URL + "/api/v1/data/getlatest"
        try:
            data = {'sensorids': sensor_ids}
            head= {"Authorization": self.get_access_token()}
            my_res = requests.get(request_url, params=data, headers=head)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the request! Code{my_res.status_code}  {my_res.text} Error is:{e}")
            return {}

    # ######################  PORTFOLIO RELATED FUNCTIONS #############################################
    def list_portfolios(self):
        request_url = config.TYDE_BASE_URL + f"/api/v1/access/portfolios/list"
        try:
            head = {"Authorization": self.get_access_token()}
            my_res = requests.get(request_url, headers=head)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the request! Code{my_res.status_code} {my_res.text} Error is:{e}")
            return {}

    def get_portfolio_info(self, ppid):
        request_url = config.TYDE_BASE_URL + f"/api/v1/access/portfolio/{ppid}"
        try:
            head = {"Authorization": self.get_access_token()}
            my_res = requests.get(request_url, headers=head)
            my_res.raise_for_status()
            return my_res.json()
        except Exception as e:
            config.LOGGER.warning(f"Something went wrong with the request! Code{my_res.status_code}  {my_res.text} Error is:{e}")
            return {}
