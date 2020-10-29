from flask import Flask, request
import json, datetime, random

# 通用部分
Bloodtype = ['A型', 'B型', 'O型', 'AB型']
Religion = ['基督教', '伊斯兰教', '印度教', '犹太教', '佛教', '道教', '神道教']
Nplace = ['北京', '天津', '上海', '重庆', '河北石家庄', '山西太原', '陕西西安', '山东济南', '河南郑州', '辽宁沈阳', '吉林长春', '黑龙江哈尔滨', '江苏南京', '浙江杭州',
          '安徽合肥','江西南昌', '福建福州', ' 湖北武汉', '湖南长沙', '四川成都', '贵州贵阳', '云南昆明', '广东广州', '海南海口', '甘肃兰州', '青海西宁', '台湾台北',
          '内蒙古呼和浩特','新疆乌鲁木齐', '西藏拉萨', '广西南宁', '宁夏银川', '香港', '澳门']

phoneNum = ['13','14','15','17','18','19']

# 学生模板使用
Schoolname = ['福清二中','福州八中','厦门六中','福清融城中学','福清第三中学','福清元洪中学','长乐华侨中学','福州四十中']


# 家长模板使用
Occupation = ['作业员','技术员','工程师','设计师','总务人员','厨师','服务员','营销人员','保安','司机','导游','售票员','调酒师','营业员','促销','保姆','医生','护士','药剂师','营养师',
              '后勤','健身教练','按摩技师','演员', '导演', '制片', '经纪', '编剧', '场务', '音乐人', '歌手', '乐师', '车手','经纪', '分析师', '服务员', '会记', '银行柜台', '业务',
              '保险销售', '团队管理', '后勤','教师', '培训师', '教练', '咨询师', '运动员', '陪练', '教练', '裁判', '公务员', '办事员', '警察', '军人', '特工', '科研人员', '记者',
              '摄影', '航天员', '会记', '人事', '保安', '总台', '业务', '翻译', '仓管', '货运', '客服']
# 专业模板使用
Major = ['电子商务专业', '电子技术应用专业', '航空旅游专业', '播音与主持专业', '高级海员专业', '机电技术应用专业', '现代物流管理专业', '旅游管理专业', '计算机应用与维护专业',
         '现代汽车、摩托车维修专业', '电脑服装设计与制作专业', '文秘与办公自动化专业', '电脑财会专业', '护理专业', '幼儿师范专业', '市场营销专业', '连锁经营与管理专业', '会计专业']
Majorintroduce = ['培养目标及就业方向：培养商务、营销等专业技术人才，毕业后从事相关的商务、计算机应用与操作技术或管理工作。如市场预测、业务洽谈、商品验收、推销、展销等。','培养初中级电子技术人才，毕业后从事相关电子技术工作。',
                  '培养熟练掌握民航服务理论和基本技能，为客户提供高品位、高质量服务，具有较强公关能力与协调能力、灵活应变能力的航空服务人才。毕业后就业于各大航空公司空乘或地面服务岗位。专业包括：空乘方向、地勤方向、安检护卫方向、铁乘服务方向','培养具有广播电视新闻传播、播音艺术技能，在广播电台、电视台及其他单位从事广播电视播音与节目主持工作的专门人才。',
                  '培养具有船舶驾驶技能的高级海员和轮机管理专业人才，学生毕业后安置在国内外各大船舶公司轮船上班。','培养具有从事机电技术理论知识和综合职业技能的机电设备、自动化设备和生产线的运行与维护人员。','培养从事现代物流业中的信息处理、配送、仓储、多式联运、采购、货代等具有专业及管理的高等技术应用型人才。毕业后在物流部门从事运输调度员、理货员、物质配送、商品储存等方面工作。',
                  '培养掌握现代旅游酒店管理基本理论知识和业务操作技能，适应星级酒店经营管理需求的酒店管理人才。','培养目标及就业方向：培养初、中级从事计算机专业工作的技术员，毕业后从事相关的技术或管理工作。如装配、维护、计算机应用、产品开发、营销、网络管理等','培养目标及就业方向：培养初、中级汽车、摩托车驾驶及维修人员，毕业后从事组装、焊工、维修、维护、驾驶、美容装饰等相关工作。',
                  '培养目标及就业方向：培养初、中级技术人员，毕业后从事事设计、制作、车缝或管理工作。','培养目标及就业方向：为各企业事业单位培养文秘及营销等专业人才，毕业安排到企事业单位如公司、工厂、文印店、酒店、宾馆等从事相关的文秘、营销或管理工作。','培养目标及就业方向：培养财务、会计等专业人才，毕业后从事企业、工厂、公司、宾馆、酒店、商场各用人单位从事财务、会计、管理等相关工作。',
                  '培养目标及就业方向：毕业及就业方向：毕业颁发护理中专毕业证书；三年级，可以参加护士资格考试；可以到医院、社区医院、门诊从事临床护理、预防保健工作。','培养目标及就业方向：培养德、智、体、美全面发展的具有良好的综合素质，熟知幼儿教育的基本工作规范和方法，具有较强的理论素养、掌握幼儿教育基本知识和专业技能、并能熟练运用于实践的学历的幼儿教育工作者，毕业后面向各级各类托幼机构以及其它有关机构从事幼儿教育教学管理工作。',
                  '就业岗位：主要就业岗位有营销业务管理员、营销方案策划员、企业市场调查分析员、企业销售代表、客户服务管理员等。','就业岗位：本专业毕业生可以在连锁企业总部业务部门从事经营管理、人力资源管理、商品促销工作；能担任连锁企业各门店的店长、经理、营业员、收银员等；还能在连锁企业物流配送中心从事物流配送、商品采购等工作。','就业岗位：会计人员、统计人员、银行清算员、银行信用卡业务、收银员、银行储蓄员、保险推销员、保险理赔员等。']




