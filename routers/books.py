from fastapi import APIRouter, status, HTTPException
from database import SessionDep
from schemas.books import SBookAdd, SBook
from repository import BookRepository

router = APIRouter(prefix="/books", tags=["Книги"])

@router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def add_book(book: SBookAdd, session: SessionDep):
    result = await BookRepository.add_book(book, session)
    return result

@router.get("", response_model=list[SBook])
async def get_books(session: SessionDep):
    result = await BookRepository.get_books(session)
    return result

@router.get("/{id}", response_model=SBook)
async def get_book(id: int, session: SessionDep):
    result = await BookRepository.get_book(id, session)
    if result is None:
	raise HTTPException(
	    status_code=status.HTTP_404_NOT_FOUND,
	    detail="Книга не найдена"
	)
    return result

@router.put("/{id}", response_model=SBook)
async def update_book(id: int, book: SBookAdd, session: SessionDep):
    result = await BookRepository.update_book(id, book, session)
    if result is None:
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int, session: SessionDep):
    result = await BookRepository.delete_book(id, session)
    if result is None:
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)