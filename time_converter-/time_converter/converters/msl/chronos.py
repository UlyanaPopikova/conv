

import datetime as dt
import os

import numpy as np

sclk_data = None


def _load_sclk_data(filename=os.path.join(os.path.dirname(__file__), 'msl.tsc')):

    global sclk_data
    if sclk_data is None:
        file = open(filename)
        correct_section = False
        skip_header = None
        max_rows = None
        for i, line in enumerate(file):
            if skip_header is not None and line.lstrip().startswith('CCSD'):
                max_rows = i - skip_header
                break
            elif correct_section and line.lstrip().startswith('*'):
                skip_header = i + 1
            elif line.startswith('Source SCLKvSCET File'):
                correct_section = True
        data = np.genfromtxt(filename, dtype=(float, dt.datetime, float, float), skip_header=skip_header, max_rows=max_rows,
                             unpack=False,
                             converters={
                                 0: np.float,
                                 1: lambda x: dt.datetime.strptime(x.decode('ascii'), "%Y-%jT%H:%M:%S.%f"),
                                 2: np.float,
                                 3: np.float
                             })
        sclk, utc, dut, sclkrate = data['f0'], data['f1'], data['f2'], data['f3']
        sclk_data = sclk, utc, dut, sclkrate
    return sclk_data


def sclk_to_dt(sclk):
   
    sclks, dts, dut, sclkrate = _load_sclk_data()
   
    index = np.searchsorted(sclks, sclk, side='right') - 1
    
    seconds = (sclk - sclks[index]) * sclkrate[index]
    return dts[index] + dt.timedelta(seconds=seconds)


def dt_to_sclk(dt):
  
    sclks, dts, dut, sclkrate = _load_sclk_data()
   
    index = np.searchsorted(dts, dt, side='right') - 1
   
    return sclks[index] + (dt - dts[index]).total_seconds() / sclkrate[index]