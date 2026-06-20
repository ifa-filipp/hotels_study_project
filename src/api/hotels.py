from fastapi import APIRouter

from sqlalchemy import insert, select, func
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("/")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = None,
        location: str | None = None,


):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)

        if location:
            query = query.where(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.where(func.lower(HotelsOrm.title).contains(title.strip().lower()))

        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )

        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels


    # return {"hotels": _hotels[(pagination.per_page * (pagination.page -1)):][:pagination.per_page]}

@router.delete("/{id}")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel[id] != id]
    return {"status": "OK"}

@router.post("/")
async def create_hotel(
        hotel_data: Hotel,
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}

@router.put("/{id_hotel}")
def update_hotel(
        id_hotel: int,
        hotel_data: Hotel,
):
    global hotels

    for hotel in hotels:
        if id_hotel == hotel["id"]:
            hotel["id"] = id_hotel
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name

    return {"status": "OK"}

@router.patch("/{id_hotel}")
def partial_update_hotel(
        id_hotel: int,
        hotel_data: HotelPATCH,

):
    global hotels

    for hotel in hotels:
        if id_hotel == hotel["id"]:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name

    return {"status": "OK"}