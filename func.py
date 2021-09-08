import sys,os
 
class Compile:
    def say(text=""):
        return "say " + text
 
 
class Function:
    def __init__(self, code="", mccode="", path="", name="null",namespace=""):
        self.code = code
        self.mccode = mccode
        self.path=path
        self.name=name
        self.namespace=namespace
 
    def compile(self, path=""):
        codelines = self.code.split("\n")
        for linen in range(len(codelines)):
            line = codelines[linen]
            command = line.split("(")[0]
            this = ""
 
            if command == "say": this = eval("Compile." + line)
 
 
class Namespace:
    def __init__(self, name="main", rawcode="", path="", functions=[]):
        self.name = name
        self.functions = functions
        self.path = path
        self.rawcode=rawcode
 
    def add_function(self, function):
        self.functions.append(function)
 
    def compile(self, path=""):
        for func in self.functions:
            func.compile(path)
 
 
def raise_error(type="/", path="Sourcecode", line="Unknown", text="/"):
    print("\n(Hard error)")
    print("Error: ", str(type))
    print("Path: ", str(path), "; In line ", line)
    print("Reason: ", str(text))
    exit()
 
 
def raise_soft_error(type="/", path="Sourcecode", line="Unknown", text="/"):
    print("\n(Soft error)", sep="")
    print("Error: ", str(type), sep="")
    print("Path: ", str(path), "; In line ", str(line), sep="")
    print("Reason: ", str(text), sep="")
 
def setup_start(pr):
    for root, dirs, files in os.walk("output/", topdown=False):
        for name in files:os.remove(os.path.join(root, name))
        for name in dirs:os.rmdir(os.path.join(root, name))
    os.mkdir("output/" + pr["name"])
    f=open("output/" + pr["name"] + "/pack.mcmeta","w");f.write("{\"pack\": {\"pack_format\": " + str("6" if pr["mc-version"] in "1.16.2 1.16.3 1.16.4 1.16.5" else "7") + ",\"description\": \""+pr["description"]+"\"}}");f.close()
    os.mkdir("output/" + pr["name"] + "/data")
    os.mkdir("output/" + pr["name"] + "/data/minecraft")
    os.mkdir("output/" + pr["name"] + "/data/minecraft/tags")
    os.mkdir("output/" + pr["name"] + "/data/minecraft/tags/functions")
    open("output/" + pr["name"] + "/data/minecraft/tags/functions/tick.json","x")
    open("output/" + pr["name"] + "/data/minecraft/tags/functions/load.json","x")
 
 
 
def seperate_func(code):
    __tick__=[]
    __load__=[]
    ###Reading Decorators
    pr = {}
    for line in range(len(code.split("\n"))):
        linen = code.split("\n")[line]
        if "@" in linen and linen[0] == "@":
            elements = linen[1:].split(":")
            if elements[0] == "project-name": pr["name"] = elements[1]
            elif elements[0] == "mc-version": pr["mc-version"] = elements[1]
            elif elements[0] == "project-description":pr["description"] = elements[1]
            elif elements[0] == "author":pr["author"] = elements[1]
            else:raise_soft_error(type="Decorator",line=line,text="Unknow Decorator: " + linen)
    if not pr["name"]: pr["name"] = "UntitledProject"
    if not pr["mc-version"]: pr["mc-version"] = "1.17.1"
    if not pr["author"]: pr["author"] = "Unknown"
    if not pr["description"]:pr["description"] = pr["name"] + " by " + pr["author"]
 
    ###Setting up basic folders
    setup_start(pr)
 
    ###Deleting Useless lines
    newcode="";code = code.rstrip()
    for i in code.split("\n"):
        b=False
        for j in """@abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZßöäü_()":""":
            if j in i:b=True
        if b==True:newcode=newcode+i+"\n"
    code=newcode
 
    ###Seperating
    namespaces=[]
    for line in range(len(code.split("\n"))):
        this=""
        if code.split("\n")[line].startswith("class "):
            name=code.split("\n")[line].split(" ")[1][:-1]
            thisotherline=" "
            j=line
            while thisotherline.startswith(" "):
                j+=1
                thisotherline=code.split("\n")[j]
                if thisotherline.startswith(" "):
                     this=this+thisotherline[4:]+"\n"
 
            os.mkdir("output/" + pr["name"] + "/data/" + name)
            namespaces.append(Namespace(name=name,rawcode=this,path="output/" + pr["name"] + "/data/" + name + "/"))
 
    ###Seperating Functions
    for namespace in namespaces:
        tcode=namespace.rawcode
        for line in range(len(tcode.split("\n"))):
            this=""
            if tcode.split("\n")[line].startswith("def "):
                name=tcode.split("\n")[line].split(" ")[1].split("(")[0]
                thisotherline=" "
                j=line
                while thisotherline.startswith(" "):
                    j+=1
                    thisotherline=tcode.split("\n")[j]
                    if thisotherline.startswith(" "):
                         this=this+thisotherline[4:]+"\n"
                thisf=Function(this.rstrip(),"",namespace.path+name+".mcfunction",name,namespace)
                if thisf.name =="__tick__":__tick__.append(thisf)
                elif thisf.name =="__load__":__load__.append(thisf)
                namespace.add_function(thisf)
                open(namespace.path+name+".mcfunction","x")
    return pr,namespaces,__tick__,__load__
 
def func_compile(pr={},namespaces=[],__tick__=[],__load__=[]):
    def function_to_mcpath(func):return func.namespace.name+":"+func.name
    for namespace in namespaces:
        for function in namespace.functions:
            this=""
            for line in function.code.split("\n"):
                try:
                    temp = eval("Compile."+line)
                    this = this + temp + "\n"
                except:
                    raise_soft_error(type="Code --> Command",text="Unable to transform this line: "+line)
            function.mccode=this
            f=open(function.path,"w")
            f.write(this)
            f.close()
    
    f=open("output/" + pr["name"] + "/data/minecraft/tags/functions/tick.json","w")
    f.write("{\"values\":"+str(list([function_to_mcpath(i) for i in __tick__]))+"}");f.close()
    f=open("output/" + pr["name"] + "/data/minecraft/tags/functions/load.json","w")
    f.write("{\"values\":"+str(list([function_to_mcpath(i) for i in __load__]))+"}");f.close()
