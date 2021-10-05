import iotGateway as iot

num_of_cols = len(iot.columns)
# Separate the column names and the values into two separate lists
def seperate_col_val(list):
    cols = []
    vals = []
    for i in range(len(list)):
        list[i] = list[i].split(':', 1)

    for i in range(len(list)):
        vals.append(list[i][1])
    for i in range(num_of_cols):
        cols.append(list[i][0])

    return cols, vals

# Create a dictioanry of the data
def create_dictionaries(cols, vals):
    num_of_dicts = len(cols)/num_of_cols
    dict_names = []
    dicts = []
    c = 0
    while c < num_of_dicts:
        j = c*num_of_cols
        dict_names.append(vals[j])
        c = c+1

    temp = dict.fromkeys(cols[0:num_of_cols])

    if dict_names is not None:
        c = 0
        for name in dict_names:
            name = temp.copy()
            for i in range(num_of_cols):
                j = c*num_of_cols
                name[cols[j+i]] = vals[j+i]
            dicts.append(name)
            c = c+1

    return dicts

# Create a dictionary when given a list
def data_dict(list):
    cols, vals = seperate_col_val(list)
    dictionary = create_dictionaries(cols, vals)
    return dictionary, cols






