class dataclass():
    def __init__(self):
        self.filepath=""
        self.filename=""
        self.name=""
        self.Total=0
        self.duration=0
        self.StartTime=""
        self.index1=0
        self.index2=0
        self.x=[]
        self.duringtime=[]
        self.in1=[]
        self.in2=[]
        self.in1_2=[]
        self.in2_1=[]
        self.dAngle=[]
        self.out=[]
        self.in1_Q=[]
        self.in2_Q=[]
        self.in1_partime=[]
        self.in2_partime=[]

        self.in1_mean=-1
        self.in1_variance=-1
        self.in1_mu=-1
        self.in2_mean=-1
        self.in2_variance=-1
        self.in2_mu=-1

        # 小组数据
        self.in1_probability_dis_x=[]
        self.in1_probability_dis=[]
        self.in1_normal_dis_x=[]
        self.in1_normal_dis=[]
        self.in1_normal_dis=[]
        self.in1_poisson_dis_x=[]
        self.in1_poisson_dis=[]

        self.in2_probability_dis_x = []
        self.in2_probability_dis = []
        self.in2_normal_dis_x = []
        self.in2_normal_dis = []
        self.in2_normal_dis = []
        self.in2_poisson_dis_x = []
        self.in2_poisson_dis = []


        # 小组分布
        self.in1_group_mean=-1
        self.in1_group_variance=-1
        self.in1_group_mu=-1

        self.in2_group_mean=-1
        self.in2_group_variance=-1
        self.in2_group_mu=-1


class settingclass():
    def __init__(self):
        self.path=""
        self.pw1in1=True
        self.pw1in2=True
        self.pw1out=True
        self.pw1in1_2=True
        self.pw1in2_1=False
        self.pw1dAngle=True
        self.pw2in1=False
        self.pw2in2=False
        self.pw2out=False
        self.pw2in1_2=True
        self.pw2in2_1=False
        self.pw2dAngle=False
        self.pw3in1=False
        self.pw3in2=False
        self.pw3out=False
        self.pw3in1_2=False
        self.pw3in2_1=False
        self.pw3dAngle=True
        self.x1=0
        self.x2=0


