


from .. import models, oauth2,schemas
from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from ..database import get_db
from typing import List,Optional
from .. import models
router=APIRouter(
    prefix="/posts" ,
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.Postout])
def get_posts(db:Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int = 10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("""select * from posts""")
    # posts=cursor.fetchall()
    
    # posts=db.query(models.Post).filter(models.Post.title.contains(search),models.Post.owner_id==current_user.id).limit(limit).offset(skip).all()
    
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search),models.Post.owner_id==current_user.id).limit(limit).offset(skip).all()
    return posts 



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):


    """old codes for database connectivity"""
    # cursor.execute(""" INSERT INTO posts(title,content,published) VALUES(%s,%s,%s)RETURNING *""",
    # (post.title,post.content,post.published))

    # new_post=cursor.fetchone()
    # connection.commit()
    #print(**post.dict())
    #**post.dict()== title=post.title,content=post.content,published=post.published
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    # post_dict=post.dict()
    # post_dict['id']=randrange(0,10000000)
    # my_post.append(post_dict)
    # return {"data":post_dict}




@router.get("/{id}",response_model=schemas.Postout)
def get_post(id: int,db:Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts where id= %s""" %(str(id)))
    # post=cursor.fetchone()
    # post=db.query(models.Post).filter(models.Post.id==id).first()
    
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    #post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {str(id)} was not found")
        
    #http response
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform required action")   
        """response.status_code=status.HTTP_404_NOT_FOUND
        return {"message":f"post with id:{id} was not found"}"""

    return  post




@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:str,db:Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""delete from posts where id =%s returning *""" %(str(id)))
    # deleted_post=cursor.fetchone()
    # connection.commit()
    post_qeury=db.query(models.Post).filter(models.Post.id==id)
    post=post_qeury.first()
    #index=find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {str(id)} does not exist")
    #my_post.pop(index)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform required action")
    post_qeury.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db:Session =Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title=%s ,content =%s,published=%s where id=%s returning *""",(post.title,post.content,post.published,(str(id))))
    # updated_post=cursor.fetchone()
    # connection.commit()
    #index=find_index_post(id)
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform required action")
    # post_dict=post.dict()
    # post_dict['id']=id
    # my_post[index]=post_dict
    #post.dict()=={'title':'hey this a updated title','content':'this is my updated content'}
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
