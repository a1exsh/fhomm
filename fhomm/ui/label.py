import fhomm.render
import fhomm.ui


# TODO: text_fn=constantly(text)
class Label(fhomm.ui.Element):
    def __init__(self, rect, font, text):
        super().__init__(rect)
        self.font = font
        self.text = text

    def on_render(self, ctx, _):
        self.font.draw_text(
            ctx,
            self.text,
            self.rect,
            halign=fhomm.render.CENTER,
            valign=fhomm.render.CENTER,
        )


class DynamicLabel(fhomm.ui.Element):
    def __init__(self, rect, font, text_fn):
        super().__init__(rect)
        self.font = font
        self.text_fn = text_fn

    def on_render(self, ctx, state, ext_state=None):
        if ext_state is not None:
            text = self.text_fn(state, ext_state)

        else:
            text = self.text_fn(state)

        if text:
            self.font.draw_text(
                ctx,
                text,
                self.rect,
                halign=fhomm.render.CENTER,
                valign=fhomm.render.CENTER,
            )
