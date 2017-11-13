'''
A function to load an eg file for the LHD experiment.
The typical usage is

>>> data = eg.load(filename)

@author: keisukefujii
'''

import numpy as np
from collections import OrderedDict
import warnings
from copy import deepcopy
from datetime import datetime
import xarray as xr

def load(filename, **overwrite_params):
    """
    Load eg-file and returns as xarray.DataSet.

    To load the data from a file,

    >>>  array = eg.load(filename)

    First, we load [Parameters] and [comments] parts of the eg-file.
    Parameters are stored in xarray.DataArray.attrs as an OrderedDict.

    If **overwrite_params is explicitly passed, e.g.

    >>> eg.load(filanema, ShotNo=131000)

    we do not read the corresponding parameter from file but
    adapt the passed value.
    """
    parameters = OrderedDict()
    comments = OrderedDict()

    def set_param(name, value, functor=lambda x: x):
        """ Set a param to parameters from file header or overwrite_params """
        if name not in overwrite_params.keys():
            parameters[name] = functor(value)
        else:
            parameters[name] = overwrite_params[name]

    # load [Parameters] and [Comments] section
    try:
        if isinstance(filename, str):
            f = open(filename, 'rb')
        else:
            f = filename

        for line in f:
            line = line.decode("utf-8")
            if '[parameters]' in line.lower():
                block = 'Parameters'
            elif '[comments]' in line.lower():
                block = 'comments'
            elif '[data]' in line.lower():
                break # data is read np.loadtxt
            elif not '#' in line:
                break # Finish reading.
            # read Parameters block
            elif block is 'Parameters':
                # Make lower case
                key = line[line.find('#')+1:line.find("=")].strip()
                # remove '(quotation) and , (space)
                val = line[line.find('=')+1:].replace(" ","").replace("'", "").strip()
                # string
                if key.lower() == 'NAME'.lower():
                    set_param('NAME', val)
                # list of string
                elif key.lower() == 'DimName'.lower():
                    set_param('DimName', val, lambda x: x.split(','))
                elif key.lower() == 'DimUnit'.lower():
                    set_param('DimUnit', val, lambda x: x.split(','))
                elif key.lower() == 'ValName'.lower():
                    set_param('ValName', val, lambda x: x.split(','))
                elif key.lower() == 'ValUnit'.lower():
                    set_param('ValUnit', val, lambda x: x.split(','))
                # string
                elif key.lower() == 'Date'.lower():
                    set_param('Date', val)
                # integers
                elif key.lower() == 'DimNo'.lower():
                    set_param('DimNo', val, int)
                elif key.lower() == 'ValNo'.lower():
                    set_param('ValNo', val, int)
                elif key.lower() == 'ShotNo'.lower():
                    set_param('ShotNo', val, int)
                elif key.lower() == 'SubShotNO'.lower():
                    set_param('SubShotNO', val, int)
                # list of integers
                elif key.lower() == 'DimSize'.lower():
                    set_param('DimSize', val, lambda x:
                                            [int(s) for s in x.split(',')])
                else: # the rest of parameters                # string
                    if key is not None and len(key)>0:
                        parameters[key] = line[line.find('=')+1:].strip()

            elif block is 'comments':
                # Make lower case
                key = line[line.find('#')+1:line.find("=")].strip()
                # remove '(quotation) and , (space)
                val = line[line.find('=')+1:].replace(" ","").replace("'", "").strip()
                if key is not None and len(key)>0:
                    comments[key] = line[line.find('=')+1:].strip()

        # Make sure some necessary parameters are certainly stored
        need_keys = ['NAME', 'DimName', 'DimUnit', 'ValName', 'ValUnit', 'Date',
                     'DimNo', 'ValNo', 'ShotNo', 'DimSize']
        for need_key in need_keys:
            if need_key not in parameters.keys():
                raise ValueError('There is no '+ need_key + ' property in ' +
                                 filename)
        """
        Next, we load [Data] part of file.
        """
        # temporary data
        try:
            tmpdata = np.loadtxt(filename, comments='#', delimiter=',')
        except ValueError as e:
            cols = range(parameters['DimNo'] + parameters['ValNo'])
            tmpdata = np.loadtxt(filename, comments='#', delimiter=',',
                                 usecols=cols)
    except Exception as e:
        print(e)
    finally:
        if isinstance(filename, str):
            f.close()

    # Even if parameters['DimNo'] contradicts with the actual data size,
    # we estimate it.
    if parameters['DimNo'] == 1:
        if parameters['DimSize'][0] != tmpdata.shape[0]:
            parameters['DimSize'] = [tmpdata.shape[0], ]
    # storing and reshape dims (dict)
    coords = OrderedDict()
    for i, dname in enumerate(parameters['DimName']):
        d = tmpdata[:,i].reshape(parameters['DimSize'])
        coords[dname] = \
            ((dname),
             np.swapaxes(d, 0, i).flatten(order='F')[:parameters['DimSize'][i]],
             {'Unit': parameters['DimUnit'][i]})
    # append scalar coordinate
    coords['ShotNo'] = parameters['ShotNo']

    # xr.DataSet that will be created by this method.
    result = OrderedDict()
    for i, vname in enumerate(parameters['ValName']):
        result[vname] = xr.DataArray(
                data=tmpdata[:,i+len(parameters['DimName'])].reshape(
                            parameters['DimSize']),
                dims=parameters['DimName'], coords=coords, name=vname,
                attrs={'Unit': parameters['ValUnit'][i]})

    attrs = OrderedDict()
    for key, item in parameters.items():
        # remove unnecessary parameters (to avoid duplicity)
        if key not in ['DimName', 'DimNo', 'ValName', 'ValNo', 'DimSize',
                       'DimUnit', 'ValUnit', 'ShotNo']:
            attrs[key] = item
    attrs.update(comments)

    ds = xr.Dataset(result, coords=coords, attrs=attrs)

    # make sure there are no duplicate values in the coordinate
    for d in ds.dims:
        if d in ds.coords:
            coord = ds[d].values
            index = [list(coord).index(v) for v in np.unique(coord)]
            ds = ds.isel(**{d: index})
    return ds


