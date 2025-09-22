import random
import unicodedata
from collections import deque

'''
打包：
pyinstaller -F random_kr.py -n 王国保卫战系列随机挑战 -i E:\编程作业\python\python_demo\pic\icon.png
配置说明：
hero：英雄数组
tower：防御塔数组
level：关卡数组
'''
# 常量定义
GAME_MODES = {
    '1': 'kr',
    '2': 'krf',
    '3': 'kro',
    '4': 'krv',
    '5': 'kra'
}
CHALLENGE_TYPES = ('英雄挑战', '钢铁挑战')
# 一次性输出的挑战次数
CHALLENGES_COUNT = 5

# 游戏配置
GAME_CONFIG = {
    'kr': {
        'hero': ['逐光者·杰拉尔德', '迅风·艾莉瑞雅', '愤怒之锤·马利克', '火炮杀手·博林', '灾祸魔导·马格纳斯',
                 '炎之魔神·伊格纳斯', '国王·迪纳斯', '冬之歌·伊罗拉', '熊爪·英格瓦', '钢锯',
                 '鬼侍', '索尔', '天十'],
        'level': ['1.南港', '2.郊原', '3.帕格拉斯', '4.双子河畔', '5.银橡森林',
                  '6.城堡之战', '7.寒步矿场', '8.冰风隘口', '9.暴云寺院', '10.废弃之地',
                  '11.凄凉山谷', '12.黑暗之塔', '13.萨雷格兹的巢穴', '14.阿卡洛斯遗迹', '15.腐朽森林',
                  '16.寂静森林', '17.强盗的巢穴', '18.冰川高地', '19.哈克拉吉高原', '20.火焰之坑',
                  '21.万魔殿', '22.真菌森林', '23.腐芯镇', '24.古代大墓地', '25.夜牙沼泽',
                  '26.布莱克本城堡'],
        'selection_rules': {
            'hero': {'count': 1, 'memory_size_range': (1, 10)},
            'level': {'count': 1, 'memory_size_range': (1, 10)}
        }
    },
    'krf': {
        'hero': ['阿尔里奇', '幻影', '黑棘船长', '克罗南', '女巫',
                 '纽维斯', '德得尔', '格劳尔', '沙塔', '阿什比特',
                 '巨蟹', '库绍', '但丁', '波恩哈特', '卡兹',
                 '塞塔姆'],
        'level': ['1.战锤要塞', '2.沙漠之鹰', '3.沙中绿洲', '4.绝望沙丘', '5.海盗老巢',
                  '6.纳泽鲁之门', '7.猩红山谷', '8.断藤大桥', '9.失落丛林', '10.马克瓦尔可',
                  '11.萨科拉神庙', '12.地下迷宫', '13.贝莱萨德的巢穴', '14.黑暗深处', '15.余烬尖刺深渊',
                  '16.海龟港', '17.风暴环礁', '18.沉没城堡', '19.白骨镇', '20.亵渎森林',
                  '21.黄昏古堡', '22.暗光深渊'],
        'selection_rules': {
            'hero': {'count': 1, 'memory_size_range': (1, 10)},
            'level': {'count': 1, 'memory_size_range': (1, 10)}
        }
    },
    'kro': {
        'hero': ['艾利丹', '埃里汎', '卡莎', '雷格森', '迪纳斯王子',
                 '瑞兹与大瑞格', '无畏树人', '维兹南', '鑫', '凤凰',
                 '杜拉斯', '莉恩', '布鲁斯', '莉莉丝', '威尔伯',
                 '浮士德'],
        'level': ['1.灰鸦港口', '2.高桥', '3.瀑布小径', '4.红杉阻击战', '5.皇家庭园',
                  '6.狮鹫驿站', '7.石环阵', '8.格林堡之战', '9.水晶之湖', '10.奇迹仙境',
                  '11.罪恶精灵王庭', '12.追本溯源', '13.奥术都市', '14.黑寡妇避难所', '15.艾纳妮神殿',
                  '16.加拉里安之墙', '17.血石矿场', '18.歼灭者王座', '19.暮色森林岗哨', '20.都尔德郊原',
                  '21.矮人国之门', '22.污染矿坑'],
        'selection_rules': {
            'hero': {'count': 1, 'memory_size_range': (1, 10)},
            'level': {'count': 1, 'memory_size_range': (1, 10)}
        }
    },
    'krv': {
        'hero': ['维鲁克', '阿斯拉', '奥洛克', '苦楝夫人', '墨忒弥斯',
                 '特拉敏', '极狗', '贝雷萨德', '毁灭坦克SG-11', '浚湃',
                 '艾斯库特', '墨尔古伦', '南瓜灯杰克', '电云', '格罗什',
                 '伊斯菲特', '卢塞尔娜'],
        'tower': ['暗影弓手', '兽人勇士巢穴', '炼狱法师', '哥布林火箭骑兵', '黑暗骑士',
                  '熔炉', '死灵墓', '回旋哥布林', '掷骨者', '精英骚扰者',
                  '兽人萨满', '阴森墓地', '腐朽森林', '女巫姐妹花', '炙热晶钻',
                  '哥布林战用飞艇', '深渊恶魔之礁', '沼泽巨人', '少林寺', '火光祭坛',
                  '沙虫巢穴', '食人魔沉船'],
        'level': ['1.矮人之门', '2.老城回廊', '3.卡赞矿区', '4.金色酿酒坊', '5.发条厂',
                  '6.博古尔的王座', '7.北国前哨站', '8.冰冻激流', '9.北国人村庄', '10.龙之埋骨场',
                  '11.冰川飞龙巢', '12.欧蒂尔农田', '13.银橡前哨站', '14.洛扎贡之城', '15.逐光者营地',
                  '16.迪纳斯城堡', '17.玛吉尼西亚海岸', '18.阿努瑞人广场', '19.贤者池塘', '20.击破寒冰',
                  '21.深入群山', '22.冰冻王座', '23.古代城门', '24.众河之城', '25.龙之力',
                  '26.重返腐朽森林', '27.沼泽地里的一夜', '28.远古幽魂', '29.挖掘出口', '30.失落通道',
                  '31.原始世界', '32.巫师登陆', '33.萨佩绿洲', '34.失落的帝国', '35.战锤要塞街道',
                  '36.大竞技场', '37.海盗兄弟会', '38.猴岛', '39.群鲨环礁', '40.骸骨沉船湾',
                  '41.金银岛'],
        'selection_rules': {
            'hero': {'count': 1, 'memory_size_range': (1, 10)},
            'tower': {'count': 5, 'memory_size_range': (1, 10)},
            'level': {'count': 1, 'memory_size_range': (1, 10)}
        }
    },
    'kra': {
        'hero': ['维斯珀', '蕾琳', '尼鲁', '托雷斯', '安雅',
                 '格里姆森', '布卢登', '赛莉恩', '奥纳格罗', '战争巨头',
                 '卢米妮尔', '科斯米尔', '斯特蕾吉', '喀拉托', '波恩哈特',
                 '希尔瓦拉', '丝派蒂尔'],
        'tower': ['皇家弓箭手', '圣骑士殿堂', '奥术法师', '三管加农炮', '巨弩哨站',
                  '树灵使者', '恶魔熔坑', '酿酒战匠', '死灵法师', '精灵观星者',
                  '矮人喷火器', '沙丘哨兵', '火箭枪手', '诡术魔导师', '幽冥战魂',
                  '暮光长弓', '沼泽隐士', '炮兵小队', '电涌巨像'],
        'level': ['1.树之海洋', '2.守卫之门', '3.森林之心', '4.翡翠树梢', '5.荒废郊区',
                  '6.野兽巢穴', '7.冷峻山谷', '8.绯红矿坑', '9.邪恶路口', '10.神庙庭院',
                  '11.峡谷高原', '12.枯萎农田', '13.亵渎神庙', '14.腐化山谷', '15.恶视魔塔',
                  '16.欲念之巅', '17.迷雾废墟', '18.深叶哨所', '19.堕落神庙', '20.树灵村落',
                  '21.沉没遗迹', '22.极饿凶谷', '23.暗钢之门', '24.狂热组装厂', '25.巨型核心',
                  '26.克隆密室', '27.统治穹顶', '28.玷污神庙', '29.繁殖室', '30.遗忘王座'],
        'selection_rules': {
            'hero': {'count': 2, 'memory_size_range': (1, 10)},
            'tower': {'count': 5, 'memory_size_range': (1, 10)},
            'level': {'count': 1, 'memory_size_range': (1, 10)}
        }
    }
}


