from time import sleep

import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client, config


JOB_NAME = "pi"

def __get_kubernetes_client(bearer_token,api_server_endpoint):
    try:
        configuration = kubernetes.client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
            api_instance1 = kubernetes.client.BatchV1beta1Api(api_client)
        return api_instance1
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def getcronjobs(cluster_details,namespace="default",all_namespaces=True):
        client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        if all_namespaces is True:
            
            ret =client_api.list_cron_job_for_all_namespaces(watch=False)
            temp_dict_obj={}
            temp_list_obj=[]
            for i in ret.items:
                temp_dict_obj={
                    "name": i.metadata.name,
                    "namespace": i.metadata.namespace
                }
                temp_list_obj.append(temp_dict_obj)
            print("cronjob under all namespaces: {}".format(temp_list_obj))
            return temp_list_obj
        else:
            cronjob_list = client_api.list_namespaced_cron_job("{}".format(namespace))
            print("cronjob under default namespaces:{}".format(cronjob_list))
            return cronjob_list    
   
def delete_job(cluster_details,namespace):


    client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )

    api_response = client_api.delete_namespaced_cron_job(
        name="cronjob3", # already created cronjobs
        namespace=namespace,
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Job deleted. status='%s'" % str(api_response.status))



if __name__ == '__main__':
    batch_v1 = client.BatchV1Api()
    cluster_details={
        "bearer_token":"GKE-Bearer-Token",
        "api_server_endpoint":"ip-k8s-control-plane"
    }

    delete_job(cluster_details,"default" )
    getcronjobs(cluster_details)