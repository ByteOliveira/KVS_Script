
class Property_dic:
    def __init__(self):
        self.sub_property_dict = {"read Count": {}, "operation Count": {}, "latency": {}, "time lag": {}, "version lag": {},
                             "read errors": {}}
        self.sub_property_dictn = {"read Count": {}, "operation Count": {}, "latency": {}, "time lag": {}, "version lag": {},
                              "read errors": {}}
        self.sub_property_dicr = {"read Count": {}, "operation Count": {}, "latency": {}, "time lag": {}, "version lag": {},
                             "read errors": {}}
        self.sub_property_dicrn = {"read Count": {}, "operation Count": {}, "latency": {}, "time lag": {}, "version lag": {},
                              "read errors": {}}
        self.sub_property_dict_churn = self.sub_property_dictn
        self.sub_property_dicr_churn = self.sub_property_dicrn

class ppd:
    def __init__(self):
        self.property_dic_nPC = {"Tomp2p": Property_dic().sub_property_dict_churn, "Redis": Property_dic().sub_property_dicr_churn,
                            "Tomp2p with Churn": Property_dic().sub_property_dict_churn}
        self.property_dic_1PnC = {"Tomp2p": Property_dic().sub_property_dict_churn, "Redis": Property_dic().sub_property_dicr_churn,
                             "Tomp2p with Churn": Property_dic().sub_property_dict_churn}
        self.property_dic_nP1C = {"Tomp2p": Property_dic().sub_property_dict_churn, "Redis": Property_dic().sub_property_dicr_churn,
                             "Tomp2p with Churn": Property_dic().sub_property_dict_churn}