def Rname(num):
    RnameList = []
    for i in range(num):
        list_firstname = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '楮', '卫', '蒋', '沈', '韩', '杨',
                          '朱', '秦', '尤', '许', '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜',
                          '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏', '潘', '葛', '奚', '范', '彭', '郎',
                          '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史', '唐',
                          ]
        list_midname = ['梦', '琪', '忆', '柳', '之', '绿', '冰', '蓝', '灵', '槐', '平', '安', '书', '翠', '翠', '风',
                        '香', '巧', '代', '云', '梦', '曼', '幼', '翠', '友', '巧', '听', '寒', '梦', '柏', '醉', '易',
                        '旋', '亦', '玉', '凌', '萱', '访', '卉', '怀', '亦', '笑', '蓝', '春', '翠', '靖', '柏', '夜',
                        '蕾', '冰', '夏', '梦', '松', '书', '雪', '乐', '枫', '念', '薇', '靖', '雁', '寻', '春', '恨',
                        '山', '从', '寒', '忆', '香', '觅', '波', '静', '曼', '凡', '旋', '以', '亦', '念', '露', '芷',
                        '蕾', '千', '兰', '新', '波', '代', '真', '新', '蕾', '雁', '玉', '冷', '卉', '紫', '山', '千',
                        '琴', '恨', '天', '傲', '芙', '盼', '山', '怀', '蝶', '冰', '兰', '山', '柏', '翠', '萱', '恨',
                        '松', '问', '旋', '从', '南', '白', '易', '问', '筠', '如', '霜', '半', '芹', '丹', '珍', '冰',
                        '彤', '亦', '寒', '寒', '雁', '怜', '云', '寻', '文', '乐', '丹', '翠', '柔', '谷', '山', '之',
                        '瑶', '冰', '露', '尔', '珍', '谷', '雪', '乐', '萱', '涵', '菡', '海', '莲', '傲', '蕾', '青',
                        '槐', '冬', '儿', '易', '梦', '惜', '雪', '宛', '海', '之', '柔', '夏', '青', '亦', '瑶', '妙',
                        '菡', '春', '竹', '痴', '梦', '紫', '蓝', '晓', '巧', '幻', '柏', '元', '风', '冰', '枫', '访',
                        '蕊', '南', '春', '芷', '蕊', '凡', '蕾', '凡', '柔', '安', '蕾', '天', '荷', '含', '玉', '书',
                        '兰', '雅', '琴', '书', '瑶', '春', '雁', '从', '安', '夏', '槐', '念', '芹', '怀', '萍', '代',
                        '曼', '幻', '珊', '谷', '丝', '秋', '翠', '白', '晴', '海', '露', '代', '荷', '含', '玉', '书',
                        '蕾', '听', '白', '访', '琴', '灵', '雁', '秋', '春', '雪', '青', '乐', '瑶', '含', '烟', '涵',
                        '双', '平', '蝶', '雅', '蕊', '傲', '之', '灵', '薇', '绿', '春', '含', '蕾', '从', '梦', '从',
                        '蓉', '初', '丹', '听', '兰', '听', '蓉', '语', '芙', '夏', '彤', '凌', '瑶', '忆', '翠', '幻',
                        '灵', '怜', '菡', '紫', '南', '依', '珊', '妙', '竹', '访', '烟', '怜', '蕾', '映', '寒', '友',
                        '绿', '冰', '萍', '惜', '霜', '凌', '香', '芷', '蕾', '雁', '卉', '迎', '梦', '元', '柏', '代',
                        '萱', '紫', '真', '千', '青', '凌', '寒', '紫', '安', '寒', '安', '怀', '蕊', '秋', '荷', '涵',
                        '雁', '以', '山', '凡', '梅', '盼', '曼', '翠', '彤', '谷', '冬', '新', '巧', '冷', '安', '千',
                        '萍', '冰', '烟', '雅', '阳', '友', '绿', '南', '松', '诗', '云', '飞', '风', '寄', '灵', '书',
                        '芹', '幼', '蓉', '以', '蓝', '笑', '寒', '忆', '寒', '秋', '烟', '芷', '巧', '水', '香', '映',
                        '之', '醉', '波', '幻', '莲', '夜', '山', '芷', '卉', '向', '彤', '小', '玉', '幼', '南', '凡',
                        '梦', '尔', '曼', '念', '波', '迎', '松', '青', '寒', '笑', '天', '涵', '蕾', '碧', '菡', '映',
                        '秋', '盼', '烟', '忆', '山', '以', '寒', '寒', '香', '小', '凡', '代', '亦', '梦', '露', '映',
                        '波', '友', '蕊', '寄', '凡', '怜', '蕾', '雁', '枫', '水', '绿', '曼', '荷', '笑', '珊', '寒',
                        '珊', '谷', '南', '慕', '儿', '夏', '岚', '友', '儿', '小', '萱', '紫', '青', '妙', '菱', '冬',
                        '寒', '曼', '柔', '语', '蝶', '青', '筠', '夜', '安', '觅', '海', '问', '安', '晓', '槐', '雅',
                        '山', '访', '云', '翠', '容', '寒', '凡', '晓', '绿', '以', '菱', '冬', '云', '含', '玉', '访',
                        '枫', '含', '卉', '夜', '白', '冷', '安', '灵', '竹', '醉', '薇', '元', '珊', '幻', '波', '盼',
                        '夏', '元', '瑶', '迎', '曼', '水', '云', '访', '琴', '谷', '波', '乐', '之', '笑', '白', '之',
                        '山', '妙', '海', '紫', '霜', '平', '夏', '凌', '旋', '孤', '丝', '怜', '寒', '向', '萍', '凡',
                        '松', '青', '丝', '翠', '安', '如', '天', '凌', '雪', '绮', '菱', '代', '云', '南', '莲', '寻',
                        '南', '春', '文', '香', '薇', '冬', '灵', '凌', '珍', '采', '绿', '天', '春', '沛', '文', '紫',
                        '槐', '幻', '柏', '采', '文', '春', '梅', '雪', '旋', '盼', '海', '映', '梦', '安', '雁', '映',
                        '容', '凝', '阳', '访', '风', '天', '亦', '平', '绿', '香', '风', '霜', '雪', '柳', '雪', '靖',
                        '白', '梦', '飞', '绿', '如', '波', '又', '晴', '友', '香', '菱', '冬', '亦', '问', '妙', '春',
                        '海', '冬', '半', '安', '平', '春', '幼', '柏', '秋', '灵', '凝', '芙', '念', '烟', '白', '山',
                        '从', '灵', '尔', '芙']
        list_lastname = ['梦', '琪', '忆', '柳', '之', '绿', '冰', '', '蓝', '灵', '槐', '平', '安', '书', '翠', '翠', '风',
                         '香', '巧', '代', '云', '梦', '曼', '', '幼', '翠', '友', '巧', '听', '寒', '梦', '柏', '醉', '易',
                         '旋', '亦', '玉', '凌', '', '萱', '访', '卉', '怀', '亦', '笑', '蓝', '春', '翠', '靖', '柏', '夜',
                         '蕾', '冰', '夏', '梦', '', '松', '书', '雪', '', '乐', '枫', '', '念', '薇', '靖', '雁', '寻', '春', '恨',
                         '山', '从', '寒', '忆', '香', '觅', '波', '静', '曼', '凡', '旋', '', '以', '亦', '念', '露', '芷',
                         '蕾', '', '千', '兰', '新', '波', '代', '真', '新', '蕾', '雁', '玉', '冷', '卉', '紫', '山', '千',
                         '', '琴', '恨', '天', '傲', '芙', '盼', '山', '怀', '蝶', '冰', '兰', '山', '柏', '翠', '萱', '恨',
                         '松', '问', '', '旋', '从', '', '南', '白', '', '易', '问', '筠', '如', '霜', '半', '芹', '丹', '珍', '冰',
                         '彤', '亦', '寒', '寒', '雁', '怜', '', '云', '寻', '', '文', '乐', '丹', '翠', '柔', '谷', '山', '之',
                         '瑶', '冰', '露', '尔', '珍', '谷', '雪', '乐', '萱', '', '涵', '菡', '海', '莲', '傲', '蕾', '青',
                         '槐', '冬', '儿', '易', '梦', '惜', '', '雪', '宛', '海', '之', '柔', '夏', '青', '亦', '瑶', '妙',
                         '菡', '春', '竹', '痴', '梦', '紫', '', '蓝', '晓', '巧', '幻', '', '柏', '元', '风', '冰', '枫', '访',
                         '蕊', '南', '春', '芷', '蕊', '凡', '蕾', '凡', '柔', '安', '蕾', '', '天', '荷', '含', '玉', '书',
                         '兰', '雅', '琴', '书', '瑶', '春', '雁', '从', '安', '夏', '槐', '念', '芹', '怀', '萍', '代',
                         '曼', '幻', '珊', '谷', '丝', '秋', '翠', '白', '晴', '海', '露', '代', '', '荷', '含', '玉', '书',
                         '蕾', '听', '白', '访', '琴', '灵', '雁', '秋', '春', '雪', '青', '乐', '瑶', '含', '烟', '涵',
                         '双', '平', '蝶', '雅', '蕊', '', '傲', '之', '灵', '薇', '绿', '春', '含', '蕾', '从', '梦', '从',
                         '蓉', '初', '丹', '听', '兰', '', '听', '蓉', '语', '芙', '夏', '彤', '凌', '瑶', '忆', '翠', '幻',
                         '灵', '怜', '菡', '紫', '南', '依', '珊', '妙', '竹', '访', '烟', '怜', '蕾', '映', '寒', '友',
                         '绿', '冰', '萍', '惜', '霜', '', '凌', '香', '芷', '蕾', '', '雁', '卉', '迎', '梦', '元', '柏', '代',
                         '萱', '紫', '真', '千', '青', '凌', '寒', '紫', '安', '', '寒', '安', '怀', '蕊', '秋', '荷', '涵',
                         '雁', '以', '山', '凡', '梅', '盼', '曼', '翠', '彤', '谷', '冬', '新', '巧', '冷', '安', '千',
                         '萍', '冰', '烟', '雅', '阳', '友', '绿', '南', '松', '诗', '云', '飞', '风', '寄', '灵', '书',
                         '芹', '幼', '蓉', '以', '蓝', '笑', '寒', '忆', '寒', '', '秋', '烟', '芷', '巧', '水', '香', '映',
                         '之', '醉', '波', '幻', '莲', '夜', '山', '芷', '卉', '向', '彤', '小', '玉', '幼', '南', '凡',
                         '梦', '尔', '曼', '念', '波', '迎', '松', '青', '寒', '笑', '天', '涵', '蕾', '碧', '菡', '映',
                         '秋', '盼', '烟', '忆', '山', '以', '寒', '寒', '香', '', '小', '凡', '代', '亦', '梦', '露', '映',
                         '波', '友', '蕊', '寄', '凡', '怜', '蕾', '雁', '枫', '', '水', '绿', '曼', '荷', '笑', '珊', '寒',
                         '珊', '谷', '南', '慕', '儿', '夏', '岚', '友', '儿', '', '小', '萱', '紫', '青', '妙', '菱', '冬',
                         '寒', '曼', '柔', '语', '蝶', '青', '筠', '夜', '安', '', '觅', '海', '问', '安', '晓', '槐', '雅',
                         '山', '访', '云', '翠', '容', '寒', '凡', '晓', '绿', '', '以', '菱', '冬', '云', '含', '玉', '访',
                         '枫', '含', '卉', '夜', '白', '冷', '安', '灵', '竹', '', '醉', '薇', '元', '珊', '幻', '波', '盼',
                         '夏', '元', '瑶', '迎', '曼', '水', '云', '访', '琴', '', '谷', '波', '乐', '之', '笑', '白', '之',
                         '山', '妙', '海', '紫', '霜', '平', '夏', '凌', '旋', '', '孤', '丝', '怜', '寒', '向', '萍', '凡',
                         '松', '青', '丝', '翠', '安', '如', '天', '凌', '雪', '', '绮', '菱', '代', '云', '南', '莲', '寻',
                         '南', '春', '文', '香', '薇', '冬', '灵', '凌', '珍', '采', '绿', '天', '春', '沛', '文', '紫',
                         '槐', '幻', '柏', '采', '文', '春', '梅', '雪', '旋', '盼', '海', '映', '梦', '安', '雁', '映',
                         '容', '凝', '阳', '访', '风', '天', '亦', '平', '绿', '香', '风', '霜', '雪', '柳', '雪', '靖',
                         '白', '梦', '飞', '绿', '如', '波', '又', '晴', '友', '香', '菱', '冬', '亦', '问', '妙', '春',
                         '海', '冬', '半', '安', '平', '', '', '', '', '', '', '春', '幼', '柏', '秋', '灵', '凝', '芙',
                         '念', '烟', '白', '山', '从', '灵', '尔', '芙']
        # print(len(list_firstname),len(list_midname),len(list_lastname))
        firstname = list_firstname[random.randint(0, len(list_firstname) - 1)]
        midname = list_midname[random.randint(0, len(list_midname) - 1)]
        lastname = list_lastname[random.randint(0, len(list_lastname) - 1)]
        RnameList.append(firstname + midname + lastname)
    return RnameList