def dump(dataset, filename, fmt='%.6e', NAME=None, ShotNo=None):
    """
    Save xarray.Dataset to file.

    parameters:
    - dataset: xarray.Dataset object.
        To make the file compatibile to eg file, the following information is
        necessary, ['NAME', 'ShotNo']
        To add these attributes to xarray.Dataset, call
        >>> dataset.attrs['NAME'] = 'some_name'
    - filename: path to file
    - fmt: format of the values. Same to np.savetxt. See
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html
        for the detail.
    """
    obj,  = xr.broadcast(dataset.copy(deep=True))
    # Make sure some necessary parameters are certainly stored
    if NAME is None:
        if 'NAME' not in obj.attrs.keys():
            raise ValueError('There is no '+ NAME + ' property in ' +
                             filename + '. Please provide NAME argument')
        else:
            NAME = obj.attrs['NAME']
    obj.attrs['NAME'] = '\'' + NAME + '\''

    if ShotNo is None:
        if 'ShotNo' in obj.attrs.keys():
            ShotNo = obj.attrs['ShotNo']
        elif 'ShotNo' in obj.coords:
            ShotNo = int(obj['ShotNo'].values)
        else:
            raise ValueError('There is no '+ ShotNo + ' property in ' + \
                            filename + '. Please provide ShotNo argument')

    obj.attrs['ShotNo'] = ShotNo

    dims = [key for key in obj.coords if key in obj.dims]
    dimsize = [len(obj.coords[key]) for key in dims]

    def add_primes(s):
        """ Attach primes if s is str or list or str"""
        if isinstance(s, list):
            line = add_primes(s[0])
            for s1 in s[1:]:
                line += ', ' + add_primes(s1)
            return line
        elif isinstance(s, str):
            return '\'' + s + '\''
        else:
            return str(s)

    # add some attributes
    obj.attrs['DimName'] = add_primes(dims)
    obj.attrs['DimNo']   = len(obj.dims)
    obj.attrs['DimUnit'] = add_primes([obj.coords[d].attrs['Unit']
                                       if 'Unit' in obj.coords[d].attrs.keys()
                                       else '' for d in dims])
    obj.attrs['DimSize'] = dimsize
    obj.attrs['ValName'] = add_primes([k for k in obj.data_vars.keys()])
    obj.attrs['ValNo']   = len(obj.data_vars.keys())
    obj.attrs['ValUnit'] = add_primes([c.attrs['Unit'] if 'Unit' in
                                       c.attrs.keys() else ''
                                       for key,c in obj.data_vars.items()])
    obj.attrs['Date']    = datetime.now().strftime('\'%m/%d/%Y %H:%M\'')

    # prepare the header
    # main parameters
    header = "[Parameters]\n"
    for key in ['NAME', 'ShotNo', 'Date', 'DimNo', 'DimName', 'DimSize',
                'DimUnit', 'ValNo', 'ValName', 'ValUnit']:
        item = obj.attrs[key]
        if isinstance(item, list):
            header += key + " = " + add_primes(item) +"\n"
        else:
            header += key + " = " + str(item) +"\n"
        del obj.attrs[key] # remove already written entries.

    # other parameters
    header += "\n[comments]\n"
    for key, item in obj.attrs.items():
        header += key + " = " + str(item) +"\n"
    # data start
    header += "\n[data]"

    #---  prepare 2d data to write into file ---
    data = []
    # prepare coords.
    for i, key in enumerate(dims):
        # expand dims to match the data_vars shape
        coord = obj.coords[key]
        for j in range(len(dims)):
            if i != j:
                coord = np.expand_dims(coord, axis=j)
        # tile the expanded dims
        shape = deepcopy(dimsize)
        shape[i] = 1
        data.append(np.tile(coord, shape).flatten(order='C'))
    # append data_vars
    for key, item in obj.data_vars.items():
        data.append(
            item.transpose(*dims).values.flatten(order='C'))

    # write to file
    np.savetxt(filename, np.stack(data, axis=0).transpose(), header=header,
               delimiter=', ', fmt=fmt)
