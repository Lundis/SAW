from .models import BoardSettings, Board, BoardMember, BoardType, Role
from members.models import Member


def setup():
    settings = BoardSettings.instance()
    if not settings.is_setup:
        # Create a board type for the board :D
        board_type = BoardType(name="The Board")
        board_type.save()

        # Create some roles
        role_chairman = Role(name="Chairman")
        role_chairman.save()
        role_treasurer = Role(name="Treasurer")
        role_treasurer.save()
        role_random_dude = Role(name="Superman")
        role_random_dude.save()

        # Create a board
        board = Board(year=2015,
                      photo=None,
                      boardtype= board_type)
        board.save()

        # Create some members
        member1 = Member(first_name="Clark",
                         last_name="Kent")
        member1.save()
        member2 = Member(first_name="Charles",
                         last_name="Xavier")
        member2.save()
        member3 = Member(first_name="Scrooge",
                         last_name="McDuck")
        member3.save()
        # Add Xavier to the board
        chairman = BoardMember(board=board,
                               role=role_chairman,
                               member=member2)
        chairman.save()
        # Add Scrooge to the board
        chairman = BoardMember(board=board,
                               role=role_treasurer,
                               member=member3)
        chairman.save()
        # Add Kent to the board
        chairman = BoardMember(board=board,
                               role=role_random_dude,
                               member=member1)
        chairman.save()

        settings.is_setup = True