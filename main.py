from turtle import title
from urllib import response
from fastapi import FastAPI,Depends,status, Response,HTTPException
import schemas,model
from database import engine,SessionLocal
from sqlalchemy.orm import Session
def get_db():
    db=SessionLocal()
    try:
        yield db
    # except:
    #     db.rollback()
    #     raise
    finally:
     db.close()

app=FastAPI()

model.Base.metadata.create_all(engine)

# create_all() creates all tables in the database.
@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=model.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return  new_blog
#delete query
@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int,db:Session=Depends(get_db)):
   blog= db.query(model.Blog).filter(model.Blog.id==id)
   if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
   blog.delete( synchronize_session=False)
   db.commit()
   return {"message":"Blog deleted"}

# updated query
@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(model.Blog).filter(model.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.update(request)
    db.commit()
    return 'updated blog' 
      
  
  
  
# get all the data
@app.get('/blog',status_code=200)
def all(db:Session=Depends(get_db)):
    blogs=db.query(model.Blog).all()
    return blogs
# filetrs the data
@app.get('/blog/{id}')
def show(id:int, Response,db:Session=Depends(get_db)):
    blog=db.query(model.Blog).filter(model.Blog.id==id).first()
    if not blog:
         raise HTTPException(status_code=404,detail=f'Blog with id {id} is not found') 
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with id {id} is not found'}
    return blog