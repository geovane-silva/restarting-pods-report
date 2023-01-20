"""
    This class retrieves the list of the cluster's pods.
    It uses the kubernetes Python client to list the pods, authenticating
    using the present kube context.
"""
import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException

class PodsList:
    """
        A class used to retrieve the list of the cluster's pods.

        ...
        Attrubutes
        ----------
        auth_method : str
            The method that will be used to authenticate to the Kubernetes cluster. Currently
            only the local kube config method is supported.
        namespace : str
            The list namespace. If not set, gets the list for all anmespaces.

        Methods
        -------
        get()
            Returns the pods list on the specified namespace. If not set, list pods for
            all namespaces
    """
    def __init__(self, auth_method="local", namespace=None):
        self.namespace = namespace
        if auth_method == 'local':
            config.load_kube_config()

    def get(self):
        """
            Returns the pods list on the specified namespace.If not set, list pods for
            all namespaces
        """
        v1_client = client.CoreV1Api()
        try:
            if self.namespace:
                return v1_client.list_namespaced_pod(self.namespace)
            return v1_client.list_pod_for_all_namespaces()
        except ApiException as exception:
            print('Exception while listing pods: ')
            print(exception.reason)
            sys.exit(1)
