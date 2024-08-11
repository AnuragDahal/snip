from pydantic import BaseModel, EmailStr,HttpUrl
from typing import List, Optional
from enum import Enum

class Privacy(str, Enum):
    public = "public"
    private = "private"
    friends = "friends"


class OauthUser(BaseModel):
    name: str
    email: EmailStr
    isEmailVerified: Optional[bool]
    isEmailVerified: Optional[bool] = False
    friends: Optional[List[str]] = []
    profile_picture: Optional[str] = []
    posts: Optional[List[str]] = []
    commented: Optional[List[str]] = []
    comments_on_posts: Optional[List[str]] = []

class UserDetails(BaseModel):
    name: str
    email: EmailStr
    password: str
    isEmailVerified: Optional[bool] = False
    profile_picture: Optional[str] = str()

class UpdateUserEmail(BaseModel):
    email: EmailStr
