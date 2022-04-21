import os


def myloading():
    cfgpath = "surnames_orig.txt"
    fconf = open(cfgpath, 'r')
    tconf = fconf.read()
    fconf.close()
    surname_list = tconf.split('\n')
    return surname_list


def mywriting(list_of_records):
    cfgpath = "surnames_pure.txt"
    fconf = open(cfgpath, 'w')
    str_list = "\n".join(list_of_records)
    fconf.write(str_list)
    fconf.close()

surnames = myloading()
surnames_pure = []
for s_record in surnames:
	try:
		surnames_pure.append(s_record.split(' ')[1])
	except:
		print("reached the end")
mywriting(surnames_pure)
print(surnames_pure)