app = Flask(__name__)


# 只接受get方法访问
@app.route("/test", methods=["GET"])
def check():

    usernames = Rname(15)
    mylist = []
    for i, u in enumerate(usernames):
        bloodtype = Bloodtype[random.randint(0, len(Bloodtype) - 1)]
        age = random.randint(20, 50)
        religion = Religion[random.randint(0, len(Religion) - 1)]
        nplace = Nplace[random.randint(0, len(Nplace) - 1)]
        schoolname = Schoolname[random.randint(0, len(Schoolname) - 1)]
        phone = '{}{}'.format(phoneNum[random.randint(0, len(phoneNum) - 1)], random.randint(100000000, 999999999))
        occupation = Occupation[random.randint(0, len(Occupation) - 1)]
        major = Major[random.randint(0, len(Major) - 1)]
        majorintroduce = Majorintroduce[random.randint(0, len(Majorintroduce) - 1)]
        dict = {
            "username": u,
            "bloodtype": bloodtype,
            "age": age,
            "religion": religion,
            "nplace": nplace,
            "schoolname": schoolname,
            "phone": phone,
            "occupation": occupation,
            "major": major,
            "majorintroduce": majorintroduce,
            "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        mylist.append(dict)

    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': mylist}
    # 判断入参是否为空
    # if request.args is None:
    #     return_dict['return_code'] = '5004'
    #     return_dict['return_info'] = '请求参数为空'
    #     return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的params参数
    # get_data = request.args.to_dict()
    # name = get_data.get('name')
    # age = get_data.get('age')
    # # 对参数进行操作
    # dict['msg'] = tt(name, age)

    return json.dumps(return_dict, ensure_ascii=False)


# 功能函数
def tt(name, age):
    result_str = "%s今年%s岁" % (name, age)
    return result_str


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)