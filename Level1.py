# The Beginning

grid = [
"                                                                                                                                                                                                         .......                 ",
"               ............                                                                                                                                                                              .XXXXX.                 ",
"               .....  .....                                                                                                   +                                                                    bbb   XXXXXXX                 ",
"               YYYYY  YYYYY                                   .                                                                                                                                          XXXXXXX                 ",
"                   Y  Y                                            g                                                  YYYY                                                                    bbb        XXXXXXX                 ",
"                   Y .Y                                   ...    YYYYY                                                                                                                                   XXXXXXX                 ",
"                   Y  Y                                                    f                                                                                                                       bbb  XXXXXXXXX                ",
"                   Y. Y              ..             ..   YYYYYYYY                                               YYYY                                                                                   +XXXXXXXXX                ",
"                   Y  Y                                                  YYYYY                                                                                                                bbb     ..XXXXXXXXX                ",
"                   Y .Y              YYYY    j     YYYYYYYY                                                                                ..                                                        ..XXXXXXXXXXX               ",
"    ..             Y  Y                                                                                   YYYY                           YYYYYY       .              .                             .XZZXXXXXXXXXXXYYYZZYXXXXXXX@@",
"        ..         Y. Y        YYYYYY      m XX                                                                                                                     YYY                           XXY  YYYYYYYYYYYYYY  YXXXXXXX@@",
"            ..                             XXXXXX            Y                                   j                                                    Y         g                                XXXY  YYYYYYYYYYYYYY  YXXXXXXXXX",
" t                 m                     XXXXXXXXXX          Y         r                                    m           m               m       ..    Y     ..                                  XXXXY  YYYYYYYYYYYYYY  YXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXY   .YXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  m            m XXXXXXXYYYYY..YYYY..YYYYYYYYYY..YYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX               XXXXXY  YYYYYYYYYYYYYY  YXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXY   gYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX . XXXXXXXXXXXX     ..    ..          ..   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    f   f    XXXXXXY     . . . .      YXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXXY   .YXXXXXXXXXXX    +     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX . XXXXXXXXXXXX                             XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     g     XXXXXXXY               m  YXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXXXY   .YXXXXXXXXXX..........XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX . XXX jg XXXXX                              XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  m B m  XXXXXXXXXYYYIIIIIIIIIIIIYYYYXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXY                        YYYYYYYYYXXXXXXXXXXXXXXXXXXXXXXXX . ZZZ    XXXXX                               XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXYYYYYYYYYYYYYYYYYYYXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXY            m       m  YYYYYYYYYYYYYYYYYXXXXXXXXXXXXXXXX . ZZZ .. XXXXX                                XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYXXXXXXXXXXXX   XXXXXXXXXXXX                                 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

from user35_8l1Rb3xip0_13 import LevelInfo
    
level = LevelInfo(
    "The Beginning",
    grid,
    {'f': (False, False, True),
     'g': ((30,50),(10,50),(20,50), (10,50), (10,50)),
     'j': ((500,1000,80),(1000,2000,250),(500,1000,80),(500,1000,80)),
     '+': (200, 100, 100, 300, 400, 200),
     'B': (1200,),
     },
    colors = ['#00FF00','#7F3300']
)