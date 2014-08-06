# Lightning

grid = [
'                                         Lj                      LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL         L',
'                                         L                                   L                      L      @@@L',
'                                         L                                   L    f                 L         L',
'                                         L                                   L                      L         L',
'                                         LXXXXXX                 L           L        LLLLLLL       L         L',
'                                         L                       L           L        L             L         L',
'                                         L                       L           L        L             L         L',
'                            f            L                       L           L  ____  L             L         L',                                                                                                               '
'                                         LLLL   LLLXXXXXXXLLLLLLLL           L        L     LLLLLLLLL         L',                                                                                                             '
'    T    j    . . . . . .                          XXXXXXX                   L        L                       L',
'XXXXXXXXXXXXX             XXXXX                    XXXXXXX                   L        L                       L',
'XXXXXXXXXXXXX                                      XXXXXXX     LLLLLLLLLLLLLLL        L                       L',
'XXXXXXXXXXXXX      g                               XXXXXXX                            L                       L',
'XXXXXXXXXXXXX     XXX               XXXXXXXXXXXXXXXXXXXXXXLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL'
]

from user35_8l1Rb3xip0_13 import LevelInfo

level = LevelInfo(
    "Lightning",
    grid,
    {'f': (False, True),
     'g': [(30,50)],
     'j': [(1000,1000,200), (1000,3000,400)],
     },
    colors = ['#00FF00','#7F3300']
)