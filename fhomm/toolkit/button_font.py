from fhomm.render import Pos, Size, Rect
import fhomm.render

class ButtonFont(fhomm.render.Font):

    BASELINE = 12

    def __init__(self, toolkit, is_pressed):
        super().__init__(
            ButtonFont.make_sprites(toolkit, is_pressed),
            baseline=ButtonFont.BASELINE,
            space_width=8,
        )

    @classmethod
    def make_sprites(cls, toolkit, is_pressed):
        img = [fhomm.render.Image.make_empty()] * 96

        magic = {
            # LOAD GAME
            ('btnmain.icn', 0): {
                'A': Rect.ltrb(63, 13, 78, 26),
                'D': Rect.ltrb(79, 13, 91, 26),
                'E': Rect.ltrb(82, 28, 93, 41),
                'G': Rect.ltrb(25, 28, 49, 41),
                'L': Rect.ltrb(38, 13, 49, 26),
                'M': Rect.ltrb(63, 28, 81, 41),
                'O': Rect.ltrb(50, 13, 62, 26),
            },
            # NEW GAME
            ('btnmain.icn', 2): {
                'N': Rect.ltrb(42, 13, 58, 26),
            },
            # VIEW HIGH SCORES
            ('btnmain.icn', 4): {
                'C': Rect.ltrb(38, 36, 50, 49),
                'H': Rect.ltrb(75, 21, 90, 34),
                'I': Rect.ltrb(52, 6, 59, 19),
                'R': Rect.ltrb(64, 36, 77, 49),
                'S': Rect.ltrb(91, 36, 103, 49),
                'V': Rect.ltrb(38, 6, 51, 19),
                'W': Rect.ltrb(73, 6, 92, 19),
            },
            # QUIT
            ('btnmain.icn', 8): {
                'Q': Rect.ltrb(39, 21, 52, 34),
                'U': Rect.ltrb(53, 21, 67, 34),
                'T': Rect.ltrb(75, 21, 89, 34),
            },
            # MULTI-PLAYER GAME
            ('btnnewgm.icn', 4): {
                '-': Rect.ltrb(95, 6, 101, 19),
                'P': Rect.ltrb(26, 21, 38, 34),
                'Y': Rect.ltrb(64, 21, 76, 34),
            },
            # PLAY LORD IRONFIST
            ('btncmpgn.icn', 0): {
                'F': Rect.ltrb(61, 36, 72, 49),
            },
            # NETWORK
            ('btnmp.icn', 2): {
                'K': Rect.ltrb(104, 21, 117, 34),
            },
            # COM 1
            ('btncom.icn', 0): {
                '1': Rect.ltrb(86, 21, 94, 34),
            },
            # COM 2
            ('btncom.icn', 2): {
                '2': Rect.ltrb(85, 21, 95, 34),
            },
            # COM 3
            ('btncom.icn', 4): {
                '3': Rect.ltrb(84, 21, 95, 34),
            },
            # COM 4
            ('btncom.icn', 6): {
                '4': Rect.ltrb(84, 21, 95, 34),
            },
            # HOST (DIALS)
            ('btnmodem.icn', 0): {
                '(': Rect.ltrb(25, 28, 31, 42),
                ')': Rect.ltrb(95, 28, 100, 42),
            },
        }

        for (icn_name, base_idx), char_to_rect in magic.items():
            if is_pressed:
                base_idx += 1
            ctx = toolkit.load_sprite(icn_name, base_idx).get_context()
            for char, rect in char_to_rect.items():
                if is_pressed:
                    rect = rect.moved_by(Pos(-2, 2))
                img[cls.get_sprite_idx(char)] = ctx.capture(rect)

        # putting "B" together from "R" and "D"
        img[cls.get_sprite_idx('B')] = img[cls.get_sprite_idx('R')].make_copy()
        ctx = img[cls.get_sprite_idx('B')].get_context()
        ctx.blit(img[cls.get_sprite_idx('R')], Pos(3, 4), Rect.ltrb(3, 5, 12, 7))
        ctx.blit(img[cls.get_sprite_idx('D')], Pos(0, 7), Rect.ltrb(0, 7, 12, 13))

        # J X Z

        return [
            fhomm.render.Sprite.from_image(i, Pos(0, -ButtonFont.BASELINE))
            for i in img
        ]
