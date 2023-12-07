from flask import  session
def checkLoc(shouldBe):
    
    # get the current page the user is on and then check if it exists and then check if it is a larger number than or equal to what it should be
    current = session.get('page')
    print(current)
    if current != None:
        if current >= shouldBe:
            return 1
        else:
            return 0
    else: 
        return 0