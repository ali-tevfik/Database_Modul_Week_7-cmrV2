import repositories.mentor_repo as mentor_repo
def mentor_vm():
    print("mentor_vm called")
    return mentor_repo.get_all_mentors()

def findMentorByName_vm(name:str):
    print("findMentorByName_vm called with name:", name)
    return mentor_repo.find_mentor_by_name(name)

def findMentorByComboBox_vm(filter:str):
    print("findMentorByName_vm called with name:", filter)
    return mentor_repo.find_mentor_by_comboBox(filter)