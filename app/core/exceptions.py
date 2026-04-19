"""
В этом файле вы описываете ваши HTTP-исключения в стиле CategoryNotFoundError(BaseHTTPException). То есть вы создаёте BaseHTTPException, который наследуется от HTTPException, а затем создаёте набор конкретных исключений для Auth Service. Здесь должны быть как минимум UserAlreadyExistsError (409), InvalidCredentialsError (401), InvalidTokenError (401), TokenExpiredError (401), UserNotFoundError (404), PermissionDeniedError (403). Эти исключения должны использоваться в usecase и dependencies вместо “ручных” raise HTTPException.
"""
