import vcs, cdms2, sys, os

file = cdms2.open(os.path.join(vcs.sample_data, "clt.nc"))
clt = file("clt", time=('1985-1', '1985-12'))
canvas = vcs.init()
move_y = .5
for i in range(0, len(clt), 3):
    mean = (clt[i] + clt[i+1] + clt[i+2]) / 3
    temp = canvas.createtemplate()
    temp.scale(.5, "x")
    temp.scale(.5, "y")
    move_x = None

    if i % 2 == 0:
        move_x = 0
    else:
        move_x = .5

    if i > 3:
        move_y = 0

    temp.move(move_x, "x")
    temp.move(move_y, "y")

    temp.blank()
    temp.data.priority = 1

    canvas.plot(mean, temp)
raw_input()
