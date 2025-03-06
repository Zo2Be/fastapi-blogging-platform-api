from fastapi import status


COMMON_RESPONSES = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Post not found",
        "content": {
            "application/json": {
                "example": {"detail": "Post not found"}
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {"detail": "Unauthorized"}
            }
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Forbidden to change the post",
        "content": {
            "application/json": {
                "example": {"detail": "You cannot change this post."}
            }
        },
    },
}