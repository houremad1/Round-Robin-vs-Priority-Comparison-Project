from queue import Queue
def roundRobin(processList, quantum):
    processList.sort(key=lambda p: p["arrivalTime"])
    for p in processList:
        p["remainingTime"]  = p["burstTime"]
        p["firstStartTime"] = -1
        p["completionTime"] = 0

    readyQueue  = Queue()
    ganttChart  = []
    currentTime = 0
    index       = 0
    n           = len(processList)

    while index < n and processList[index]["arrivalTime"] <= currentTime:
        readyQueue.put(processList[index]); index += 1

    while index < n or not readyQueue.empty():
        if readyQueue.empty():
            currentTime = processList[index]["arrivalTime"]
            while index < n and processList[index]["arrivalTime"] <= currentTime:
                readyQueue.put(processList[index]); index += 1
            continue
        cur = readyQueue.get()
        if cur["firstStartTime"] == -1:
            cur["firstStartTime"] = currentTime
        execT = min(quantum, cur["remainingTime"])
        ganttChart.append((cur["id"], currentTime, currentTime + execT))
        currentTime          += execT
        cur["remainingTime"] -= execT
        while index < n and processList[index]["arrivalTime"] <= currentTime:
            readyQueue.put(processList[index]); index += 1
        if cur["remainingTime"] > 0:
            readyQueue.put(cur)
        else:
            cur["completionTime"] = currentTime

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
    nn = len(processList)
    averages = {
        "average_waiting_time":    twt  / nn,
        "average_turnaround_time": ttat / nn,
        "average_response_time":   trt  / nn,
    }
    return [{"pid":g[0],"start":g[1],"end":g[2]} for g in ganttChart], results, averages