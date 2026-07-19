"""初始化数据脚本

创建默认管理员账号和贝斯配置选项。
如果数据已存在则跳过，不会重复创建。

使用方法：
    cd backend
    python init_data.py
"""

import asyncio
import sys
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 添加 backend 目录到路径
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sqlalchemy import select

from app.core.config import settings
from app.core.security import get_password_hash
from app.database.base import Base
from app.database.session import AsyncSessionLocal, engine
from app.models.option import BassOption
from app.models.user import User

# 贝斯配置选项初始数据
BASS_OPTIONS = [
    # 琴体木材
    {"category": "body", "name": "Alder / 赤杨木", "description": "经典琴体木材，音色均衡，中频饱满", "price": 0},
    {"category": "body", "name": "Ash / 水曲柳", "description": "音色明亮，低频紧实，高频通透", "price": 800},
    {"category": "body", "name": "Mahogany / 桃花心木", "description": "音色温暖厚实，中低频丰富", "price": 1200},
    {"category": "body", "name": "Basswood / 椴木", "description": "轻质木材，音色柔和平衡", "price": 400},
    {"category": "body", "name": "Walnut / 黑胡桃木", "description": "密度高，音色饱满有力", "price": 1500},

    # 琴颈木材
    {"category": "neck", "name": "Maple / 枫木", "description": "经典琴颈材料，音色明亮清晰", "price": 0},
    {"category": "neck", "name": "Roasted Maple / 烘烤枫木", "description": "经过热处理，稳定性更好，音色更加温暖", "price": 600},
    {"category": "neck", "name": "Mahogany / 桃花心木", "description": "音色温暖，与桃花心木琴体搭配最佳", "price": 800},
    {"category": "neck", "name": "Wenge / 鸡翅木", "description": "硬度极高，音色清晰有力", "price": 1200},

    # 指板材质
    {"category": "fingerboard", "name": "Rosewood / 玫瑰木", "description": "经典指板材质，手感舒适，音色温暖", "price": 300},
    {"category": "fingerboard", "name": "Maple / 枫木", "description": "音色明亮，外观干净利落", "price": 0},
    {"category": "fingerboard", "name": "Ebony / 乌木", "description": "密度最高，手感顺滑，音色清晰紧实", "price": 800},
    {"category": "fingerboard", "name": "Pau Ferro / 铁苏木", "description": "音色介于玫瑰木和枫木之间", "price": 500},

    # 拾音器
    {"category": "pickup", "name": "Standard Single Coil / 标准单线圈", "description": "经典复古音色，清晰通透", "price": 0},
    {"category": "pickup", "name": "Standard Humbucker / 标准双线圈", "description": "音色厚实，降噪效果好", "price": 600},
    {"category": "pickup", "name": "Premium Single Coil / 高级单线圈", "description": "手工绕制，音色纯净富有动态", "price": 1000},
    {"category": "pickup", "name": "Premium Humbucker / 高级双线圈", "description": "高输出，适合摇滚和金属风格", "price": 1500},
    {"category": "pickup", "name": "Active Preamp / 主动前级", "description": "内置前级电路，可调节范围更广", "price": 2000},

    # 琴桥
    {"category": "bridge", "name": "Standard Fixed / 标准固定琴桥", "description": "稳定可靠，延音好", "price": 0},
    {"category": "bridge", "name": "High-Mass Bridge / 重型琴桥", "description": "增加延音和共振", "price": 500},
    {"category": "bridge", "name": "String-Through Body / 穿体琴桥", "description": "琴弦穿过琴体，延音更长", "price": 700},
    {"category": "bridge", "name": "Hipshot Style / Hipshot 风格", "description": "现代设计，调音更精准", "price": 900},

    # 颜色/表面处理
    {"category": "finish", "name": "Natural / 原木色", "description": "保留木材天然纹理", "price": 0},
    {"category": "finish", "name": "Gloss Black / 亮光黑", "description": "经典亮光黑色漆面", "price": 300},
    {"category": "finish", "name": "Sunburst / 日落色", "description": "经典渐变色，从深到浅", "price": 500},
    {"category": "finish", "name": "Matte Finish / 哑光漆面", "description": "现代哑光质感", "price": 400},
    {"category": "finish", "name": "Metallic / 金属漆", "description": "闪耀金属光泽", "price": 800},
    {"category": "finish", "name": "Custom Stain / 定制染色", "description": "根据色卡选择，打造专属颜色", "price": 1000},

    # 弦数
    {"category": "strings", "name": "4-String / 4弦", "description": "标准贝斯配置 E-A-D-G", "price": 0},
    {"category": "strings", "name": "5-String / 5弦", "description": "增加低音B弦 B-E-A-D-G", "price": 400},
    {"category": "strings", "name": "6-String / 6弦", "description": "增加高音C弦 B-E-A-D-G-C", "price": 800},

    # 左右手
    {"category": "handedness", "name": "Right Hand / 右手", "description": "标准右手款", "price": 0},
    {"category": "handedness", "name": "Left Hand / 左手", "description": "左手定制款", "price": 500},
]


async def init_data():
    """初始化数据"""
    print("=" * 50)
    print("Bass Studio - 数据初始化")
    print("=" * 50)

    # 确保表已创建
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ 数据库表已就绪")

    async with AsyncSessionLocal() as db:
        # 创建默认管理员
        result = await db.execute(
            select(User).where(User.username == settings.ADMIN_USERNAME)
        )
        admin = result.scalar_one_or_none()

        if admin:
            print(f"→ 管理员账号已存在: {settings.ADMIN_USERNAME}")
        else:
            admin_user = User(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                password_hash=get_password_hash(settings.ADMIN_PASSWORD),
                is_admin=True,
            )
            db.add(admin_user)
            await db.flush()
            print(f"✓ 创建管理员账号")
            print(f"  用户名: {settings.ADMIN_USERNAME}")
            print(f"  密码: {settings.ADMIN_PASSWORD}")
            print(f"  ⚠ 请在生产环境立即修改密码！")

        # 创建配置选项
        created_count = 0
        skipped_count = 0

        for opt_data in BASS_OPTIONS:
            result = await db.execute(
                select(BassOption).where(
                    BassOption.category == opt_data["category"],
                    BassOption.name == opt_data["name"],
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                skipped_count += 1
                continue

            opt = BassOption(**opt_data)
            db.add(opt)
            created_count += 1

        await db.flush()
        await db.commit()
        print(f"\n✓ 配置选项: 新增 {created_count} 项, 已存在 {skipped_count} 项")

    print("\n" + "=" * 50)
    print("数据初始化完成！")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(init_data())
