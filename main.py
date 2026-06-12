from fastapi import FastAPI, Body
import uvicorn

app = FastAPI()

hotels = [
    {
        "id": 1,
        "title": "Sochi",
        "name": "sochi"
    },
    {
        "id": 2,
        "title": "Дубай",
        "name": "dubai"
    }
]

@app.get("/hotels")
def get_hotels(
        title: str | None = None,
        id: int | None = None
):
    _hotels = []
    for hotel in hotels:
        if title:
            hotel["title"] != title
            continue
        if id:
            hotel["id"] != id
            continue
        _hotels.append(hotel)
    return {"hotels": _hotels}

@app.delete("/hotels/{id}")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel[id] != id]
    return {"status": "OK"}

@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title
        }
    )
    return {"status": "OK"}

@app.put("/hotels/{id_hotel}")
def update_hotel(
        id_hotel: int,
        title: str,
        name: str
):
    global hotels

    for hotel in hotels:
        if id_hotel == hotel["id"]:
            hotel["id"] = id_hotel
            hotel["title"] = title
            hotel["name"] = name

    return {"status": "OK"}

@app.patch("/hotels/{id_hotel}")
def partial_update_hotel(
        id_hotel: int,
        title: str | None = None,
        name: str | None = None
):
    global hotels

    for hotel in hotels:
        if id_hotel == hotel["id"]:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name

    return {"status": "OK"}



@app.get("/")
def health_check():
    return "все ок"



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
