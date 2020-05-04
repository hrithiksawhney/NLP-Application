import sys
import chilkat

# The Chilkat API can be unlocked for a fully-functional 30-day trial by passing any
# string to the UnlockBundle method.  A program can unlock once at the start. Once unlocked,
# all subsequently instantiated objects are created in the unlocked state. 
# 
# After licensing Chilkat, replace the "Anything for 30-day trial" with the purchased unlock code.
# To verify the purchased unlock code was recognized, examine the contents of the LastErrorText
# property after unlocking.  For example:
glob = chilkat.CkGlobal()
success = glob.UnlockBundle("Anything for 30-day trial")
if (success != True):
    print(glob.lastErrorText())
    sys.exit()

status = glob.get_UnlockStatus()
if (status == 2):
    print("Unlocked using purchased unlock code.")
else:
    print("Unlocked in trial mode.")

# The LastErrorText can be examined in the success case to see if it was unlocked in
# trial more, or with a purchased unlock code.
print(glob.lastErrorText())