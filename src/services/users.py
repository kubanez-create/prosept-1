from src.utils.unitofwork import IUnitOfWork


class UsersService:

    async def get_user(self, uow: IUnitOfWork, email: str):
        async with uow:
            user = await uow.users.find_one(email=email)
            return user
