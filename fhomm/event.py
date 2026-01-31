import pygame

EVENT_TICK = pygame.USEREVENT   # pygame.event.custom_type()
EVENT_STATE_UPDATED = pygame.USEREVENT + 1
EVENT_WINDOW_CLOSED = pygame.USEREVENT + 2


def post_tick(dt):
    pygame.event.post(
        pygame.event.Event(EVENT_TICK, dt=dt)
    )


def post_window_close(state_key, return_key, return_value):
    pygame.event.post(
        pygame.event.Event(
            EVENT_WINDOW_CLOSED,
            state_key=state_key,
            return_key=return_key,
            return_value=return_value,
        )
    )


def post_state_update(key, old, new):
    pygame.event.post(
        pygame.event.Event(EVENT_STATE_UPDATED, key=key, old=old, new=new)
    )
