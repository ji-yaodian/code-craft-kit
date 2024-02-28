"""
this code is from structlog
"""

import contextlib
import contextvars

from typing import Any, Generator, Mapping

CONTEXT_VAR_KEY_PREFIX = "debug_info_"
CONTEXT_VAR_KEY_PREFIX_LEN = len(CONTEXT_VAR_KEY_PREFIX)

_CONTEXT_VARS: dict[str, contextvars.ContextVar[Any]] = {}


def get_contextvars() -> dict[str, Any]:
    """
    Return a copy of the specific context-local context.

    """
    rv = {}
    ctx = contextvars.copy_context()

    for k in ctx:
        if k.name.startswith(CONTEXT_VAR_KEY_PREFIX) and ctx[k] is not Ellipsis:
            rv[k.name[CONTEXT_VAR_KEY_PREFIX_LEN:]] = ctx[k]

    return rv


def clear_contextvars() -> None:
    """
    Clear the context-local context.

    The typical use-case for this function is to invoke it early in request-
    handling code.

    """
    ctx = contextvars.copy_context()
    for k in ctx:
        if k.name.startswith(CONTEXT_VAR_KEY_PREFIX):
            k.set(Ellipsis)


def bind_contextvars(**kw: Any) -> Mapping[str, contextvars.Token[Any]]:
    r"""
    Put keys and values into the context-local context.

    Use this instead of :func:`~structlog.BoundLogger.bind` when you want some
    context to be global (context-local).

    Return the mapping of `contextvars.Token`\s resulting
    from setting the backing :class:`~contextvars.ContextVar`\s.
    Suitable for passing to :func:`reset_contextvars`.

    .. versionadded:: 20.1.0
    .. versionchanged:: 21.1.0 Return the `contextvars.Token` mapping
        rather than None. See also the toplevel note.
    """
    rv = {}
    for k, v in kw.items():
        structlog_k = f"{CONTEXT_VAR_KEY_PREFIX}{k}"
        try:
            var = _CONTEXT_VARS[structlog_k]
        except KeyError:
            var = contextvars.ContextVar(structlog_k, default=Ellipsis)
            _CONTEXT_VARS[structlog_k] = var

        rv[k] = var.set(v)

    return rv


def reset_contextvars(**kw: contextvars.Token[Any]) -> None:
    r"""
    Reset contextvars corresponding to the given Tokens.

    .. versionadded:: 21.1.0
    """
    for k, v in kw.items():
        structlog_k = f"{CONTEXT_VAR_KEY_PREFIX}{k}"
        var = _CONTEXT_VARS[structlog_k]
        var.reset(v)


def unbind_contextvars(*keys: str) -> None:
    """
    Remove *keys* from the context-local context if they are present.

    Use this instead of :func:`~structlog.BoundLogger.unbind` when you want to
    remove keys from a global (context-local) context.

    .. versionadded:: 20.1.0
    .. versionchanged:: 21.1.0 See toplevel note.
    """
    for k in keys:
        structlog_k = f"{CONTEXT_VAR_KEY_PREFIX}{k}"
        if structlog_k in _CONTEXT_VARS:
            _CONTEXT_VARS[structlog_k].set(Ellipsis)


@contextlib.contextmanager
def bound_contextvars(**kw: Any) -> Generator[None, None, None]:
    """
    Bind *kw* to the current context-local context. Unbind or restore *kw*
    afterwards. Do **not** affect other keys.

    Can be used as a context manager or decorator.

    .. versionadded:: 21.4.0
    """
    context = get_contextvars()
    saved = {k: context[k] for k in context.keys() & kw.keys()}

    bind_contextvars(**kw)
    try:
        yield
    finally:
        unbind_contextvars(*kw.keys())
        bind_contextvars(**saved)
