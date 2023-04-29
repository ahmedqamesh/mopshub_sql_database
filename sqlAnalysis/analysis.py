from __future__ import division
import numpy as np
import logging
import numba
import tables as tb
from scipy.optimize import curve_fit
class Analysis(object):
    
    def __init__(self):
        pass
    # Conversion functions
    # Computing mean for array of data 
    def Data_Mean(self, dataArray):
        return round(statistics.mean(dataArray),2)
    
    
    # Computing standard deviation for array of data
    def Data_SD(self,dataArray):
        return round(statistics.stdev(dataArray),1) 
    
    
    # calculate pooled standard deviation (SD)
    def Pooled_SD(self,dataArray1,dataArray2):
        n1, n2 = len(dataArray1),len(dataArray2)
        dataArray1_SD, dataArray2_SD = Data_SD(dataArray1) ,Data_SD(dataArray2)
        pooled_standard_deviation = math.sqrt(((n1 - 1)*dataArray1_SD * dataArray1_SD +(n2-1)*dataArray2_SD * dataArray2_SD) / (n1 + n2-2))
        return round(pooled_standard_deviation,1)
    
    # Calculate Coefficient of Variation for data array(CV)
    def Data_CV(self,dataArray):
        dataArray_Mean = Data_Mean(dataArray)
        dataArray_SD = Data_SD(dataArray)
        return round((dataArray_SD/dataArray_Mean)*100,2)
    
    # Calculate Measurments Uncertainty (MU)
    def Data_MU(self,dataArray):
        dataArray_MU = Data_Mean(dataArray)
        return str(ufloat(dataArray_MU,0.01))
    
    # Compute the Calculate the Exponentially weighted moving average (EWMA)
    def Data_EWMA(self,dataArray):
      EWMA = pd.DataFrame(dataArray).ewm
      return EWMA
    
    # Calculate Cumulative Sum of data array (CUSUM)
    def Data_CUSUM(self,dataArray):
        return np.cumsum(dataArray)
    
    
    # Calculate all and return an array of all statistical calculations 
    def Calculate_All(self,dataArray):
       dataArray_Mean = self.Data_Mean(dataArray)
       dataArray_SD = self.Data_SD(dataArray)
       dataArray_CV = self.Data_CV(dataArray)
       dataArray_MU = self.Data_MU(dataArray)
       dataArray_EWMA = self.Data_EWMA(dataArray)
       dataArray_CUSUM = self.Data_CUSUM(dataArray)
       Calculations_Array = [dataArray_Mean, dataArray_SD, dataArray_CV, dataArray_MU]
       return Calculations_Array


    def binToHexa(self, n):
        # convert binary to int
        num = int(n, 2)   
        # convert int to hexadecimal
        hex_num = hex(num)
        return(num)
    
if __name__ == "__main__":
        pass
