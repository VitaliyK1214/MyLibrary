from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.books import BooksModel
from schemas.books import SBookAdd

class BookRepository:
    @classmethod
    async def add_book(cls, data: SBookAdd, session: AsyncSession):
	book_dict = data.model_dump()
	book = BooksModel(**book_dict)
	session.add(book)
	await session.commit()
	await session.refresh(book)
	return book
    
    @classmethod
    async def get_books(cls, session: AsyncSession):
	query = select(BooksModel)
	result = await session.execute(query)
	return result.scalars().all()
    
    @classmethod
    async def get_book(cls, book_id: int, session: AsyncSession):
	query = select(BooksModel).where(BooksModel.id == book_id)
	result = await session.execute(query)
	return result.scalars().first()
    
    @classmethod
    async def update_book(cls, book_id: int, data: SBookAdd, session: AsyncSession):
	query = select(BooksModel).where(BooksModel.id == book_id)
	result = await session.execute(query)
	if result.scalars().first():
	    book_dict = data.model_dump()
	    query = update(BookModel).where(BooksModel.id == book_id).values(**book_dict)
	    result = await session.execute(query)
	    await session.commit()
	    await session.refresh(result)
	    return result
    
    @classmethod
    async def delete_book(cls, book_id: int, session: SBookAdd):
	query = select(BooksModel).where(BooksModel.id == book_id)
	result = await session.execute(query)
	if result.scalars().first():
	    query = delete(BooksModel).where(BooksModel.id == book_id)
	    await session.execute(query)
	    await session.commit()
	    return 204