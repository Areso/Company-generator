import mysql.connector
import random
import os


def loading_surnames():
    cfgpath = "surnames_pure.txt"
    fconf = open(cfgpath, 'r')
    tconf = fconf.read()
    fconf.close()
    surname_list = tconf.split('\n')
    if len(surname_list[len(surname_list)-1])==0:
        print('drop last record')
        surname_list = surname_list[:-1]
    #print(surname_list)
    return surname_list


def loading_firstnames():
    cfgpath = "firstnames_pure.txt"
    fconf = open(cfgpath, 'r')
    tconf = fconf.read()
    fconf.close()
    firstname_list = tconf.split('\n')
    if len(firstname_list[len(firstname_list)-1])==0:
        print('drop last record')
        firstname_list = firstname_list[:-1]
    #print(firstname_list)
    return firstname_list


def loading_patronicnames():
    cfgpath = "patronicnames_pure.txt"
    fconf = open(cfgpath, 'r')
    tconf = fconf.read()
    fconf.close()
    patronicname_list = tconf.split('\n')
    if len(patronicname_list[len(patronicname_list)-1])==0:
        print('drop last record')
        patronicname_list = patronicname_list[:-1]
    #print(patronicname_list)
    return patronicname_list


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


def gen_person():
    global surnames, firstnames, patronames
    year_of_birth  = random.randrange(1970, 2001)
    month_of_birth = random.randrange(1, 12)
    day_of_birth   = random.randrange(1, 28)
    id_random_surname   = random.randrange(0, len(surnames)-1)
    random_surname      = surnames[id_random_surname]
    id_random_firstname = random.randrange(0, len(firstnames)-1)
    random_firstname    = firstnames[id_random_firstname]
    id_random_patroname = random.randrange(0, len(patronames)-1)
    random_patroname    = patronames[id_random_patroname]
    gender    = 1
    fullname  = random_surname + " " + random_firstname + " " + random_patroname
    birthdate = str(year_of_birth) + '-' + str(month_of_birth) + '-' + str(day_of_birth)
    salary    = random.randrange(30, 300)*1000
    return [fullname, gender, birthdate, salary]


def insert_employees():
    global mydb   
    mydb.ping(reconnect=True, attempts=1, delay=0)
    mycursor = mydb.cursor()
    mycursor.execute("""SELECT * FROM deps""")
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        for dep in myresult:
            dep_id      = dep[0]
            prnt_dep_id = dep[1]
            head_of_dep = dep[3]
            # check if there is child deps
            mycursor.execute("""SELECT dep_id FROM deps 
                               WHERE parent_dep_id =%(parent_dep_id)s""",
                              {'parent_dep_id': dep_id})
            checkchild_res = mycursor.fetchall()
            if len(checkchild_res)>0:
                # insert only head of the dep
                # person = [fullname (str), gender (int, birthdate (str), salary (int)]
                person = gen_person()
                mycursor.execute("""INSERT INTO employees(dep_id, fullname,
                salary, gender, birthdate ) VALUES (%(dep_id)s, %(fullname)s,
                %(salary)s, %(gender)s, %(birthdate)s)""",
                      {'dep_id':   dep_id,
                       'fullname': person[0],
                       'salary': person[3],
                       'gender': person[1],
                       'birthdate': person[2]
                       })
                mydb.commit()
                head_of_dep_id = mycursor.lastrowid
                mycursor.execute("""UPDATE deps
                SET head_of_dep = %(head_id)s
                WHERE dep_id = %(dep_id)s""",
                                 {'head_id': head_of_dep_id,
                                  'dep_id': dep_id})
                mydb.commit()
            else:
                # insert 5..30 people
                number_of_employees_in_dep = random.randrange(5, 30)
                iterator = 0
                while iterator<number_of_employees_in_dep:
                    iterator += 1
                    person = gen_person()
                    mycursor.execute("""INSERT INTO employees(dep_id, fullname,
                                    salary, gender, birthdate ) VALUES (%(dep_id)s, %(fullname)s,
                                    %(salary)s, %(gender)s, %(birthdate)s)""",
                                     {'dep_id': dep_id,
                                      'fullname': person[0],
                                      'salary': person[3],
                                      'gender': person[1],
                                      'birthdate': person[2]
                                      })
                mydb.commit()
    else:
        print("no deps found. exiting")


if __name__ == '__main__':
    surnames   = loading_surnames()
    firstnames = loading_firstnames()
    patronames = loading_patronicnames()
    create_db_con()
    # clear the employees
    global mydb
    mycursor = mydb.cursor()
    mycursor.execute("delete from employees;")
    mydb.commit()
    # ended
    insert_employees()
