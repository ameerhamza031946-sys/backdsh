# Utility function to convert MongoDB document to Python dictionary
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"]
    }

def post_helper(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "content": post["content"],
        "owner_id": post["owner_id"],
        "created_at": post.get("created_at")
    }
