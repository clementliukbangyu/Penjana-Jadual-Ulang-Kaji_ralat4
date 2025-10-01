import random
import math
import re

def generate_weekly_schedule(subjects, difficulties, daily_hours, subjects_per_day):
    if not subjects:
        raise ValueError("Tiada subjek diberikan.")
    minutes_per_day = int(round(float(daily_hours) * 60))
    total_slots = 7 * subjects_per_day
    if total_slots < len(subjects):
        subjects_per_day = math.ceil(len(subjects) / 7)
        total_slots = 7 * subjects_per_day

    days = [[] for _ in range(7)]
    order = subjects.copy()
    random.shuffle(order)
    for subj in order:
        min_len = min(len(d) for d in days)
        for i in range(7):
            if len(days[i]) == min_len and len(days[i]) < subjects_per_day:
                days[i].append(subj)
                break
    for i in range(7):
        while len(days[i]) < subjects_per_day:
            avail = [s for s in subjects if s not in days[i]]
            pool = avail if avail else subjects
            weights = [difficulties.get(s, 1) for s in pool]
            chosen = random.choices(pool, weights=weights, k=1)[0]
            days[i].append(chosen)

    weekly_plan = {}
    for i, day in enumerate(days):
        weights = [difficulties.get(s, 1) for s in day]
        total_w = sum(weights)
        day_minutes = [0]*len(day)
        if total_w <= 0:
            base = minutes_per_day // len(day)
            day_minutes = [base]*len(day)
            rem = minutes_per_day - sum(day_minutes)
            for j in range(rem):
                day_minutes[j % len(day)] += 1
        else:
            for j, s in enumerate(day):
                day_minutes[j] = int(round(minutes_per_day * (difficulties.get(s,1) / total_w)))
            diff = minutes_per_day - sum(day_minutes)
            if diff != 0:
                max_idx = max(range(len(day)), key=lambda j: weights[j])
                day_minutes[max_idx] += diff
        day_agg = {}
        for idx, s in enumerate(day):
            day_agg[s] = day_agg.get(s, 0) + day_minutes[idx]
        formatted = {}
        for s, mins in day_agg.items():
            hours = round(mins / 60, 2)
            formatted[s] = {"minutes": mins, "hours": hours}
        weekly_plan[f"Hari {i+1}"] = formatted
    return weekly_plan
