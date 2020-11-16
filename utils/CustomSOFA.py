import numpy as np

class SOFA:
    def __init__(self, obj):

        self.IR = obj.getDataIR().data
        self.SamplingRate = obj.getSamplingRate().data.item()
        self.SamplingRateUnits = obj.getSamplingRateUnits()
        self.Delay = obj.getDataDelay().data
        
        dim_dict = obj.getDimensionsAsDict()
        self.M = dim_dict["M"].size # Num measurement positions
        self.R = dim_dict["R"].size # Num receivers (ears)
        self.E = dim_dict["E"].size # Num emitters (speakers)
        self.N = dim_dict["N"].size # Length of HRTF
        self.I = dim_dict["I"].size 
        self.S = dim_dict["S"].size

        self.Listener = {
            "Position": obj.getListenerPositionValues().data,
            "PositionType": obj.getListenerPositionInfo()[1],
            "PositionUnits": obj.getListenerPositionInfo()[0],
            "Up": obj.getListenerUpValues().data,
            "View": obj.getListenerViewValues().data,
            "ViewType": obj.getListenerViewInfo()[1],
            "ViewUnits": obj.getListenerViewInfo()[0],
        }

        self.Receiver = {
            "Position": obj.getReceiverPositionValues().data,
            "PositionType": obj.getReceiverPositionInfo()[1],
            "PositionUnits": obj.getReceiverPositionInfo()[0],
        }

        self.Source = {
            "Position": obj.getSourcePositionValues().data,
            "PositionType": obj.getSourcePositionInfo()[1],
            "PositionUnits": obj.getSourcePositionInfo()[0],
        }

        self.Emitter = {
            "Position": obj.getEmitterPositionValues().data,
            "PositionType": obj.getEmitterPositionInfo()[1],
            "PositionUnits": obj.getEmitterPositionInfo()[0],
        }

    @staticmethod
    def sph2cart(coords):
        alpha = coords[:, 0]*(np.pi/180)
        beta = coords[:, 1]*(np.pi/180)
        r = coords[:, 2]

        x = r * np.cos(alpha) * np.cos(beta)
        y = r * np.sin(alpha) * np.cos(beta)
        z = r * np.sin(beta)
        return np.array([x, y, z]).T

    @staticmethod
    def cart2sph(coords):
        x = coords[:, 0]
        y = coords[:, 1]
        z = coords[:, 2]
        
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        alpha = np.arctan2(y, x)
        beta = np.arcsin(z / np.where(r != 0, r, 1))
        return alpha, beta, r

    @staticmethod    
    def split_HRIR_by_location(self, azimuth, elevation):
        outputs = self.IR[np.all(self.Source["Position"][:, :2] == np.array([azimuth, elevation]), axis=1)], self.IR[np.any(self.Source["Position"][:, :2] != np.array([azimuth, elevation]), axis=1)]
        if len(outputs[0]) == 0:
            raise ValueError("The given (azimuth, elevation) angle pair does not exist in the HRIR")
        return outputs