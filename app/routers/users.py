from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.models import UserCreate, UserUpdate, UserResponse, ErrorResponse
from app.database import get_database

def get_utc_now():
    """Get current UTC datetime (timezone-aware, then convert to naive for MongoDB)"""
    return datetime.now(timezone.utc).replace(tzinfo=None)

router = APIRouter(prefix="/api/users", tags=["users"])

def serialize_user(doc: dict) -> dict:
    """Convert MongoDB document to UserResponse format"""
    return {
        "user_id": UUID(doc["user_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "age": doc["age"],
        "created_at": doc.get("created_at", get_utc_now()),
        "updated_at": doc.get("updated_at", get_utc_now())
    }

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input or duplicate email"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_user(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Create a new user"""
    try:
        # Check if email already exists
        existing_user = await db.users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {user.email} already exists"
            )
        
        user_data = {
            "user_id": str(uuid4()),
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "created_at": get_utc_now(),
            "updated_at": get_utc_now()
        }
        
        result = await db.users.insert_one(user_data)
        if result.inserted_id:
            return serialize_user(user_data)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.get(
    "",
    response_model=List[UserResponse],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_all_users(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get all users"""
    try:
        users = []
        async for user in db.users.find():
            users.append(serialize_user(user))
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        400: {"model": ErrorResponse, "description": "Invalid user ID format"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get a user by ID"""
    try:
        # Validate UUID format
        try:
            UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user ID format: {user_id}"
            )
        
        user = await db.users.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        return serialize_user(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user: {str(e)}"
        )

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        400: {"model": ErrorResponse, "description": "Invalid input or duplicate email"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update a user by ID"""
    try:
        # Validate UUID format
        try:
            UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user ID format: {user_id}"
            )
        
        # Check if user exists
        existing_user = await db.users.find_one({"user_id": user_id})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        # Check for duplicate email if email is being updated
        if user_update.email and user_update.email != existing_user["email"]:
            duplicate_user = await db.users.find_one({"email": user_update.email})
            if duplicate_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User with email {user_update.email} already exists"
                )
        
        # Prepare update data
        update_data = {}
        if user_update.name is not None:
            update_data["name"] = user_update.name
        if user_update.email is not None:
            update_data["email"] = user_update.email
        if user_update.age is not None:
            update_data["age"] = user_update.age
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )
        
        update_data["updated_at"] = get_utc_now()
        
        result = await db.users.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )
        
        # Fetch updated user
        updated_user = await db.users.find_one({"user_id": user_id})
        return serialize_user(updated_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        400: {"model": ErrorResponse, "description": "Invalid user ID format"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def delete_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Delete a user by ID"""
    try:
        # Validate UUID format
        try:
            UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user ID format: {user_id}"
            )
        
        result = await db.users.delete_one({"user_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )
