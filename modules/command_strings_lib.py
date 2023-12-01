def generate_objective_structures(data):
    result_string = ""    
    result_string = result_string + "addO = {}\n "
    result_string = result_string + f"addO.country = {data['country']}\n "
    result_string = result_string + f"addO.category = {data['category']}\n "
    result_string = result_string + f"addO.x = {data['x']}\n "
    result_string = result_string + f"addO.y = {data['y']}\n "
    result_string = result_string + f"addO.type = '{data['type']}'\n "
    result_string = result_string + f"addO.heading = {data['heading']}\n "
    result_string = result_string + f"addCP = mist.dynAddStatic(addO)\n "
    result_string = result_string + f"table.insert(target_data['{data['zonename']}']['struct'], addCP)\n "
    return result_string

def generate_objective_groundUnits(data):
    result_string = ""    
    result_string = result_string + f"gp = Group.getByName('{data['mockname']}')\n "
    result_string = result_string + f"gPData = mist.getGroupData('{data['mockname']}',true)\n "
    result_string = result_string + f"addUnit = mist.utils.deepCopy(gPData)\n "
    result_string = result_string + f"addO = addUnit\n "
    result_string = result_string + f"addO.country = {data['country']}\n "
    result_string = result_string + f"addO.category = {data['category']}\n "
    result_string = result_string + f"addO.visible = true\n "
    result_string = result_string + f"addO.clone = true\n "
    result_string = result_string + f"addO.units[1].x = {data['x']}\n "
    result_string = result_string + f"addO.units[1].y = {data['y']}\n "
    result_string = result_string + f"addO.units[1].heading =  {data['heading']}\n "
    result_string = result_string + f"addUni = mist.dynAdd(addO)\n "
    result_string = result_string + f"table.insert(target_data['{data['zonename']}']['unit'], addUni)\n "
    return result_string