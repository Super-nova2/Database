import mastcasjobs
from mq_cat import get_mq_cat
from crossmatch import crossmatch
import pandas as pd
import numpy as np

if __name__ == '__main__':

    # MAST CasJobs authentication
    user = "***"
    pwd = "***"
    jobs = mastcasjobs.MastCasJobs(username=user, password=pwd,request_type='POST')
    name = "milliquas_z1"
    #upload the catalogue of milliquas to MAST CasJobs
    get_mq_cat(l = 30000)
    match_num,match_id = crossmatch()
    if match_num:
        print("Crossmatch successful")
        data = jobs.fast_table('{}_PS1det'.format(name))
        data.write('/data/database/PS1/{}_PS1det9.csv'.format(name),format='csv',overwrite=True)
    else:
        print("Crossmatch failed")
    
    print("Data have been load successfully")
    
    # divide the data by objid#
    obj = pd.DataFrame(columns=['objdata','objID'],index=range(match_num))   #objID belonging to PS1
    objid = np.zeros(match_num)
    for k in range(0,match_num):
        w = np.where(data['Id']==match_id[k])
        obj.loc[k,'objdata'] = data[w]
        obj.loc[k,'objID'] = data['objID'][w[0][0]]

        if k%500==0:
            print("Dividing the data by objid, {}/{} completed".format(k,match_num))
        
    # save each AGN's data to a csv file
    for i in range(0, match_num):      
        agn_data = obj.loc[i,'objdata']
        agn_data.write('/data/database/PS1/data/{}_{}_{}.csv'.format(agn_data['Id'][0],agn_data['Name'][0],objid[i]),format='csv',overwrite=True)
        
        if i%500==0:
            print("Saving AGN's Data, {}/{} completed".format(i,match_num))
    print("Each AGN's Data have been saved to /data/database/PS1/data/")
