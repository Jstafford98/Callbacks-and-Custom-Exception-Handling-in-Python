from loguru import logger
from typing import NamedTuple, Any
from protocols import _ExceptionCallback
from callbacks import _ExceptionInformation, _FormattedExceptionCallback

class Response(NamedTuple):
    ''' 
        Simple response object for standardizing the expected output from a 
        function
        
        args:
            result : any response returned from a valid function call. 
            exception : _ExceptionInformation about any exception that 
                        occured in code
    '''
    
    result    : Any = None
    exception : _ExceptionInformation | None = None

class Exponential:
    ''' Simple dummy class to showcase callbacks. '''
    
    def __init__(self, callback : _ExceptionCallback = None) -> None :
        ''' 
            args:
                callback : _ExceptionCallback compliant callback
        '''
        self.callback = callback
        
    def __call__(self, x : int) -> Response:
        ''' 
            Calculates the second power of x, if x is below 5.
            
            args:
                x : value to raise to the second power
            
            raises:
                ValueError, if x is less than 5.
        '''
        try:
            
            if x < 5:
                raise ValueError(f"{x} < 5")
            
            return Response(result=x**2)
        
        except Exception as e:
            
            if self.callback is None:
                raise e
            
            return Response(exception=self.callback(e))

if __name__ == '__main__':

    power = Exponential(callback=_FormattedExceptionCallback())
    
    for x in range(3, 7):
        
        response = power(x=x)
        
        if response.exception:
            logger.error(response.exception)
            continue
        
        logger.info(f'{x}**2 = {response.result}')