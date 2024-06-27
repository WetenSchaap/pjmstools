#%%
import sys
sys.path.append("./../")
import pjmstools

a = pjmstools.grouper( "ABCDEFGHIJKLMNOPQ", 3, "x" )
print(type(a))
print(a)
print(list(a))
