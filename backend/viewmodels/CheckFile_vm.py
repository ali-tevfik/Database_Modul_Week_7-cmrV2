import repositories.CheckFile_repo as checkfile_repo
async def get(db):
    return await checkfile_repo.checkFile(db)