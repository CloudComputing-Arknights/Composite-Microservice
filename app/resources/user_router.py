from uuid import UUID

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.client.user.user_address_api_client.api.default.update_user_users_user_id_put import asyncio as update_user_async
from app.client.user.user_address_api_client.models.user_update import UserUpdate

from app.client.user.user_address_api_client.api.default.login_auth_token_post import asyncio as user_login_async
from app.client.user.user_address_api_client.api.default.get_user_users_user_id_get import (
    asyncio as get_user_async,
)
from app.client.user.user_address_api_client.api.default.get_address_addresses_address_id_get import (
    asyncio as get_address_async,
)
from app.client.user.user_address_api_client.api.default.create_user_users_post import (
    asyncio as create_user_async,
)
from app.client.user.user_address_api_client.models.body_login_auth_token_post import BodyLoginAuthTokenPost
from app.client.user.user_address_api_client.models.http_validation_error import HTTPValidationError
from app.client.user.user_address_api_client.models.token import Token
from app.client.user.user_address_api_client.models.user_create import UserCreate
from app.client.user.user_address_api_client.models.user_read import UserRead
from app.client.user.user_address_api_client.types import UNSET
from app.client.user.user_address_api_client.models.address_read import AddressRead

from app.models.dto.user_dto import (
    SignInRes,
    SignInReq,
    SignedInUserRes,
    SignUpReq,
    UpdateProfileReq,
)

from app.models.dto.address_dto import AddressDTO

from app.services.address_user_repository import get_user_addresses
from app.utils.auth import get_user_id_from_token
from app.utils.config import get_user_client, get_address_client
from app.utils.db_connection import get_session

user_router = APIRouter()

@user_router.post("/token", response_model=SignInRes)
async def sign_in(payload: SignInReq):
    body = BodyLoginAuthTokenPost(username=payload.username, password=payload.password)

    result = await user_login_async(client=get_user_client(), body=body)

    if result is None:
        raise HTTPException(status_code=500)

    if isinstance(result, HTTPValidationError):
        raise HTTPException(status_code=401)

    token: Token = result
    token_type = token.token_type if token.token_type is not UNSET else "bearer"

    return SignInRes(access_token=token.access_token, token_type=token_type)


@user_router.post("/users", status_code=201, response_model=SignedInUserRes)
async def create_user(payload: SignUpReq):
    user_create = UserCreate(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        # optional fields (phone, birth_date, avatar_url, addresses) left as defaults
    )

    result = await create_user_async(client=get_user_client(), body=user_create)

    if result is None:
        raise HTTPException(status_code=500, detail="User service did not respond")

    if isinstance(result, HTTPValidationError):
        raise HTTPException(status_code=400, detail="Invalid user data")

    user: UserRead = result

    return SignedInUserRes(
        id=user.id if user.id is not UNSET else None,
        username=user.username,
        email=user.email,
        phone=user.phone if getattr(user, "phone", UNSET) is not UNSET else None,
        birth_date=(
            user.birth_date
            if getattr(user, "birth_date", UNSET) is not UNSET
            else None
        ),
        avatar_url=(
            user.avatar_url
            if getattr(user, "avatar_url", UNSET) is not UNSET
            else None
        ),
        addresses=[],
        created_at=(
            user.created_at
            if getattr(user, "created_at", UNSET) is not UNSET
            else None
        ),
        updated_at=(
            user.updated_at
            if getattr(user, "updated_at", UNSET) is not UNSET
            else None
        ),
    )

@user_router.get("/me/user", response_model=SignedInUserRes)
async def auth_me(
        request: Request,
        session: AsyncSession = Depends(get_session),
):

    authorization_header = request.headers.get("Authorization")
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    try:
        token_str = authorization_header.split(" ")[1]
        user_id = get_user_id_from_token(token_str)
        user_id = UUID(str(user_id))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await get_user_async(user_id=user_id, client=get_user_client())

    if result is None:
        raise HTTPException(status_code=502, detail="User service returned no data")

    if isinstance(result, HTTPValidationError):
        raise HTTPException(status_code=404, detail="User not found")

    user: UserRead = result

    address_ids = await get_user_addresses(session, str(user_id))

    addresses_dto: list[AddressDTO] = []

    for addr_id in address_ids:
        try:
            addr_uuid = UUID(str(addr_id))
        except ValueError:
            continue

        addr_result = await get_address_async(address_id=addr_uuid, client=get_address_client())

        if addr_result is None or isinstance(addr_result, HTTPValidationError):
            continue

        addr: AddressRead = addr_result

        addresses_dto.append(
            AddressDTO(
                id=addr.id if addr.id is not UNSET else None,
                street=addr.street,
                city=addr.city,
                state=addr.state if not isinstance(addr.state, type(UNSET)) else None,
                postal_code=addr.postal_code if not isinstance(addr.postal_code, type(UNSET)) else None,
                country=addr.country,
                created_at=addr.created_at if not isinstance(addr.created_at, type(UNSET)) else None,
                updated_at=addr.updated_at if not isinstance(addr.updated_at, type(UNSET)) else None,
            )
        )

    return SignedInUserRes(
        id=user.id if not isinstance(user.id, type(UNSET)) else None,
        username=user.username,
        email=user.email,
        phone=user.phone if not isinstance(user.phone, type(UNSET)) else None,
        birth_date=user.birth_date if not isinstance(user.birth_date, type(UNSET)) else None,
        avatar_url=user.avatar_url if not isinstance(user.avatar_url, type(UNSET)) else None,
        addresses=addresses_dto,
        created_at=user.created_at if not isinstance(user.created_at, type(UNSET)) else None,
        updated_at=user.updated_at if not isinstance(user.updated_at, type(UNSET)) else None,
    )

@user_router.put("/me/user", response_model=SignedInUserRes)
async def update_me(
    payload: UpdateProfileReq,
    request: Request,
):
    # 1. Verify Token
    authorization_header = request.headers.get("Authorization")
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Header")
    try:
        # Using the clean token string fix here as well
        token_str = authorization_header.split(" ")[1]
        user_id = get_user_id_from_token(token_str)
        user_uuid = UUID(str(user_id))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")

    # 2. Prepare Data for Downstream Service
    user_update = UserUpdate(
        email=payload.email,
        phone=payload.phone,
        avatar_url=payload.avatar_url,
        birth_date=payload.birth_date
    )

    # 3. Call Downstream Update Endpoint
    result = await update_user_async(
        client=get_user_client(),
        user_id=user_uuid,
        body=user_update
    )

    if result is None:
         raise HTTPException(status_code=500, detail="Update failed or service unavailable")
    if isinstance(result, HTTPValidationError):
         raise HTTPException(status_code=400, detail="Invalid data for update")

    # 4. Return Updated User Data (using existing mapping logic)
    user: UserRead = result
    
    # NOTE: You would typically call auth_me logic here to refetch and include addresses,
    # but for simplicity, we return the user with an empty address list.
    return SignedInUserRes(
        id=user.id if not isinstance(user.id, type(UNSET)) else None,
        username=user.username,
        email=user.email,
        phone=user.phone if not isinstance(user.phone, type(UNSET)) else None,
        birth_date=user.birth_date if not isinstance(user.birth_date, type(UNSET)) else None,
        avatar_url=user.avatar_url if not isinstance(user.avatar_url, type(UNSET)) else None,
        addresses=[], 
        created_at=user.created_at if not isinstance(user.created_at, type(UNSET)) else None,
        updated_at=user.updated_at if not isinstance(user.updated_at, type(UNSET)) else None,
    )
