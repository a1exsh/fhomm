from fhomm.render import Pos, Size, Rect
import fhomm.render

class ButtonFont(fhomm.render.Font):

    BASELINE = 12

    def __init__(self, toolkit):
        super().__init__(
            ButtonFont.make_sprites(toolkit),
            baseline=ButtonFont.BASELINE,
            space_width=8,
        )

    @classmethod
    def make_sprites(cls, toolkit):
        img = [fhomm.render.Image.make_empty()] * 96

        # LOAD GAME
        ctx = toolkit.load_sprite('btnmain.icn', 0).get_context()
        img[cls.get_sprite_idx('A')] = ctx.capture(Rect.ltrb(63, 13, 78, 26))
        img[cls.get_sprite_idx('D')] = ctx.capture(Rect.ltrb(79, 13, 91, 26))
        img[cls.get_sprite_idx('E')] = ctx.capture(Rect.ltrb(82, 28, 93, 41))
        img[cls.get_sprite_idx('G')] = ctx.capture(Rect.ltrb(25, 28, 49, 41))
        img[cls.get_sprite_idx('L')] = ctx.capture(Rect.ltrb(38, 13, 49, 26))
        img[cls.get_sprite_idx('M')] = ctx.capture(Rect.ltrb(63, 28, 81, 41))
        img[cls.get_sprite_idx('O')] = ctx.capture(Rect.ltrb(50, 13, 62, 26))

        # NEW GAME
        ctx = toolkit.load_sprite('btnmain.icn', 2).get_context()
        img[cls.get_sprite_idx('N')] = ctx.capture(Rect.ltrb(42, 13, 58, 26))

        # VIEW HIGH SCORES
        ctx = toolkit.load_sprite('btnmain.icn', 4).get_context()
        img[cls.get_sprite_idx('C')] = ctx.capture(Rect.ltrb(38, 36, 50, 49))
        img[cls.get_sprite_idx('H')] = ctx.capture(Rect.ltrb(75, 21, 90, 34))
        img[cls.get_sprite_idx('I')] = ctx.capture(Rect.ltrb(52, 6, 59, 19))
        img[cls.get_sprite_idx('R')] = ctx.capture(Rect.ltrb(64, 36, 77, 49))
        img[cls.get_sprite_idx('S')] = ctx.capture(Rect.ltrb(91, 36, 103, 49))
        img[cls.get_sprite_idx('V')] = ctx.capture(Rect.ltrb(38, 6, 51, 19))
        img[cls.get_sprite_idx('W')] = ctx.capture(Rect.ltrb(73, 6, 92, 19))

        # QUIT
        ctx = toolkit.load_sprite('btnmain.icn', 8).get_context()
        img[cls.get_sprite_idx('Q')] = ctx.capture(Rect.ltrb(39, 21, 52, 34))
        img[cls.get_sprite_idx('U')] = ctx.capture(Rect.ltrb(53, 21, 67, 34))
        img[cls.get_sprite_idx('T')] = ctx.capture(Rect.ltrb(75, 21, 89, 34))

        # MULTI-PLAYER GAME
        ctx = toolkit.load_sprite('btnnewgm.icn', 4).get_context()
        img[cls.get_sprite_idx('-')] = ctx.capture(Rect.ltrb(95, 6, 101, 19))
        img[cls.get_sprite_idx('P')] = ctx.capture(Rect.ltrb(26, 21, 38, 34))
        img[cls.get_sprite_idx('Y')] = ctx.capture(Rect.ltrb(64, 21, 76, 34))

        # PLAY LORD IRONFIST
        ctx = toolkit.load_sprite('btncmpgn.icn', 0).get_context()
        img[cls.get_sprite_idx('F')] = ctx.capture(Rect.ltrb(61, 36, 72, 49))

        # NETWORK
        ctx = toolkit.load_sprite('btnmp.icn', 2).get_context()
        img[cls.get_sprite_idx('K')] = ctx.capture(Rect.ltrb(104, 21, 117, 34))

        # putting "B" together from "R" and "D"
        img[cls.get_sprite_idx('B')] = img[cls.get_sprite_idx('R')].make_copy()
        ctx = img[cls.get_sprite_idx('B')].get_context()
        ctx.blit(img[cls.get_sprite_idx('R')], Pos(3, 4), Rect.ltrb(3, 5, 12, 7))
        ctx.blit(img[cls.get_sprite_idx('D')], Pos(0, 7), Rect.ltrb(0, 7, 12, 13))

        # B J X Z

        # COM 1
        ctx = toolkit.load_sprite('btncom.icn', 0).get_context()
        img[cls.get_sprite_idx('1')] = ctx.capture(Rect.ltrb(86, 21, 94, 34))

        # COM 2
        ctx = toolkit.load_sprite('btncom.icn', 2).get_context()
        img[cls.get_sprite_idx('2')] = ctx.capture(Rect.ltrb(85, 21, 95, 34))

        # COM 3
        ctx = toolkit.load_sprite('btncom.icn', 4).get_context()
        img[cls.get_sprite_idx('3')] = ctx.capture(Rect.ltrb(85, 21, 95, 34))

        # COM 4
        ctx = toolkit.load_sprite('btncom.icn', 6).get_context()
        img[cls.get_sprite_idx('4')] = ctx.capture(Rect.ltrb(84, 21, 95, 34))

        # HOST (DIALS)
        ctx = toolkit.load_sprite('btnmodem.icn', 0).get_context()
        img[cls.get_sprite_idx('(')] = ctx.capture(Rect.ltrb(25, 28, 31, 42))
        img[cls.get_sprite_idx(')')] = ctx.capture(Rect.ltrb(95, 28, 100, 42))

        return [
            fhomm.render.Sprite.from_image(i, Pos(0, -ButtonFont.BASELINE))
            for i in img
        ]
