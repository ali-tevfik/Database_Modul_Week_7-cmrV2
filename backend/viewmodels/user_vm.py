from repositories import user_repo


async def login_vm(db, username: str, password: str):
    users =  user_repo.get_user_by_username(db, username)
    
    for user in users:
        if user.password == password: 
            return {"status": "success", "user" : user}
    
    return {"status": "error", "message": "Invalid username or password"}