class PoolManager:
    """短期记忆池管理器"""

    def __init__(self, item, select_count, memory_size):
        if select_count > len(item):
            raise Exception(f'选择数量 {select_count} 超过池大小 {len(item)}（{"，".join(item)}）')
        self.original_pool = item.copy()
        self.select_count = select_count
        self.memory = deque(maxlen=memory_size)

    def get_selection(self):
        """获取排除近期记忆的随机选择"""
        # 排除最近使用过的元素
        available = [i for i in self.original_pool if i not in self.memory]

        # 如果可用元素不足，清空记忆重新尝试
        if len(available) < self.select_count:
            self.memory.clear()
            available = self.original_pool.copy()

        # 随机选择并更新记忆
        selected = random.sample(available, self.select_count)
        self.memory.extend(selected)
        return selected


def get_display_width(string):
    """计算字符串显示宽度"""
    return sum(2 if unicodedata.east_asian_width(c) in ('F', 'W') else 1 for c in string)


class GameManager:
    """游戏管理器"""

    def __init__(self, config_name):
        self.config = GAME_CONFIG[config_name]
        self.memory_sizes = {}
        self.pools = self._init_pools()

    def _init_pools(self):
        """初始化所有选择池"""
        pools = {}
        for key, rule in self.config['selection_rules'].items():
            memory_size = random.randint(*rule['memory_size_range'])
            pools[key] = PoolManager(
                item=self.config[key],
                select_count=rule['count'],
                memory_size=memory_size  # 动态生成记忆池大小
            )
            self.memory_sizes[key] = memory_size  # 记录记忆池大小
        return pools

    def generate_challenge(self):
        """生成一次完整挑战"""
        result = {key: pool.get_selection() for key, pool in self.pools.items()}
        result.update({'challenge_type': random.choice(CHALLENGE_TYPES)})
        return result

    def generate_multiple_challenges(self, count=5):
        """生成多个挑战"""
        return [self.generate_challenge() for _ in range(count)]


