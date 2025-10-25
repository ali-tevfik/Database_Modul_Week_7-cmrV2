import repositories.applicaitons_repo as applicaitons_repo
def get():
    print("applicaitons_vm get called ")
    return applicaitons_repo.get_all_users_raw()

def searchText(text):
    print("applicaitons_vm get called ")
    return applicaitons_repo.searchText(text)

def getAll():
    print("applicaitons_vm get called ")
    return applicaitons_repo.getAll()

def showmentor():
    print("applicaitons_vm get called ")
    return applicaitons_repo.showmentor()

def ushowmentor():
    print("applicaitons_vm get called ")
    return applicaitons_repo.ushowmentor()

def dublicate():
    print("applicaitons_vm get called ")
    return applicaitons_repo.dublicate()

def fltered():
    print("applicaitons_vm get called ")
    return applicaitons_repo.fltered()

def prevvitcheck():
    print("applicaitons_vm get called ")
    return applicaitons_repo.prevvitcheck()

def differenreg():
    print("applicaitons_vm get called ")
    return applicaitons_repo.differenreg()