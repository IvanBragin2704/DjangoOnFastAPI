from fastapi import APIRouter, status, HTTPException
from datetime import datetime
from ..schemas.post import Post
from ..schemas.comment import CommentCreate

# Временное хранилище постов
posts_db = []
post_counter = 1

router = APIRouter()


@router.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> dict:
    global post_counter

    if len(post.text) < 10:
        raise HTTPException(
            detail="Длина поста должна быть не меньше 10 символов",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    # Добавляем ID к посту и сохраняем
    post_dict = post.model_dump()
    post_dict["id"] = post_counter
    post_counter += 1
    posts_db.append(post_dict)

    response = {
        "title": post.title,
        "text": post.text,
        "author_id": post.author_id,
        "pub_date": post.pub_date,
        "location_id": post.location_id,
        "category_id": post.category_id,
        "id": post_dict["id"]
    }

    return response


@router.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def get_post(post_id: int) -> dict:
    """Получение конкретного поста по ID"""
    # Ищем пост во временном хранилище
    for post in posts_db:
        if post["id"] == post_id:
            return post

    # Если пост не найден
    raise HTTPException(
        detail=f"Пост с id {post_id} не найден",
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(post_id: int, updated_post: Post) -> dict:
    """Полное обновление поста"""
    # Ищем пост
    for i, post in enumerate(posts_db):
        if post["id"] == post_id:
            # Валидация текста
            if len(updated_post.text) < 10:
                raise HTTPException(
                    detail="Длина поста должна быть не меньше 10 символов",
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                )

            # Обновляем все поля
            updated_data = updated_post.model_dump()
            updated_data["id"] = post_id  # сохраняем тот же ID
            posts_db[i] = updated_data

            return updated_data

    raise HTTPException(
        detail=f"Пост с id {post_id} не найден",
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int) -> dict:
    """Удаление поста по ID"""
    # Ищем пост
    for i, post in enumerate(posts_db):
        if post["id"] == post_id:
            # Удаляем пост из хранилища
            deleted_post = posts_db.pop(i)

            return {
                "message": "Пост успешно удален",
                "deleted_post": deleted_post
            }

    raise HTTPException(
        detail=f"Пост с id {post_id} не найден",
        status_code=status.HTTP_404_NOT_FOUND,
    )

"""@router.post("/posts/{post_id}/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: int, comment: CommentCreate):

    global comment_counter

    # Проверяем, существует ли пост
    post_exists = any(p["id"] == post_id for p in posts_db)
    if not post_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пост с id {post_id} не найден"
        )

    # Валидация длины текста (опционально)
    if len(comment.text) < 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Текст комментария должен содержать минимум 2 символа"
        )

    # Создаём запись комментария
    comment_dict = comment.model_dump()
    comment_dict.update({
        "id": comment_counter,
        "post_id": post_id,
        "created_at": datetime.utcnow()
    })
    comments_db.append(comment_dict)
    comment_counter += 1

    return comment_dict


@router.get("/posts/{post_id}/comments", status_code=status.HTTP_200_OK)
async def get_post_comments(post_id: int, skip: int = 0, limit: int = 10):

    # Проверяем существование поста (необязательно, но для целостности)
    post_exists = any(p["id"] == post_id for p in posts_db)
    if not post_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пост с id {post_id} не найден"
        )

    # Фильтруем комментарии по post_id
    post_comments = [c for c in comments_db if c["post_id"] == post_id]

    # Применяем пагинацию
    start = skip
    end = skip + limit
    paginated = post_comments[start:end]

    return {
        "total": len(post_comments),
        "skip": skip,
        "limit": limit,
        "comments": paginated
    }


@router.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: int, author_id: int = None):

    global comments_db

    # Ищем комментарий
    for i, comment in enumerate(comments_db):
        if comment["id"] == comment_id:
            # Если передан author_id, проверяем, что он совпадает с автором комментария
            if author_id is not None and comment["author_id"] != author_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Нет прав на удаление этого комментария"
                )

            # Удаляем комментарий
            deleted = comments_db.pop(i)
            return {
                "message": "Комментарий успешно удалён",
                "deleted_comment": deleted
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Комментарий с id {comment_id} не найден"
    )"""