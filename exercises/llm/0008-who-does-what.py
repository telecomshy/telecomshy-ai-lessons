"""
LLM 底层 · 第 8 课 · 这件事到底是谁干的
=====================================

这一课的核心问题：**你在接口上看到的一个行为，是哪一层做的？**

配套脚本用三个能真跑、能验证的演示把「引擎层」立起来：

  [1] 约束解码 —— 同一张分表，加一道语法闸和不加，合法率差多少
  [2] 投机解码 —— 小模型先打草稿，大模型一次验一批；输出逐字相同，大模型少被叫几次
  [3] 凑批会改答案 —— 为什么「同一个 prompt」两次跑出来可能不一样

只用 Python 标准库，离线可跑：

    python exercises/llm/0008-who-does-what.py

诚实声明（很重要，别在课里说过头）：
  * [1] 的分表是**手编的**，所以「不合法率」那个数字只说明机制，不是任何真实模型的表现。
    能当真的是两头：不加闸会漏，加闸不漏。
  * [2] 的大小模型都是玩具规则，好处是**可以逐字验证「输出没变」**。
    能当真的是「少叫了几次」这件事；真实的加速倍数见课里引的论文数字。
  * [3] 只演示「为什么会发生」，**不给出发生概率**。
"""

import json
import math
import random

random.seed(7)


