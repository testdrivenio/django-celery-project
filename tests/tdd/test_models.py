def test_model(db, member):
    assert member.username
    assert member.avatar
    assert not member.avatar_thumbnail