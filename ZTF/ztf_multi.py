from ztfquery import lightcurve
import matplotlib.pyplot as plt
from astropy.table import Table
import numpy as np

#load the crossmatch data
name = 'S240629by'
cat = Table.read('/home/supernova/桌面/python/database/crossmatch_data/{}.xml'.format(name))
for i in range(len(cat)):
    print(i)
    lcq = lightcurve.LCQuery.from_position(cat[i]['RAJ2000'], cat[i]['DEJ2000'], 3)
    if lcq.data.empty==True:
        continue
    data_ztf = Table.from_pandas(lcq.data)
    t_ztf = data_ztf['mjd'] 
    mag_ztf = data_ztf['mag']
    err_ztf = data_ztf['magerr']
    xlim = np.array([t_ztf.min(),t_ztf.max()])
    xlim = xlim + np.array([-1,1])*0.02*(xlim[1]-xlim[0])
    #plot the lightcures
    plt.rcParams.update({'font.size': 14})
    plt.figure(1,(10,10))
    for j, filter in enumerate("gri"):
        plt.subplot(311+j)
        u = np.where(data_ztf['filtercode']=='z{}'.format(filter))
        plt.errorbar(t_ztf[u],mag_ztf[u],err_ztf[u],fmt='o',markersize=4, color='blue', ecolor='red', capsize=3,linestyle='None')
        plt.ylabel(filter+' [mag]')
        plt.xlim(xlim)
        plt.gca().invert_yaxis()
        if j==0:
            plt.title("Name:{} Dec:{:.3f} Ra:{:.3f} Dis:{}".format(cat[i]['Name'],cat[i]['RAJ2000'], cat[i]['DEJ2000'],cat[i]['Distance']))
    plt.xlabel('Time [MJD]')
    plt.tight_layout()
    # plt.show()
    plt.savefig('/data/lightcurves/{}/ZTF/{}_{}.png'.format(name,i,cat[i]['Name']),dpi=400)
    plt.close()

