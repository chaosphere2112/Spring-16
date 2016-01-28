import vcs, cdms2, sys, os

file = cdms2.open(os.path.join(vcs.sample_data, "clt.nc"))
clt = file("clt", time=('1985-1', '1986-1'))
t = clt.getTime()[::3]
canvas = vcs.init()
alt_c = None
move_y = 0
for i in range(len(t)-1):

    mean = (clt[i] + clt[i+1] + clt[i+2]) / 3
    temp = canvas.createtemplate()
    temp.scale(.5, "x")
    temp.scale(.5, "y")
    move_x = None

    if i % 2 == 0:
        move_x = 0
    else:
        move_x = .5

    if i % 2 == 0:
        if move_y == .5:
            move_y = 0
        elif move_y == 0:
            move_y = .5

    temp.move(move_x, "x")
    temp.move(move_y, "y")

    temp.blank()
    temp.data.priority = 1

    canvas.plot(mean, temp)
raw_input()