def print_memory_sizes(managers):
    """打印各游戏模式的记忆池大小详细信息"""
    print('*记忆池容量配置')
    for mode, manager in managers.items():
        result = f'{GAME_MODES[mode].upper()}模式（英雄池：{manager.memory_sizes["hero"]}，'
        if 'tower' in manager.memory_sizes:
            result += f'防御塔池：{manager.memory_sizes["tower"]}，'
        result += f'关卡池：{manager.memory_sizes["level"]}）'
        print(result)
    print()


def print_star_box(selections):
    """带边框的输出格式化"""
    lines = [f'【随机英雄】{"，".join(selections["hero"])}']
    # KR1-3代没有选塔功能
    if 'tower' in selections:
        lines.append(f'【随机防御塔】{"，".join(selections["tower"])}')
    lines.append(f'【随机关卡】{selections["level"][0]}')
    lines.append(f'【不妨试试】{selections["challenge_type"]}')

    max_width = max(get_display_width(line) for line in lines)
    border = '=' * max_width
    print(border)
    print('\n'.join(lines))
    print(f'{border}\n')


def print_multiple_challenges(challenges):
    """一次生成多个随机挑战"""
    for i in challenges:
        print_star_box(i)


if __name__ == '__main__':
    # 初始化游戏管理器
    # 只初始化已配置的游戏模式
    managers = {
        num: GameManager(mode)
        for num, mode in GAME_MODES.items()
        if mode in GAME_CONFIG
    }
    # 打印记忆池大小详细信息
    print_memory_sizes(managers)
    while True:
        choice = input(f'输入 1-5 生成{CHALLENGES_COUNT}个对应KR系列挑战，输入 0 退出：')
        if choice == '0':
            print('程序已退出！')
            break
        elif choice in managers:
            game_manager = managers[choice]
            challenges = game_manager.generate_multiple_challenges(count=CHALLENGES_COUNT)
            print_multiple_challenges(challenges)
        else:
            print('无效输入，请重新输入！\n')
