import docker

def build_docker():
    print('Docker login ecr...')
    dkr_c = docker.from_env()
    dkr_c.login(username=user, password=passwd, registry=repo_uri)
    img = dkr_c.images.get('local:haproxy')
    print(img.tags)
    img.tag(repository=repo_uri, tag='haproxy')
    print('Uploading...')
    for l in dkr_c.images.push(repository=repo_uri, tag='haproxy', stream=True, auth_config={'username': user, 'password': passwd}, decode=True):
        print(l)
    print('Uploaded...')

def main():
    dkr_f = open('/Users/greg/docker/python3/python3dockerfile', 'rb')
    dkr_c = docker.from_env()
    #dkr_c.images.build(path='/Users/greg/docker/python3/', dockerfile=dkr_f, tag='local:dockerpy')
    dkr_c.images.build(fileobj=dkr_f, tag='local:dockerpy')

if __name__ == '__main__':
    main()
