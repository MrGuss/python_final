from app.core.security import create_access_token, decode_token, hash_password, verify_password


def test_password_hash_is_not_plaintext_and_verifies_correct_password():
    password = "correct horse battery staple"

    password_hash = hash_password(password)

    assert password_hash != password
    assert verify_password(password, password_hash) is True
    assert verify_password("incorrect horse battery staple", password_hash) is False


def test_create_access_token_round_trips_expected_payload():
    token = create_access_token(sub="42", role="admin")

    payload = decode_token(token)

    assert payload.sub == "42"
    assert payload.role == "admin"
    assert payload.iat
    assert payload.exp
    assert payload.exp > payload.iat
