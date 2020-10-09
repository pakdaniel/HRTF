class SOFA:
    def __init__(self, obj):

        self.IR = obj.getDataIR().data
        self.SamplingRate = obj.getSamplingRate().data
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