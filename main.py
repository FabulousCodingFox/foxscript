code="""
@project-name:Fox
@project-description:Foxscript test
@mc-version:1.16.5
@author:FabulousFox
class Weaponcore:
    def __tick__():
        say("Tick")
    def __load__():
        say("Load")
    def test(test:int):
        say("Test")
class Test:
    def __load__():
        say("-")
"""
 
from func import *
a,b,c,d=seperate_func(code)
func_compile(a,b,c,d)

