from fastapi import APIRouter, Depends, HTTPException, status
from database.mongodb import get_db
from schemas.post import PostCreate, PostUpdate, PostResponse
from auth.deps import get_current_user
from models.helpers import post_helper
from bson.objectid import ObjectId
from datetime import datetime, timezone

router = APIRouter()

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db=Depends(get_db), current_user: dict = Depends(get_current_user)):
    post_dict = post.model_dump()
    post_dict["owner_id"] = current_user["id"]
    post_dict["created_at"] = datetime.now(timezone.utc)
    
    new_post = await db["posts"].insert_one(post_dict)
    created_post = await db["posts"].find_one({"_id": new_post.inserted_id})
    return post_helper(created_post)

@router.get("/", response_model=list[PostResponse])
async def get_posts(db=Depends(get_db)):
    posts = []
    cursor = db["posts"].find()
    async for post in cursor:
        posts.append(post_helper(post))
    return posts

@router.get("/{id}", response_model=PostResponse)
async def get_post(id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    post = await db["posts"].find_one({"_id": ObjectId(id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_helper(post)

@router.put("/{id}", response_model=PostResponse)
async def update_post(id: str, post_data: PostUpdate, db=Depends(get_db), current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    post = await db["posts"].find_one({"_id": ObjectId(id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    if post["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
        
    update_data = {k: v for k, v in post_data.model_dump(exclude_unset=True).items() if v is not None}
    
    if update_data:
        await db["posts"].update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
    updated_post = await db["posts"].find_one({"_id": ObjectId(id)})
    return post_helper(updated_post)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: str, db=Depends(get_db), current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    post = await db["posts"].find_one({"_id": ObjectId(id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    if post["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
        
    await db["posts"].delete_one({"_id": ObjectId(id)})
    return None
