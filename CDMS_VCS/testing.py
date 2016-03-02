import cdms2, vcs, os

if __name__ == "__main__":
    clt = cdms2.open(os.path.join(vcs.sample_data, "clt.nc"))
    v = clt.variables['clt']
    print v

    canvas = vcs.init()
    t = canvas.createtemplate()

    canvas.plot(v, t)

    raw_input("Enter when ready: ")