from tdd.tasks import generate_avatar_thumbnail


def test_task_generate_avatar_thumbnail(db, member):
    # init state
    assert member.avatar
    assert not member.avatar_thumbnail

    generate_avatar_thumbnail(member.pk)

    member.refresh_from_db()

    assert member.avatar_thumbnail
    assert member.avatar_thumbnail.height == 100
    assert member.avatar_thumbnail.width == 100
