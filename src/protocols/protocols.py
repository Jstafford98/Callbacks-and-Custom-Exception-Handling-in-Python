from typing import Protocol

__all__ = ['_ExceptionCallback']

class _ExceptionCallback(Protocol):
    ''' Defines the expected signature for an exception callback '''
    
    def __call__(self, exception : Exception) -> str :
        ...

