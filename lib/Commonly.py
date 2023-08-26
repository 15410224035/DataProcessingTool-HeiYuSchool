from pypinyin import lazy_pinyin


import re

def create_username(name,username_list):
    '''
    根据中文名字生成账号
    :param name:
    :param username_list:
    :return: username
    '''
    pinyin_name = lazy_pinyin(name)
    pinyin_name = ''.join(pinyin_name)
    username = differen_names(pinyin_name,username_list)
    username_list.append(username)
    return username

def differen_names(name,namelist):
    '''
    保证账号的唯一性
    :param name:
    :param namelist:
    :return:
    '''
    if name in namelist:
        i = re.findall(r'\d+',name)
        if i:
            i = int(i[0])
            i += 1
            name = re.findall(r'\D+',name)[0]
            name = name + str(i)
            return differen_names(name,namelist)
        else:
            i = 1
            name = name + str(i)
            return differen_names(name, namelist)
    else:
        return name

