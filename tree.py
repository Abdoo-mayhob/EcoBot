# EcoBot
# @AbdooEco_bot
# Tree Management File
# Created    : 2021 - 2 - 11
# LastEdited : 2021 - 2 - 14 20:22

# ===========================================================================================================================
# ===========================================================================================================================
# Data Types  :

class bot_file:
    def __init__(self,  name, father,**properties): 
        self.obj_type = "bot_file" 
        self.name = name # All properties except name, cz name wil be displayed in draw_tree
        self.father = father
        self.properties = dict()
        self.properties["full_name"] = None
        self.properties["stored_msg_id"] = None
        self.properties["comment"] = None
        self.properties["num_of_times_called"] = None
        self.properties["size"] = None
        self.properties["date"] = None
        self.properties["sender_id"] = None
        self.properties["sender_name"] = None
        self.properties["sender_username"] = None
        self.properties = properties
    
    def set_comment(self,comment):
        self.properties["comment"] = comment.strip()

    def __repr__(self):
        return self.name

    def delete(self):
        self.father.sub[self.name] = None # Incase the next line donsn't work 
        del self.father.sub[self.name]

    def get_ancestors(self):
        text = ''
        papa = self
        text += papa.name
        while True:
            try:
                papa = papa.father
                text += " <= "
                text += papa.name
            except:
                text += '|\n'
                break
        return text

# Imortant rule : folder name(aka value.name) == folder object name(aka Key) (Make you life easy man)
class folder:
    def __init__(self, folder_name: str, father_folder: "folder", **properties):
        self.obj_type = "folder" 
        self.name = folder_name
        self.father = father_folder
        self.properties = properties 
        self.set_comment(properties["comment"])
        self.sub = dict()

        if self.properties.get("num_of_times_called",None) == None:
            self.properties["num_of_times_called"] = 0

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name
    def set_comment(self,comment):
        self.properties["comment"] = comment.strip()
        
        if  self.properties["comment"] in (None, '',' ','#'):
            t = ['ئلي امرني',
            'أوك',
            'ماشي',
            'طيب',
            'إختر',
            'نقي',
            'وه',
            'ووو؟']
            from random import randint
            self.properties["comment"] = t[randint(0,len(t)-1)]

    def add_folder(self, name, **properties):
        new_folder = folder(name, self, **properties)
        self.sub[new_folder.name] = new_folder
        return new_folder

    def add_bot_file(self, name,**properties):
        new_bot_file = bot_file(name, self,**properties)
        self.sub[new_bot_file.name] = new_bot_file
        return new_bot_file

    def delete(self):
        self.father.sub[self.name] = None # Incase the next line donsn't work 
        del self.father.sub[self.name]

    def get_ancestors(self):
        text = ''
        papa = self
        text += papa.name
        while True:
            try:
                papa = papa.father
                text += " <= "
                text += papa.name
            except:
                text += '|\n'
                break
        return text



# ===========================================================================================================================
# ===========================================================================================================================
# Tree Functions :
def save_tree(tr,custom_name = "tree"):
    try:
        from copy import deepcopy
        def rec(tree): # tree.__dict__ pass a refrence to the actuall attribute 
            data = deepcopy(tree.__dict__) # Deepcopy creats a new copy
            data["father"] = str(data["father"]) # So when father = None =>"None"
            if type(tree) == folder:
                for sub_t in tree.sub.keys():
                    data["sub"][sub_t] = rec(tree.sub[sub_t])
            return data

        d = rec(tr)
        import json
        with open(custom_name+".json", "w") as write_file:
            json.dump(d, write_file,indent=4)
        print(f"[HighLevelLog] {custom_name}.json Saved")

    except Exception as E:
        print(f"[HighLevelLog] Couldn't Save {custom_name}.json,Error:\n{E}")
        return None


def load_tree(custom_name = "tree"):
    try:
        import json
        with open(custom_name+".json", "r") as read_file:
            tree_data = json.load(read_file)
        
        start = folder(tree_data["name"], None, **tree_data["properties"])
        def rec(h,d):
            for _ , v in d.items():
                if v["obj_type"] == "folder":
                    h.add_folder(v["name"] , **v["properties"])
                    rec(h.sub[v["name"]],v["sub"])
                else:
                    h.add_bot_file(v["name"] , **v["properties"])

        rec(start,tree_data["sub"])
        return start

    except Exception as E:
        print(f"[HighLevelLog] Couldn't Load {custom_name}.json,Error:\n{E}")
        return None

def draw_tree(tree, level_deep=1):  # make it 1 if you want to indent years too
    text = '-'+tree.name+'\n'
    if not type(tree) == bot_file:
        for sub_tree in tree.sub.values():
            text +=' '*4*level_deep
            text += draw_tree(sub_tree, level_deep+1)
    return text

def build_default_tree():
    print("[HighLevelLog] Loading Defult Tree..")
    tree = folder("start", None, comment = "أي كلية؟")
    t = "أي سنة ؟"
    tree.add_folder("كلية الإقتصاد", comment =t)

    for college in tree.sub.values():
        t = "أي فصل؟"
        college.add_folder("سنفور",comment = t)
        college.add_folder("سنة ثانية",comment = t)
        college.add_folder("سنة ثالثة", comment =t)
        college.add_folder("سنة رابعة", comment =t)

        for y in college.sub.values():
            tt = " شو المادة؟"
            y.add_folder("فصل أول",comment = tt)
            y.add_folder("فصل ثاني",comment = tt)

    return tree

"""
To Abdoo:
Available Functions In This File:
save_tree(tr,custom_name = "tree")
load_tree(custom_name = "tree")
draw_tree(tree, level_deep=1)
build_default_tree()
"""
