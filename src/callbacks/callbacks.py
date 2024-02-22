''' Callbacks used for custom exception logging '''

from __future__ import annotations

import traceback
from pathlib import Path
from typing import NamedTuple

__all__ = ['_ExceptionInformation', '_FormattedExceptionCallback']

class _ExceptionInformation(NamedTuple):
    ''' 
        Container class for information about an exception in code 

        args:
            filename : Python file in which exception occured
            function : Python function in which exception occured
            line_num : Line number in filename where exception occured
            exception_type : Class name for the exception
            exception_message : Message associated with the exception
    '''
    
    filename : str
    function : str
    line_num : int | None
    exception_type : str
    exception_message : str | None
    
    @staticmethod
    def build(
        frame_summary : traceback.FrameSummary, exception : Exception
    ) -> _ExceptionInformation :
        ''' 
            Constructs an _ExceptionInformation container given the Exception
            and the FrameSummary in which it occured
            
            args:
                frame_summary : Information about the stack frame in which 
                                Exception occured.
                exception     : The exception which was raised
        '''
        filename = Path(frame_summary.filename).name
        function = frame_summary.name
        line_num = frame_summary.lineno
        exc_type = type(exception).__name__
        (msg,)   = exception.args
        
        return _ExceptionInformation(
            filename=filename, function=function, line_num=line_num, 
            exception_type=exc_type, exception_message=msg
        )
        
    def __repr__(self) -> str :
        ''' String represenation for logging '''
        
        return f'ExceptionInformation('\
                    f'PyFile = {self.filename}, '\
                    f'PyFunction = {self.function}, '\
                    f'PyLine = {self.line_num}, '\
                    f'Type = {self.exception_type}, '\
                    f'Message = {self.exception_message}'\
                ')'     

class _FormattedExceptionCallback:
    ''' Exception callback following the _ExceptionCallback protocol '''
    
    def __call__(self, exception : Exception) -> _ExceptionInformation :
        ''' 
            Takes in an exception which occured in code and returns 
            formatted information retrieved from the stack frame in 
            which it occured
        '''
        
        '''
            Get last traceback.FrameSummary in the stack. 
            This returns information about the last frame
            before the jump in _FormattedExceptionCallback.__call__
        '''
        last_frame = traceback.extract_stack()[-2]
        
        ''' Build exception information and return '''
        return _ExceptionInformation.build(
            frame_summary=last_frame, exception=exception
        )