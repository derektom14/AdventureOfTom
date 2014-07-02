# The Desert

grid = [
"                                                                                                                                                                                                                                 ",
"                                                                               ......                                                                                                                                            ",
"                                                                               ......                                                                                                                                            ",
"                                                                               NNNNNN                                                                                                                                            ",
"                                                               ...                                                                                                                                                               ",
"                                                           .                              NNNNNN                                                                                                                                 ",
"                                                          NNN                                                   . . . .               . . . .                                                                                    ",
"                                                      .                                               YYY      . . . .                 . . . .                                                                                   ",
"                                                     NNN                                            Y          XX XX XX       +       XX XX XX                                                                                   ",
"               YY                 YYY            .                                              YYY             XXXXXX  .  .  .  .  .  XXXXXX                                                                                    ",
"                                                NNN                                            Y                  XXXXXX XX XX XX XX XXXXXX                                                                                      ",
"                        g                   .                                    ...      YYY                       XXXXXXXXXXXXXXXXXXXXX                  .                                                                     ",
"                     YYYYYY                NNN                                         YY                           XXXXXXXXXXXXXXXXXXXXX                  Y                                                                     ",
"               Y                  YYY                   Y   Y                    YYY                                XXXXXXXX....XXXXXXXXX                 YYY                                                               .....",
"      Y Y                               +              YY . YY                    Y                f                XXXXXXXX....XXXXXXXXX        Y   YYYYYYYYYYYYYY                                                 f       .....",
" t   YY YY       YYYm      mYYY              r        YYY   YYY                   Y    r                            XXXXXXXX....XXXXXXXXX        Y   Y            Y       r       m m m    ^^^   ^^^  ^^^  ^^^ r            .....",
"XXXXXXXKXXX--XXXXXYYY  ..  YYYXXXXXXXXXXXXXXXXXXXXXXXXXXX . XXXXXXXXNNXXXXXXXXXXXXXXXXXXXXXXXXXXXYNNNYXXXXXXXXXXXXXXXXXXXXXXZZZZXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   NNNN   XXXXXXX",
"XXXXXXX XXXj.XXXXXXYYY .. YYYXXXXXXXXXXXXXXXXXXXXXXXXXXXX>  XXXXXXXXZZZZXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXZZZZXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXX  f  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        XXXXXXXX",
"XXXXXXX X    XXXXXXXXXYYYYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX . XXXXXXXX      XXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXX....X   f                XXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX",
"XXXXXXX X f mXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXX     f  .    .XXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXX....X                    XXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX",
"XXXXXXX X  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-. XXXXXXXXXXXXX     . +  .XXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXX....X----XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX",
"XXXXXXX.X  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXX              XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX",
"XXXXXXX.X f  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX .-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXX                   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX",
"XXXXXXX.Xm    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  <XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           XXXXXXXXX  f          mXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX",
"XXXXXXX.XXX   gXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX . XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           XXXXXX       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX",
"XXXXXXX.       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX",
"XXXXXXX.       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXNNNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           Z          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX",
"XXXXXXXNNNNNNNNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXN         NZ       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX@@@@XXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX",
"XXXXXXX        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX@@@@XXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXX"
]

from user35_8l1Rb3xip0_13 import LevelInfo

level = LevelInfo(
    "The Desert",
    grid,
    {'f': (True, False, False, True, False, True, True, True),
     'g': ((30,50),(10,50),(20,50)),
     'j': ((500,1000,80),),
     '+': (200, 100, 100)},
    colors = ['#FFD87F','#7F3300'],
    complete_color = 'purple'
)