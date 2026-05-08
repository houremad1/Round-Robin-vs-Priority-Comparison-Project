def preemptivePriority(processList, priorityRule="low_is_high"):
    n = len(processList)
    currentTime = 0; ganttChart = []; completed = 0
    for p in processList:
        p["remainingTime"]     = p["burstTime"]
        p["firstStartTime"]    = -1
        p["completionTime"]    = 0
        p["effectivePriority"] = p["priority"] if priorityRule == "low_is_high" else -p["priority"]
    processList.sort(key=lambda x: x["arrivalTime"])
    currentProcess = None; lastTime = 0

    while completed < n:
        available = [p for p in processList if p["arrivalTime"] <= currentTime and p["remainingTime"] > 0]
        if not available:
            currentTime += 1; continue
        nextProcess = min(available, key=lambda x: (x["effectivePriority"], x["arrivalTime"]))
        if currentProcess is None or nextProcess["id"] != currentProcess["id"]:
            if currentProcess is not None:
                ganttChart.append((currentProcess["id"], lastTime, currentTime))
            currentProcess = nextProcess; lastTime = currentTime
            if currentProcess["firstStartTime"] == -1:
                currentProcess["firstStartTime"] = currentTime
        currentProcess["remainingTime"] -= 1
        currentTime += 1
        if currentProcess["remainingTime"] == 0:
            ganttChart.append((currentProcess["id"], lastTime, currentTime))
            currentProcess["completionTime"] = currentTime
            completed += 1; currentProcess = None; lastTime = currentTime

    results = []; twt = ttat = trt = 0
    for p in processList:
        tat  = p["completionTime"] - p["arrivalTime"]
        wt   = tat - p["burstTime"]
        rt   = p["firstStartTime"] - p["arrivalTime"]
        twt += wt; ttat += tat; trt += rt
        results.append({
            "process_id": p["id"], "arrival": p["arrivalTime"],
            "burst": p["burstTime"], "completion": p["completionTime"],
            "turnaround_time": tat, "waiting_time": wt, "response_time": rt,
            "priority": p.get("priority", 1),
        })
    averages = {
        "average_waiting_time":    twt / n,
        "average_turnaround_time": ttat / n,
        "average_response_time":   trt  / n,
    }
    return [{"pid":g[0],"start":g[1],"end":g[2]} for g in ganttChart], results, averages