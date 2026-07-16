from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


async def create_post(
    db: AsyncSession,
    post: PostCreate,
    author_id: int,
) -> Post:
    new_post = Post(
        title=post.title,
        content=post.content,
        author_id=author_id,
    )
    db.add(new_post)
    return new_post


async def fetch_posts_list(
    db: AsyncSession,
    limit: int,
    offset: int,
) -> list[Post]:
    result = await db.execute(
        select(Post)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(result.scalars().all())


async def search_posts_repository(db: AsyncSession, q: str) -> list[Post]:
    trimmed_q = q.strip()
    if not trimmed_q:
        return []

    search_pattern = f"%{trimmed_q}%"
    result = await db.execute(
        select(Post)
        .where(
            or_(
                Post.title.ilike(search_pattern),
                Post.content.ilike(search_pattern),
            )
        )
        .order_by(Post.created_at.desc())
    )
    return list(result.scalars().all())


async def get_posts_count(db: AsyncSession) -> int:
    result = await db.execute(select(func.count()).select_from(Post))
    return int(result.scalar_one())


async def get_post_by_id(
    db: AsyncSession,
    post_id: int,
) -> Post | None:
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()


async def update_post(
    db: AsyncSession,
    post_id: int,
    post_update: PostUpdate,
) -> Post | None:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if post is None:
        return None

    post.title = post_update.title
    post.content = post_update.content
    return post


async def delete_post(
    db: AsyncSession,
    post_id: int,
) -> Post | None:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if post is None:
        return None

    await db.delete(post)
    return post
