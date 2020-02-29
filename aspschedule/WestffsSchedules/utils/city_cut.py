# coding: utf-8
import jieba


def city_cut(citys):
    # print(citys)
    if citys is None:
        seg_list = ['', '']
    elif citys == "新疆阿勒泰地区":
        seg_list = ['新疆维吾尔自治区', '阿勒泰地区']
    else:
        seg_list = jieba.lcut(citys)
        # print(seg_list)
        for i in seg_list:
            # print(i)
            if i == "新疆伊犁哈萨克自治州":
                seg_list = ['新疆维吾尔自治区', '伊犁哈萨克自治州']
                break
            if i == "新疆巴音郭楞蒙古自治州":
                seg_list = ['新疆维吾尔自治区', '巴音郭楞蒙古自治州']
                break
            if '内蒙古' in i:
                index = seg_list.index(i)
                seg_list[index] = '内蒙古自治区'
            if '新疆' in i:
                index = seg_list.index(i)
                seg_list[index] = '新疆维吾尔自治区'
            if '宁夏' in i:
                index = seg_list.index(i)
                seg_list[index] = '宁夏回族自治区'
            if '广西' in i:
                index = seg_list.index(i)
                seg_list[index] = '广西壮族自治区'
            if '香港' in i:
                index = seg_list.index(i)
                seg_list[index] = '香港特别行政区'
            if '澳门' in i:
                index = seg_list.index(i)
                seg_list[index] = '澳门特别行政区'
            if '西藏' in i:
                index = seg_list.index(i)
                seg_list[index] = '西藏自治区'
            if '恩施' in i:
                index = seg_list.index(i)
                seg_list[index] = '恩施土家族苗族自治州'
            if '上海' in i:
                index = seg_list.index(i)
                seg_list[index] = '上海市'
            if '重庆' in i:
                index = seg_list.index(i)
                seg_list[index] = '重庆市'
            if '天津' in i:
                index = seg_list.index(i)
                seg_list[index] = '天津市'
            if '北京' in i:
                index = seg_list.index(i)
                seg_list[index] = '北京市'
            if '文山' in i:
                index = seg_list.index(i)
                seg_list[index] = '文山壮族苗族自治州'
            if '巴彦淖尔' in i:
                index = seg_list.index(i)
                seg_list[index] = '巴彦淖尔市'
            if '延边' in i:
                index = seg_list.index(i)
                seg_list[index] = '延边朝鲜族自治州'
            if '伊犁' in i:
                index = seg_list.index(i)
                seg_list[index] = '伊犁哈萨克自治州'
            if '克孜勒苏' in i:
                index = seg_list.index(i)
                seg_list[index] = '克孜勒苏柯尔克孜自治州'
            if '博尔塔拉' in i:
                index = seg_list.index(i)
                seg_list[index] = '博尔塔拉蒙古自治州'
            if '吐鲁番' in i:
                index = seg_list.index(i)
                seg_list[index] = '吐鲁番地区'
            if '巴音郭楞' in i:
                index = seg_list.index(i)
                seg_list[index] = '巴音郭楞蒙古自治州'
            if '昌吉' in i:
                index = seg_list.index(i)
                seg_list[index] = '昌吉回族自治州'
            if '和田' in i:
                index = seg_list.index(i)
                seg_list[index] = '和田地区'
            if '喀什' in i:
                index = seg_list.index(i)
                seg_list[index] = '喀什地区'
            if '哈密' in i:
                index = seg_list.index(i)
                seg_list[index] = '哈密地区'
            if '塔城' in i:
                index = seg_list.index(i)
                seg_list[index] = '塔城地区'
            if '阿克苏' in i:
                index = seg_list.index(i)
                seg_list[index] = '阿克苏地区'
            if '阿勒泰' in i:
                index = seg_list.index(i)
                seg_list[index] = '阿勒泰地区'
            if '红河' in i:
                index = seg_list.index(i)
                seg_list[index] = '红河哈尼族彝族自治州'

    return seg_list


def get_city(citys):
    if citys is not None:
        words_list = city_cut(citys)
        if len(words_list) == 1:
            province = words_list[0]
            city_detail = ''
        else:
            province = words_list[0]
            city_detail = words_list[1]
    else:
        province = ''
        city_detail = ''

    return province, city_detail


def user_city_cut(citys):
    if citys is None:
        seg_list = ['', '']
    else:
        province = {'北京': '北京市', '天津': '天津市', '上海': '上海市', '重庆': '重庆市',
                    '河北': '河北省', '山西': '山西省', '辽宁': '辽宁省', '吉林': '吉林省',
                    '黑龙江': '黑龙江省', '江苏': '江苏省', '浙江': '浙江省', '安徽': '安徽省',
                    '福建': '福建省', '江西': '江西省', '山东': '山东省', '河南': '河南省',
                    '湖北': '湖北省', '湖南': '湖南省', '广东': '广东省', '海南': '海南省',
                    '四川': '四川省', '贵州': '贵州省', '云南': '云南省',
                    '陕西': '陕西省', '甘肃': '甘肃省', '青海': '青海省', '台湾': '台湾省', '内蒙古': '内蒙古自治区', '广西': '广西壮族自治区', '西藏': '西藏自治区',
                    '宁夏': '宁夏回族自治区', '新疆': '新疆维吾尔自治区', '香港': '香港特别行政区', '澳门': '澳门特别行政区'}
        keys = province.keys()
        if '吉林长春' in citys:
            seg_list = ['吉林省', '长春市']
        elif '广西北海' in citys:
            seg_list = ['广西壮族自治区', '北海市']
        elif '新疆吐鲁番地区' in citys:
            seg_list = ['新疆维吾尔自治区', '吐鲁番地区']
        elif '新疆巴音郭楞蒙古自治州' in citys:
            seg_list = ['新疆维吾尔自治区', '巴音郭楞蒙古自治州']
        elif '湖南永州' in citys:
            seg_list = ['湖南省', '永州市']
        elif '湖南长沙市' in citys:
            seg_list = ['湖南省', '长沙市']
        elif '甘肃兰州' in citys:
            seg_list = ['甘肃省', '兰州市']
        elif '山西大同' in citys:
            seg_list = ['山西省', '大同市']
        elif '贵州铜仁地区' in citys:
            seg_list = ['贵州省', '铜仁地区']
        elif '辽宁抚顺' in citys:
            seg_list = ['辽宁省', '抚顺市']
        elif '新疆伊犁哈萨克自治州' in citys:
            seg_list = ['新疆维吾尔自治区', '伊犁哈萨克自治州']
        elif '浦东新区' in citys:
            seg_list = ['上海市', '浦东新区']
        else:
            seg_list = jieba.lcut(citys)
            for i in seg_list:
                # print(i)
                if i in keys:
                    index = seg_list.index(i)
                    seg_list[index] = province.get(i)
                    if i in ['北京', '上海', '天津', '重庆']:
                        seg_list[1] = seg_list[2]

    return seg_list

