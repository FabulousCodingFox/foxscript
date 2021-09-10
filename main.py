class Function:
    def __init__(self, code="", mccode="", path="", name="null",namespace=""):
        self.code = code
        self.mccode = mccode
        self.path=path
        self.name=name
        self.namespace=namespace
class Namespace:
    def __init__(self, name="main", rawcode="", path="", functions=[]):
        self.name = name
        self.functions = functions
        self.path = path
        self.rawcode=rawcode
    def add_function(self,function):
        self.functions.append(function)

def error(line,linenumber,text):global err;print("\nError in line "+str(linenumber)+":\nLine: "+str(line)+":\nText: "+str(text));err=True

import os,sys,time
def check_for_syntax_error(code):
    err=False
    ##########################################################################################################################################################Removing Empty lines
    newcode=""
    for linenumber in range(len(code.split("\n"))):
        line = code.split("\n")[linenumber];b=False
        for x in "ABCDEFGHIJKLMNOPQRSTUVWabcdefghijklmnopqrstuvwxyz1234567890ß!?+#-.,:()[]":
            if x in line:b=True
        if b:newcode=newcode+line+"\n"
    code=newcode
    ##########################################################################################################################################################
    for linenumber in range(len(code.rstrip().split("\n"))):
        line = code.rstrip().split("\n")[linenumber]
        ######################################################################################################################################################Check for false indents
        linestrip=line
        lineintents=0
        while linestrip.startswith("    "):linestrip=linestrip[4:];lineintents+=1
        if linestrip.startswith(" "):error(linestrip.strip(),linenumber,"The intendation level isnt correct.")
        try:
            nextlineintents=0
            nextlinestrip=code.rstrip().split("\n")[linenumber+1]
            while nextlinestrip.startswith("    "):nextlinestrip=nextlinestrip[4:];nextlineintents+=1
        except:
            nextlineintents=lineintents
            nextlinestrip=code.rstrip().split("\n")[linenumber]
        ######################################################################################################################################################Check for intents after a ":":
        if line.strip()[-1]==":":
            if not lineintents + 1 == nextlineintents:error(nextlinestrip.strip(),linenumber+1,"The line isnt intended correctly!")
    if err:exit()
    return code


def generate_data_structures(code):
    _tick_ = []
    _load_ = []
    ##########################################################################################################################################################Reading Project Data
    pr={"name":None,"mc-version":None,"description":None,"author":None}
    for linenumber in range(len(code.rstrip().split("\n"))):
        line = code.rstrip().split("\n")[linenumber]
        if line.startswith("__project__"):
            elements = line.strip().split("=")
            elements = [i.strip() for i in elements]
            if elements[0].startswith("__project__[\"name\"]"):         pr["name"]        = elements[1].replace("\"","")
            elif elements[0].startswith("__project__[\"mc-version\"]"): pr["mc-version"]  = elements[1].replace("\"","")
            elif elements[0].startswith("__project__[\"description\"]"):pr["description"] = elements[1].replace("\"","")
            elif elements[0].startswith("__project__[\"author\"]"):     pr["author"]      = elements[1].replace("\"","")
            else:error(line.strip(),linenumber,"Unknow __project__ parameter!")
    if pr["name"]==None: pr["name"] = "UntitledProject"
    if pr["mc-version"]==None: pr["mc-version"] = "1.16.5"
    if pr["author"]==None: pr["author"] = "Unknown"
    if pr["description"]==None:pr["description"] = pr["name"] + " by " + pr["author"] + " for Minecraft version" + pr["mc-version"]
    ##########################################################################################################################################################Seting up the folder structure
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
    ##########################################################################################################################################################Getting Namespaces
    namespaces = []
    for linenumber in range(len(code.rstrip().split("\n"))):
        line = code.split("\n")[linenumber]
        this=""
        if line.startswith("class "):
            namespacename = line.strip().split(" ")[1][:-1]
            looplinenumber=linenumber
            loopline="    "
            while loopline.startswith("    "):
                looplinenumber+=1
                loopline = code.split("\n")[looplinenumber]
                if loopline.startswith("    "):this = this + loopline[4:] + "\n"
            os.mkdir("output/" + pr["name"] + "/data/" + name)
            namespaces.append(Namespace(name=namespacename,rawcode=this,path="output/" + pr["name"] + "/data/" + name + "/"))
    ##########################################################################################################################################################Getting Functions
    for namespace in namespaces:
        for linenumber in range(len(namespace.rawcode.rstrip().split("\n"))):
            line = namespace.rawcode.split("\n")[linenumber]
            this=""
            if line.startswith("def "):
                funcname = line.strip().split(" ")[1].split("(")[0]
                looplinenumber=linenumber
                loopline="    "
                while loopline.startswith("    "):
                    looplinenumber+=1
                    loopline = namespace.rawcode.split("\n")[looplinenumber]
                    if loopline.startswith("    "):this = this + loopline[4:] + "\n"
                    
                thisfunc=Function(this,"",namespace.path+funcname+".mcfunction",funcname,namespace)
                if thisfunc.name =="__tick__":_tick_.append(thisfunc)
                elif thisfunc.name =="__load__":_load_.append(thisfunc)
                namespace.add_function(thisfunc)
                open(thisfunc.path,"x")
    ##########################################################################################################################################################
    return pr,namespaces,_tick_,_load_











def seperate_func(code):
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
        nscode = namespace.rawcode
        for line in range(len(nscode.split("\n"))):
            code=""
            if nscode.split("\n")[line].startswith("def "):
                funcname = nscode.split("\n")[line].split(" ")[1][:-1]
                currentcodeline = "    "
                linenumber=line
                while currentcodeline.startswith("    "):
                    linenumber+=1
                    currentcodeline = nscode.split("\n")[linenumber]
                    code = code + currentcodeline[4:] + "\n"
                thisfunc=Function(code,"",namespace.path+funcname+".mcfunction",funcname,namespace)
                if thisfunc.name =="__tick__":__tick__.append(thisfunc)
                elif thisfunc.name =="__load__":__load__.append(thisfunc)
                namespace.add_function(thisfunc)
                open(namespace.path+funcname+".mcfunction","x")
                
    return pr,namespaces,__tick__,__load__



starttime=time.time()

code="""
__project__["mc-version"]  = "1.16.5"
__project__["name"]        = "Fox"
__project__["description"] = "FoxSciptTest"
__project__["author"]      = "FabulousFox"

class Main: 
    def __tick__():
        say("Main.Tick")
    def __load__():
        say("Main.Load")
"""

print("Checking for Syntax errors...")
c=check_for_syntax_error(code)
print("Generating Data Structures(Pre-Compile)...")
pr,namespaces,_tick_,_load_generate_data_structures(c)

print("Finished in",time.time()-starttime,"Seconds")
