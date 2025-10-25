import repositories.interviews_repo as interviews_repo
def get():
    print("interviews_vm get called ")
    return interviews_repo.get_all_users_raw()


def get_project_submission_date():
    print("interviews_vm get called ")
    return interviews_repo.get_project_submission_date()

def get_project_progress_date():
    print("interviews_vm get called ")
    return interviews_repo.get_project_progress_date()