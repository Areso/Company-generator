import mysql.connector
import random
import argparse

mydb = {}
types = []
titles = []
cur_lvl = []
nxt_lvl = []
dep_id = 0


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
    root_dep_id = 0
    root_dep_name = "Рога и Копыта ООО"
    number_of_depth = 5
    n = 0
    depth = 0
    parent_id = 0

    lang = "ru"
    global types, titles
    # types  = ["дирекция","блок","отделение"]
    # titles = [["экономики", "технологий"],
    #          ["b2b", "b2c"],
    #          ["Москвы", "Питера"]]
    types = ["дирекция", "блок", "управление", "департамент", "отдел"]
    titles = [["экономики", "технологий", "бизнеса", "инноваций"],
              ["планирования", "аудита", "розничного бизнеса", "b2b", "технологий"],
              ["capex", "opex", "кредитов", "депозитов", "РКО", "инкассации",
               "инвестпродуктов", "ЦОДов", "сетей", "поддержки АРМ и ВАРМ", "кибербезы",
               "УБД", "Серверов приложений", "Продуктов для разработки"],
              ["планирования", "аудита", "тер $modf"],
              ["офис $modo"]]
    modo = ['На Маяковской', 'На Каховской', 'На Полтавской', 'На Красноярской',
            'На Тенистой', 'На Смолистой', 'На Смоленской', 'На Эсперантистов']
    modf = ['Московский', 'Питерский', 'Среднерусский', 'Южнорусский', 'Кавказский',
            'Волжский', 'Уральский', 'Сибирский', 'Дальневосточный',
            'Северозападный', 'Калининградский', 'Архангельский']
    global mydb
    mydb.ping(reconnect=True, attempts=1, delay=0)
    mycursor = mydb.cursor()
    mycursor.execute("delete from deps;")
    mydb.commit()
    mycursor = mydb.cursor()
    mycursor.execute("""INSERT INTO deps(dep_id, dep_name)
                        VALUES (%(dep_id)s,%(dep_name)s)""",
                     {'dep_id': root_dep_id,
                      'dep_name': root_dep_name})
    mydb.commit()
    spawn_childs(depth, len(titles))


def spawn_childs(cur_depth, depth):
    global types, titles, dep_id, cur_lvl, nxt_lvl
    global mydb
    print(titles)
    print("cur_depth", cur_depth)
    if cur_depth == 0:
        print("cur_depth is 0. start")
        if cur_depth < depth:
            cur_level_prefix = types[cur_depth]
            for the_title in titles[cur_depth]:
                dep_id = dep_id + 1
                depname = cur_level_prefix + " " + the_title
                nxt_lvl.append(dep_id)
                mycursor = mydb.cursor()
                mycursor.execute("""INSERT INTO deps(dep_id, parent_dep_id, dep_name) 
				VALUES (%(dep_id)s,%(parent_dep_id)s,%(dep_name)s)""",
                                 {'dep_id': dep_id,
                                  'parent_dep_id': 0,
                                  'dep_name': depname})
                mydb.commit()
    else:
        cur_lvl = []
        cur_lvl = cur_lvl + nxt_lvl
        nxt_lvl = []
        print("cur_depth is " + str(cur_depth))
        print("nxt lvl, cur lvl")
        print(nxt_lvl)
        print(cur_lvl)
        if cur_depth < depth + 1:
            print("first if satisfied")
            for every_cur_parent in cur_lvl:
                cur_level_prefix = types[cur_depth]
                for the_title in titles[cur_depth]:
                    dep_id = dep_id + 1
                    depname = cur_level_prefix + " " + the_title
                    nxt_lvl.append(dep_id)
                    mycursor = mydb.cursor()
                    mycursor.execute("""INSERT INTO deps(dep_id, parent_dep_id, dep_name) 
					VALUES (%(dep_id)s,%(parent_dep_id)s,%(dep_name)s)""",
                                     {'dep_id': dep_id,
                                      'parent_dep_id': every_cur_parent,
                                      'dep_name': depname})
                    mydb.commit()
    cur_depth += 1
    print(cur_lvl, nxt_lvl)
    if cur_depth < depth:
        spawn_childs(cur_depth, depth)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prod',
                        help='set directory /root/git/ivoc-server',
                        action="store_true")
    args = parser.parse_args()
    create_db_con()
    populate_deps()
