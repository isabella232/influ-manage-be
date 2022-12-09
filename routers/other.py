from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from models import Post, PostData
from database import Database

router = APIRouter()
db = Database()

@router.get("/r/{generated_url}", response_class=RedirectResponse)
def redirect_generated(
    generated_url: str
) -> None:
    with db.session() as db:
        post: Post = db.query(Post).filter(Post.generated_redirect == generated_url).first()
        if post:
            post_data: PostData = db.query(PostData).filter(PostData.post_id == post.id).first()
            post_data.num_clicks += 1
            db.add(post_data)
            db.commit()
            return post.url
        else:
            return "/badredirect"
