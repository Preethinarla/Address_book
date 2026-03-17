# from pydantic import BaseModel, Field

# class AddressCreate(BaseModel):
#     name: str
#     latitude: float = Field(..., ge=-90, le=90)
#     longitude: float = Field(..., ge=-180, le=180)

# class AddressOut(AddressCreate):
#     id: int

#     class Config:
#         orm_mode = True



from pydantic import BaseModel, Field

class AddressBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    name: str | None = None
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)

class AddressOut(AddressBase):
    id: int

    class Config:
        from_attributes = True