def hr(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


# ---------------------------------------------------------------- 演示 1


# 一条合法 JSON 的全部合法形态：城市名从三个里挑。
# token 是「模型一次往外蹦的那个零件」——这里故意比字更粗，
# 好让整串合法答案只有 5 个零件，脚本读起来一眼看得完。
CITIES = ["北京", "上海", "广州"]
CITY_TOKENS = ['"%s"' % c for c in CITIES]
LEGAL = {'{"city":%s}' % t for t in CITY_TOKENS}

# 词表故意混进一堆「不听话」的零件：模型完全可能挑中它们，
# 只是挑中之后这串字符再也走不回合法 JSON。
DISTRACTORS = ['"cityy"', 'null', ',', 'x', '"nope"']
VOCAB = ['{', '"city"', ':', '}'] + CITY_TOKENS + DISTRACTORS

TEMPLATE = ['{', '"city"', ':', CITY_TOKENS[0], '}']


def allowed_next(prefix):
    """给定已经拼出来的前缀，返回「下一个字拼上去还可能合法」的那些 token。

    做法：只有当 prefix+t 是某个合法答案的前缀时才算数。
    这就是约束解码干的那件事——把不合法的字直接从分表里划掉。
    """
    out = set()
    for t in VOCAB:
        if any(s.startswith(prefix + t) for s in LEGAL):
            out.add(t)
    return out


LEGAL_BOOST = 150.0


def make_distribution(prefix):
    """给当前前缀手编一张分表（模型给出的原始偏好，跟有没有闸无关）。

    刻意做成「合法的零件占大多数、但非法零件也有份」——
    这样不加闸时才会**偶尔**漏出去（漏的比例由这个权重定，不是由约束定的）。
    """
    raw = {}
    for t in VOCAB:
        raw[t] = random.uniform(0.2, 1.0)
    for t in allowed_next(prefix):
        raw[t] *= LEGAL_BOOST  # 合法字加权，看起来更「想走正路」
    return raw


def sample_from(dist, allowed=None):
    items = [(t, p) for t, p in dist.items() if allowed is None or t in allowed]
    total = sum(p for _, p in items)
    x = random.random() * total
    up = 0.0
    for t, p in items:
        up += p
        if x <= up:
            return t
    return items[-1][0]


def generate(constrained):
    """走一遍生成。constrained=True 时每一步都按语法把不合法的字划掉。

    ⚠ 加闸那条路是一步都不能错的：只要一步挑错，后面就再也拼不回合法 JSON。
    不加闸那条路可以随便挑，所以经常走着走着就废掉。
    """
    out = ""
    for _ in range(8):  # 合法答案 5 个零件，8 步足够走到头
        if constrained:
            allowed = allowed_next(out)
            if not allowed:
                break  # 拼不出来了（只可能发生在加闸那条路上）
        else:
            allowed = None  # 什么都能挑，包括会砸掉整串的那些
        out += sample_from(make_distribution(out), allowed)
        if out in LEGAL:
            break
    return out


TRIALS = 2000


def demo_constrained_decoding():
    hr("[1] 约束解码：引擎在分表上动手脚")
    print("  合法答案只有这三种：")
    for s in sorted(LEGAL):
        print("    " + s)
    print("  词表里还混着这些「不听话」的零件：  " + "  ".join(repr(t) for t in DISTRACTORS))
    print("  （每一轮模型都在整张词表上给分，只是加不加闸）")
    print()
    print("  同一个模型、同一张分表，抽 %d 次：" % TRIALS)

    plain = [generate(constrained=False) for _ in range(TRIALS)]
    bad_plain = sum(1 for s in plain if s not in LEGAL)

    guarded = [generate(constrained=True) for _ in range(TRIALS)]
    bad_guarded = sum(1 for s in guarded if s not in LEGAL)

    print("    不加闸（模型爱挑什么挑什么）        合法 %5d / %d   不合法率 %.1f%%"
          % (TRIALS - bad_plain, TRIALS, 100.0 * bad_plain / TRIALS))
    print("    加了闸（引擎每步划掉不合法字）      合法 %5d / %d   不合法率 %.1f%%"
          % (TRIALS - bad_guarded, TRIALS, 100.0 * bad_guarded / TRIALS))

    print()
    print("  不加闸时，坏的长这样（从 2000 次里挑前 3 次失败的）：")
    bad_ones = [s for s in plain if s not in LEGAL][:3]
    for s in bad_ones:
        print("    ✗ " + s)
    print("  同一批实验里，成功的长这样：")
    for s in [s for s in plain if s in LEGAL][:3]:
        print("    ✓ " + s)

    print()
    print("  再用真解析器（json.loads）跑一遍，只看两件事：会不会崩、能不能取出字段：")
    for label, runs in (("不加闸", plain), ("加了闸", guarded)):
        crashed = 0
        nofield = 0
        for s in runs:
            try:
                obj = json.loads(s)
                if "city" not in obj:
                    nofield += 1
            except Exception:
                crashed += 1
        print("    %s：解析失败 %d 次    解析成功但取不到 city 字段 %d 次"
              % (label, crashed, nofield))

    print()
    print("  ★ 分表是手编的，所以「不合法率 %.1f%%」只是机制的演示，不是任何真实模型的成绩。"
          % (100.0 * bad_plain / TRIALS))
    print("    能当真的只有两头：不加闸会漏，加闸不漏。")


# ---------------------------------------------------------------- 演示 2


# 玩具「大模型」：真答案。到这里就是「说完了」——
# 玩具里没有真的「结束符」，用「超出这个表」来表示说完。
ANSWER = ["今天", "天气", "不错", "，", "我", "建议", "带", "把", "伞", "，", "出门", "方便", "。"]

# 玩具「小模型」：便宜近似。它和大模型**一模一样**，
# 只在第 4、8 个零件上猜错（1 基）——这正是它「大概知道、但可能错」的意思。
MISTAKES = {3: "晴", 7: "拿"}


def big_at(i):
    """大模型在第 i 个位置的真答案。计数：每一次调用＝大模型被叫了一次。"""
    CALLS.append(1)
    return ANSWER[i]


def big_batch_at(indices):
    """大模型一次被叫，就把这一串位置的答案全给出来。

    这正是投机解码省下的东西：基线是一次问一个字，
    投机解码是一次验一整批。
    """
    CALLS.append(1)
    return [ANSWER[i] for i in indices]


def small_at(i):
    """小模型在第 i 个位置的猜测。"""
    return MISTAKES.get(i, ANSWER[i])


CALLS = []


def baseline():
    """老老实实：一次问一个字，问出一个算一个。"""
    CALLS.clear()
    out = []
    for i in range(len(ANSWER)):
        t = big_at(i)
        if not t:
            break
        out.append(t)
    return out, len(CALLS)


def speculative(k=4):
    """投机解码：小模型连打 k 个草稿，大模型一次把这一批全验一遍。

    这是最朴素的版本：大模型说「从第 j 个开始不对」，
    就丢掉 j 之后的所有草稿，从那里按大模型给的接着走。
    原论文用的是拒绝采样，能把一部分草稿留下来。
    """
    CALLS.clear()
    out = []
    i = 0
    while i < len(ANSWER):
        draft = []
        for _ in range(k):
            p = i + len(draft)
            if p >= len(ANSWER):
                break
            draft.append(small_at(p))
        if not draft:
            break
        # 大模型一次验：草稿占的那些位置，外加再往后一个位置
        span = min(i + len(draft) + 1, len(ANSWER))
        truth = big_batch_at(list(range(i, span)))
        hit = 0
        for want, got in zip(draft, truth):
            if want == got:
                hit += 1
            else:
                break
        # 接受命中的那几个，再补上大模型在断点处给的那一个
        out.extend(draft[:hit])
        if hit >= len(truth):
            break  # 已经验到句号，没有「下一个」可补了
        nxt = truth[hit]
        if not nxt:
            break
        out.append(nxt)
        i += hit + 1
    return out, len(CALLS)


def demo_speculative_decoding():
    hr("[2] 投机解码：先打草稿，再一次验收")
    print("  玩具「大模型」的真答案： " + "".join(ANSWER))
    print("  玩具「小模型」猜的：     " + "".join(small_at(i) for i in range(len(ANSWER) - 1)))
    print("  小模型只在第 %s 个零件上猜错（1 基），其余全对。"
          % "、".join(str(j + 1) for j in sorted(MISTAKES)))
    print()

    base_txt, base_calls = baseline()
    spec_txt, spec_calls = speculative()
    same = spec_txt == base_txt
    print("  大模型被叫的次数：")
    print("    老实一个个问（基线）         %d 次" % base_calls)
    print("    小模型打草稿 + 一次验一批     %d 次" % spec_calls)
    print("    省下 %.0f%%" % (100.0 * (base_calls - spec_calls) / base_calls))
    print()
    print("  两次输出逐字一样吗？  " + ("一样 ✓" if same else "不一样 ✗"))
    print("    基线： " + "".join(base_txt))
    print("    投机： " + "".join(spec_txt))
    if not same:
        raise SystemExit("投机解码必须与基线逐字一致，这里不一致，说明实现有 bug")
    print()
    print("  ★ 大小模型都是玩具规则，所以「省下几次」说明的是机制，不是真实加速倍数。")
    print("    能当真的是那个「逐字一样」：加速不改变输出。")
    print("    真实数字见课里引的论文：T5-XXL 上 2～3 倍，输出完全一致。")


# ---------------------------------------------------------------- 演示 3


def demo_batch_changes_answer():
    hr("[3] 凑批会改答案：为什么同一句话两次可能不一样")
    print("  显卡做的是浮点加法。浮点加法不满足结合律——")
    print("  同样的数，先加谁后加谁，末位可能不一样：")
    a, b, c = 0.1, 0.2, 0.3
    left = (a + b) + c
    right = a + (b + c)
    print("    (0.1+0.2)+0.3 = %.20f" % left)
    print("    0.1+(0.2+0.3) = %.20f" % right)
    print("    差 %.3e   （完全正常，浮点本来就这样）" % abs(left - right))
    print()
    print("  凑批会改变「谁跟谁先加」：你独自一批是一种分法，")
    print("  旁边挤进来八个人是另一种分法，算出来的末位就可能不同。")
    print()
    print("  而显卡能分辨的最小刻度，是这个：")
    x = 10.0
    step = math.ulp(x)
    y = math.nextafter(x, math.inf)
    print("    一个「刻度」(1 ulp) = %.3e" % step)
    print("    候选甲 = %.17f" % x)
    print("    候选乙 = %.17f" % y)
    print("    打印出来长得一模一样，但它们是两个不同的数，甲 < 乙。")
    print()
    print("  所以只要两个候选的分数咬得比一个刻度还紧，")
    print("  「谁的分高」这件事就由末位说了算——而末位会被凑批的方式改变。")
    print()
    print("  ★ 这一段只说明「为什么会发生」，不给发生概率——")
    print("    绝大多数请求翻不了面，但工程上不能假设它一次都不翻。")
    print("    厂商也是这么说的：见课里引的 vLLM 文档，")
    print("    它明说「批大小变化可能让 logprob 变化，进而让输出不同」。")


def main():
    print(__doc__)
    demo_constrained_decoding()
    demo_speculative_decoding()
    demo_batch_changes_answer()
    print()
    print("=" * 72)
    print("收口：三个演示分别属于「约束解码」「投机加速」「数值」——")
    print("它们全都发生在**引擎**那一层，模型自己一件都没做。")
    print("=" * 72)


if __name__ == "__main__":
    main()