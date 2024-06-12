def icons_for_ranks(rank: int):
    if rank >= 1500:
        return "🔴"
    elif rank > 300:
        return "🟡"
    else:
        return "🟢"
