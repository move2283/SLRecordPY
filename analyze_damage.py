import re


def analyze_click_order(current_sequence, file_path):
    rounds = []
    damages = []
    with open(file_path, "r", encoding="utf-8") as file:
        rounds_data = []
        for line in file:
            if line.startswith("第"):
                rounds_data.append(line.strip())
            elif line.startswith("重新开始战斗"):
                rounds.append(rounds_data)
                rounds_data = []
                damage = int(re.search(r"薪火受到伤害: (\d+)", line).group(1))
                damages.append(damage)

        if rounds_data:
            rounds.append(rounds_data)

    click_count = 0
    total_damage = 0

    for round_set, damage in zip(rounds, damages):
        matched = True
        for round_data, current_round in zip(round_set, current_sequence):
            if not round_data.startswith(current_round):
                matched = False
                break

        if matched:
            click_count += 1
            total_damage += damage

    if click_count > 0:
        expected_damage = total_damage / click_count
    else:
        expected_damage = 0

    return click_count, expected_damage


def main():
    file_path = "click_order.txt"
    current_sequence = [
        "第1回合: 5->3.1 3->3.1  结束回合",
        "第2回合: 5->3",
    ]

    click_count, expected_damage = analyze_click_order(current_sequence, file_path)

    print(f"点击次数: {click_count}")
    print(f"预期受到伤害: {expected_damage:.2f}")


if __name__ == "__main__":
    main()
