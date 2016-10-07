import requests
import configparser

if __name__ == '__main__':
    # r = requests.get('https://fit.cvut.cz')
    # print(r.status_code)

    config = configparser.ConfigParser()
    config.read('./config/auth.cfg')
    print(config['github']['token'])