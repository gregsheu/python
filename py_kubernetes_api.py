from kubernetes import config, client

sapp_c = client.AppsV1Api(client.ApiClient(config.load_kube_config(context='arn:aws:eks:us-east-2:993514063544:cluster/tenxeng-silver-container')))
sapi_c =  client.ApiClient(config.load_kube_config(context='arn:aws:eks:us-east-2:993514063544:cluster/tenxeng-silver-container'))
sresp = sapp_c.read_namespaced_deployment(namespace='sit', name='sydneyproductsummaryv1-sit')
sresp = sapi_c.sanitize_for_serialization(sresp)
for i in sresp['spec']['template']['spec']['containers']:
    print('%s %s' % (i['name'], i['image']))

gapp_c = client.AppsV1Api(client.ApiClient(config.load_kube_config(context='arn:aws:eks:us-east-1:339644262595:cluster/tenxeng-gold-container')))
gapi_c = client.ApiClient(config.load_kube_config(context='arn:aws:eks:us-east-1:339644262595:cluster/tenxeng-gold-container'))
gresp = gapp_c.read_namespaced_deployment(namespace='default', name='sydneyproductsummaryv1')
gresp = gapi_c.sanitize_for_serialization(gresp)
for i in gresp['spec']['template']['spec']['containers']:
    print('%s %s' % (i['name'], i['image']))

papp_c = client.AppsV1Api(client.ApiClient(config.load_kube_config(context='arn:aws:eks:us-east-1:988647855354:cluster/tenxeng-platinum-container')))
papi_c = client.ApiClient(config.load_kube_config(context='arn:aws:eks:us-east-1:988647855354:cluster/tenxeng-platinum-container'))
presp = papp_c.read_namespaced_deployment(namespace='prod', name='sydneyproductsummaryv1-prod')
presp = papi_c.sanitize_for_serialization(presp)
for i in presp['spec']['template']['spec']['containers']:
    print('%s %s' % (i['name'], i['image']))
