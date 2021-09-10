##############################################################################################################################################################
class Function:
    def __init__(self, code="", mccode="", path="", name="null",namespace=""):
        self.code = code
        self.mccode = mccode
        self.path=path
        self.name=name
        self.namespace=namespace
##############################################################################################################################################################
class Namespace:
    def __init__(self, name="main", rawcode="", path="", functions=[]):
        self.name = name
        self.functions = functions
        self.path = path
        self.rawcode=rawcode
    def add_function(self,function):
        self.functions.append(function)
##############################################################################################################################################################
class Player:
    def __init__(self,name=None,type="@a",advancements=None,distance=None,dx=None,dy=None,dz=None,gamemode=None,level=None,limit=None,nbt=None,predicate=None,scores=None,sort=None,tag=None,team=None,x=None,x_rotation=None,y=None,y_rotation=None,z=None):
        string=type+"["
        if not advancements==None:string=string+"advancements="+str(advancements)+","
        if not distance==None:string=string+"distance="+str(distance)+","
        if not dx==None:string=string+"dx="+str(dx)+","
        if not dy==None:string=string+"dy="+str(dy)+","
        if not dz==None:string=string+"dz="+str(dz)+","
        if not gamemode==None:string=string+"gamemode="+str(gamemode)+","
        if not level==None:string=string+"level="+str(level)+","
        if not limit==None:string=string+"limit="+str(limit)+","
        if not name==None:string=string+"name="+str(name)+","
        if not nbt==None:string=string+"nbt="+str(nbt)+","
        if not predicate==None:string=string+"="+str(predicate)+","
        if not scores==None:string=string+"="+str(scores)+","
        if not sort==None:string=string+"="+str(sort)+","
        if not tag==None:string=string+"tag="+str(tag)+","
        if not team==None:string=string+"team="+str(team)+","
        if not x==None:string=string+"x="+str(x)+","
        if not x_rotation==None:string=string+"x_rotation="+str(x_rotation)+","
        if not y==None:string=string+"y="+str(y)+","
        if not y_rotation==None:string=string+"y_rotation="+str(y_rotation)+","
        if not z==None:string=string+"z="+str(z)+","
        if string[-1]!="[":string=string[:-1]+"]"
        else:string=string[:-1]
        self.selector=string
    def __str__(self):
        return self.selector
##############################################################################################################################################################





















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



def compile_function(func):
    this=""
    for linenumber in range(len(func.code.rstrip().split("\n"))):
        line = func.code.split("\n")[linenumber]

        if not line.startswith("    "):
            ##################################################################################################################################################
            if line.strip().startswith("scoreboard("):
                try:
                    def scoreboard(name="main",type="dummy",operation="add"):return "scoreboard objectives "+operation+" "+name+" "+type
                    this = this + eval(line.strip()) + "\n"
                except:error(line.strip(),linenumber,"Incorrect usage of scoreboard()")
            ##################################################################################################################################################
            if line.strip().startswith("say("):
                try:
                    def say(text):return "say "+str(text)
                    this = this + eval(line.strip()) + "\n"
                except:error(line.strip(),linenumber,"Incorrect usage of say()")
            ##################################################################################################################################################IF
            if line.strip().startswith("if "):
                def get_current_if():
                    lambda w:w.translate(dict(zip(s,s[::-1])))
                    files=os.listdir(func.namespace.path);highest="if_";s=False
                    for i in files:
                        if "if_" in i:s=True
                    if s==False:return "if_"
                    for i in files:
                        if "if_" in i and i>highest:highest=i
                    if highest!="if_.mcfunction":
                        letters=i[3]
                        if letters=="":lettersn=0
                        if letters=="a":lettersn=1
                        if letters=="b":lettersn=2
                        if letters=="c":lettersn=3
                        if letters=="d":lettersn=4
                        if letters=="e":lettersn=5
                        if letters=="f":lettersn=6
                        if letters=="g":lettersn=7
                        if letters=="h":lettersn=8
                        if letters=="j":lettersn=9
                        if letters=="k":lettersn=10
                        return "if_"+["a","b","c","d","e","f","g","h","i","j","k"][lettersn+1]
                    else:
                        return "if_a"
                            
                iffilepath = func.namespace.path+get_current_if()+".mcfunction"
                iffunctionpath = func.namespace.name+":"+get_current_if()
                if "==" in line.strip():
                    statements=line.strip().split("==")
                    statements=[statements[0].replace("if ","").strip(),statements[1][:-1].strip()]
                    try:int(statements[0]);statements.append(True)
                    except:statements.append(False)
                    try:int(statements[1]);statements.append(True)
                    except:statements.append(False)
                    if statements[2]==True and statements[3] ==True: error(line.strip(),linenumber,"No two numbers in an if statement!")
                    if statements[2]==True and statements[3]==False: statements=[statements[1],statements[0],statements[3],statements[2]]
                    
                    if "Player(" in statements[0]:
                        elements=statements[0].split(".");elements=[i.strip() for i in elements]
                        if not elements[1] in ["nbt"]:
                            this = this + "execute if score "+str(eval(elements[0]))+" "+str(elements[1])+" "
                            if statements[3] == True:
                               this = this + "matches "+statements[1]+" run function "+iffunctionpath+"\n"


                looplinenumber=linenumber;loopline="    ";this=""
                while loopline.startswith("    "):
                    looplinenumber+=1;loopline = func.code.split("\n")[looplinenumber]
                    if loopline.startswith("    "):this = this + loopline[4:] + "\n"

                thisf=Function(this,"",iffilepath,get_current_if(),func.namespace)
                func.namespace.add_function(thisf)
                open(iffilepath,"x")
                compile_function(thisf)
            ##################################################################################################################################################IF

                    

                    
        
    return this




      
starttime=time.time()

f=open("source.fs","r");code=str(f.read());f.close()

print("Checking for Syntax errors...")
c=check_for_syntax_error(code)
print("Generating Data Structures(Pre-Compile)...")
pr,namespaces,_tick_,_load_=generate_data_structures(c)


def function_to_mcpath(func):return func.namespace.name+":"+func.name
for namespace in namespaces:
    for function in namespace.functions:
        this=compile_function(function)
        function.mccode=this
        f=open(function.path,"w");f.write(this);f.close()
f=open("output/" + pr["name"] + "/data/minecraft/tags/functions/tick.json","w");f.write("{\"values\":"+str(list([str(i.namespace.name+":"+i.name) for i in _tick_]))+"}");f.close()
f=open("output/" + pr["name"] + "/data/minecraft/tags/functions/load.json","w");f.write("{\"values\":"+str(list([str(i.namespace.name+":"+i.name) for i in _load_]))+"}");f.close()


print("Finished in",time.time()-starttime,"Seconds")
