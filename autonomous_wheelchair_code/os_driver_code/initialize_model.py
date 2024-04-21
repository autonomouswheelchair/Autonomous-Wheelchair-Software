import torch

class InitializeModel:
    @staticmethod
    def initialize_model(model_type="MiDaS_small"):
        midas = torch.hub.load("intel-isl/MiDaS", model_type)
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        midas.to(device)
        midas.eval()
        return midas, device