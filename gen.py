import mysql.connector
import random


mydb = {}

def myloading():
    cfgpath = "config_mysql.txt"
    fconf = open(cfgpath, 'r')
    tconf = fconf.read()
    fconf.close()
    conf_list = tconf.split('\n')
    return conf_list


def create_db_con():
    myconfig = myloading()
    global mydb
    mydb = mysql.connector.connect(
        host=myconfig[2],
        user=myconfig[0],
        password=myconfig[1],
        database=myconfig[4]
    )


def populate_deps():
    root_dep_id = 1
    number_of_depth = 5
    types = ["дирекция", "блок", "управление", "департамент", "отдел"]
    titles = [["экономики", "технологий"],
              [],
              [],
              [],
              []] 
    modo   = ['На Маяковской','На Каховской','На Полтавской']
    modf   = ['Московский','Питерский']
    nr    = [5, 5, 10, 10, 30]


if __name__ == '__main__':
    print(os.getcwd())
    parser = argparse.ArgumentParser()
    parser.add_argument('--prod',
                        help='set directory /root/git/ivoc-server',
                        action="store_true")
    args   = parser.parse_args()
    create_db_con()
    populate_deps()
