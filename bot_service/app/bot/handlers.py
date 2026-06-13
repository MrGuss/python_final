import time

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.core.jwt_model import JwtPayload
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()


def get_token_key(user_id: int) -> str:
    return f"tg_user_token:{user_id}"


@router.message(Command("token"))
async def cmd_set_token(message: Message):
    if message.text is None:
        await message.answer(
            "Получено пустое сообщение.\nИспользуйте: `/token <ваш_jwt_токен>`",
        )
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "Неверный формат команды.\nИспользуйте: `/token <ваш_jwt_токен>`",
        )
        return

    token = parts[1].strip()
    user_id = message.from_user.id  # pyright: ignore[reportOptionalMemberAccess]
    redis_client = get_redis()

    try:
        payload: JwtPayload = decode_and_validate(token)

        ttl = payload.exp - int(time.time())
        if ttl <= 0:
            await message.answer(
                "Этот токен уже истек. Пожалуйста, получите новый в Auth Service."
            )
            return

        await redis_client.setex(get_token_key(user_id), ttl, token)

        await message.answer(
            "Токен успешно сохранен!\nТеперь вы можете отправлять текстовые сообщения, и они будут обработаны LLM."
        )

    except Exception as e:
        await message.answer(
            "Ошибка валидации токена.\nУбедитесь, что вы скопировали его полностью и он не истек. Если проблема сохраняется, пройдите авторизацию в Auth Service заново."
        )
        print(e)


@router.message(F.text)
async def handle_text_message(message: Message):
    if message.text is None:
        await message.answer(
            "Получено пустое сообщение.\nИспользуйте: `/token <ваш_jwt_токен>`",
        )
        return

    user_id = message.from_user.id  # pyright: ignore[reportOptionalMemberAccess]
    chat_id = message.chat.id
    redis_client = get_redis()

    token_bytes = await redis_client.get(get_token_key(user_id))

    if not token_bytes:
        await message.answer(
            "Доступ запрещен.\n\nТокен не найден. Пожалуйста, пройдите авторизацию в Auth Service и отправьте полученный JWT командой:\n`/token <ваш_токен>`",
        )
        return

    if isinstance(token_bytes, bytes):
        token = token_bytes.decode("utf-8")
    else:
        token = str(token_bytes)

    try:
        decode_and_validate(token)
    except Exception as e:
        await redis_client.delete(get_token_key(user_id))
        await message.answer(
            "Токен недействителен или срок его действия истек.\n\nПожалуйста, пройдите авторизацию в Auth Service заново и обновите токен командой `/token`.",
            parse_mode="Markdown",
        )
        print(e)
        return

    llm_request.delay(tg_chat_id=chat_id, prompt=message.text)

    await message.answer(
        "Ваш запрос принят в обработку.\nПожалуйста, подождите, ответ от модели придет отдельным сообщением."
    )
