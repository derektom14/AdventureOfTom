# Level3
# Colors:
# X White

grid = [
"                                                                                                                                                                                                                   ",
"                                                                                                                                                                                                       .            ",
"                                                                                                                                       III                                                       .        @@        ",
"                                                   .               ....                                                                I    .                                    .    .    .        II              ",
"                                                   .       .II     bbbb     .                                                          I       .        . . .. .. . . .. .                    II                    ",
"                                                   .     . b                 .                                                         I..IIII  III  IIIbIbIbbbbbbbIbIbbIbI b II b II    II                         ",
"                                                   b                         .                                                         I                                                                            ",
"                                                       II                     .                                                        I   .    . b                                                                 ",
"                                                         bb  .                .                                                         III  II   b                                                                 ",
"                                                                               .                                                              b . b                                                                 ",
"                                                             II   .            .                                                                  b                                                                 ",
"                                                                                .                                                            ..                                                                     ",
"                                                                 III            .                                                           IIII                                                                    ",
"                                                                                 .                                                    ..                                                                            ",
"                                                            bbbb                 .                                  ..               bbbb                                                                           ",
"                                                                                  .                                                                                                                                 ",
" t                                    m               m  B     r                  .                    ..       ..    r  ..m    B                                                                                   ",
"XXXIIIIIIISSS .                       XXXXXSSSSSSSSSSSSSXXXXXXXXXXXXXXXXXX---      .           ..      II  SSSSSSSSSSSXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXXXXXXXXXII .         f          XXXXXXXXXSSSSSSSSXXXXXXXXXXXXXXXXXXXX         .           II  ..      SSSSSSSSSXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXXXXXXXXXXXII .                 XXXXXXXXSSSSSSSSSXXXXXXXXXXXXXXXXXXXXX        III              II      SSSSSSSXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXXXXXXXXXXXXXII .    IIII      XXXXXXXXX.SSSSS.XXXXXXXXXXXXXXXXXXXXXXX   ..                       ..   SSSSSXXXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXXXXXXXXXXXXXXXII             XXXXXXXXXXSSXXXXXXXXXXXXXXXXXXXXXXXXXXXX   II                   ..  II   SSXXXXXXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXX. . . . . . XXX            XXXXXXXXXXXSSSSSSSSSSSXXXXXXXXXXXXXXXXXXX               f        II       XXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXX                          XXXXXXXXXXXXSSSSSSSSSSSXXXXXXXXXXXXXXXXXXX     .                           XXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXX        f                 XXXXXXXXXXXXXXXXXXXXXSSXXXXXXXXXXXXXXXXXXX     I              ..           XXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXXg              SSSSSSSSSXXXXXXXXXXXXXXXXXXXXXXXSSXXXXXXXXXXXXXXXXXXX        ..          II           XXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXXIIIIIIIIIIIIIIIXXXXSSSSXXXXXXXXXXXXXXXXXXXXXXXXSSXXXXXXXXXXXXXXXXXXX       III                       XXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXXXXXXXXXXXXXXXXXXXXX....XXXXXXXXXXXXXXXXXXXXXXXXSSXXXXXXXXXXXXXXXXXXX             ...                 XXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXSSSS. . . . . . . . .------       III                 XXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXSSSS . . . . . . . .                                  XXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                              ",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXII                               XXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                              "
]

from user35_8l1Rb3xip0_13 import LevelInfo

level = LevelInfo(
    "The Snow",
    grid,
    {'f': (True,False,True),
     'g': ((30,50),),
     'B': (1000,1000),
     '+': (200,)},
    colors = ['#FFFFFF'],
    snow = 'X'
)  